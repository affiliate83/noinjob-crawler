import sys
import os
import time

sys.path.insert(0, os.path.dirname(__file__))

from utils.logger import logger
from utils.dedup import is_published, mark_published
from sources import senuri, welfare
from poster.wordpress import post_exists, create_post


def run():
    logger.info("=" * 50)
    logger.info("👴 noinjob.kr — 자동 수집 봇 시작")
    logger.info("=" * 50)

    all_items = []
    all_items += senuri.fetch(max_pages=5)
    all_items += welfare.fetch(max_items=100)

    logger.info(f"[진행] 총 {len(all_items)}건 수집 완료, 발행 시작")

    success = 0
    skip = 0

    for item in all_items:
        item_id = item['item_id']
        title = item['title']

        if is_published(item_id):
            skip += 1
            continue

        if post_exists(title):
            mark_published(item_id, title)
            skip += 1
            continue

        post_id = create_post(
            title=title,
            content=item['content'],
            category=item.get('category', 'senuri'),
            excerpt=item.get('excerpt', ''),
            deadline=item.get('deadline', ''),
            region=item.get('region'),
        )

        if post_id:
            mark_published(item_id, title)
            success += 1

        time.sleep(3)

    logger.info("=" * 50)
    logger.info(f"👴 완료 — 발행: {success}건 / 건너뜀: {skip}건")
    logger.info("=" * 50)


if __name__ == "__main__":
    run()