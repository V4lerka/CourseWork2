import datetime
import json
import os
from abc import ABC, abstractmethod
from typing import Any

from src.aeroplanes import Aeroplane


class FileProcessor(ABC):
    """Абстрактный класс для работы с файлами"""

    @abstractmethod
    def add_to_file(self, *args):
        pass

    @abstractmethod
    def clear_info(self, *args):
        pass

    @abstractmethod
    def get_info(self, *args):
        pass


class JSONSaver(FileProcessor):
    """Класс для сохранения данных в файл JSON"""

    def add_to_file(self, jets_list: list[Aeroplane], filename: str) -> None:
        """Добавляет в JSON-файл данные по самолетам из списка объектов Aeroplane"""
        full_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../data", f"{filename}"))
        my_aeroplanes = []
        if jets_list:
            for jet in jets_list:
                keys = ["callsign", "assigned_to", "velocity", "geo_altitude", "on_ground", "vertical_rate"]
                values = [
                    jet.callsign,
                    jet.assigned_to,
                    jet.velocity,
                    jet.geo_altitude,
                    jet.on_ground,
                    jet.vertical_rate,
                ]
                aeroplane = dict(zip(keys, values))
                my_aeroplanes.append(aeroplane)
        try:
            with open(full_path, encoding="utf-8") as file:
                data = json.load(file)
        except json.JSONDecodeError as e:
            print(f"Ошибка чтения файла: {e}")
            data = []
        except FileNotFoundError as e:
            print(f"Ошибка: {e}")
            data = []
        callsigns = [jet.get("callsign") for jet in data]
        for aeroplane in my_aeroplanes:
            if aeroplane.get("callsign") not in callsigns:
                data.append(aeroplane)
        with open(full_path, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4)

    @staticmethod
    def clear_info(filename: str) -> None:
        full_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../data", f"{filename}"))
        try:
            with open(full_path, "w", encoding="utf-8") as file:
                json.dump([], file)
        except FileNotFoundError as e:
            print(f"Ошибка: {e}")

    @staticmethod
    def get_info(filename: str, parameter: str, value: float | int) -> list[dict[str, Any]]:
        """Функция выводит данные о тех самолетах из указанного файла, для которых значение указанного
        параметра больше"""
        full_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../data", f"{filename}"))
        try:
            with open(full_path, encoding="utf-8") as file:
                data = json.load(file)
        except json.JSONDecodeError as e:
            print(f"Ошибка чтения файла: {e}")
            return []
        except FileNotFoundError as e:
            print(f"Ошибка: {e}")
            return []
        else:
            sorted_jets = [jet for jet in data if jet.get(parameter) is not None and jet.get(parameter) > value]
            if sorted_jets:
                return sorted_jets
            else:
                print("Самолетов под указанный критерий не найдено")
                return []

    @staticmethod
    def save_to_file(data: dict, filename) -> None:
        """Метод сохраняет ответ от API сервера в файл JSON (данные по всем самолетам в выбранной стране)"""
        if data:
            if data.get("states"):
                keys = [
                    "ICAO24",
                    "callsign",
                    "assigned_to",
                    "time position",
                    "last contact",
                    "longitude",
                    "latitude",
                    "baro_altitude",
                    "on_ground",
                    "velocity",
                    "true_track",
                    "vertical_rate",
                    "ID sensors",
                    "geo_altitude",
                    "transponder_code",
                    "emergency/priority",
                    "position_source",
                ]
                jets = []
                for item in data["states"]:
                    item[3] = datetime.datetime.fromtimestamp(int(item[3])).strftime("%Y-%m-%d %H:%M:%S")
                    item[4] = datetime.datetime.fromtimestamp(int(item[4])).strftime("%Y-%m-%d %H:%M:%S")
                    jet = dict(zip(keys, item))
                    jets.append(jet)
                try:
                    full_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../data", f"{filename}"))
                    with open(full_path, "w", encoding="utf-8") as file:
                        json.dump(jets, file, indent=4)
                except FileNotFoundError as e:
                    print(f"Ошибка c файлом: {e}")
                except TypeError as e:
                    print(f"Ошибка конвертации в JSON: {e}")
                except ValueError as e:
                    print(f"Ошибка в структуре данных: {e}")
            else:
                print("Данные о самолетах отсутствуют")
        else:
            print("Данные с сервера не были получены или не содержат информации")
