import contextlib
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


# Generalized fixture factory for patching skilled_worker_data_current
@pytest.fixture
def patch_skilled_worker_data_current():
    @contextlib.contextmanager
    def _patch(data):
        with patch(
            "app.services.search.skilled_worker_data_current"
        ) as mock_skilled_worker_data_current:
            mock_skilled_worker_data_current.__getitem__.side_effect = data.__getitem__
            mock_skilled_worker_data_current.loc.__getitem__.side_effect = (
                data.loc.__getitem__
            )
            yield mock_skilled_worker_data_current

    return _patch


def test_exact_match(patch_skilled_worker_data_current, mock_data):
    with patch_skilled_worker_data_current(mock_data):
        results = search_companies("Foo Company", threshold=90)
        assert any("Foo Company" in r.Organisation_Name for r in results)


def test_fuzzy_match(patch_skilled_worker_data_current, mock_data):
    with patch_skilled_worker_data_current(mock_data):
        results = search_companies("Foo", threshold=70)
        assert any("Foo Company" in r.Organisation_Name for r in results)


def test_no_match(patch_skilled_worker_data_current, mock_data):
    with patch_skilled_worker_data_current(mock_data):
        results = search_companies("Nonexistent Company", threshold=90)
        assert not results


def test_nan_handling(patch_skilled_worker_data_current):
    nan_data = pd.DataFrame(
        {"Organisation Name": [None], "Town/City": [None], "County": [None]}
    )
    with patch_skilled_worker_data_current(nan_data):
        results = search_companies("anything", threshold=0)
        assert results[0].Organisation_Name == ""
