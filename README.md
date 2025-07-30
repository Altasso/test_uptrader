# Django Древовидное Меню — README

## Описание проекта

Это Django-приложение реализует древовидное меню с хранением данных в базе и редактированием через стандартную админку.
Меню поддерживает несколько уровней вложенности, активные пункты меню подсвечиваются в зависимости от текущего URL,
переходы осуществляются по явным URL или по именованным маршрутам (named_url). Меню выводится в шаблонах через template
tag `{% draw_menu 'menu_name' %}`.

---

## Установка и запуск

1. Клонируйте репозиторий:

git clone https://github.com/Altasso/test_uptrader.git
cd test_uptrader

2. Создайте виртуальное окружение и активируйте его:

- Linux/macOS:

python3 -m venv .venv
source .venv/bin/activate

- Windows:

python -m venv .venv
.venv\Scripts\activate

3. Установите зависимости:

pip install -r requirements.txt

4. Выполните миграции базы данных:

python manage.py makemigrations
python manage.py migrate

5. Создайте суперпользователя для доступа в админку:

python manage.py createsuperuser

6. Запустите сервер разработки:

python manage.py runserver

---

## Использование

- Откройте админку по адресу http://127.0.0.1:8000/admin/
- Создайте меню, указав `menu_name` (например, `main_menu`)
- Добавьте пункты меню, укажите для них:
    - имя (`name`)
    - родительский пункт (`parent`) для вложенности
    - явный URL (`url`) или имя маршрута из `urls.py` (`named_url`)


```django
{% load menu_tags %}
{% draw_menu 'main_menu' %}
```
## Структура проекта
- menu/models.py — модель MenuItem для пунктов меню

- menu/templatetags/menu_tags.py — templatetag для рендеринга меню

- menu/templates/menu/ — шаблоны меню и пунктов меню

- menu/views.py — представление для динамической страницы по slug

- uptrader/urls.py — маршруты проекта, включая dynamic_page

## Особенности
- Одно SQL-запрос для загрузки всего меню

- Автоматическое раскрытие активных веток меню

- Поддержка нескольких меню на одной странице

- Переходы по явным URL или по именованным маршрутам с передачей slug

- Активный пункт меню определяется по текущему URL

## Важные моменты
- Для пунктов с named_url='dynamic_page' обязательно указывать поле slug

- Метод get_absolute_url строит URL либо через reverse с именем маршрута и slug, либо через явный url

- В URLconf задан маршрут с regex, ловящий все запросы re_path(r'^(?P<slug>.+)/$', views.dynamic_page, name='dynamic_page')
