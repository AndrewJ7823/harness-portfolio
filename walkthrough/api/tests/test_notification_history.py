"""PROJ-1234 알림 발송 이력 조회 — 스펙 §3 케이스 C1~C12.

테스트 이름에 케이스 ID를 넣는다(주석이 아니라 이름으로 추적 — 커버리지 판정의 앵커).
"""

from datetime import date, timedelta

import pytest

from notification_history import MAX_PAGE_SIZE, Forbidden, InvalidPeriod, list_send_history


def query(repo, **overrides):
    params = dict(requester_workspace_id=1, workspace_id=1, start=date(2026, 10, 1), end=date(2026, 10, 31))
    params.update(overrides)
    return list_send_history(repo, **params)


def test_C1_returns_logs_in_period(make_repo, log):
    repo = make_repo(log("2026-10-05T09:00:00"), log("2026-10-20T14:30:00"))

    result = query(repo)

    assert result.total == 2
    assert [r.sent_at.day for r in result.items] == [20, 5]


def test_C2_no_logs_returns_empty_page(make_repo):
    result = query(make_repo())

    assert result.items == []
    assert result.total == 0


def test_C3_end_date_included_until_midnight(make_repo, log):
    repo = make_repo(log("2026-10-31T23:59:59"), log("2026-11-01T00:00:00"))

    result = query(repo)

    assert [r.sent_at.isoformat() for r in result.items] == ["2026-10-31T23:59:59"]


def test_C4_start_after_end_rejected(make_repo):
    with pytest.raises(InvalidPeriod, match="start_after_end"):
        query(make_repo(), start=date(2026, 10, 31), end=date(2026, 10, 1))


@pytest.mark.parametrize(
    ("days", "ok"),
    [(1, True), (92, True), (93, False)],
    ids=["C5-1일", "C5-92일", "C5-93일"],
)
def test_C5_period_length_boundary(make_repo, days, ok):
    start = date(2026, 1, 1)
    end = start + timedelta(days=days - 1)

    if ok:
        assert query(make_repo(), start=start, end=end).total == 0
    else:
        with pytest.raises(InvalidPeriod, match="period_too_long"):
            query(make_repo(), start=start, end=end)


def test_C6_other_workspace_forbidden(make_repo, log):
    repo = make_repo(log("2026-10-05T09:00:00", workspace_id=2))

    with pytest.raises(Forbidden):
        query(repo, requester_workspace_id=1, workspace_id=2)


def test_C7_page_size_capped(make_repo, log):
    repo = make_repo(*[log(f"2026-10-01T{i // 60:02d}:{i % 60:02d}:00") for i in range(120)])

    result = query(repo, page_size=500)

    assert result.page_size == MAX_PAGE_SIZE
    assert len(result.items) == MAX_PAGE_SIZE
    assert result.total == 120


def test_C8_year_boundary(make_repo, log):
    repo = make_repo(log("2026-12-31T23:00:00"), log("2027-01-01T01:00:00"), log("2027-01-02T00:00:00"))

    result = query(repo, start=date(2026, 12, 31), end=date(2027, 1, 1))

    assert [r.sent_at.year for r in result.items] == [2027, 2026]


def test_C9_failed_logs_included_with_status(make_repo, log):
    repo = make_repo(log("2026-10-05T09:00:00", status="failed"), log("2026-10-06T09:00:00"))

    result = query(repo)

    assert {r.status for r in result.items} == {"sent", "failed"}


def test_C10_same_time_ordered_by_id_desc(make_repo, log):
    repo = make_repo(log("2026-10-05T09:00:00", id=7), log("2026-10-05T09:00:00", id=9))

    result = query(repo)

    assert [r.id for r in result.items] == [9, 7]


def test_C11_page_out_of_range_keeps_total(make_repo, log):
    repo = make_repo(log("2026-10-05T09:00:00"), log("2026-10-06T09:00:00"))

    result = query(repo, page=5, page_size=10)

    assert result.items == []
    assert result.total == 2
