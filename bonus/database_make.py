import os, requests, csv, shelve
from bs4 import BeautifulSoup


def mledoze_update_checking():
    """" Проверка обновлений базы данных mledoze """

    try:
        with open('last_update_date.txt') as old_date_f:
            old_date = old_date_f.readline()
    except IOError as e:
        # Если файла нет, то задаем дату, гарантирующую обновление
        old_date = '2000-01-01'

    page_url = 'https://github.com/mledoze/countries/blob/master/dist/countries.csv'
    page_req = requests.get(page_url)
    soup = BeautifulSoup(page_req.text, 'lxml')
    new_date = str(soup.find('relative-time'))
    # Тег с нужной датой (без учета GMT) имеет вид
    # <relative-time datetime="2017-01-03T17:02:27Z">Jan 4, 2017</relative-time>
    # Поэтому выделим дату в виде "гггг-мм-дд":
    new_date = new_date[25:35]
    if new_date > old_date:
        with open('last_update_date.txt', 'w') as new_date_f:
            new_date_f.write(new_date)
            return True
    else:
        return True


def mledoze_database_update(countries_db):
    """" Обновление нашей б/д с помощью mledoze """

    # Выгрузка базы данных mledoze в формате csv
    database_url = 'https://raw.githubusercontent.com/mledoze/countries/master/dist/countries.csv'
    database_req = requests.get(database_url, stream=True)
    with open('mledoze_database.csv', 'wb') as file:
        file.write(database_req.text.encode())
    del database_req

    # Добавление к нашей б/д словаря, в котором ключи - возможные названия стран (общие, официальные,
    # местные названия, переводы на популярные языки (8 языков), альтернативные названия
    # (в том числе 2-х и 3-х буквенные индексы), названия столиц),
    # а значения - уникальные идентификаторы стран.
    database = open('mledoze_database.csv', encoding='utf8')
    reader = csv.DictReader(database, delimiter=';', quotechar='"')
    fields = ['translations', 'capital', 'name', 'currency', 'altSpellings', 'cca2', 'cca3', 'cioc', 'currency']
    priority_fields = ['name', 'currency', 'cca2', 'cca3', 'cioc']
    for row in reader:
        # Список имен упорядочен в виде: общее, официальное, общее местное, официальное местное,
        # далее - названия на других национальных языках (если их несколько и названия известны)
        # По умолчанию названием страны считается официальное название
        country_names = row["name"].split(",")
        official_name = country_names[0] # Регулируемый параметр
        for field in fields:
            possible_names_list = row[field].split(",")
            for name in possible_names_list:
                # Расставляем приоритет. В функции нормализации сначала проверяется
                # совпадение со значениями с меньшим приоритетом
                if field in priority_fields:
                    countries_db[name.lower()] = '1' + official_name
                else:
                    countries_db[name.lower()] = '2' + official_name

    database.close()
    os.remove('mledoze_database.csv')


def i18nGeoNamesDB_update_checking():
    """" Проверка обновлений базы данных i18nGeoNamesDB """

    # Здесь нужно знать, может ли наша программа скачивать и сохранять архив до 10 Мб. Сделать это можно
    # Да и база обновлялась 4 года назад, так что в этом может не быть смысла
    return True


def i18nGeoNamesDB_database_update(countries_db):
    """ Добавляем в библиотеку названия регионов (на основе б/д регионов, полученной из ВКонтакте)
    Каждый регион имеет до 14 переводов на другие языки. Учитывая особую индексацию данной б/д
    (индексация начинается с России), нужно использовать б/д стран (из ВКонтакте) для сопоставления
    индекса страны в этой б/д настоящему названию """

    # Здесь может быть автоматическая выгрузка б/д

    # Добавление новых ключей
    countries = open('countries_vk.csv', encoding='utf8')
    id_to_name = {}
    fields = ['title_ru', 'title_ua', 'title_be', 'title_en', 'title_es', 'title_pt', 'title_de',
              'title_fr', 'title_it', 'title_pl', 'title_ja', 'title_lt', 'title_lv', 'title_cz']
    reader = csv.DictReader(countries)
    for row in reader:
        # C несколькими странами в данной базе случается проблема - несмотря на то, что они есть в базе в качестве
        # ключа и находятся в конструкции "if... in...", их ключ считается несуществующим. Это вызывает KeyError,
        # а затем EOFError при поимке KeyError. Поэтому мы игнорируем такие страны (около 3-х)
        try:
            if row["title_en"].lower() in countries_db.keys():
                id_to_name[row["country_id"]] = row["title_en"].lower()
                for field in fields:
                    countries_db[row[field].lower()] = countries_db[row["title_en"].lower()]
            else:
                for field in fields:
                    countries_db[row[field].lower()] = '1' + row["title_en"]
        except Exception:
            pass
    regions = open('regions_vk.csv', encoding='utf8')
    reader = csv.DictReader(regions)
    for row in reader:
        for field in fields:
            try:
                if row["country_id"] in id_to_name.keys() and id_to_name[row["country_id"]] in countries_db.keys():
                    countries_db[row[field].lower()] = '2' + countries_db[id_to_name[row["country_id"]]][1:]
            except Exception:
                pass
    regions.close()
    countries.close()


def update():
    """ Обновление нашей б/д с помощью сторонних """

    with shelve.open('countries_db') as countries_db:
        if mledoze_update_checking():
            mledoze_database_update(countries_db)
        if i18nGeoNamesDB_update_checking():
            i18nGeoNamesDB_database_update(countries_db)


def main():

    update()


if __name__ == "__main__":
    main()
