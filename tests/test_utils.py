import json
from unittest.mock import mock_open, patch

from src.utils import JSONSaver

json_processor = JSONSaver()


def test_add_to_file(existing_json, aeroplanes_list):
    """Успешный тест добавления самолетов с уникальным позывным"""

    file_content = existing_json
    mocked_file = mock_open(read_data=file_content)
    with patch("builtins.open", mocked_file), patch("json.dump") as mock_dump:
        json_processor.add_to_file(aeroplanes_list, "jets.json")
        saved_data = mock_dump.call_args[0][0]
    assert len(saved_data) == 6
    assert [jet["callsign"] for jet in saved_data] == ["RYR25WB", "TAY8FO", "Bravo", "Charlie", "Alpha", "Eagle"]


def test_add_to_file_error1(aeroplanes_list, capsys):
    """Тест, если файл не найден"""

    def mock_open_raise_error(*args, **kwargs):
        raise FileNotFoundError("[Errno 2] No such file or directory")

    with (
        patch("builtins.open", mock_open_raise_error),
        patch("json.dump", mock_open_raise_error),
    ):
        json_processor.add_to_file(aeroplanes_list, "missing.json")
    message = capsys.readouterr()
    assert "[Errno 2] No such file or directory" in message.out


def test_add_to_file_error2(existing_json, aeroplanes_list, capsys):
    """Ошибки при десериализации / сериализации"""

    file_content = existing_json
    mocked_file = mock_open(read_data=file_content)

    def load_raise_error(*args, **kwargs):
        raise json.JSONDecodeError(msg="Expecting value", doc="invalid json", pos=0)

    def dump_raise_type_error(*args, **kwargs):
        raise TypeError("Object of type Aeroplane is not JSON serializable")

    with (
        patch("builtins.open", mocked_file),
        patch("json.load", load_raise_error),
        patch("json.dump", dump_raise_type_error),
    ):
        json_processor.add_to_file(aeroplanes_list, "fake.json")
        message = capsys.readouterr()
        assert (
            message.out
            == "Ошибка чтения файла: Expecting value: line 1 column 1 (char 0)\nОбъект нельзя преобразовать \
в JSON: Object of type Aeroplane is not JSON serializable\n"
        )


def test_add_to_file_error3(existing_json, aeroplanes_list, capsys):
    """Ошибки при десериализации / сериализации"""

    file_content = existing_json
    mocked_file = mock_open(read_data=file_content)

    def dump_raise_value_error(*args, **kwargs):
        raise ValueError("Object of type Aeroplane has incorrect values")

    with patch("builtins.open", mocked_file), patch("json.dump", dump_raise_value_error):
        json_processor.add_to_file(aeroplanes_list, "fake.json")
        message = capsys.readouterr()
        assert message.out == "Ошибка значений: Object of type Aeroplane has incorrect values\n"


def test_get_info_ok1(existing_json):
    """Успешный тест получения информации из файла"""
    file_content = existing_json
    mocked_file = mock_open(read_data=file_content)

    with patch("builtins.open", mocked_file):
        result = json_processor.get_info("jets.json", "velocity", 150)
        assert result == [
            {
                "callsign": "TAY8FO",
                "assigned_to": "Austria",
                "on_ground": False,
                "velocity": 175.28,
                "vertical_rate": 22.11,
                "geo_altitude": 5105.4,
            }
        ]


def test_get_info_ok2(existing_json, capsys):
    """Успешный тест получения информации из файла, н осамолеты не найдены"""
    file_content = existing_json
    mocked_file = mock_open(read_data=file_content)

    with patch("builtins.open", mocked_file):
        result = json_processor.get_info("jets.json", "velocity", 250)
        assert result == []
        message = capsys.readouterr()
        assert message.out == "Самолетов под указанный критерий не найдено\n"


