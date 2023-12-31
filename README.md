# Online platform of the electronics retail network
# Онлайн платформа торговой сети электроники
Бэкенд часть spa-приложения.

#### Технические требования:
-   Python 3.8+
-   Django 3+
-   DRF 3.10+
-   PostgreSQL 10+

Сеть представляет собой иерархическую структуру из 3 уровней:

-   Завод;
-   Розничная сеть;
-   Индивидуальный предприниматель.

Каждое звено сети ссылается только на одного поставщика оборудования (не обязательно предыдущего по иерархии). Уровень иерархии определяется не названием звена, а отношением к остальным элементам сети, т.е. завод всегда находится на 0 уровне, а если розничная сеть относится напрямую к заводу, минуя остальные звенья - её уровень - 1.

В проекте реализованы следующие модели:

__Сеть:__

Поля:
-   Название;
-   Контакты:
-   Email;
-   Страна;
-   Город;
-   Улица;
-   Номер дома;
-   Продукт.
-   Поставщик (предыдущий по иерархии объект сети);
-   Задолженность перед поставщиком в денежном выражении с точностью до копеек;
-   Время создания (заполняется автоматически при создании).

__Продукт:__

Поля:
- Название;
- Модель;
- Дата выхода продукта на рынок;

В админ-панели настроен доступ к объектам.

Для моделей реализован CRUD.
Для модели поставщика запрещено обновление через API поля «Задолженность перед поставщиком».

Реализован метод «admin action», очищающий задолженность перед поставщиком у выбранного объекта сети.
Реализована фильтрация по названию города и страны.

Доступ к API имеют только активные пользователи.

## Начало работы

### Настройки проекта
    POSTGRES_USER пользователь базы данных
    POSTGRES_PASSWORD пароль для базы данных
    POSTGRES_PORT=5432 порт базы данных
    POSTGRES_DB название базы данных
    POSTGRES_HOST=localhost - хост для базы данных для локального запуска


### Для локального запуска проекта необходимо выполнить следующие команды (Linux/Windows):
-   при работе на Linux запустить сервис postgresql:

    sudo service postgresql start

-   создать базу данных и записать ее название в переменную POSTGRES_DB в .env-файл
-   установить виртуальное окружение:

    python -m venv venv

    python3 -m venv venv
-   активировать виртуальное окружение:

    venv/Scripts/activate

    source venv/bin/activate
-   установить зависимости:

    python -m pip install -r requirements-win.txt

    python3 -m pip install -r requirments.txt
-   применить миграции:

    python manage.py migrate

-   загрузить данные из дампа:

    python  manage.py loaddata data.json

-   либо работать с пустой базой, тогда нужно создать пользователей:

    python  manage.py csu
-   запустить проект:

    python  manage.py runserver