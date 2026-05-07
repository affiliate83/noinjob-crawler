import os
import json
import requests
from dotenv import load_dotenv
from utils.logger import logger

load_dotenv()

WP_URL = os.getenv('WP_URL')
WP_USER = os.getenv('WP_USER')
WP_APP_PASS = os.getenv('WP_APP_PASS')

CATEGORY_IDS = {
    'senuri': 2,   # 노인일자리
    'welfare': 3,  # 복지혜택
}

_region_cache: dict[str, int] = {}


def get_or_create_region_term(name: str, slug: str) -> int | None:
    """job_region 택소노미 텀 ID 반환. 없으면 생성."""
    if slug in _region_cache:
        return _region_cache[slug]
    try:
        res = requests.get(
            f"{WP_URL}/wp-json/wp/v2/job_region",
            auth=(WP_USER, WP_APP_PASS),
            params={'slug': slug, 'per_page': 1},
            timeout=10,
        )
        terms = res.json()
        if isinstance(terms, list) and terms:
            _region_cache[slug] = terms[0]['id']
            return _region_cache[slug]
    except Exception as e:
        logger.error(f"[WP] 지역 텀 조회 실패: {e}")
        return None
    try:
        res = requests.post(
            f"{WP_URL}/wp-json/wp/v2/job_region",
            auth=(WP_USER, WP_APP_PASS),
            headers={'Content-Type': 'application/json'},
            data=json.dumps({'name': name, 'slug': slug}),
            timeout=10,
        )
        if res.status_code == 201:
            term_id = res.json().get('id')
            _region_cache[slug] = term_id
            logger.info(f"[WP] 지역 텀 생성: {name} (ID:{term_id})")
            return term_id
    except Exception as e:
        logger.error(f"[WP] 지역 텀 생성 실패: {e}")
    return None


def post_exists(title: str) -> bool:
    try:
        res = requests.get(
            f"{WP_URL}/wp-json/wp/v2/posts",
            auth=(WP_USER, WP_APP_PASS),
            params={'search': title, 'per_page': 5},
            timeout=10
        )
        for post in res.json():
            if post.get('title', {}).get('rendered', '').strip() == title.strip():
                return True
    except Exception as e:
        logger.error(f"[WP] 중복 확인 실패: {e}")
    return False


def _save_post_meta(post_id: int, key: str, value: str):
    try:
        requests.post(
            f"{WP_URL}/wp-json/wp/v2/posts/{post_id}",
            auth=(WP_USER, WP_APP_PASS),
            headers={'Content-Type': 'application/json'},
            data=json.dumps({'meta': {key: value}}),
            timeout=10
        )
    except Exception as e:
        logger.error(f"[WP] 메타 저장 실패 ID:{post_id} {key}: {e}")


def create_post(title: str, content: str, category: str = 'senuri', excerpt: str = '', deadline: str = '', region: tuple | None = None) -> int | None:
    if not all([WP_URL, WP_USER, WP_APP_PASS]):
        logger.error("[WP] .env 연결 정보 누락")
        return None

    data = {
        'title': title,
        'content': content,
        'excerpt': excerpt,
        'status': 'publish',
    }

    cat_id = CATEGORY_IDS.get(category)
    if cat_id:
        data['categories'] = [cat_id]

    if region:
        name, slug = region
        term_id = get_or_create_region_term(name, slug)
        if term_id:
            data['job_region'] = [term_id]

    try:
        res = requests.post(
            f"{WP_URL}/wp-json/wp/v2/posts",
            auth=(WP_USER, WP_APP_PASS),
            headers={'Content-Type': 'application/json'},
            data=json.dumps(data),
            timeout=15
        )
        if res.status_code == 201:
            post_id = res.json().get('id')
            logger.info(f"[WP] 발행 성공 ID:{post_id} — {title[:40]}")
            if deadline and post_id:
                _save_post_meta(post_id, '_deadline', deadline)
            return post_id
        else:
            logger.error(f"[WP] 발행 실패 {res.status_code}: {res.text[:200]}")
            return None
    except Exception as e:
        logger.error(f"[WP] 통신 오류: {e}")
        return None