"""PROJ-1234 알림 발송 이력 조회.

하네스 예시용 가상 기능이다. 스펙: harness/specs/PROJ-1234-notification-send-history.md
저장소 접근은 `SendLogRepository` 프로토콜 뒤로 숨긴다 — 테스트는 인메모리 구현(합성 데이터)만 쓴다.
"""

from dataclasses import dataclass
from datetime import date, datetime, time, timedelta
from typing import Protocol

MAX_PERIOD_DAYS = 92
DEFAULT_PAGE_SIZE = 20
MAX_PAGE_SIZE = 100


class InvalidPeriod(ValueError):
    """조회 기간 계약 위반(400)."""


class Forbidden(PermissionError):
    """다른 사업장 이력 접근(403)."""


@dataclass(frozen=True)
class SendLog:
    id: int
    workspace_id: int
    channel: str  # sms | kakao | email
    status: str  # sent | failed
    sent_at: datetime


@dataclass(frozen=True)
class Page:
    items: list[SendLog]
    total: int
    page: int
    page_size: int


class SendLogRepository(Protocol):
    def find_by_workspace(self, workspace_id: int, lower: datetime, upper: datetime) -> list[SendLog]: ...


def list_send_history(
    repo: SendLogRepository,
    *,
    requester_workspace_id: int,
    workspace_id: int,
    start: date,
    end: date,
    page: int = 1,
    page_size: int = DEFAULT_PAGE_SIZE,
) -> Page:
    """사업장의 알림 발송 이력을 기간으로 조회한다. 최신순, end 일자 포함."""
    if requester_workspace_id != workspace_id:
        raise Forbidden("workspace_mismatch")
    if start > end:
        raise InvalidPeriod("start_after_end")
    if (end - start).days + 1 > MAX_PERIOD_DAYS:
        raise InvalidPeriod("period_too_long")

    page_size = min(page_size, MAX_PAGE_SIZE)
    # end 일자를 통째로 포함하려고 상한을 다음 날 0시(미포함)로 잡는다 — C3.
    lower = datetime.combine(start, time.min)
    upper = datetime.combine(end + timedelta(days=1), time.min)

    rows = repo.find_by_workspace(workspace_id, lower, upper)
    rows = sorted(rows, key=lambda r: (r.sent_at, r.id), reverse=True)

    offset = (page - 1) * page_size
    return Page(items=rows[offset : offset + page_size], total=len(rows), page=page, page_size=page_size)
