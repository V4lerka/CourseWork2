from src.api import APIJetLocator, APIOpenStreetMap
from src.aeroplanes import Aeroplane
from src.utils import JSONSaver

api_geo = APIOpenStreetMap()
api_jet = APIJetLocator()
json_saver = JSONSaver()

# Функция для взаимодействия с пользователем
def user_interaction():
    print("Трекер самолетов приветствует вас! Программа ищет самолеты в воздушном пространстве выбранной страны")
    country = input("Введите название страны на английском языке:\n")
    print("Вычисляю список самолетов в воздушном пространстве страны...")
    coordinates = api_geo.get_response(country)
    jets = api_jet.get_response(coordinates)

    while True:
        is_save = input("Сохранить данные по всем самолетам в файл? yes/no:\n").lower().strip()
        if is_save == "yes":
            json_saver.save_to_file(jets, "jets.json")
            break
        elif is_save == "no":
            break
        else:
            print("Неизвестная команда. Повторите ввод, пожалуйста.")

    while True:
        try:
            top_n = int(input("Введите количество самолетов для вывода в топ N по высоте:\n"))
        except ValueError:
            print("Значение должно быть целым числом")
        else:
            if top_n > 0:
                aeroplanes = Aeroplane.data_to_object_list(jets)
                sorted_jets = Aeroplane.sort_aeroplanes(aeroplanes, top_n)
                break
            else:
                print("Значение должно быть положительным числом")

    while True:
        is_print1 = input("Вывести полученный список самолетов? yes/no\n")
        if is_print1.lower().strip() == "yes":
            for jet in sorted_jets:
                print(jet)
            break
        elif is_print1.lower().strip() == "no":
            break
        else:
            print("Неизвестная команда. Повторите ввод, пожалуйста.")

    filtered_jets = []
    while True:
        filter_words = input("Введите через запятую названия стран на английском языке для фильтрации по стране \
регистрации воздушного судна:\n").split(",")
        filter_words_correct = [word.strip().title() for word in filter_words if word.strip()]
        if filter_words_correct:
            filtered_jets = Aeroplane.filter_aeroplane(sorted_jets, filter_words_correct)
            if filtered_jets:
                break
            else:
                print("По запросу ничего не найдено.")
        else:
            print("Вы ничего не ввели.")

        while True:
            is_repeat = input("Повторить запрос? yes/no \n").lower().strip()
            if is_repeat == "yes":
                break
            elif is_repeat == "no":
                break
            else:
                print("Неизвестная команда. Повторите ввод, пожалуйста.")
        if is_repeat == "no":
            break

    while True:
        is_print2 = input("Вывести полученный список самолетов? yes/no\n").lower().strip()
        if is_print2 == "yes":
            if filtered_jets:
                for aeroplane in filtered_jets:
                    print(aeroplane)
                break
            else:
                print("Самолеты не найдены")
                break
        elif is_print2 == "no":
            break
        else:
            print("Неизвестная команда. Повторите ввод, пожалуйста.")

    while True:
        is_filter = input("Отобрать самолеты по высоте полета? yes/no\n").lower().strip()
        if is_filter == "yes":
            while True:
                try:
                    min_value = int(input("Введите минимальное значение высоты полета в метрах:\n"))
                    max_value = int(input("Введите максимальное значение высоты полета в метрах:\n"))
                except ValueError:
                    print("Значение высоты должно быть целым числом")
                else:
                    if min_value < 0 or max_value < 0:
                        print("Значение высоты должно быть положительным числом")
                    elif min_value > max_value:
                        print("Минимальная высота не может быть больше максимальной.")
                    else:
                        jets_by_altitude = Aeroplane.aeroplanes_by_altitude_range(filtered_jets, min_value, max_value)
                        break
            break
        elif is_filter == "no":
            jets_by_altitude = filtered_jets
            break
        else:
            print("Неизвестная команда. Повторите ввод, пожалуйста.")

    while True:
        is_save = input("Сохранить избранные самолеты в файл? yes/no\n").lower().strip()
        if is_save == "yes":
            json_saver.add_to_file(jets_by_altitude, "my_aeroplanes.json")
            break
        elif is_save == "no":
            break
        else:
            print("Неизвестная команда. Повторите ввод, пожалуйста.")

    print("Печатаю итоговый список самолетов...")
    if jets_by_altitude:
        for jet in jets_by_altitude:
            print(jet)
    else:
        print("Самолеты подходящие под условия фильтрации не найдены")


if __name__ == "__main__":

    user_interaction()