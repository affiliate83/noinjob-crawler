"""
하루 2개씩 칼럼 자동 생성·발행 (GitHub Actions 스케줄용)
기존 제목과 중복되면 스킵
"""
import os
import re
import time
import requests
import anthropic
from dotenv import load_dotenv

load_dotenv()

WP_URL = os.getenv('WP_URL')
WP_USER = os.getenv('WP_USER')
WP_APP_PASS = os.getenv('WP_APP_PASS')
PEXELS_API_KEY = os.getenv('PEXELS_API_KEY')
ANTHROPIC_API_KEY = os.getenv('ANTHROPIC_API_KEY')

AUTH = (WP_USER, WP_APP_PASS)
PEXELS_HEADERS = {'Authorization': PEXELS_API_KEY}
client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

COLUMN_CATEGORY_SLUG = 'column'
DAILY_LIMIT = 2

# 새 칼럼 주제 풀 (100개 — 기존 73개와 중복 없는 주제)
TOPICS = [
    ("노인 일자리 신청 전 꼭 알아야 할 5가지 체크리스트", "senior job checklist elderly", "일자리"),
    ("만 65세 이상 고령자 고용장려금 – 기업과 어르신 모두 혜택", "elderly employment incentive", "일자리"),
    ("노인 일자리 사업 참여 중 다칠 경우 – 산재보험 적용 여부", "senior worker injury insurance", "일자리"),
    ("시니어 취업 상담 서비스 – 무료로 받을 수 있는 곳 총정리", "senior job counseling", "일자리"),
    ("60대 이상 직장인의 연차·퇴직금 권리 완벽 정리", "senior worker rights benefits", "일자리"),
    ("노인 일자리 사업 월급은 얼마? 2026년 최신 급여 기준", "senior job salary 2026", "일자리"),
    ("시니어 바리스타 자격증 – 커피로 새 직업 시작하기", "senior barista coffee job", "일자리"),
    ("어르신 택배 분류 일자리 – 신청 방법과 근무 조건", "senior delivery sorting job", "일자리"),
    ("노인 학교 급식 보조 일자리 – 지원 자격과 신청 절차", "senior school cafeteria job", "일자리"),
    ("60대 경비·주차 관리 취업 – 준비물과 자격 요건", "senior security guard job", "일자리"),
    ("어르신 도서관 사서 보조 일자리 신청 가이드", "senior library assistant job", "일자리"),
    ("노인 일자리 사업 조기 종료 시 불이익이 있을까?", "senior job early termination", "일자리"),
    ("시니어 강사·강연 일자리 – 내 경험을 돈으로 만드는 법", "senior lecturer instructor", "일자리"),
    ("어르신 농촌 일손 돕기 프로그램 – 신청 방법과 숙박 지원", "senior rural farm work", "일자리"),
    ("60대 번역·통역 프리랜서 – 외국어 능력 활용하기", "senior translator interpreter", "일자리"),
    ("노인 일자리 사업과 기초연금 동시 수령 가능한가?", "senior job pension simultaneous", "복지"),
    ("기초연금 40만 원 시대 – 2026년 인상 내용 총정리", "elderly basic pension increase", "복지"),
    ("노인 맞춤돌봄서비스 신청 방법과 이용 절차 안내", "elderly care service application", "복지"),
    ("치매 가족을 위한 정부 지원 – 쉼터, 치료비, 돌봄 서비스", "dementia family support", "복지"),
    ("어르신 무릎·관절 수술비 지원 – 건강보험 보장 범위", "elderly joint surgery support", "복지"),
    ("노인 복지관 프로그램 종류와 이용 방법 총정리", "elderly welfare center program", "복지"),
    ("어르신 스마트폰 교육 – 무료로 배울 수 있는 곳", "elderly smartphone education free", "복지"),
    ("노인 대상 사기 예방 – 건강식품·보험 사기 대처법", "elderly scam prevention", "복지"),
    ("시니어 정신건강 지원 서비스 – 우울증 상담 무료 이용법", "senior mental health support", "건강"),
    ("어르신 고혈압·당뇨 무료 검진 받는 방법", "elderly free health checkup", "건강"),
    ("노인 걷기 운동 루틴 – 하루 30분으로 건강 지키기", "elderly walking exercise routine", "건강"),
    ("어르신 수면 장애 원인과 해결 방법 – 숙면을 위한 습관", "elderly sleep disorder solution", "건강"),
    ("시니어 근력 운동 – 낙상 예방을 위한 하체 강화 방법", "elderly strength exercise", "건강"),
    ("어르신 영양제 선택 가이드 – 꼭 챙겨야 할 성분", "elderly supplement guide", "건강"),
    ("노인 구강 건강 관리법 – 틀니·임플란트 올바른 관리", "elderly oral health denture", "건강"),
    ("60대 이상 독감·폐렴구균 예방접종 무료로 맞는 법", "elderly vaccination free flu", "건강"),
    ("어르신 눈 건강 지키기 – 백내장·녹내장 조기 발견법", "elderly eye health cataract", "건강"),
    ("노인 당뇨 관리 식단 – 혈당 조절을 위한 식사법", "elderly diabetes diet management", "건강"),
    ("시니어 요가·스트레칭 – 집에서 할 수 있는 유연성 운동", "senior yoga stretching home", "건강"),
    ("어르신 심장 건강 지키기 – 협심증·심근경색 예방법", "elderly heart health prevention", "건강"),
    ("노인 골다공증 예방 – 뼈 건강을 위한 생활 습관", "elderly osteoporosis prevention", "건강"),
    ("시니어 피부 관리법 – 건조한 피부 촉촉하게 유지하는 법", "elderly skin care dry", "건강"),
    ("어르신 변비 해결법 – 장 건강을 위한 식이요법", "elderly constipation diet solution", "건강"),
    ("60대 이상 암 검진 – 무료로 받을 수 있는 검사 종류", "elderly cancer screening free", "건강"),
    ("노인 약 복용 주의사항 – 중복 투약·부작용 예방하기", "elderly medication safety precaution", "건강"),
    ("시니어 해외여행 준비 – 건강 챙기고 안전하게 여행하기", "senior overseas travel health", "생활"),
    ("어르신 스마트폰 사기 예방 – 문자·전화 피싱 대처법", "elderly phone scam prevention", "생활"),
    ("노인 혼자 사는 집 안전 점검 – 낙상·화재 예방하기", "elderly home safety check", "생활"),
    ("어르신 반려동물 키우기 – 건강과 외로움 해소 효과", "elderly pet companionship health", "생활"),
    ("60대 이상 운전면허 갱신 – 조건부 면허와 반납 혜택", "elderly driver license renewal", "생활"),
    ("시니어 독서 모임 참여하기 – 인지 건강과 사회 활동 동시에", "senior book club reading", "생활"),
    ("어르신 텃밭 가꾸기 – 도시 농부로 건강하게 사는 법", "elderly urban gardening", "생활"),
    ("노인 여름철 건강 관리 – 폭염·열사병 예방 수칙", "elderly summer heat stroke prevention", "건강"),
    ("어르신 겨울철 건강 – 한파·낙상 사고 예방법", "elderly winter cold prevention", "건강"),
    ("시니어 자서전 쓰기 – 인생 기록으로 치매 예방하기", "senior autobiography writing", "생활"),
    ("노인 봉사활동 종류와 신청 방법 – 사회 참여로 활기 찾기", "senior volunteer activity type", "생활"),
    ("어르신 평생교육 프로그램 – 무료로 배울 수 있는 강좌", "elderly lifelong education free", "생활"),
    ("60대 SNS 시작하기 – 유튜브·인스타그램 활용법", "senior social media youtube", "생활"),
    ("노인 금융 사기 예방 – 보이스피싱 완벽 대처 가이드", "elderly financial fraud prevention", "생활"),
    ("어르신 주택연금 신청 방법 – 집을 담보로 월 생활비 받기", "elderly reverse mortgage", "복지"),
    ("노인 유산 상속 – 미리 준비하는 법정 상속 절차", "elderly inheritance estate planning", "생활"),
    ("시니어 디지털 금융 – 모바일 뱅킹 안전하게 사용하기", "senior mobile banking safety", "생활"),
    ("어르신 전기요금 할인 – 복지 할인 신청 방법 총정리", "elderly electricity bill discount", "복지"),
    ("노인 건강보험료 경감 – 피부양자 등록과 조정 신청", "elderly health insurance reduction", "복지"),
    ("시니어 법률 지원 서비스 – 무료 법률 상담 받는 방법", "elderly free legal service", "복지"),
    ("어르신 장례 사전 준비 – 사전 연명의료 의향서 작성법", "elderly funeral advance directive", "생활"),
    ("노인 고독사 예방 – 안부 확인 서비스 신청 방법", "elderly solitary death prevention", "복지"),
    ("시니어 자원봉사 시간 기록 – 나중에 돌려받는 시간 은행", "senior time bank volunteer", "생활"),
    ("어르신 공연·전시 무료 관람 – 문화 바우처 신청하기", "elderly culture voucher free", "복지"),
    ("60대 새로운 취미 시작하기 – 그림·도예·사진 추천", "senior new hobby painting pottery", "생활"),
    ("노인 수영 배우기 – 관절에 좋은 수중 운동 시작법", "elderly swimming water exercise", "건강"),
    ("어르신 등산 안전 수칙 – 체력에 맞는 산행 코스 선택", "elderly hiking safety mountain", "건강"),
    ("시니어 자전거 타기 – 건강 효과와 안전 장비 선택법", "senior cycling health benefit", "건강"),
    ("노인 게이트볼·파크골프 – 가까운 곳에서 즐기는 스포츠", "elderly gateball park golf sport", "생활"),
    ("어르신 노래·합창 활동 – 건강과 사회성을 키우는 음악", "elderly singing chorus activity", "생활"),
    ("60대 컴퓨터 활용 능력 키우기 – 한글·엑셀 무료 교육", "senior computer skills education", "생활"),
    ("노인 손주 돌봄 수당 – 지자체별 지원 금액과 신청법", "elderly grandchild care allowance", "복지"),
    ("어르신 식사 배달 서비스 – 무료·저가 도시락 신청하기", "elderly meal delivery service", "복지"),
    ("시니어 목욕·이발 지원 서비스 – 거동 불편한 어르신 혜택", "elderly bathing haircut support", "복지"),
    ("노인 보조기기 지원 – 전동휠체어·보행기 무료 대여", "elderly assistive device support", "복지"),
    ("어르신 스트레스 해소법 – 명상·호흡법으로 마음 건강 지키기", "elderly stress relief meditation", "건강"),
    ("노인 기억력 향상 방법 – 치매 예방을 위한 두뇌 활동", "elderly memory improvement brain", "건강"),
    ("시니어 사회적 고립 탈출 – 관계 회복을 위한 활동 추천", "senior social isolation recovery", "건강"),
    ("어르신 분노 조절 – 화를 다스리는 심리적 방법", "elderly anger management mental", "건강"),
    ("60대 인생 2막 설계 – 은퇴 후 의미 있는 삶 만들기", "senior retirement life planning", "생활"),
    ("노인 세대 간 교류 프로그램 – 젊은이와 함께하는 활동", "senior intergenerational program", "생활"),
    ("어르신 일기 쓰기 – 감사 일기로 긍정적 노년 만들기", "elderly gratitude journal writing", "생활"),
    ("시니어 외국어 배우기 – 영어·일어 무료 온라인 강의", "senior foreign language learning free", "생활"),
    ("노인 요리 교실 – 건강식 만들기로 즐거운 노후 보내기", "elderly cooking class healthy", "생활"),
    ("어르신 미술 치료 – 그림 그리기로 치매 예방하는 법", "elderly art therapy dementia", "건강"),
    ("시니어 음악 치료 – 음악으로 기억력·감정 관리하기", "elderly music therapy memory", "건강"),
    ("노인 원예 치료 – 식물 가꾸기로 우울증 극복하기", "elderly horticulture therapy depression", "건강"),
    ("어르신 반려식물 키우기 – 심리적 안정과 공기 정화 효과", "elderly houseplant indoor garden", "생활"),
    ("60대 인생 유산 만들기 – 자녀에게 남기는 삶의 기록", "senior life legacy children", "생활"),
    ("노인 봉사 멘토링 – 경험을 나누고 보람 찾는 법", "elderly mentoring volunteer experience", "생활"),
    ("어르신 명절 외로움 극복 – 가족과 연결되는 방법", "elderly holiday loneliness family", "생활"),
    ("시니어 주거 공동체 – 함께 사는 노후의 새로운 트렌드", "senior cohousing community living", "생활"),
    ("노인 죽음 준비 교육 – 웰다잉으로 인생 마무리하기", "elderly well dying end of life", "생활"),
    ("어르신 스마트 홈 기기 활용 – AI 스피커·안전 센서", "elderly smart home AI speaker", "생활"),
    ("60대 재정 관리 – 노후 자금 절약하는 생활비 관리법", "senior financial management savings", "생활"),
    ("노인 실버 택배·배달 창업 – 소자본으로 시작하는 법", "senior delivery startup small business", "일자리"),
    ("어르신 중고거래 활용법 – 번개장터·당근마켓으로 부수입 만들기", "senior secondhand market income", "일자리"),
    ("시니어 유튜버 시작하기 – 어르신 콘텐츠로 수익 만드는 법", "senior youtuber content creator", "일자리"),
    ("노인 블로그·SNS로 부업하기 – 글쓰기로 수입 만드는 법", "senior blog writing income", "일자리"),
]


