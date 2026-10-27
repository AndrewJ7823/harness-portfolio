# 기능 스펙: 알림 발송 이력 조회 API

> 하네스 예시용 **가상 기능**이다. 실제 프로젝트·고객 정보와 무관하다.

| 항목 | 값 |
|---|---|
| 티켓 | PROJ-1234 |
| 대상 레포 | `api` |
| 도메인 | notification |
| status | approved |
| 작성일 | 2026-10-20 |

## 0. 요약

- **문제:** 사업장 관리자가 고객에게 나간 알림(문자·알림톡·메일)이 실제로 발송됐는지 직접 확인할 화면이 없어, 문의가 오면 운영팀이 대신 조회해 준다.
- **원인:** 발송 로그는 저장되고 있지만 사업장 단위로 기간 조회하는 API가 없다.
- **변경:** `api`에 사업장별 발송 이력 기간 조회 API 1개를 신규로 추가한다. 기존 발송 로직은 건드리지 않는다.
- **범위:** 조회 전용, 스키마 변경 없음, 백엔드 단독 배포(화면은 후속 티켓).
- **결정:** 최대 조회 기간 92일(작업자 확정), 실패 이력도 포함(작업자 확정 — 리뷰어 질문 1).
- **검증:** 케이스 12건(테스트 11 · waiver 1), 외부 발송 경로 없음.

## 1. 요구사항

- **배경/목표:** 사업장 관리자가 기간을 지정해 자기 사업장의 발송 이력을 최신순으로 확인한다.
- **비목표(scope out):** 화면, 엑셀 다운로드, 재발송, 수신자 정보 노출.
- **미확인/작업자 질문:** 없음(질문 1건 → 확정 완료, §0 결정).
- **리뷰 비채택:** "채널별 필터 케이스 누락" — 필터는 이번 범위가 아님(비목표), 후속 티켓 후보로 record §3에 기록.

## 2. 계약

- **인터페이스:** `GET /workspaces/{workspace_id}/notification-logs`
- **입력:** `start`(date, 필수) · `end`(date, 필수, 당일 포함) · `page`(int ≥ 1, 기본 1) · `page_size`(int, 기본 20, 최대 100 — 초과 시 100으로 보정)
- **출력:** `{ items: [{ id, channel, status, sent_at }], total, page, page_size }` — `sent_at` 내림차순, 같으면 `id` 내림차순
- **에러 계약:** 시작 > 종료 → 400 `start_after_end` / 기간 92일 초과 → 400 `period_too_long` / 다른 사업장 → 403
- **인증/인가:** 로그인 사용자의 소속 사업장 = `workspace_id`일 때만

## 3. 케이스 전수 열거

| ID | 케이스 | 기대 동작 |
|---|---|---|
| C1 | 기간 안에 이력 여러 건 | 기간 내 건만 최신순 반환 |
| C2 | 기간 안에 이력 0건 | 빈 목록, total 0 (에러 아님) |
| C3 | 종료일 23:59:59 / 다음 날 00:00:00 | 앞의 것만 포함 |
| C4 | 시작일 > 종료일 | 400 `start_after_end` |
| C5 | 기간 1일 · 92일 · 93일 | 1·92일은 정상, 93일은 400 `period_too_long` |
| C6 | 다른 사업장 이력 요청 | 403 |
| C7 | page_size 500 요청 | 100으로 보정, 응답 page_size = 100 |
| C8 | 연말~연초에 걸친 기간 | 해를 넘겨도 기간 내 건 모두 반환 |
| C9 | 발송 실패 이력 | 상태값 `failed`로 함께 반환 |
| C10 | 발송 시각이 같은 이력 | id 내림차순으로 순서 고정 |
| C11 | 전체 페이지 수를 넘는 page | 빈 목록, total은 유지 |
| C12 | page = 0 | 422 (입력 검증) |

## 4. 데이터 변경

없음. 기존 발송 로그 테이블의 `(workspace_id, sent_at)` 인덱스를 그대로 쓴다.

## 5. 외부 의존

없음. 조회 전용이라 발송 경로를 타지 않는다. 테스트는 인메모리 저장소(합성 데이터)로 대체한다.

## 6. 테스트 계획

| 케이스 ID | 테스트 |
|---|---|
| C1 | tests/test_notification_history.py::test_C1_returns_logs_in_period |
| C2 | tests/test_notification_history.py::test_C2_no_logs_returns_empty_page |
| C3 | tests/test_notification_history.py::test_C3_end_date_included_until_midnight |
| C4 | tests/test_notification_history.py::test_C4_start_after_end_rejected |
| C5 | tests/test_notification_history.py::test_C5_period_length_boundary |
| C6 | tests/test_notification_history.py::test_C6_other_workspace_forbidden |
| C7 | tests/test_notification_history.py::test_C7_page_size_capped |
| C8 | tests/test_notification_history.py::test_C8_year_boundary |
| C9 | tests/test_notification_history.py::test_C9_failed_logs_included_with_status |
| C10 | tests/test_notification_history.py::test_C10_same_time_ordered_by_id_desc |
| C11 | tests/test_notification_history.py::test_C11_page_out_of_range_keeps_total |
| C12 | waiver ② — 프레임워크 쿼리 파라미터 검증(`ge=1`)이 보장, 커스텀 에러 계약 없음 |

## 7. 화면 영향

없음(화면은 후속 티켓). 백엔드 단독 배포.

## 8. 구현 배치 계획

- 신규: `src/notification_history.py`(조회 로직), `tests/test_notification_history.py`
- 기존 수정 지점: 라우터 등록 1줄뿐
- 재사용: 기존 발송 로그 저장소의 조회 메서드
