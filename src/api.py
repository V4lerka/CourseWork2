from abc import ABC, abstractmethod
from json import JSONDecodeError
from typing import Any

from requests import ConnectionError, HTTPError, RequestException, Timeout, TooManyRedirects, get


class DefaultAPIAdapter(ABC):
    """Абстрактный класс для работы с API"""

    @abstractmethod
    def get_response(self, *args):
        pass


class APIOpenStreetMap(DefaultAPIAdapter):
    """Класс для получения географических координат выбранных стран по API"""

    def __init__(self) -> None:
        self.__url = "https://nominatim.openstreetmap.org/search"
        self.headers = {"User-Agent": "test-app/1.0"}
        self.__format = "json"
        self.__limit = 1

    def get_response(self, country: str) -> list[Any]:
        """Метод для отправки запроса к API и получения координат стран"""

        params_nominatim = {
            "country": country,
            "format": self.__format,
            "limit": self.__limit,
        }
        try:
            response = get(url=self.__url, params=params_nominatim, headers=self.headers)
            response.raise_for_status()
            data = response.json()
        except TooManyRedirects as e:
            print(f"Слишком много перенаправлений: {e}")
            return []
        except Timeout as e:
            print(f"Превышено время ожидания: {e}")
            return []
        except HTTPError as e:
            print(f"HTTP ошибка: {e}")
            return []
        except ConnectionError as e:
            print(f"Ошибка соединения: {e}")
            return []
        except JSONDecodeError as e:
            print(f"Не удалось преобразовать ответ сервера в json: {e}")
            return []
        except RequestException as e:
            print(f"Непредвиденная ошибка запроса: {e}")
            return []
        else:
            if data[0].get("boundingbox"):
                geo_coordinates = data[0]["boundingbox"]
                return geo_coordinates
            else:
                return []


class APIJetLocator(DefaultAPIAdapter):
    """Класс для получения информации о самолетах через API"""

    def __init__(self) -> None:
        self.__url = "https://opensky-network.org/api/states/all?"
        self.aeroplanes = None

    def get_response(self, geo_coordinates: list) -> dict[str, Any]:
        """Метод для получения информации по самолетам по их географическим координатам"""

        params = {
            "lamin": geo_coordinates[0],
            "lamax": geo_coordinates[1],
            "lomin": geo_coordinates[2],
            "lomax": geo_coordinates[3],
        }
        try:
            response = get(url=self.__url, params=params)
            response.raise_for_status()
            self.aeroplanes = response.json()
        except TooManyRedirects as e:
            print(f"Слишком много перенаправлений: {e}")
            return {}
        except Timeout as e:
            print(f"Превышено время ожидания: {e}")
            return {}
        except HTTPError as e:
            print(f"HTTP ошибка: {e}")
            return {}
        except ConnectionError as e:
            print(f"Ошибка соединения: {e}")
            return {}
        except JSONDecodeError as e:
            print(f"Ошибка декодирования json: {e}")
            return {}
        except RequestException as e:
            print(f"Непредвиденная ошибка запроса: {e}")
            return {}
        else:
            return self.aeroplanes

