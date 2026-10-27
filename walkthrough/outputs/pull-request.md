# PR — PROJ-1234 (예시)

"커밋해줘" 한 마디로 커밋 · 푸시 · PR 생성 · 상태 확인 · 자동 리뷰 대응까지 진행된 결과.

## 커밋

```
feat: 알림 발송 이력 조회 API
```

기능 1건 = 커밋 1개. 영문 conventional 타입 + 한글 내용, 한 줄.

## PR 제목·본문

```markdown
[Feat] 알림 발송 이력 조회 API (PROJ-1234)

- 스펙: specs/PROJ-1234-notification-send-history.md
- 케이스 커버: 12/12 (테스트 11 · waiver 1)
- 기록: records/notification/PROJ-1234-notification-send-history.md
```

## 에이전트의 보고

```
PR: https://github.com/example-org/api/pull/321

- 머지 가능 상태: CLEAN
- CI: 통과
- 자동 리뷰: 코멘트 2건 처리
  1) 매직 넘버 92·100 상수화 → 반영 (커밋 a1b2c3d, 답글 남김)
  2) 정렬을 DB 쿼리로 내리자 → 비채택 (저장소 메서드 변경이 필요해 범위 밖 — 근거 답글, record §3 후속 기록)
- 트래커: in_progress → review
```

보고 첫 줄은 항상 `PR: <전체 URL>`입니다. 도구 출력에 나온 URL을 그대로 쓰고, 직접 조합하지 않습니다.
