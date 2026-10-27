#!/usr/bin/env python3
"""개념 예시 — 보호 브랜치로의 직접 push를 막는 PreToolUse 훅.

실제 하네스의 가드 훅이 아니다. "규칙을 문서에만 두지 않고 훅으로도 막는다"가
어떤 모양인지 보여 주는 최소 예시다.

Claude Code는 Bash 도구를 실행하기 직전에 이 스크립트에 JSON(stdin)을 넘긴다.
exit 2 + stderr 메시지 = 차단(메시지는 에이전트에게 전달된다), exit 0 = 통과.
"""

import json
import re
import sys

PROTECTED = {"main", "master", "prd", "dev"}


def main() -> int:
    try:
        payload = json.load(sys.stdin)
    except ValueError:
        return 0  # 입력을 못 읽으면 통과(fail-open) — 문서 규칙이 1차 방어선이다

    command = payload.get("tool_input", {}).get("command", "")
    for segment in re.split(r"&&|\|\||;", command):
        tokens = segment.split()
        if tokens[:2] != ["git", "push"]:
            continue
        targets = {t.split(":")[-1] for t in tokens[2:] if not t.startswith("-")}
        hit = targets & PROTECTED
        if hit:
            print(
                f"보호 브랜치({', '.join(sorted(hit))})로 직접 push할 수 없습니다. "
                "작업 브랜치로 push하고 PR을 여세요.",
                file=sys.stderr,
            )
            return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