def get_existing_titles() -> set:
    titles, page = set(), 1
    res = requests.get(
        f'{WP_URL}/wp-json/wp/v2/categories',
        auth=AUTH,
        params={'slug': COLUMN_CATEGORY_SLUG, 'per_page': 1},
        timeout=10,
    )
    cats = res.json()
    if not cats:
        return titles
    cat_id = cats[0]['id']

    while True:
        res = requests.get(
            f'{WP_URL}/wp-json/wp/v2/posts',
            auth=AUTH,
            params={'categories': cat_id, 'per_page': 100, 'page': page, 'fields': 'id,title'},
            timeout=15,
        )
        if res.status_code != 200:
            break
        batch = res.json()
        if not batch:
            break
        for p in batch:
            titles.add(p['title']['rendered'])
        page += 1
    return titles


def get_category_id(slug: str) -> int | None:
    res = requests.get(
        f'{WP_URL}/wp-json/wp/v2/categories',
        auth=AUTH,
        params={'slug': slug, 'per_page': 1},
        timeout=10,
    )
    cats = res.json()
    return cats[0]['id'] if cats else None


def generate_article(title: str) -> str:
    message = client.messages.create(
        model='claude-haiku-4-5-20251001',
        max_tokens=2000,
        messages=[{
            'role': 'user',
            'content': f'''다음 제목으로 노인·시니어 독자를 위한 실용적인 칼럼을 작성해주세요.
제목: {title}

조건:
- 1,200자 이상
- 마크다운 형식 (## 소제목, **강조** 사용)
- 구체적인 정보와 실천 팁 포함
- 따뜻하고 친근한 문체
- 제목은 포함하지 말고 본문만 작성'''
        }]
    )
    return message.content[0].text


