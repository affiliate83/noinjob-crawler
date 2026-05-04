"""
기존 발행 글에 AI 풍부화 섹션(직무 소개·자격 안내·FAQ 등)을 일괄 추가합니다.
이미 'faq-item' 클래스가 있는 글은 건너뜁니다.

사용법:
    py enrich_existing_posts.py            # 전체 실행
    py enrich_existing_posts.py --dry-run  # 변경 없이 대상 글만 확인
"""
import os
import sys
import time
import requests
from dotenv import load_dotenv

load_dotenv()

WP_URL      = os.getenv('WP_URL')
WP_USER     = os.getenv('WP_USER')
WP_APP_PASS = os.getenv('WP_APP_PASS')

# senuri=2, welfare=3
CATEGORY_TYPE = {2: 'job', 3: 'welfare'}

DRY_RUN = '--dry-run' in sys.argv


def get_posts(page=1, per_page=50, category_ids=None):
    params = {'page': page, 'per_page': per_page, 'status': 'publish'}
    if category_ids:
        params['categories'] = ','.join(str(c) for c in category_ids)
    res = requests.get(
        f"{WP_URL}/wp-json/wp/v2/posts",
        auth=(WP_USER, WP_APP_PASS),
        params=params,
        timeout=15,
    )
    res.raise_for_status()
    total_pages = int(res.headers.get('X-WP-TotalPages', 1))
    return res.json(), total_pages


def update_post(post_id, content):
    res = requests.post(
        f"{WP_URL}/wp-json/wp/v2/posts/{post_id}",
        auth=(WP_USER, WP_APP_PASS),
        json={'content': content},
        timeout=20,
    )
    res.raise_for_status()


def inject_before_last_div(html: str, extra: str) -> str:
    """기존 HTML의 마지막 </div> 앞에 추가 섹션 삽입."""
    idx = html.rfind('</div>')
    if idx == -1:
        return html + '\n\n' + extra
    return html[:idx] + extra + '\n\n' + html[idx:]


def detect_post_type(post):
    """카테고리 ID로 job/welfare 구분."""
    cats = post.get('categories', [])
    for cat_id, ptype in CATEGORY_TYPE.items():
        if cat_id in cats:
            return ptype
    return None


def main():
    # enricher는 crawler/ 패키지 밖에서 직접 import할 수 없으므로 여기서 인라인 import
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'crawler'))
    from utils.enricher import enrich_from_html

    if not all([WP_URL, WP_USER, WP_APP_PASS]):
        print("오류: .env에 WP_URL, WP_USER, WP_APP_PASS가 필요합니다.")
        sys.exit(1)

    if DRY_RUN:
        print("[DRY-RUN] 실제 변경은 없습니다.\n")

    updated = skipped = errors = 0
    page = 1

    while True:
        try:
            posts, total_pages = get_posts(
                page=page, per_page=50,
                category_ids=list(CATEGORY_TYPE.keys()),
            )
        except Exception as e:
            print(f"목록 조회 오류 (page {page}): {e}")
            break

        if not posts:
            break

        print(f"페이지 {page}/{total_pages} — {len(posts)}건")

        for post in posts:
            pid    = post['id']
            title  = post['title']['rendered']
            raw    = post['content']['rendered']
            ptype  = detect_post_type(post)

            if ptype is None:
                skipped += 1
                continue

            # 이미 풍부화된 글은 건너뜀
            if 'faq-item' in raw:
                skipped += 1
                continue

            print(f"  처리 중 ID:{pid} [{ptype}] {title[:45]}...")

            if DRY_RUN:
                updated += 1
                continue

            extra = enrich_from_html(raw, ptype)
            if not extra:
                print(f"    AI 생성 실패, 건너뜀")
                errors += 1
                continue

            new_content = inject_before_last_div(raw, extra)

            try:
                update_post(pid, new_content)
                print(f"    완료")
                updated += 1
            except Exception as e:
                print(f"    업데이트 실패: {e}")
                errors += 1

            time.sleep(1)

        if page >= total_pages:
            break
        page += 1
        time.sleep(2)

    label = "대상" if DRY_RUN else "업데이트"
    print(f"\n완료: {label} {updated}건 / 건너뜀 {skipped}건 / 오류 {errors}건")


if __name__ == '__main__':
    main()