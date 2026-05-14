import os
import time
import requests
import xml.etree.ElementTree as ET
from dotenv import load_dotenv
from utils.logger import logger

load_dotenv()

API_KEY = os.getenv('DATA_GO_KR_API_KEY')
ENDPOINT = os.getenv('WELFARE_API_ENDPOINT', 'https://apis.data.go.kr/B554287/NationalWelfareInformationsV001')


def _xml_text(element, tag, default=''):
    if element is None:
        return default
    node = element.find(tag)
    return node.text.strip() if node is not None and node.text else default


def _get_welfare_list(page=1, size=100):
    url = f"{ENDPOINT}/NationalWelfarelistV001"
    params = {
        'serviceKey': API_KEY,
        'numOfRows': size,
        'pageNo': page,
        'srchKeyCode': '001',
    }
    try:
        res = requests.get(url, params=params, timeout=15)
        res.raise_for_status()
        root = ET.fromstring(res.content)
        items = root.findall('.//servList') or root.findall('.//item')
        total_node = root.find('.//totCnt') or root.find('.//totalCount')
        total = int(total_node.text) if total_node is not None and total_node.text else 0
        return items, total
    except Exception as e:
        logger.error(f"[복지서비스] 목록 조회 실패: {e}")
        return [], 0


def _get_welfare_detail(service_id):
    url = f"{ENDPOINT}/NationalWelfaredetailedV001"
    params = {
        'serviceKey': API_KEY,
        'servId': service_id,
    }
    try:
        res = requests.get(url, params=params, timeout=15)
        if res.status_code == 429:
            logger.warning(f"[복지서비스] 상세 API 할당량 초과 (id={service_id}), 목록 데이터만 사용")
            return None
        res.raise_for_status()
        root = ET.fromstring(res.content)
        return root.find('.//servDtlInfo') or root.find('.//item')
    except Exception as e:
        logger.error(f"[복지서비스] 상세 조회 실패 (id={service_id}): {e}")
        return None


def _build_content(item, detail):
    # 목록 API 필드
    overview   = _xml_text(item, 'servDgst')
    dept       = _xml_text(item, 'jurMnofNm')
    org        = _xml_text(item, 'jurOrgNm')
    contact    = _xml_text(item, 'rprsCtadr')
    detail_url = _xml_text(item, 'servDtlLink')
    cycle      = _xml_text(item, 'sprtCycNm')
    method     = _xml_text(item, 'srvPvsnNm')
    online     = _xml_text(item, 'onapPsbltYn')
    themes     = _xml_text(item, 'intrsThemaArray')

    # 상세 API 필드 (있을 때만)
    if detail is not None:
        overview   = _xml_text(detail, 'wlfareInfoOutlCn') or overview
        target     = _xml_text(detail, 'tgtrDtlCn') or _xml_text(item, 'tgtrDtlCn')
        criteria   = _xml_text(detail, 'slctCritCn')
        how_to     = _xml_text(detail, 'alwServCn')
        contact    = _xml_text(detail, 'rprsCtadr') or contact
        dept       = _xml_text(detail, 'jurMnofNm') or dept
    else:
        target   = _xml_text(item, 'tgtrDtlCn')
        criteria = ''
        how_to   = ''

    online_text = '가능' if online == 'Y' else ('불가' if online == 'N' else '')

    content = '<div class="welfare-detail">\n\n'

    if overview:
        content += f'<h2>서비스 개요</h2>\n<p>{overview}</p>\n\n'

    if target:
        content += f'<h2>지원 대상</h2>\n<p>{target}</p>\n\n'

    if criteria:
        content += f'<h2>선정 기준</h2>\n<p>{criteria}</p>\n\n'

    if how_to:
        content += f'<h2>신청 방법</h2>\n<p>{how_to}</p>\n\n'

    # 서비스 정보 표
    info_rows = [
        ('소관 부처', dept),
        ('소관 기관', org),
        ('지원 주기', cycle),
        ('서비스 형태', method),
        ('온라인 신청', online_text),
        ('관심 테마', themes.replace(',', ', ') if themes else ''),
        ('문의처', contact),
    ]
    table_rows = '\n'.join(
        f'  <tr><th>{k}</th><td>{v}</td></tr>'
        for k, v in info_rows if v
    )
    if table_rows:
        content += f'<h2>서비스 정보</h2>\n<table class="welfare-table">\n{table_rows}\n</table>\n\n'

    if detail_url:
        content += (
            f'<div class="welfare-link">\n'
            f'<a href="{detail_url}">복지로에서 자세한 내용 확인하기 →</a>\n'
            f'</div>\n\n'
        )

    content += '</div>'
    return content


def fetch(max_items=100):
    logger.info("[복지서비스] 수집 시작")
    results = []

    items, total = _get_welfare_list(page=1, size=max_items)
    logger.info(f"[복지서비스] {len(items)}건 수집 (전체 {total}건)")

    for item in items:
        service_id = _xml_text(item, 'servId')
        if not service_id:
            continue

        time.sleep(2)
        detail = _get_welfare_detail(service_id)

        name    = _xml_text(item, 'servNm')
        title   = f"[복지혜택] {name}"
        content = _build_content(item, detail)
        summary = _xml_text(item, 'servDgst')
        excerpt = summary[:100] if summary else ''

        overview = _xml_text(item, 'servDgst')
        dept     = _xml_text(item, 'jurMnofNm')
        method   = _xml_text(item, 'srvPvsnNm')
        if detail is not None:
            overview = _xml_text(detail, 'wlfareInfoOutlCn') or overview
            target   = _xml_text(detail, 'tgtrDtlCn') or _xml_text(item, 'tgtrDtlCn')
            criteria = _xml_text(detail, 'slctCritCn')
            how_to   = _xml_text(detail, 'alwServCn')
        else:
            target   = _xml_text(item, 'tgtrDtlCn')
            criteria = ''
            how_to   = ''

        results.append({
            'item_id': f"welfare_{service_id}",
            'title': title,
            'content': content,
            'excerpt': excerpt,
            'post_type': 'post',
            'category': 'welfare',
            '_enrich_data': {
                'name': name, 'overview': overview, 'target': target,
                'criteria': criteria, 'how_to': how_to, 'dept': dept, 'method': method,
            },
        })

    logger.info(f"[복지서비스] 수집 완료 — {len(results)}건")
    return results
