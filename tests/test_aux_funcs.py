import pytest

from src.aux_funcs import normalize_country


@pytest.mark.parametrize(
    "country, expected",
    [
        ("moroc", "Morocco"),
        ("USA", "United States"),
        ("German", "Germany"),
        ("England", "United Kingdom"),
        ("hffuf74", None),
        ("637847463", None),
        ("Espania", None),
        ("Europe", None),
        ("Holland", "Netherlands"),
        ("Russia", "Russian Federation"),
    ],
)
def test_normalize_country(country, expected):
    result = normalize_country(country)
    assert result == expected