def markdown_to_html(text: str) -> str:
    text = re.sub(r'^## (.+)$', r'<h2>\1</h2>', text, flags=re.MULTILINE)
    text = re.sub(r'^### (.+)$', r'<h3>\1</h3>', text, flags=re.MULTILINE)
    text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)
    paragraphs = []
    for block in text.split('\n\n'):
        block = block.strip()
        if not block:
            continue
        if block.startswith('<h'):
            paragraphs.append(block)
        elif block.startswith(('- ', '* ')):
            items = [f'<li>{line[2:].strip()}</li>' for line in block.split('\n') if line.strip().startswith(('- ', '* '))]
            paragraphs.append('<ul>' + ''.join(items) + '</ul>')
        else:
            paragraphs.append(f'<p>{block}</p>')
    return '\n'.join(paragraphs)


def get_pexels_image(query: str) -> dict | None:
    try:
        res = requests.get(
            'https://api.pexels.com/v1/search',
            headers=PEXELS_HEADERS,
            params={'query': query, 'per_page': 5, 'orientation': 'landscape'},
            timeout=10,
        )
        photos = res.json().get('photos', [])
        return photos[0] if photos else None
    except Exception as e:
        print(f'  [Pexels] 오류: {e}')
    return None


def upload_image(image_url: str, filename: str, alt_text: str) -> int | None:
    try:
        img_data = requests.get(image_url, timeout=15).content
        res = requests.post(
            f'{WP_URL}/wp-json/wp/v2/media',
            auth=AUTH,
            headers={
                'Content-Disposition': f'attachment; filename="{filename}"',
                'Content-Type': 'image/jpeg',
            },
            data=img_data,
            timeout=30,
        )
        if res.status_code == 201:
            media_id = res.json().get('id')
            requests.post(
                f'{WP_URL}/wp-json/wp/v2/media/{media_id}',
                auth=AUTH,
                json={'alt_text': alt_text, 'caption': 'Photo by Pexels'},
                timeout=10,
            )
            return media_id
    except Exception as e:
        print(f'  [WP] 이미지 업로드 오류: {e}')
    return None


