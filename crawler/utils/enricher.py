import os
import re
import anthropic
from dotenv import load_dotenv

load_dotenv()

_FENCE_RE = re.compile(r'```[^\n`]*\n?|&#8220;`[a-z]*\s*', re.IGNORECASE)

_client = None


def _get_client():
    global _client
    if _client is None:
        api_key = os.getenv('ANTHROPIC_API_KEY')
        if not api_key:
            return None
        _client = anthropic.Anthropic(api_key=api_key)
    return _client


def enrich_job(data: dict) -> str:
    """채용공고 데이터 dict를 받아 AI 생성 HTML 섹션 반환. 실패 시 빈 문자열."""
    client = _get_client()
    if client is None:
        return ''

    lines = [
        f"- 회사명: {data.get('company', '')}",
        f"- 근무지: {data.get('address', '')}",
        f"- 고용형태: {data.get('emp_type', '')}",
        f"- 모집인원: {data.get('count', '')}명" if data.get('count') else '',
        f"- 지원연령: {data.get('age', '')}세 이상" if data.get('age') else '',
        f"- 모집기간: {data.get('start_date', '')} ~ {data.get('deadline', '')}",
        f"- 기타조건: {data.get('etc', '')}" if data.get('etc') else '',
    ]
    info = '\n'.join(l for l in lines if l)

    prompt = f"""다음 노인 채용 공고 데이터를 바탕으로 시니어 구직자를 위한 HTML 콘텐츠를 작성하세요.

{info}

아래 4개 섹션을 순서대로 HTML로만 출력하세요 (다른 텍스트 없이):

<h2>이런 일을 합니다</h2>
(고용형태와 근무지 기반 예상 업무 2~3문장, p 태그)

<h2>지원 자격 안내</h2>
(연령·기타 조건을 쉬운 말로 ul/li)

<h2>이런 분께 추천합니다</h2>
(어울리는 경험·성향 3개 ul/li)

<h2>자주 묻는 질문</h2>
(아래 형식으로 Q&A 3개)
<div class='faq-item'><h3 class='faq-q'>Q. 질문내용</h3><p class='faq-a'>A. 답변내용</p></div>

규칙: HTML 속성은 작은따옴표. h1 태그 절대 사용 금지(h2·h3만). 코드 펜스(```) 절대 사용 금지. 없는 정보 지어내지 말 것. 쉽고 친근한 말투."""

    try:
        msg = client.messages.create(
            model='claude-haiku-4-5-20251001',
            max_tokens=1500,
            messages=[{'role': 'user', 'content': prompt}],
        )
        return _FENCE_RE.sub('', msg.content[0].text).strip()
    except Exception:
        return ''


def enrich_welfare(data: dict) -> str:
    """복지서비스 데이터 dict를 받아 AI 생성 HTML 섹션 반환. 실패 시 빈 문자열."""
    client = _get_client()
    if client is None:
        return ''

    lines = [
        f"- 서비스명: {data.get('name', '')}",
        f"- 개요: {data.get('overview', '')}",
        f"- 지원 대상: {data.get('target', '')}",
        f"- 선정 기준: {data.get('criteria', '')}" if data.get('criteria') else '',
        f"- 신청 방법: {data.get('how_to', '')}" if data.get('how_to') else '',
        f"- 소관 부처: {data.get('dept', '')}",
        f"- 서비스 형태: {data.get('method', '')}" if data.get('method') else '',
    ]
    info = '\n'.join(l for l in lines if l)

    prompt = f"""다음 복지서비스 데이터를 바탕으로 어르신과 가족을 위한 HTML 콘텐츠를 작성하세요.

{info}

아래 3개 섹션을 순서대로 HTML로만 출력하세요 (다른 텍스트 없이):

<h2>이 서비스가 도움이 되는 분</h2>
(지원 대상을 쉬운 말로 ul/li 3~4개)

<h2>신청 전 꼭 확인하세요</h2>
(선정 기준·유의사항 2~3개 ul/li)

<h2>자주 묻는 질문</h2>
(아래 형식으로 Q&A 3개)
<div class='faq-item'><h3 class='faq-q'>Q. 질문내용</h3><p class='faq-a'>A. 답변내용</p></div>

규칙: HTML 속성은 작은따옴표. h1 태그 절대 사용 금지(h2·h3만). 코드 펜스(```) 절대 사용 금지. 없는 정보 지어내지 말 것. 쉽고 친근한 말투."""

    try:
        msg = client.messages.create(
            model='claude-haiku-4-5-20251001',
            max_tokens=1500,
            messages=[{'role': 'user', 'content': prompt}],
        )
        return _FENCE_RE.sub('', msg.content[0].text).strip()
    except Exception:
        return ''


def enrich_from_html(html: str, post_type: str) -> str:
    """기존 발행 글 HTML 기반으로 추가 섹션 생성. 일괄 업데이트용."""
    client = _get_client()
    if client is None:
        return ''

    if post_type == 'job':
        extra_sections = """\
<h2>이런 일을 합니다</h2>
(예상 업무 2~3문장, p 태그)

<h2>지원 자격 안내</h2>
(연령·기타 조건 ul/li)

<h2>이런 분께 추천합니다</h2>
(어울리는 경험·성향 3개 ul/li)"""
    else:
        extra_sections = """\
<h2>이 서비스가 도움이 되는 분</h2>
(지원 대상 ul/li 3~4개)

<h2>신청 전 꼭 확인하세요</h2>
(유의사항 2~3개 ul/li)"""

    prompt = f"""다음 HTML 콘텐츠를 분석하고 추가 섹션을 작성하세요.

기존 콘텐츠:
{html[:2000]}

추가할 섹션 (HTML만 출력, 다른 텍스트 없이):

{extra_sections}

<h2>자주 묻는 질문</h2>
(아래 형식으로 Q&A 3개)
<div class='faq-item'><h3 class='faq-q'>Q. 질문내용</h3><p class='faq-a'>A. 답변내용</p></div>

규칙: HTML 속성은 작은따옴표. h1 태그 절대 사용 금지(h2·h3만). 코드 펜스(```) 절대 사용 금지. 기존 내용 기반으로 작성. 쉽고 친근한 말투."""

    try:
        msg = client.messages.create(
            model='claude-haiku-4-5-20251001',
            max_tokens=1500,
            messages=[{'role': 'user', 'content': prompt}],
        )
        return _FENCE_RE.sub('', msg.content[0].text).strip()
    except Exception:
        return ''