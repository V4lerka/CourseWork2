import pytest

from src.aeroplanes import Aeroplane


@pytest.fixture
def test_data_openstreetmap():
    return [
        {
            "place_id": 346277167,
            "licence": "Data © OpenStreetMap contributors, ODbL 1.0. http://osm.org/copyright",
            "osm_type": "relation",
            "osm_id": 1428125,
            "lat": "61.0666922",
            "lon": "-107.9917070",
            "class": "boundary",
            "type": "administrative",
            "place_rank": 4,
            "importance": 0.9082390417046676,
            "addresstype": "country",
            "name": "Canada",
            "display_name": "Canada",
            "boundingbox": ["41.6765597", "83.3362128", "-141.0027500", "-52.3237664"],
        }
    ]


@pytest.fixture
def wrong_test_data_openstreetmap():
    return [
        {
            "place_id": 346277167,
            "licence": "Data © OpenStreetMap contributors, ODbL 1.0. http://osm.org/copyright",
            "osm_type": "relation",
            "osm_id": 1428125,
            "lat": "61.0666922",
            "lon": "-107.9917070",
            "class": "boundary",
            "type": "administrative",
            "place_rank": 4,
            "importance": 0.9082390417046676,
            "addresstype": "country",
            "name": "Canada",
            "display_name": "Canada",
        }
    ]


@pytest.fixture
def test_data_opensky():
    return {
        "ICAO24": "4ca56a",
        "callsign": "RYR25WB ",
        "assigned_to": "Ireland",
        "time position": "2026-11-27 01:20:49",
        "last contact": "2026-11-27 01:20:50",
        "longitude": 14.4144,
        "latitude": 35.8989,
        "baro_altitude": 861.06,
        "on_ground": False,
        "velocity": 115.69,
        "true_track": 308.5,
        "vertical_rate": 14.96,
        "ID sensors": None,
        "geo_altitude": 922.02,
        "transponder_code": "6572",
        "emergency/priority": False,
        "position_source": 0,
    }


@pytest.fixture()
def test_data_aeroplane1():
    return Aeroplane("RYR25WB", "Ireland", 115.69, 12000, False, 12.2)


@pytest.fixture()
def test_data_aeroplane2():
    return Aeroplane("R25WB", "Russia", 215.69, 10000, False, 12.2)


@pytest.fixture()
def test_data_to_object_list():
    return {
        "time": 1766142246,
        "states": [
            [
                "4ca56a",
                "RYR25WB",
                "Ireland",
                "2026-11-27 01:20:49",
                "2026-11-27 01:20:50",
                14.4144,
                35.8989,
                861.06,
                False,
                115.69,
                308.5,
                14.96,
                None,
                922.02,
                "6572",
                False,
                0,
            ],
            [
                "440d92",
                "TAY8FO",
                "Austria",
                "2026-11-27 01:20:50",
                "2026-11-27 01:20:50",
                14.163,
                36.0853,
                4975.86,
                False,
                175.28,
                324.68,
                22.11,
                None,
                5105.4,
                "6562",
                False,
                0,
            ],
        ],
    }


@pytest.fixture()
def test_incomplete_data_to_object_list():
    return {
        "time": 1766142246,
        "states": [
            [
                "4ca56a",
                "RYR25WB",
                "Ireland",
                "2026-11-27 01:20:49",
                "2026-11-27 01:20:50",
                14.4144,
                35.8989,
                861.06,
                False,
                115.69,
                308.5,
            ],
            [
                "440d92",
                "TAY8FO",
                "Austria",
                "2026-11-27 01:20:50",
                "2026-11-27 01:20:50",
                14.163,
                36.0853,
                4975.86,
                False,
                175.28,
                324.68,
                22.11,
                None,
                5105.4,
                "6562",
                False,
                0,
            ],
        ],
    }


@pytest.fixture()
def aeroplanes_list():
    return [
        Aeroplane("RYR25WB", "Ireland", 115.69, 12000, False, 12.2),
        Aeroplane("Bravo", "USA", 125.69, 9500, False, 2.2),
        Aeroplane("Charlie", "France", 115.69, 11000, False, 12.2),
        Aeroplane("RYR25WB", "Spain", 115.69, 13000, False, 12.2),
        Aeroplane("Alpha", "USA", 125.69, 7000, False, 2.2),
        Aeroplane("Eagle", "USA", 125.69, 9000, False, 2.2),
    ]
