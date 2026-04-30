"""
칼럼 자동 생성 스크립트
Claude Haiku로 노인일자리/복지 관련 칼럼을 생성하여 WordPress에 발행합니다.

사용법:
    pip install anthropic
    .env에 ANTHROPIC_API_KEY 추가 후
    python generate_columns.py
"""
import os
import sys
import time
import json
import requests
import anthropic
from dotenv import load_dotenv

load_dotenv()

WP_URL      = os.getenv('WP_URL')
WP_USER     = os.getenv('WP_USER')
WP_APP_PASS = os.getenv('WP_APP_PASS')
API_KEY     = os.getenv('ANTHROPIC_API_KEY')

TOPICS = [
    "노인일자리 지원사업 5가지 유형 완벽 비교 - 나에게 맞는 유형은?",
    "만 60세 이상 취업하면 받을 수 있는 혜택 총정리",
    "노인 재취업 성공 사례 - 70대에도 할 수 있는 직종 5가지",
    "기초연금 받으면서 일해도 되나요? 소득 기준 완벽 정리",
    "시니어 직업훈련 무료로 받는 방법 - 고용노동부 지원 프로그램",
    "노인일자리 월급은 얼마? 유형별 급여와 근무 조건 비교",
    "65세 이상 취업 시 세금 혜택 - 노인 근로소득 공제 완벽 가이드",
    "재가 돌봄 서비스 종류와 신청 방법 - 집에서 받을 수 있는 복지",
    "홀몸 어르신 생활 지원 서비스 - 신청 가능한 혜택 한눈에 보기",
    "노인 의료비 지원 제도 총정리 - 병원비 줄이는 5가지 방법",
    "경로당 프로그램으로 일자리 연결되는 방법 - 지역 사례 소개",
    "어르신 스마트폰 활용 취업 - 온라인 플랫폼 노동 입문 가이드",
    "시니어 창업 지원금 받는 법 - 60세 이상 창업 시 활용할 수 있는 지원",
    "장기요양보험 등급 신청 방법과 받을 수 있는 서비스 정리",
    "노인 우울증 예방하는 일자리 - 사회 참여가 건강에 미치는 효과",
    "퇴직 후 재취업 준비 체크리스트 - 60대 구직 활동 시작 전 꼭 확인",
    "사회서비스 일자리란? 요양보호사·노인복지사 자격증 취득 가이드",
    "노인복지관 취업 지원 프로그램 활용법 - 무료 직업 상담부터 취업 연계까지",
]


def get_column_category_id():
    """WordPress에서 칼럼 카테고리 ID를 가져옵니다."""
    res = requests.get(
        f"{WP_URL}/wp-json/wp/v2/categories",
        auth=(WP_USER, WP_APP_PASS),
        params={'slug': 'column', 'per_page': 5},
        timeout=10
    )
    cats = res.json()
    if cats and isinstance(cats, list):
        return cats[0]['id']
    # slug가 다를 경우 전체 목록 출력
    res2 = requests.get(
        f"{WP_URL}/wp-json/wp/v2/categories",
        auth=(WP_USER, WP_APP_PASS),
        params={'per_page': 20},
        timeout=10
    )
    print("카테고리 목록:")
    for c in res2.json():
        print(f"  ID:{c['id']} slug:{c['slug']} name:{c['name']}")
    return None


def post_exists(title):
    """제목으로 중복 글 확인"""
    res = requests.get(
        f"{WP_URL}/wp-json/wp/v2/posts",
        auth=(WP_USER, WP_APP_PASS),
        params={'search': title[:30], 'per_page': 5},
        timeout=10
    )
    for post in res.json():
        if post.get('title', {}).get('rendered', '').strip() == title.strip():
            return True
    return False


def generate_article(topic: str) -> dict:
    """Claude Haiku로 칼럼 글을 생성합니다."""
    client = anthropic.Anthropic(api_key=API_KEY)

    prompt = f"""다음 주제로 노인일자리 정보 사이트에 올릴 실용적인 칼럼을 작성해 주세요.

주제: {topic}

요구사항:
- 어르신과 그 가족이 읽는 사이트이므로 쉽고 친절한 문체로 작성
- 800~1200자 분량
- WordPress HTML 형식으로 작성 (h2, h3, p, ul, li 태그 사용)
- 실제로 유용한 정보를 구체적으로 포함
- 첫 문단은 독자의 공감을 이끄는 도입부로 시작
- 마지막에 한 줄 요약 또는 행동 권장 문구로 마무리
- 출처 표시나 "AI가 작성" 같은 문구는 절대 포함하지 말 것
- HTML 속성에 큰따옴표 대신 작은따옴표 사용 (JSON 파싱 오류 방지)

아래 형식으로만 응답하세요 (다른 텍스트 없이):
TITLE: 여기에 제목
EXCERPT: 여기에 100자 이내 요약
CONTENT:
여기에 HTML 본문"""

    message = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=2000,
        messages=[{"role": "user", "content": prompt}]
    )

    text = message.content[0].text.strip()

    # TITLE / EXCERPT / CONTENT 형식 파싱
    title = excerpt = content = ''
    if 'TITLE:' in text and 'CONTENT:' in text:
        lines = text.split('\n')
        mode = None
        content_lines = []
        for line in lines:
            if line.startswith('TITLE:'):
                title = line.replace('TITLE:', '').strip()
            elif line.startswith('EXCERPT:'):
                excerpt = line.replace('EXCERPT:', '').strip()
            elif line.startswith('CONTENT:'):
                mode = 'content'
            elif mode == 'content':
                content_lines.append(line)
        content = '\n'.join(content_lines).strip()
    else:
        raise ValueError(f"응답 형식 오류: {text[:200]}")

    return {'title': title, 'content': content, 'excerpt': excerpt}


def publish_to_wp(title, content, excerpt, category_id):
    """WordPress에 글을 발행합니다."""
    res = requests.post(
        f"{WP_URL}/wp-json/wp/v2/posts",
        auth=(WP_USER, WP_APP_PASS),
        headers={'Content-Type': 'application/json'},
        data=json.dumps({
            'title':      title,
            'content':    content,
            'excerpt':    excerpt,
            'status':     'publish',
            'categories': [category_id],
        }),
        timeout=15
    )
    if res.status_code == 201:
        return res.json().get('id')
    print(f"  발행 실패 {res.status_code}: {res.text[:200]}")
    return None


def main():
    if not API_KEY:
        print("오류: .env에 ANTHROPIC_API_KEY가 없습니다.")
        sys.exit(1)

    print("칼럼 카테고리 ID 확인 중...")
    cat_id = get_column_category_id()
    if not cat_id:
        print("오류: 칼럼 카테고리를 찾을 수 없습니다. 위 목록에서 ID를 확인하세요.")
        sys.exit(1)
    print(f"칼럼 카테고리 ID: {cat_id}")

    success = 0
    for i, topic in enumerate(TOPICS, 1):
        print(f"\n[{i}/{len(TOPICS)}] {topic[:40]}...")

        if post_exists(topic):
            print("  이미 발행됨, 건너뜀")
            continue

        try:
            article = generate_article(topic)
            title   = article['title']
            content = article['content']
            excerpt = article.get('excerpt', '')

            post_id = publish_to_wp(title, content, excerpt, cat_id)
            if post_id:
                print(f"  발행 완료 ID:{post_id} — {title[:50]}")
                success += 1
            time.sleep(3)

        except Exception as e:
            print(f"  오류: {e}")
            time.sleep(2)

    print(f"\n완료: {success}/{len(TOPICS)}건 발행")


if __name__ == '__main__':
    main()