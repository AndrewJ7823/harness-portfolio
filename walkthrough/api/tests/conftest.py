import sys
from datetime import datetime
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from notification_history import SendLog  # noqa: E402


class InMemorySendLogRepository:
    """합성 데이터 전용 저장소. 공유·운영 DB 행을 옮겨 오지 않는다."""

    def __init__(self, rows: list[SendLog]):
        self.rows = rows

    def find_by_workspace(self, workspace_id: int, lower: datetime, upper: datetime) -> list[SendLog]:
        return [r for r in self.rows if r.workspace_id == workspace_id and lower <= r.sent_at < upper]


@pytest.fixture
def make_repo():
    def _make(*rows: SendLog) -> InMemorySendLogRepository:
        return InMemorySendLogRepository(list(rows))

    return _make


@pytest.fixture
def log():
    seq = iter(range(1, 10_000))

    def _log(sent_at: str, *, workspace_id: int = 1, channel: str = "sms", status: str = "sent", id: int | None = None) -> SendLog:
        return SendLog(
            id=id if id is not None else next(seq),
            workspace_id=workspace_id,
            channel=channel,
            status=status,
            sent_at=datetime.fromisoformat(sent_at),
        )

    return _log
