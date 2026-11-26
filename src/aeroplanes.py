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
        if type(callsign) is str:
            self.__callsign = callsign
        else:
            raise TypeError("Позывной должен быть строковым значением")

        if type(assigned_to) is str:
            self.__assigned_to = assigned_to
        else:
            raise TypeError("Страна регистрации должна быть строковым значением")

        if not isinstance(velocity, (int, float)):
            raise TypeError("Значение скорости должно быть числовым")
        if velocity >= 0:
            self.__velocity = velocity
        else:
            raise ValueError("Скорость самолета не может быть отрицательной")

        if not isinstance(geo_altitude, (int, float)):
            raise TypeError("Значение высоты должно быть числовым")
        else:
            self.__geo_altitude = geo_altitude

        if type(on_ground) is bool:
            self.__on_ground = on_ground
        else:
            raise TypeError("Статус нахождения на земле должен быть False или True")

        if not isinstance(velocity, (int, float)):
            raise TypeError("Значение скорости должно быть числовым")
        else:
            self.__vertical_rate = vertical_rate

    @property
    def callsign(self):
        return self.__callsign

    @property
    def assigned_to(self):
        return self.__assigned_to

    @property
    def velocity(self):
        return self.__velocity

    @property
    def geo_altitude(self):
        return self.__geo_altitude

    @property
    def on_ground(self):
        return self.__on_ground

    @property
    def vertical_rate(self):
        return self.__vertical_rate

    def __gt__(self, other) -> bool:
        """Метод сравнения по скорости полета"""

        if isinstance(other, Aeroplane):
            return self.velocity > other.velocity
        else:
            raise TypeError("Сравнение объектов разных типов невозможно")

    def compare_altitude(self, other) -> bool:
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
        if data:
            if data.get("states"):
                jets = []
                for item in data.get("states"):
                    attributes = [item[1], item[2], item[9], item[13], item[8], item[11]]
                    if all(elem is not None for elem in attributes):
                        jet = cls(*attributes)
                        jets.append(jet)
                return jets
            print("Данные о самолетах отсутствуют")
            return []
        print("Данные с сервера не были получены или не содержат информации")
        return []

    @staticmethod
    def sort_aeroplanes(data: list[Aeroplane], top_n: int) -> list[Aeroplane]:
        """Метод сортировки самолетов по высоте и отбор топ N"""
        sorted_jets = sorted(data, reverse=True, key=lambda jet: jet.geo_altitude)
        if top_n <= len(data):
            return sorted_jets[0:top_n]
        else:
            print(f"Всего найдено самолетов: {len(data)}")
            return sorted_jets

    @staticmethod
    def filter_aeroplane(data: list[Aeroplane], countries: list) -> list[Aeroplane]:
        """Метод фильтрации самолетов по стране регистрации"""

        filtered_jets = list(filter(lambda jet: jet.assigned_to in countries, data))
        if filtered_jets:
            return filtered_jets
        print("По запросу ничего не найдено")
        return []

    @staticmethod
    def aeroplanes_by_altitude_range(data: list[Aeroplane], min_value: int, max_value: int) -> list[Aeroplane]:
        """Фильтрация самолетов по высоте полета"""

        filtered_jets = list(filter(lambda jet: min_value < jet.geo_altitude < max_value, data))
        if filtered_jets:
            return filtered_jets
        print("По запросу ничего не найдено")
        return []
