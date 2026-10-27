# 검증 보고 — PROJ-1234

> `/verify-feature PROJ-1234`가 남기는 판정 보고(예시). 기준은 "테스트가 통과했다"가 아니라 **"승인된 스펙의 케이스가 전부 테스트로 증명됐다"** 이다.

## 1차 — FAIL

```
케이스 매핑
  C1  COVERED  test_C1_returns_logs_in_period
  C2  COVERED  test_C2_no_logs_returns_empty_page
  C3  COVERED  test_C3_end_date_included_until_midnight
  ...
  C11 COVERED  test_C11_page_out_of_range_keeps_total
  C12 WAIVER   ② 프레임워크 보장
  케이스 커버 12/12 (테스트 11 · waiver 1) · GAP 0

테스트
  pytest -q → 1 failed, 12 passed
  FAILED test_C3_end_date_included_until_midnight
```

| 항목 | 값 |
|---|---|
| 케이스 커버 | 12/12 (waiver 1건 — 프레임워크 입력 검증) |
| 테스트 | `pytest -q` → `1 failed, 12 passed` |
| 감사기 | 경로 규칙 PASS |
| 스모크 | 미실행(테스트 FAIL) |
| **종합 판정** | **FAIL** — 종료일 상한을 `<= end 00:00`으로 잡아 종료일 당일 이력이 빠짐 |

→ 상한을 "다음 날 0시 미포함"으로 고친 뒤 재검증.

## 2차 — PASS

| 항목 | 값 |
|---|---|
| 케이스 커버 | 12/12 (waiver 1건) · GAP 0 |
| 테스트 | `pytest -q` → `13 passed` |
| 감사기 | 경로 규칙 PASS |
| 스모크 | C1 정상 일치 · C4 400 일치 · C3 자정 경계 일치 (로컬 DB + 합성 행) |
| **종합 판정** | **PASS** |

> C3는 검토 에이전트가 찾아 준 케이스입니다. 이 케이스가 스펙에 없었다면 "테스트 전부 통과"로 끝났을 것이고, 결함은 배포 후에야 발견됐을 겁니다.
