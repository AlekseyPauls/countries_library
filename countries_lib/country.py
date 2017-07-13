import shelve
import difflib


# Путь до базы данных. Имя файла прописать без расширения
DB_PATH = 'C:\python3\Lib\site-packages\countries_lib\countries_db'


def match_country_name(key, value, priority='2'):
    """ Добавление страны. Аргументы: key - ариант названия страны (строка), value - общее название страны (строка),
    priority (строка с цифрой или целое число 1 или 2) - приоритет варианта при нормализации ('1' - высокий
    (название страны, перевод, сокращение), '2' - низкий (столица, регион, и т.д.) """

    with shelve.open(DB_PATH) as countries_db:
        countries_db[key.lower()] = str(priority) + value
    return None


def del_country_name(key):
    """ Удаление варианта названия страны. Аргумент: key - удаляемый вариант названия страны. 
    Возращаемое значение: нет """

    with shelve.open(DB_PATH) as countries_db:
        del countries_db[key.lower()]
    return None


def normalize_country_name(posname, dif_acc=0.7):
    """ Приведение названия страны к общепринятому виду. Аргументы: posname (possible name) - нормализуемое название 
    (строка), dif_acc - параметр точности (вещественное число от 0 до 1, по умолчанию 0.7). 
    Возвращаемое значение: общее название страны (строка), если не найдено - 'None' (строка) """

    with shelve.open(DB_PATH) as countries_db:
        try:
            posname = str(posname).lower()
            # Очищаем входную строку от знаков препинания, которые не встречаются в названиях стран
            # Данный способ безопаснее, чем регулярные выражения и применение некоторых стандартных функций,
            # всвязи с национальными символами в названиях стран. Если пользователь умудрится использовать
            # иные символы, то он либо опечатался, либо издевается. Опечатки исправляются далее.
            symbols = [',', '.', '/', '!', '?', '<', '>', '[', ']', '|', '(', ')', '+', '=', '_', '*', '&', '%',
                       ';', '№', '~', '@', '#', '$', '{', '}']
            for symb in symbols:
                posname = posname.replace(symb, '')

            # Сначала ищем совпадение всей строки и значения с приоритетом '1'
            # Проверка на длину - чтобы исключить варианты, когда совпало только начало строки
            posname_1 = difflib.get_close_matches(posname, countries_db.keys(), n=1, cutoff=dif_acc)
            if posname_1 != [] and countries_db[posname_1[0]][0] == '1' and \
                    len(posname) - len(posname_1[0]) <= 1:
                return countries_db[posname_1[0]][1:]
            # Ищем совпадение всей строки и значения с приоритетом '2'
            posname_2 = difflib.get_close_matches(posname, countries_db.keys(), n=1, cutoff=dif_acc)
            if posname_2 != [] and countries_db[posname_2[0]][0] == '2' and \
                    len(posname) - len(posname_2[0]) <= 1:
                return countries_db[posname_2[0]][1:]
            # Делим входную строку на слова, разделитель - пробел
            parts = posname.split(" ")
            for part in parts:
                # Ищем совпадение части строки и значения с приоритетом '1'
                part_1 = difflib.get_close_matches(part, countries_db.keys(), n=1, cutoff=dif_acc)
                if part_1 != [] and countries_db[part_1[0]][0] == '1' and len(part) - len(part_1[0]) <= 1:
                    return countries_db[part_1[0]][1:]
            for part in parts:
                # Теперь ищем совпадение части строки и значения с приоритетом '2'
                part_2 = difflib.get_close_matches(part, countries_db.keys(), n=1, cutoff=dif_acc)
                if part_2 != [] and countries_db[part_2[0]][0] == '2' and len(part) - len(part_2[0]) <= 1:
                    return countries_db[part_2[0]][1:]
            return 'None'
        except LookupError:
            return 'None'