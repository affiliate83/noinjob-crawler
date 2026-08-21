"""
노인잡 앱 푸시 알림 발송 유틸리티
Expo Push Notification API 사용
"""
import requests
import logging

WP_TOKEN_API = 'https://noinjob.kr/wp-json/noinjob/v1/push-tokens'
EXPO_PUSH_API = 'https://exp.host/--/api/v2/push/send'

logger = logging.getLogger(__name__)


def get_tokens_for_region(region_slug: str | None = None) -> list[str]:
    """WordPress에서 특정 지역 구독자 토큰 조회"""
    try:
        params = {'region': region_slug} if region_slug else {}
        res = requests.get(WP_TOKEN_API, params=params, timeout=10)
        res.raise_for_status()
        return res.json().get('tokens', [])
    except Exception as e:
        logger.warning(f'토큰 조회 실패: {e}')
        return []


def send_push(tokens: list[str], title: str, body: str, data: dict = None) -> None:
    """Expo Push API로 알림 발송 (최대 100개씩 배치)"""
    if not tokens:
        return

    messages = [
        {
            'to': token,
            'title': title,
            'body': body,
            'data': data or {},
            'sound': 'default',
        }
        for token in tokens
        if token.startswith('ExponentPushToken') or token.startswith('ExpoPushToken')
    ]

    # 100개씩 나눠서 발송
    for i in range(0, len(messages), 100):
        batch = messages[i:i + 100]
        try:
            res = requests.post(
                EXPO_PUSH_API,
                json=batch,
                headers={'Content-Type': 'application/json'},
                timeout=15,
            )
            res.raise_for_status()
            logger.info(f'푸시 발송 완료: {len(batch)}건')
        except Exception as e:
            logger.warning(f'푸시 발송 실패: {e}')


def notify_new_job(post_id: int, title: str, region_slug: str | None = None) -> None:
    """새 공고 등록 시 호출 — 해당 지역 구독자에게 알림 발송"""
    tokens = get_tokens_for_region(region_slug)
    if not tokens:
        logger.info(f'구독자 없음 (region={region_slug}), 푸시 생략')
        return

    region_label = f' [{region_slug}]' if region_slug else ''
    send_push(
        tokens=tokens,
        title=f'🔔 새 공고{region_label}',
        body=title,
        data={'postId': post_id},
    )
    logger.info(f'푸시 발송: postId={post_id}, region={region_slug}, 수신자={len(tokens)}명')
