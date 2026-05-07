import os
import time
import requests
import xml.etree.ElementTree as ET
from dotenv import load_dotenv
from utils.logger import logger
from utils.enricher import enrich_job
from utils.region import extract_region

load_dotenv()

API_KEY = os.getenv('DATA_GO_KR_API_KEY')
ENDPOINT = os.getenv('SENURI_API_ENDPOINT', 'https://apis.data.go.kr/B552474/SenuriService')


EMPL_TYPE = {
    'CM0101': '정규직',
    'CM0102': '계약직',
    'CM0103': '시간제',
    'CM0104': '일용직',
    'CM0105': '기간제',
    'CM0106': '파견직',
    'CM0107': '용역직',
    'CM0108': '특수고용',
    'CM0109': '프리랜서',
    'CM0110': '기타',
}


def _xml_text(element, tag, default=''):
    node = element.find(tag)
    return node.text.strip() if node is not None and node.text else default


def _get_job_list(page=1, size=100):
    url = f"{ENDPOINT}/getJobList"
    params = {
        'serviceKey': API_KEY,
        'numOfRows': size,
        'pageNo': page,
    }
    try:
        res = requests.get(url, params=params, timeout=15)
        res.raise_for_status()
        root = ET.fromstring(res.content)
        items = root.findall('.//item')
        total_node = root.find('.//totalCount')
        total = int(total_node.text) if total_node is not None and total_node.text else 0
        return items, total
    except Exception as e:
        logger.error(f"[노인구인정보] 목록 조회 실패: {e}")
        return [], 0


def _get_job_detail(job_id):
    url = f"{ENDPOINT}/getJobInfo"
    params = {
        'serviceKey': API_KEY,
        'id': job_id,
    }
    try:
        res = requests.get(url, params=params, timeout=15)
        res.raise_for_status()
        root = ET.fromstring(res.content)
        item = root.find('.//item')
        return item
    except Exception as e:
        logger.error(f"[노인구인정보] 상세 조회 실패 (id={job_id}): {e}")
        return None


def fmt_date(d):
    return f"{d[:4]}-{d[4:6]}-{d[6:]}" if len(d) == 8 else d


def _build_content(item, detail):
    def t(el, tag):
        return _xml_text(el, tag) if el is not None else ''

    company    = t(detail, 'plbizNm') or t(item, 'oranNm')
    address    = t(detail, 'plDetAddr')
    emp_type   = EMPL_TYPE.get(t(item, 'emplymShpNm'), t(item, 'emplymShpNm'))
    start_date = fmt_date(t(item, 'frDd'))
    deadline   = fmt_date(t(item, 'toDd'))
    age        = t(detail, 'age')
    count      = t(detail, 'clltPrnnum')
    clerk      = t(detail, 'clerk')
    phone      = t(detail, 'clerkContt')
    homepage   = t(detail, 'homepage')
    etc        = t(detail, 'etcItm')

    rows = [
        ('회사명', company),
        ('근무지', address),
        ('고용형태', emp_type),
        ('모집인원', f"{count}명" if count else ''),
        ('지원연령', f"{age}세 이상" if age else ''),
        ('모집기간', f"{start_date} ~ {deadline}"),
        ('담당자', clerk),
        ('연락처', phone),
        ('홈페이지', f'<a href="{homepage}">{homepage}</a>' if homepage else ''),
        ('기타', etc),
    ]

    table_rows = '\n'.join(
        f'  <tr><th>{k}</th><td>{v}</td></tr>'
        for k, v in rows if v
    )

    content = f'<div class="job-detail">\n\n<h2>채용 정보</h2>\n<table class="job-table">\n{table_rows}\n</table>\n\n'

    enriched = enrich_job({
        'company': company, 'address': address, 'emp_type': emp_type,
        'count': count, 'age': age, 'start_date': start_date,
        'deadline': deadline, 'etc': etc,
    })
    if enriched:
        content += enriched + '\n\n'

    content += '</div>'
    return content


def fetch(max_pages=5):
    logger.info("[노인구인정보] 수집 시작")
    results = []

    for page in range(1, max_pages + 1):
        items, total = _get_job_list(page=page)
        if not items:
            logger.info(f"[노인구인정보] 페이지 {page} — 데이터 없음, 종료")
            break

        logger.info(f"[노인구인정보] 페이지 {page} — {len(items)}건 (전체 {total}건)")

        for item in items:
            job_id = _xml_text(item, 'jobId')
            if not job_id:
                continue

            time.sleep(2)
            detail = _get_job_detail(job_id)

            company = _xml_text(item, 'oranNm')
            title = f"[노인일자리] {_xml_text(item, 'recrtTitle') or company}"
            content = _build_content(item, detail)

            emp_type = EMPL_TYPE.get(_xml_text(item, 'emplymShpNm'), _xml_text(item, 'emplymShpNm'))
            address = _xml_text(detail, 'plDetAddr') if detail is not None else ''
            excerpt = f"{company} | {emp_type} | {address}".strip(' |')
            deadline = fmt_date(_xml_text(item, 'toDd'))
            region = extract_region(address)

            results.append({
                'item_id': f"senuri_{job_id}",
                'title': title,
                'content': content,
                'excerpt': excerpt,
                'deadline': deadline,
                'region': region,
                'post_type': 'post',
                'category': 'senuri',
            })

        if len(items) < 100:
            break
        time.sleep(3)

    logger.info(f"[노인구인정보] 수집 완료 — {len(results)}건")
    return results