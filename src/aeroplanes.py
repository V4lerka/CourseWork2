class Aeroplane:
    """класс для работы с информацией о самолетах"""

    def __init__(
        self,
        callsign: str,
        assigned_to: str,
        velocity: float,
        geo_altitude: float,
        on_ground: bool,
        vertical_rate: float,
    ):

        self.callsign = self._validate_callsign(callsign)
        self.assigned_to = self._validate_assigned_to(assigned_to)
        self.velocity = self._validate_velocity(velocity)
        self.geo_altitude = self._validate_geo_altitude(geo_altitude)
        self.on_ground = self._validate_on_ground(on_ground)
        self.vertical_rate = self._validate_vertical_rate(vertical_rate)

    @staticmethod
    def _validate_callsign(value):
        if type(value) is str:
            return value
        else:
            raise TypeError("Позывной должен быть строковым значением")

    @staticmethod
    def _validate_assigned_to(value):
        if type(value) is str:
            return value
        else:
            raise TypeError("Страна регистрации должна быть строковым значением")

    @staticmethod
    def _validate_velocity(value):
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            raise TypeError("Значение скорости должно быть числовым")
        if value >= 0:
            return value
        raise ValueError("Скорость самолета не может быть отрицательной")

    @staticmethod
    def _validate_geo_altitude(value):
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            raise TypeError("Значение высоты должно быть числовым")
        return value

    @staticmethod
    def _validate_on_ground(value):
        if type(value) is bool:
            return value
        raise TypeError("Статус нахождения на земле должен быть False или True")

    @staticmethod
    def _validate_vertical_rate(value):
        if not isinstance(value, (int, float)):
            raise TypeError("Значение вертикальной скорости должно быть числовым")
        return value

    def __gt__(self, other) -> bool:
        """Метод сравнения по скорости полета"""

        if isinstance(other, Aeroplane):
            return self.velocity > other.velocity
        else:
            raise TypeError("Сравнение объектов разных типов невозможно")

    def altitude_is_greater_than(self, other) -> bool:
        """Метод сравнения высоты нахождения самолетов"""

        if isinstance(other, Aeroplane):
            return self.geo_altitude > other.geo_altitude
        else:
            raise TypeError("Сравнение объектов разных типов невозможно")

    def __str__(self) -> str:
        """Вывод краткой информации о борте"""

        if not self.on_ground:
            if self.vertical_rate < 0:
                return f"Борт {self.callsign}, регистрация: {self.assigned_to}, статус: В полете на высоте \
{self.geo_altitude} м, снижается"
            elif self.vertical_rate > 0:
                return f"Борт {self.callsign}, регистрация: {self.assigned_to}, статус: В полете на высоте \
{self.geo_altitude} м, набирает высоту"
            else:
                return f"Борт {self.callsign}, регистрация: {self.assigned_to}, статус: В полете на высоте \
{self.geo_altitude} м, высота постоянна"
        else:
            return f"Борт {self.callsign}, регистрация: {self.assigned_to}, статус: В аэропорту"

    @classmethod
    def data_to_object_list(cls, data: dict) -> list[Aeroplane]:
        """Преобразует json-ответ от API сервера в список объектов Aeroplane со значениями атрибутов не None"""
        if data and type(data) is dict:
            if data.get("states", []) and len(data.get("states")) > 0:
                jets = []
                for item in data.get("states"):
                    if len(item) >= 14:
                        attributes = [item[1], item[2], item[9], item[13], item[8], item[11]]
                        if all(elem is not None for elem in attributes):
                            jet = cls(*attributes)
                            jets.append(jet)
                    else:
                        continue
                return jets
            print("Данные о самолетах отсутствуют")
            return []
        print("Данные с сервера не были получены или не содержат требуемой информации")
        return []

    @staticmethod
    def sort_aeroplanes(data: list[Aeroplane], top_n: int) -> list[Aeroplane]:
        """Метод сортировки самолетов по высоте и отбор топ N"""
        if data:
            sorted_jets = sorted(data, reverse=True, key=lambda jet: jet.geo_altitude)
            if top_n <= len(data):
                return sorted_jets[0:top_n]
            else:
                print(f"Всего найдено самолетов: {len(data)}")
                return sorted_jets
        return []

    @staticmethod
    def filter_aeroplane(data: list[Aeroplane], countries: list) -> list[Aeroplane]:
        """Метод фильтрации самолетов по стране регистрации"""
        if data:
            filtered_jets = list(filter(lambda jet: jet.assigned_to in countries, data))
            if filtered_jets:
                return filtered_jets
            print("По запросу ничего не найдено")
            return []
        print("Список самолетов пуст")
        return []

    @staticmethod
    def aeroplanes_by_altitude_range(data: list[Aeroplane], min_value: int, max_value: int) -> list[Aeroplane]:
        """Фильтрация самолетов по высоте полета"""
        if data:
            filtered_jets = list(filter(lambda jet: min_value < jet.geo_altitude < max_value, data))
            if filtered_jets:
                return filtered_jets
            print("По запросу ничего не найдено")
            return []
        print("Список самолетов пуст")
        return []
