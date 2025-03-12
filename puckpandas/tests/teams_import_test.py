from puckpandas import TeamsImport
import pytest


def test_init_not_empty() -> None:
    teams = TeamsImport(test=1)
    assert len(teams.teams_df.index) != 0


def test_update_db():
    assert True


def test_clear_db():
    assert True


def test_query_db():
    assert True


def test_query_api():
    assert True


def test_query_api_update_db():
    assert True


def test_team_id_from_tri_code():
    assert True


def test_tri_code_from_team_id():
    assert True
