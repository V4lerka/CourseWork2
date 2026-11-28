import pytest

from src.aeroplanes import Aeroplane


def test_init_aeroplane():
    """Тест инициализации самолета"""
    my_jet = Aeroplane("RYR25WB", "Ireland", 115.69, 10000, False, 12.2)

    assert my_jet.callsign == "RYR25WB"
    assert my_jet.assigned_to == "Ireland"
    assert my_jet.velocity == 115.69
    assert my_jet.geo_altitude == 10000
    assert my_jet.on_ground is False
    assert my_jet.vertical_rate == 12.2


@pytest.mark.parametrize(
    "attributes, expected",
    [
        ([1, "Ireland", 115.69, 10000, False, 12.2], "Позывной должен быть строковым значением"),
        (["D2", 34, 115.69, 10000, False, 12.2], "Страна регистрации должна быть строковым значением"),
        (["D2", "Ireland", "High", 10000, False, 12.2], "Значение скорости должно быть числовым"),
        (["D2", "Ireland", 340, "Low", False, 12.2], "Значение высоты должно быть числовым"),
        (["D2", "Ireland", 340, 12000, "OK", 12.2], "Статус нахождения на земле должен быть False или True"),
        (["D2", "Ireland", 340, 10000, False, "Fast"], "Значение вертикальной скорости должно быть числовым"),
    ],
)
def test_validators_aeroplane1(attributes, expected):
    """Тест валидаторов аттрибутов самолета"""
    with pytest.raises(TypeError) as e:
        my_jet = Aeroplane(*attributes)
        print(my_jet)
    assert str(e.value) == expected


def test_validators_aeroplane2():
    """Тест валидаторов аттрибутов самолета"""
    with pytest.raises(ValueError) as e:
        my_jet = Aeroplane("Tango", "Ireland", -115.69, 10000, False, 12.2)
        print(my_jet)
    assert str(e.value) == "Скорость самолета не может быть отрицательной"


def test_gt_magic1(test_data_aeroplane1, test_data_aeroplane2):
    assert test_data_aeroplane2 > test_data_aeroplane1


def test_gt_magic2(test_data_aeroplane1):
    with pytest.raises(TypeError) as e:
        assert test_data_aeroplane1 > 123
        assert str(e.value) == "Сравнение объектов разных типов невозможно"


def test_altitude_is_greater_than1(test_data_aeroplane1, test_data_aeroplane2):
    assert test_data_aeroplane1.altitude_is_greater_than(test_data_aeroplane2)


def test_altitude_is_greater_than2(test_data_aeroplane1):
    with pytest.raises(TypeError) as e:
        assert test_data_aeroplane1.altitude_is_greater_than(12300)
        assert str(e.value) == "Сравнение объектов разных типов невозможно"


@pytest.mark.parametrize(
    "attributes, expected",
    [
        (
            ["Bravo", "Ireland", 115.69, 10000, False, 12.2],
            "Борт Bravo, регистрация: Ireland, статус: В полете на высоте 10000 м, набирает высоту\n",
        ),
        (
            ["Bravo", "Ireland", 115.69, 10000, False, -12.2],
            "Борт Bravo, регистрация: Ireland, статус: В полете на высоте 10000 м, снижается\n",
        ),
        (
            ["Bravo", "Ireland", 115.69, 10000, False, 0],
            "Борт Bravo, регистрация: Ireland, статус: В полете на высоте 10000 м, высота постоянна\n",
        ),
        (["Bravo", "Ireland", 0, 0, True, 0], "Борт Bravo, регистрация: Ireland, статус: В аэропорту\n"),
    ],
)
def test_str_magic(attributes, expected, capsys):
    jet = Aeroplane(*attributes)
    print(jet)
    captured = capsys.readouterr()
    assert captured.out == expected


def test_data_to_object_list_empty1(capsys):
    """Тест пустых данных"""
    result = Aeroplane.data_to_object_list({})
    assert result == []
    captured = capsys.readouterr()
    assert captured.out == "Данные с сервера не были получены или не содержат требуемой информации\n"


def test_data_to_object_list_empty2(capsys):
    """Тест пустых данных"""
    result = Aeroplane.data_to_object_list({"time": 1766142246, "states": []})
    assert result == []
    captured = capsys.readouterr()
    assert captured.out == "Данные о самолетах отсутствуют\n"


def test_data_to_object_list_ok(test_data_to_object_list):
    """Успешный тест"""
    result = Aeroplane.data_to_object_list(test_data_to_object_list)
    assert len(result) == 2
    assert result[0].assigned_to == "Ireland"
    assert result[0].callsign == "RYR25WB"
    assert result[0].on_ground is False
    assert result[0].geo_altitude == 922.02
    assert result[0].velocity == 115.69
    assert result[0].vertical_rate == 14.96
    assert result[1].assigned_to == "Austria"


def test_data_to_object_list_short(test_incomplete_data_to_object_list):
    """Успешный тест, если данные в списке не все"""
    result = Aeroplane.data_to_object_list(test_incomplete_data_to_object_list)
    assert len(result) == 1
    assert result[0].assigned_to == "Austria"


def test_sort_aeroplanes1(aeroplanes_list, capsys):
    """Тест, если топ N больше длины списка"""
    result = Aeroplane.sort_aeroplanes(aeroplanes_list, 10)
    assert len(result) == 6
    assert result[0].geo_altitude == 13000
    assert result[5].geo_altitude == 7000
    captured = capsys.readouterr()
    assert captured.out == "Всего найдено самолетов: 6\n"


def test_sort_aeroplanes2(aeroplanes_list):
    """Просто успешный тест"""
    result = Aeroplane.sort_aeroplanes(aeroplanes_list, 3)
    assert len(result) == 3
    assert result[0].geo_altitude == 13000
    assert result[2].geo_altitude == 11000


def test_sort_aeroplanes3(aeroplanes_list):
    """Тест пустого списка"""
    result = Aeroplane.sort_aeroplanes([], 3)
    assert result == []


def test_filter_aeroplane1(aeroplanes_list):
    """Просто успешный тест"""
    result = Aeroplane.filter_aeroplane(aeroplanes_list, ["USA"])
    assert len(result) == 3


def test_filter_aeroplane2(aeroplanes_list, capsys):
    """Если страны нет в списке"""
    result = Aeroplane.filter_aeroplane(aeroplanes_list, ["Germany"])
    assert len(result) == 0
    captured = capsys.readouterr()
    assert captured.out == "По запросу ничего не найдено\n"


def test_filter_aeroplane3(capsys):
    """Если список самолетов пуст"""
    result = Aeroplane.filter_aeroplane([], ["Germany"])
    assert result == []
    captured = capsys.readouterr()
    assert captured.out == "Список самолетов пуст\n"


def test_aeroplanes_by_altitude_range1(aeroplanes_list):
    """Успешный тест"""
    result = Aeroplane.aeroplanes_by_altitude_range(aeroplanes_list, 10500, 13100)
    assert len(result) == 3


def test_aeroplanes_by_altitude_range2(aeroplanes_list, capsys):
    """Успешный тест, но ничего не найдено"""
    result = Aeroplane.aeroplanes_by_altitude_range(aeroplanes_list, 13500, 15100)
    assert result == []
    captured = capsys.readouterr()
    assert captured.out == "По запросу ничего не найдено\n"


def test_aeroplanes_by_altitude_range3(capsys):
    """Успешный тест, но список пуст"""
    result = Aeroplane.aeroplanes_by_altitude_range([], 13500, 15100)
    assert result == []
    captured = capsys.readouterr()
    assert captured.out == "Список самолетов пуст\n"
