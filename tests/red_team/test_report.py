import pytest

from aisploit.core import BaseReport, Score
from aisploit.red_team import RedTeamReport, RedTeamReportEntry


@pytest.fixture
def red_team_report():
    return RedTeamReport(run_id="test_run")


@pytest.fixture
def red_team_report_entry():
    return RedTeamReportEntry(
        attempt=1,
        prompt="Test prompt",
        response="Test response",
        score=Score(flagged=True, value=0.8),
    )


def test_red_team_report_init(red_team_report):
    assert isinstance(red_team_report, BaseReport)
    assert red_team_report.run_id == "test_run"
    assert len(red_team_report._entries) == 0


def test_red_team_report_add_entry(red_team_report, red_team_report_entry):
    red_team_report.add_entry(red_team_report_entry)
    assert len(red_team_report._entries) == 1
    assert red_team_report._entries[0] == red_team_report_entry


def test_red_team_report_final_score(red_team_report, red_team_report_entry):
    assert red_team_report.final_score is None

    red_team_report.add_entry(red_team_report_entry)
    assert red_team_report.final_score == red_team_report_entry.score


def test_red_team_report_final_response(red_team_report, red_team_report_entry):
    assert red_team_report.final_response is None

    red_team_report.add_entry(red_team_report_entry)
    assert red_team_report.final_response == red_team_report_entry.response
