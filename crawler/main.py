import sys
import os
import time
import argparse

sys.path.insert(0, os.path.dirname(__file__))

from utils.logger import logger
from utils.dedup import is_published, mark_published
from utils.enricher import enrich_job, enrich_welfare
from sources import senuri, welfare
from poster.wordpress import post_exists, create_post


def run(dry_run: bool = False, limit: int | None = None, no_push: bool = False):
    mode_tag = "[DRY-RUN] " if dry_run else ""
    logger.info("=" * 50)
    logger.info(f"{mode_tag}[시작] noinjob.kr — 자동 수집 봇 시작")
    logger.info("=" * 50)
    if dry_run:
        logger.info("[DRY-RUN] WordPress 발행 / dedup.db 기록 / 푸시 알림을 건너뜁니다.")

    all_items = []
    all_items += senuri.fetch(max_pages=5)
    all_items += welfare.fetch(max_items=100)

    if limit is not None:
        all_items = all_items[:limit]
        logger.info(f"[진행] --limit {limit} 적용 — {len(all_items)}건으로 제한")

    logger.info(f"[진행] 총 {len(all_items)}건 수집 완료, {'확인' if dry_run else '발행'} 시작")

    success = 0
    skip = 0
    would_publish = []

    for item in all_items:
        item_id = item['item_id']
        title = item['title']

        # dedup.db 읽기는 dry-run에서도 수행 (로컬, 읽기 전용)
        if is_published(item_id):
            skip += 1
            continue

        # post_exists()는 WordPress GET 호출 — dry-run에서는 건너뜀
        if not dry_run and post_exists(title):
            mark_published(item_id, title)
            skip += 1
            continue

        # AI enrichment: 실제 발행 시에만 실행 (dry-run에서는 Anthropic API 불필요)
        if not dry_run:
            enrich_data = item.get('_enrich_data', {})
            if enrich_data:
                category = item.get('category', '')
                if category == 'senuri':
                    enriched = enrich_job(enrich_data)
                elif category == 'welfare':
                    enriched = enrich_welfare(enrich_data)
                else:
                    enriched = ''
                if enriched:
                    item['content'] = item['content'].rsplit('</div>', 1)[0] + enriched + '\n\n</div>'

        if dry_run:
            region_info = item.get('region')
            region_label = region_info[0] if region_info else '기타'
            logger.info(
                f"[DRY-RUN] 발행 예정: [{item.get('category', '?')}] "
                f"{title[:50]} | 지역:{region_label} | 마감:{item.get('deadline', '-')}"
            )
            would_publish.append(title)
        else:
            post_id = create_post(
                title=title,
                content=item['content'],
                category=item.get('category', 'senuri'),
                excerpt=item.get('excerpt', ''),
                deadline=item.get('deadline', ''),
                region=item.get('region'),
                send_notification=not no_push,
            )
            if post_id:
                mark_published(item_id, title)
                success += 1
            time.sleep(3)

    logger.info("=" * 50)
    if dry_run:
        logger.info(f"[DRY-RUN] 발행 예정: {len(would_publish)}건 / 이미 처리됨(dedup): {skip}건")
        logger.info("[DRY-RUN] 실제 발행 없음. WordPress 및 dedup.db 변경 없음.")
    else:
        logger.info(f"[완료] 발행: {success}건 / 건너뜀: {skip}건")
    logger.info("=" * 50)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='noinjob.kr 자동 수집 봇')
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='수집만 하고 WordPress 발행, dedup.db 기록, 푸시 알림을 건너뜀',
    )
    parser.add_argument(
        '--limit',
        type=int,
        default=None,
        metavar='N',
        help='처리할 최대 항목 수 (기본값: 무제한)',
    )
    parser.add_argument(
        '--no-push',
        action='store_true',
        help='새 게시물 발행 시 즉시 푸시 알림을 보내지 않음',
    )
    args = parser.parse_args()
    run(dry_run=args.dry_run, limit=args.limit, no_push=args.no_push)
