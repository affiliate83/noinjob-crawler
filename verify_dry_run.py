"""
Task 4 dry-run 검증 스크립트
목적: dry_run=True 시 create_post, mark_published, 푸시 알림이
     호출되지 않음을 unittest.mock 으로 확인한다.

실행: py verify_dry_run.py
"""
import sys
import os
from unittest.mock import patch, MagicMock

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'crawler'))

# 검증용 픽스처: 실제 API 없이 공고 1건
_FIXTURE_SENURI = [
    {
        'item_id': 'senuri_DRY001',
        'title': '[노인일자리] 드라이런 테스트 공고',
        'content': '<div class="job-detail"><h2>채용 정보</h2></div>',
        'excerpt': '드라이런 테스트 excerpt',
        'deadline': '2026-12-31',
        'region': ('서울', 'seoul'),
        'category': 'senuri',
        '_enrich_data': {
            'company': '테스트기업', 'address': '서울시 강남구',
            'emp_type': '시간제', 'count': '2', 'age': '60',
            'start_date': '2026-07-01', 'deadline': '2026-12-31', 'etc': '',
        },
    }
]

import main as main_module

errors = []

with (
    patch.object(main_module, 'create_post', return_value=None) as mock_create,
    patch.object(main_module, 'mark_published') as mock_mark,
    patch.object(main_module, 'post_exists', return_value=False),
    patch.object(main_module, 'is_published', return_value=False),
    patch.object(main_module.senuri, 'fetch', return_value=_FIXTURE_SENURI),
    patch.object(main_module.welfare, 'fetch', return_value=[]),
):
    main_module.run(dry_run=True, limit=1)

    if mock_create.called:
        errors.append(f'create_post 호출됨 ({mock_create.call_count}회)')
    if mock_mark.called:
        errors.append(f'mark_published 호출됨 ({mock_mark.call_count}회)')

# --limit 없이 기본 실행 시 create_post 는 호출되어야 함 (동작 보존 확인)
with (
    patch.object(main_module, 'create_post', return_value=42) as mock_create_normal,
    patch.object(main_module, 'enrich_job', return_value=''),
    patch.object(main_module, 'mark_published') as mock_mark_normal,
    patch.object(main_module, 'post_exists', return_value=False),
    patch.object(main_module, 'is_published', return_value=False),
    patch.object(main_module.senuri, 'fetch', return_value=_FIXTURE_SENURI),
    patch.object(main_module.welfare, 'fetch', return_value=[]),
    patch('time.sleep'),  # 딜레이 제거
):
    main_module.run(dry_run=False, limit=1)

    if not mock_create_normal.called:
        errors.append('기본 실행에서 create_post 가 호출되지 않음 — 발행 경로 손상')
    if not mock_mark_normal.called:
        errors.append('기본 실행에서 mark_published 가 호출되지 않음 — dedup 기록 손상')

# 예약 수집은 발행하되 게시물별 즉시 푸시를 꺼야 함
with (
    patch.object(main_module, 'create_post', return_value=43) as mock_create_no_push,
    patch.object(main_module, 'enrich_job', return_value=''),
    patch.object(main_module, 'mark_published'),
    patch.object(main_module, 'post_exists', return_value=False),
    patch.object(main_module, 'is_published', return_value=False),
    patch.object(main_module.senuri, 'fetch', return_value=_FIXTURE_SENURI),
    patch.object(main_module.welfare, 'fetch', return_value=[]),
    patch('time.sleep'),
):
    main_module.run(dry_run=False, limit=1, no_push=True)
    if mock_create_no_push.call_args.kwargs.get('send_notification') is not False:
        errors.append('no_push 실행에서 send_notification=False가 전달되지 않음')

if errors:
    print('FAIL:')
    for e in errors:
        print(f'  - {e}')
    sys.exit(1)
else:
    print('PASS: dry-run 시 create_post/mark_published 미호출 확인')
    print('PASS: 기본 실행 시 create_post/mark_published 정상 호출 확인')
    print('PASS: 예약 수집 시 게시물별 즉시 푸시 비활성화 확인')
