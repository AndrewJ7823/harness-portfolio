# 세션 기록 — PROJ-1234 하나를 끝까지

가상의 기능 하나로 실제 세션 흐름을 재구성했습니다. `▶` 표시가 제가 입력한 부분이고, 나머지는 에이전트가 진행합니다.

---

### ▶ 시작

```
/develop-feature PROJ-1234
```

```
에이전트: 티켓 PROJ-1234 확인 — "사업장 관리자가 알림 발송 이력을 기간으로 조회"
          담당자: andrewj7823 (본인) · 하네스 트래커에는 없음 → todo로 등록 후 spec으로 전환
          기존 자산 조사: 발송 로그 저장소에 workspace 기준 조회 메서드 있음 → 재사용
          스펙 초안 작성 중… specs/PROJ-1234-notification-send-history.md
```

### 독립 반박 검토 (에이전트끼리)

```
에이전트: 검토 에이전트 실행 → 지적 4건 (빠진 케이스 3 · 계약 모순 1)
          3건 반영(C3·C10 추가, page_size 계약 명시), 1건 비채택(채널 필터 — 비목표)
```

→ [outputs/spec-review.md](outputs/spec-review.md)

### ▶ 스펙 승인

```
에이전트: 스펙 승인 요청드립니다.
          specs/PROJ-1234-notification-send-history.md
          - 케이스 12건 (테스트 11 · waiver 1)
          - 데이터 변경: 없음 / 외부 의존: 없음 / 화면 영향: 없음
          - 검토 지적 4건 / 반영 3건
          질문 1. 발송 실패 이력도 목록에 보여줄까요? (기본안: 포함)

나     : 질문 1은 기본안대로. 스펙 승인
```

```
에이전트: 스펙 status: draft → approved, 트래커 spec → in_progress, 이슈 트래커 "진행중" 전환
          feat/PROJ-1234 브랜치 생성 (origin/main 베이스)
          C1~C11 테스트 먼저 작성 → 11 failed (구현 전이라 정상)
          구현 → 검증 진행
```

### 검증 (FAIL → 수정 → PASS)

```
에이전트: 1차 검증 FAIL — C3(종료일 자정 경계) 실패. 상한 조건 수정
          2차 검증 PASS — 케이스 12/12 · 13 passed · 감사기 PASS · 스모크 일치
          record 작성, 트래커 in_progress → review
          diff 검토 부탁드립니다. (신규 2파일 + 라우터 1줄)
```

→ [outputs/verify-report.md](outputs/verify-report.md) · [record](harness/records/notification/PROJ-1234-notification-send-history.md)

### ▶ 커밋해줘

```
나     : 커밋해줘
```

```
에이전트: PR: https://github.com/example-org/api/pull/321
          CLEAN · CI 통과 · 자동 리뷰 2건 처리(반영 1 · 비채택 1)
```

→ [outputs/pull-request.md](outputs/pull-request.md)

### ▶ 머지 · 배포

사람이 합니다. 머지 후 확인이 끝나면 "done 처리해줘" → 트래커 `done`, 이슈 트래커 상태 전환.

---

**제가 입력한 것:** 명령 1줄, "스펙 승인", 질문 답 1개, "커밋해줘".