def test_get_info_error1(existing_json, capsys):
    """Ошибка чтения файла"""
    file_content = existing_json
    mocked_file = mock_open(read_data=file_content)

    def load_raise_error(*args, **kwargs):
        raise json.JSONDecodeError(msg="Expecting value", doc="invalid json", pos=0)

    with patch("builtins.open", mocked_file), patch("json.load", load_raise_error):
        result = json_processor.get_info("jets.json", "velocity", 150)
        assert result == []
        message = capsys.readouterr()
        assert message.out == "Ошибка чтения файла: Expecting value: line 1 column 1 (char 0)\n"


def test_get_info_error2(capsys):
    """Тест, если файл не существует"""

    def mock_open_raise_error(*args, **kwargs):
        raise FileNotFoundError("[Errno 2] No such file or directory")

    with patch("builtins.open", mock_open_raise_error):
        result = json_processor.get_info("jets.json", "velocity", 150)
        assert result == []
        message = capsys.readouterr()
        assert message.out == "Ошибка: [Errno 2] No such file or directory\n"


def test_clear_info(capsys):
    """Тест, если файл не существует"""

    def mock_open_raise_error(*args, **kwargs):
        raise FileNotFoundError("[Errno 2] No such file or directory")

    with patch("builtins.open", mock_open_raise_error):
        json_processor.clear_info("jets.json")
        message = capsys.readouterr()
        assert message.out == "Ошибка: [Errno 2] No such file or directory\n"


def test_clear_info2(existing_json, capsys):
    """Успешный тест"""
    file_content = existing_json
    mocked_file = mock_open(read_data=file_content)
    with patch("builtins.open", mocked_file), patch("json.dump") as mock_dump:
        json_processor.clear_info("jets.json")
        mock_dump.assert_called_once()
        assert mock_dump.call_args[0][0] == []
        message = capsys.readouterr()
        assert message.out == "Данные в файле jets.json очищены\n"


def test_save_to_file1(test_data_save_to_file, capsys):
    """Тест, если файл не существует"""

    def mock_open_raise_error(*args, **kwargs):
        raise FileNotFoundError("[Errno 2] No such file or directory")

    with patch("builtins.open", mock_open_raise_error):
        json_processor.save_to_file(test_data_save_to_file, "jets.json")
        message = capsys.readouterr()
        assert message.out == "Ошибка c файлом: [Errno 2] No such file or directory\n"


def test_save_to_file2(test_data_save_to_file, capsys):
    """Тест ошибок"""
    mocked_file = mock_open(read_data=None)

    def dump_raise_type_error(*args, **kwargs):
        raise TypeError("Data in type dict is not JSON serializable")

    with patch("builtins.open", mocked_file), patch("json.dump", dump_raise_type_error):
        json_processor.save_to_file(test_data_save_to_file, "jets.json")
        message = capsys.readouterr()
        assert message.out == "Ошибка конвертации в JSON: Data in type dict is not JSON serializable\n"


def test_save_to_file3(test_data_save_to_file, capsys):
    """Тест ошибок"""
    mocked_file = mock_open(read_data=None)

    def dump_raise_value_error(*args, **kwargs):
        raise ValueError("Object of type dict has incorrect values")

    with patch("builtins.open", mocked_file), patch("json.dump", dump_raise_value_error):
        json_processor.save_to_file(test_data_save_to_file, "jets.json")
        message = capsys.readouterr()
        assert message.out == "Ошибка в структуре данных: Object of type dict has incorrect values\n"


def test_save_to_file4(capsys):
    """Тест пустых данных"""
    json_processor.save_to_file({}, "jets.json")
    message = capsys.readouterr()
    assert message.out == "Данные с сервера не были получены или не содержат требуемой информации\n"


def test_save_to_file5(capsys):
    """Тест пустых данных"""

    data = {"time": 1766142246, "states": []}
    json_processor.save_to_file(data, "jets.json")
    message = capsys.readouterr()
    assert message.out == "Данные о самолетах отсутствуют\n"
