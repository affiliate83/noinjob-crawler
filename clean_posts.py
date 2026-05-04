"""
기존 발행 글에서 공공데이터 출처 문구 및 출처 행 일괄 제거 스크립트
"""
import re
import os
import sys
import time
import requests
from dotenv import load_dotenv

load_dotenv()

WP_URL      = os.getenv('WP_URL')
WP_USER     = os.getenv('WP_USER')
WP_APP_PASS = os.getenv('WP_APP_PASS')

# 제거할 패턴들
PATTERNS = [
    # <p class="data-source">...</p>
    re.compile(r'<p class=["\']data-source["\']>.*?</p>\s*', re.DOTALL),
    # 출처 테이블 행 (워크넷 등)
    re.compile(r'\s*<tr><th>출처</th><td>.*?</td></tr>', re.DOTALL),
    # WordPress wptexturize가 ``(백틱 2개)를 &#8220;으로 변환한 형태
    # ```html → &#8220;`html,  ``` → &#8220;`
    re.compile(r'<p>\s*&#8220;`[a-z]*\s*</p>\s*', re.IGNORECASE),
    re.compile(r'&#8220;`[a-z]*\s*', re.IGNORECASE),
    # 혹시 변환 전 raw 리터럴 백틱이 남아있을 경우
    re.compile(r'<p>```[a-z]*\s*</p>\s*', re.IGNORECASE),
    re.compile(r'```[^\n`]*\n?'),
]


def clean_content(html: str) -> str:
    for pat in PATTERNS:
        html = pat.sub('', html)
    return html.strip()


def get_posts(page=1, per_page=100, categories=None):
    params = {'page': page, 'per_page': per_page, 'status': 'publish'}
    if categories:
        params['categories'] = ','.join(str(c) for c in categories)
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
        timeout=15,
    )
    res.raise_for_status()
    return res.status_code


def main():
    # senuri=2, welfare=3 카테고리만 대상
    target_categories = [2, 3]

    updated = skipped = errors = 0
    page = 1

    while True:
        try:
            posts, total_pages = get_posts(page=page, per_page=100, categories=target_categories)
        except Exception as e:
            print(f"목록 조회 오류 (page {page}): {e}")
            break

        if not posts:
            break

        print(f"페이지 {page}/{total_pages} — {len(posts)}건 처리 중...")

        for post in posts:
            pid   = post['id']
            title = post['title']['rendered']
            raw   = post['content']['rendered']

            cleaned = clean_content(raw)

            if cleaned == raw:
                skipped += 1
                continue

            try:
                update_post(pid, cleaned)
                print(f"  수정 완료 ID:{pid} — {title[:50]}")
                updated += 1
                time.sleep(0.5)
            except Exception as e:
                print(f"  수정 실패 ID:{pid}: {e}")
                errors += 1

        if page >= total_pages:
            break
        page += 1
        time.sleep(1)

    print(f"\n완료: 수정 {updated}건 / 변경없음 {skipped}건 / 오류 {errors}건")


if __name__ == '__main__':
    if not all([WP_URL, WP_USER, WP_APP_PASS]):
        print("오류: .env에 WP_URL, WP_USER, WP_APP_PASS가 필요합니다.")
        sys.exit(1)
    main()