import pytest


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
