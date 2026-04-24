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


def create_post(title: str, content: str, category: str = 'senuri', excerpt: str = '', deadline: str = '') -> int | None:
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