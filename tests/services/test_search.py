from unittest.mock import patch

import pandas as pd
import pytest

from app.services.search import search_companies


@pytest.fixture
def mock_data():
    return pd.DataFrame(
        {
            "Organisation Name": ["Foo Company", "Xyz Motion", "Test Company"],
            "Town/City": ["London", "London", "Manchester"],
            "County": ["Greater London", "Greater London", "Greater Manchester"],
        }
    )


# Fixture to patch skilled_worker_data_current and set up side effects
@pytest.fixture
def setup_mock_skilled_worker_data_current(mock_data):
    with patch(
        "app.services.search.skilled_worker_data_current"
    ) as mock_skilled_worker_data_current:
        mock_skilled_worker_data_current.__getitem__.side_effect = mock_data.__getitem__
        mock_skilled_worker_data_current.loc.__getitem__.side_effect = (
            mock_data.loc.__getitem__
        )
        yield mock_skilled_worker_data_current


def test_exact_match(setup_mock_skilled_worker_data_current):
    results = search_companies("Foo Company", threshold=90)
    assert any("Foo Company" in r.Organisation_Name for r in results)


def test_fuzzy_match(setup_mock_skilled_worker_data_current):
    results = search_companies("Foo", threshold=70)
    assert any("Foo Company" in r.Organisation_Name for r in results)


def test_no_match(setup_mock_skilled_worker_data_current):
    results = search_companies("Nonexistent Company", threshold=90)
    assert results == []


@pytest.fixture
def setup_mock_skilled_worker_data_current_nan():
    mock_data = pd.DataFrame(
        {"Organisation Name": [None], "Town/City": [None], "County": [None]}
    )
    with patch(
        "app.services.search.skilled_worker_data_current"
    ) as mock_skilled_worker_data_current:
        mock_skilled_worker_data_current.__getitem__.side_effect = mock_data.__getitem__
        mock_skilled_worker_data_current.loc.__getitem__.side_effect = (
            mock_data.loc.__getitem__
        )
        yield mock_skilled_worker_data_current


def test_nan_handling(setup_mock_skilled_worker_data_current_nan):
    results = search_companies("anything", threshold=0)
    assert results[0].Organisation_Name == ""
