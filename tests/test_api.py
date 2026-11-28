from unittest.mock import Mock, patch

from requests import ConnectionError, HTTPError, JSONDecodeError, RequestException, Timeout, TooManyRedirects

from src.api import APIJetLocator, APIOpenStreetMap


def test_init_api_openstreetmap():
    """Тест инициализации"""
    api = APIOpenStreetMap()
    assert api.url == "https://nominatim.openstreetmap.org/search"
    assert api.headers == {"User-Agent": "test-app/1.0"}
    assert api.format == "json"
    assert api.limit == 1


def test_get_response(test_data_openstreetmap):
    """Тест успешного запроса"""
    api = APIOpenStreetMap()
    mock_response = Mock()
    mock_response.json.return_value = test_data_openstreetmap
    with patch("src.api.get", return_value=mock_response) as mock_get:
        result = api.get_response("test")

    assert result == ["41.6765597", "83.3362128", "-141.0027500", "-52.3237664"]
    mock_get.assert_called_once_with(
        url="https://nominatim.openstreetmap.org/search",
        params={"country": "test", "format": "json", "limit": 1},
        headers={"User-Agent": "test-app/1.0"},
    )


def test_get_response_empty(wrong_test_data_openstreetmap):
    """Тест, когда сервер ответил, но нет координат"""
    api = APIOpenStreetMap()
    mock_response = Mock()
    mock_response.json.return_value = wrong_test_data_openstreetmap
    with patch("src.api.get", return_value=mock_response) as mock_get:
        result = api.get_response("test")

    assert result == []
    mock_get.assert_called_once_with(
        url="https://nominatim.openstreetmap.org/search",
        params={"country": "test", "format": "json", "limit": 1},
        headers={"User-Agent": "test-app/1.0"},
    )


def test_http_errors1(capsys):
    """Тест ошибки перенаправлений"""
    api = APIOpenStreetMap()
    mock_response = Mock()

    def error_func():
        raise TooManyRedirects("Too many redirects")

    mock_response.raise_for_status = error_func
    with patch("src.api.get", return_value=mock_response) as mock_get:
        result = api.get_response("test")

    assert result == []
    mock_get.assert_called_once_with(
        url="https://nominatim.openstreetmap.org/search",
        params={"country": "test", "format": "json", "limit": 1},
        headers={"User-Agent": "test-app/1.0"},
    )
    captured = capsys.readouterr()
    assert captured.out == "Слишком много перенаправлений: Too many redirects\n"


def test_http_errors2(capsys):
    """Тест ошибки ожидания"""
    api = APIOpenStreetMap()
    mock_response = Mock()

    def error_func():
        raise Timeout("Request is timed out")

    mock_response.raise_for_status = error_func
    with patch("src.api.get", return_value=mock_response) as mock_get:
        result = api.get_response("test")

    assert result == []
    mock_get.assert_called_once_with(
        url="https://nominatim.openstreetmap.org/search",
        params={"country": "test", "format": "json", "limit": 1},
        headers={"User-Agent": "test-app/1.0"},
    )
    captured = capsys.readouterr()
    assert captured.out == "Превышено время ожидания: Request is timed out\n"


def test_http_errors3(capsys):
    """Тест ошибки HTTP"""
    api = APIOpenStreetMap()
    mock_response = Mock()

    def error_func():
        raise HTTPError("Request error")

    mock_response.raise_for_status = error_func
    with patch("src.api.get", return_value=mock_response) as mock_get:
        result = api.get_response("test")

    assert result == []
    mock_get.assert_called_once_with(
        url="https://nominatim.openstreetmap.org/search",
        params={"country": "test", "format": "json", "limit": 1},
        headers={"User-Agent": "test-app/1.0"},
    )
    captured = capsys.readouterr()
    assert captured.out == "HTTP ошибка: Request error\n"


def test_http_errors4(capsys):
    """Тест ошибки соединения"""
    api = APIOpenStreetMap()
    mock_response = Mock()

    def error_func():
        raise ConnectionError("Connection failed")

    mock_response.raise_for_status = error_func
    with patch("src.api.get", return_value=mock_response) as mock_get:
        result = api.get_response("test")

    assert result == []
    mock_get.assert_called_once_with(
        url="https://nominatim.openstreetmap.org/search",
        params={"country": "test", "format": "json", "limit": 1},
        headers={"User-Agent": "test-app/1.0"},
    )
    captured = capsys.readouterr()
    assert captured.out == "Ошибка соединения: Connection failed\n"


def test_http_errors5(capsys):
    """Тест ошибки декодирования"""
    api = APIOpenStreetMap()
    mock_response = Mock()

    def error_func():
        raise JSONDecodeError("Some problem occurred", "", 0)

    mock_response.raise_for_status = error_func
    with patch("src.api.get", return_value=mock_response) as mock_get:
        result = api.get_response("test")

    assert result == []
    mock_get.assert_called_once_with(
        url="https://nominatim.openstreetmap.org/search",
        params={"country": "test", "format": "json", "limit": 1},
        headers={"User-Agent": "test-app/1.0"},
    )
    captured = capsys.readouterr()
    assert "Не удалось преобразовать ответ сервера в json:" in captured.out


def test_http_errors6(capsys):
    """Тест неизвестной ошибки"""
    api = APIOpenStreetMap()
    mock_response = Mock()

    def error_func():
        raise RequestException("Unidentified problem occurred")

    mock_response.raise_for_status = error_func
    with patch("src.api.get", return_value=mock_response) as mock_get:
        result = api.get_response("test")

    assert result == []
    mock_get.assert_called_once_with(
        url="https://nominatim.openstreetmap.org/search",
        params={"country": "test", "format": "json", "limit": 1},
        headers={"User-Agent": "test-app/1.0"},
    )
    captured = capsys.readouterr()
    assert captured.out == "Непредвиденная ошибка запроса: Unidentified problem occurred\n"


