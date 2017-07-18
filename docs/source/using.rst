==========
Применение
==========

------------------  
Общая демонстрация
------------------

Код, используемый для демонстрации возможностей модуля::

    from countries_lib import country


    def main():
    """ Пример использования библиотеки для нормализации названия страны """

    # Вывод корректные названия для вариантов из списка:
    test_list = ['USA', 'US', 'Amurica!!!', 'NewYork', 'Untgd States of America', 'Paris, USA', 'agagagag']
    for variant in test_list:
        print(variant, ' - ', country.normalize_country_name(variant))
    print('-------------------------------------------------------------')
    # Добавление значения
    print('Проверка "AddCountryTest" на существование: ', country.normalize_country_name('AddCountryTest'))
    country.match_country_name('AddCountryTest', 'AddCountryTest')
    print('Проверка "AddCountryTest" на существование: ', country.normalize_country_name('AddCountryTest'))
    print('-------------------------------------------------------------')
    # Удаление значения
    print('Проверка "AddCountryTest" на существование: ', country.normalize_country_name('AddCountryTest'))
    country.del_country_name('AddCountryTest')
    print('Проверка "AddCountryTest" на существование: ', country.normalize_country_name('AddCountryTest'))
    print('-------------------------------------------------------------')
    # Демонстрация низкой и высокой точности
    print('Testing variant: ', 'ololo')
    print('0.3 (low) accurate: ', country.normalize_country_name('ololo', 0.3))
    print('0.6 (standard) accurate: ', country.normalize_country_name('ololo'))
    print('0.9 (high) accurate: ', country.normalize_country_name('ololo', 0.9))
    print('Testing variant: ', 'Rasia')
    print('0.3 (low) accurate: ', country.normalize_country_name('Rasia', 0.3))
    print('0.6 (standard) accurate: ', country.normalize_country_name('Rasia'))
    print('0.9 (high) accurate: ', country.normalize_country_name('Rasia', 0.9))


    if __name__ == "__main__":
        main()

Вывод при выполнении данного кода::

    USA  -  United States
    US  -  United States
    Amurica!!!  -  United States
    NewYork  -  United States
    Untgd States of America  -  United States
    Paris, USA  -  United States
    agagagag  -  None
    -------------------------------------------------------------
    Проверка "AddCountryTest" на существование:  None
    Проверка "AddCountryTest" на существование:  AddCountryTest
    -------------------------------------------------------------
    Проверка "AddCountryTest" на существование:  AddCountryTest
    Проверка "AddCountryTest" на существование:  None
    -------------------------------------------------------------
    Testing variant:  ololo
    0.3 (low) accurate:  Norway
    0.6 (standard) accurate:  None
    0.9 (high) accurate:  None
    Testing variant:  Rasia
    0.3 (low) accurate:  Russia
    0.6 (standard) accurate:  Russia
    0.9 (high) accurate:  None

Как видно из результатов, функции делают именно то, что заявлено в их описании (без учета ошибок, это рассматривается далее).

Возможна другая форма импорта::

    from countries_lib.country import normalize_country_name, match_country_name, del_country_name

Такая форма позволяет обращаться к функциям напрямую.

------------------------
Необязательные аргументы
------------------------

В функциях **normalize_country_name** и **match_country_name** есть необязательные аргументы. Рассмотрим их применение.

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
dif_acc (функция normalize_country_name) 
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Параметр точности (коэффициент совпадения строк). Отвечает за минимальное расстояние между строками, при котором они 
считаются похожими. Принимает значения от **0.0** до **1.0** и по умолчанию равен **0.7**. Чем больше данный параметр, тем точнее будет результат - это напрямую 
регулирует исправление опечаток. При низком **dif_acc** даже для сильных опечаток будет найден подходящий вариант, но при этом возможно нахождение подходящего варианта 
для бессмысленной последовательности букв типа "azazazaz". При высоком **dif_acc** уменьшится количество исправляемых опечаток и на очевидные для человека ошибки 
программа будет выдавать, что совпадений не найдено. 

Стоит отметить, что если для заданного возможного имени есть полностью совпадающий ключ, то его значение будет 
возвращено независимо от **dif_acc**, так как расстояние между этими строками будет равно 0 (коэффициент совпадения - 1.0, предельное корректное значение). 
Поэтому **dif_acc** влияет только на исправление опечаток.

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
priority (функция match_country_name)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ 

Приоритет ключа, принимающий значения **1** или **2** (по умолчанию - **2**) и определяющий, что содержится в ключе: 
название, сокращение, индекс или перевод названия страны, если приоритет равен **1**, и все остальное, если приоритет равен **2**. Так как большинство ключей, 
подходящих под приоритет **1**, уже в базе, то возможно задать приоритет по умолчанию равный **2**. 

-----------------
Работа с ошибками
-----------------

Пример кода, обрабатывающего функцию **normalize_country_name**::

    name = normalize_country_name('Some Name')
    if name == 'Invalid argument type':
        # Your code
    elif name == 'DatabaseError':
        # Your code
    else:
        # Your code

Для функций **match_country_name** и **del_country_name** принцип тот же.

Если Вы уверены в том, что на вход функций подаются корректные аргументы и с базой данных все в порядке, то в обработке ошибок нет необходимости.