def publish_post(title: str, content: str, cat_id: int, media_id: int | None) -> int | None:
    data = {
        'title': title,
        'content': content,
        'status': 'publish',
        'categories': [cat_id],
    }
    if media_id:
        data['featured_media'] = media_id
    try:
        res = requests.post(
            f'{WP_URL}/wp-json/wp/v2/posts',
            auth=AUTH,
            json=data,
            timeout=20,
        )
        if res.status_code == 201:
            return res.json().get('id')
        print(f'  [WP] 발행 실패 {res.status_code}: {res.text[:100]}')
    except Exception as e:
        print(f'  [WP] 발행 오류: {e}')
    return None


def main():
    print('기존 칼럼 제목 로딩...')
    existing = get_existing_titles()
    print(f'기존 칼럼 수: {len(existing)}개')

    cat_id = get_category_id(COLUMN_CATEGORY_SLUG)
    if not cat_id:
        print('칼럼 카테고리를 찾을 수 없습니다.')
        return

    new_topics = [(t, q, c) for t, q, c in TOPICS if t not in existing]
    print(f'발행 가능한 새 주제: {len(new_topics)}개')

    targets = new_topics[:DAILY_LIMIT]
    print(f'오늘 발행할 글: {len(targets)}개\n')

    if not targets:
        print('발행할 새 주제가 없습니다. 주제 풀을 보충해주세요.')
        return

    for i, (title, pexels_query, _) in enumerate(targets, 1):
        print(f'[{i}/{len(targets)}] {title[:50]}')

        try:
            content_md = generate_article(title)
            content_html = markdown_to_html(content_md)
            print(f'  글 생성 완료 ({len(content_md)}자)')
        except Exception as e:
            print(f'  글 생성 실패: {e}')
            time.sleep(5)
            continue

        photo = get_pexels_image(pexels_query)
        media_id = None
        if photo:
            media_id = upload_image(photo['src']['large'], f'col_daily_{i}.jpg', title)
            if media_id:
                print(f'  이미지 업로드 완료 (ID: {media_id})')

        post_id = publish_post(title, content_html, cat_id, media_id)
        if post_id:
            print(f'  발행 완료 (포스트 ID: {post_id})')
        else:
            print('  발행 실패')

        time.sleep(3)

    print('\n오늘 작업 완료!')


if __name__ == '__main__':
    main()