def test_init_api_jet_locator():
    """Тест инициализации"""
    api = APIJetLocator()
    assert api.url == "https://opensky-network.org/api/states/all?"
    assert api.aeroplanes is None


def test_get_response_jet_locator(test_data_opensky):
    """Тест успешного запроса"""
    api = APIJetLocator()
    mock_response = Mock()
    mock_response.json.return_value = test_data_opensky
    with patch("src.api.get", return_value=mock_response) as mock_get:
        api.aeroplanes = api.get_response([0, 0, 0, 0])

    assert api.aeroplanes == test_data_opensky
    mock_get.assert_called_once_with(
        url="https://opensky-network.org/api/states/all?", params={"lamin": 0, "lamax": 0, "lomin": 0, "lomax": 0}
    )


def test_get_response_jet_locator_empty():
    """Тест успешного запроса, но ответ пустой"""
    api = APIJetLocator()
    mock_response = Mock()
    mock_response.json.return_value = {}
    with patch("src.api.get", return_value=mock_response) as mock_get:
        api.aeroplanes = api.get_response([0, 0, 0, 0])

    assert api.aeroplanes == {}
    mock_get.assert_called_once_with(
        url="https://opensky-network.org/api/states/all?", params={"lamin": 0, "lamax": 0, "lomin": 0, "lomax": 0}
    )


def test_locator_http_errors_1(capsys):
    """Тест ошибки перенаправлений"""
    api = APIJetLocator()
    mock_response = Mock()

    def error_func():
        raise TooManyRedirects("Too many redirects")

    mock_response.raise_for_status = error_func
    with patch("src.api.get", return_value=mock_response) as mock_get:
        api.aeroplanes = api.get_response([0, 0, 0, 0])

    assert api.aeroplanes == {}
    mock_get.assert_called_once_with(
        url="https://opensky-network.org/api/states/all?", params={"lamin": 0, "lamax": 0, "lomin": 0, "lomax": 0}
    )

    captured = capsys.readouterr()
    assert captured.out == "Слишком много перенаправлений: Too many redirects\n"


def test_locator_http_errors2(capsys):
    """Тест ошибки ожидания"""
    api = APIJetLocator()
    mock_response = Mock()

    def error_func():
        raise Timeout("Request is timed out")

    mock_response.raise_for_status = error_func
    with patch("src.api.get", return_value=mock_response) as mock_get:
        api.aeroplanes = api.get_response([0, 0, 0, 0])

    assert api.aeroplanes == {}
    mock_get.assert_called_once_with(
        url="https://opensky-network.org/api/states/all?", params={"lamin": 0, "lamax": 0, "lomin": 0, "lomax": 0}
    )

    captured = capsys.readouterr()
    assert captured.out == "Превышено время ожидания: Request is timed out\n"


def test_locator_http_errors3(capsys):
    """Тест ошибки HTTP"""
    api = APIJetLocator()
    mock_response = Mock()

    def error_func():
        raise HTTPError("Request error")

    mock_response.raise_for_status = error_func
    with patch("src.api.get", return_value=mock_response) as mock_get:
        api.aeroplanes = api.get_response([0, 0, 0, 0])

    assert api.aeroplanes == {}
    mock_get.assert_called_once_with(
        url="https://opensky-network.org/api/states/all?", params={"lamin": 0, "lamax": 0, "lomin": 0, "lomax": 0}
    )

    captured = capsys.readouterr()
    assert captured.out == "HTTP ошибка: Request error\n"


def test_locator_http_errors4(capsys):
    """Тест ошибки соединения"""
    api = APIJetLocator()
    mock_response = Mock()

    def error_func():
        raise ConnectionError("Connection failed")

    mock_response.raise_for_status = error_func
    with patch("src.api.get", return_value=mock_response) as mock_get:
        api.aeroplanes = api.get_response([0, 0, 0, 0])

    assert api.aeroplanes == {}
    mock_get.assert_called_once_with(
        url="https://opensky-network.org/api/states/all?", params={"lamin": 0, "lamax": 0, "lomin": 0, "lomax": 0}
    )

    captured = capsys.readouterr()
    assert captured.out == "Ошибка соединения: Connection failed\n"


def test_locator_http_errors5(capsys):
    """Тест ошибки декодирования"""
    api = APIJetLocator()
    mock_response = Mock()

    def error_func():
        raise JSONDecodeError("Some problem occurred", "", 0)

    mock_response.raise_for_status = error_func
    with patch("src.api.get", return_value=mock_response) as mock_get:
        api.aeroplanes = api.get_response([0, 0, 0, 0])

    assert api.aeroplanes == {}
    mock_get.assert_called_once_with(
        url="https://opensky-network.org/api/states/all?", params={"lamin": 0, "lamax": 0, "lomin": 0, "lomax": 0}
    )

    captured = capsys.readouterr()
    assert "Ошибка декодирования json:" in captured.out


def test_locator_http_errors6(capsys):
    """Тест неизвестной ошибки"""
    api = APIJetLocator()
    mock_response = Mock()

    def error_func():
        raise RequestException("Unidentified problem occurred")

    mock_response.raise_for_status = error_func
    with patch("src.api.get", return_value=mock_response) as mock_get:
        api.aeroplanes = api.get_response([0, 0, 0, 0])

    assert api.aeroplanes == {}
    mock_get.assert_called_once_with(
        url="https://opensky-network.org/api/states/all?", params={"lamin": 0, "lamax": 0, "lomin": 0, "lomax": 0}
    )

    captured = capsys.readouterr()
    assert captured.out == "Непредвиденная ошибка запроса: Unidentified problem occurred\n"
