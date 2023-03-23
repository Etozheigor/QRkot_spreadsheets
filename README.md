# Cat Charity Fund
### О проекте
Cat Charity Fund - API-сервис для благотворительного фонда поддержки котиков. Администраторами фонда создаются 
целевые проекты для сбора средств, а пользователи могут делать пожертвования. Пожертвования делаются не на кокретный проект, а в фонд в целом. Все пожертвования идут в проект, открытый раньше других, после сбора нужной суммы проект закрывается и пожертвования начинают поступать в следующий проект. Есть возможность сформировать отчет о скорости сбора средств всех балготворительных проектов в гугл-таблице.


### Технологии
В данном проекте я отвечал за бэкенд-часть и использовал следующие технологии:
- Python
- FastAPI
- Alembic
- SQLAlchemy
- Uvicorn



### Как запустить проект:

- Клонировать репозиторий и перейти в него в командной строке:

```
git clone https://github.com/Etozheigor/cat_charity_fund.git
```

```
cd cat_charity_fund
```

- Cоздать и активировать виртуальное окружение:

```
python -m venv venv
```

```
source venv/Scripts/activate
```

- Установить зависимости из файла requirements.txt:

```
python -m pip install --upgrade pip
```

```
pip install -r requirements.txt
```

- создать файл .env и заполнить его по шаблону:

```
touch .env
```

шаблон заполнения файла:

```
DATABASE_URL=описание подключения к базе данных, по умолчанию в проекте стоит база данных sqlite+aiosqlite:///./fastapi.db, вы можете установить свою
SEKRET=ваш секретный ключ
```

- Выполнить миграции:

```
alembic init
```
```
alembic upgrade head
```

- Запустить проект:

```
uvicorn app.main:app
```

Проект будет доступен локально по адресу:

```
http://127.0.0.1:8000/
```

Эндпоинт с документацией swagger, через который можно делать запросы:
```
http://127.0.0.1:8000/docs
```

### Работа с Google Spreadsheets

Чтобы сформировать отчет о скорости сбора средств на благотворительные проекты, нужно сделать GET-запрос на эндпоинт /google.
Отчет появится в Spreadsheets на Google Drive. Для работы этого эндпоинта необходимо дополнить .env-файл, созданный ранее следующими данными:

```
TYPE=service_account
PROJECT_ID=***
PRIVATE_KEY_ID=***
PRIVATE_KEY=***
CLIENT_EMAIL=***
CLIENT_ID=***
AUTH_URI=***
TOKEN_URI=***
AUTH_PROVIDER_X509_CERT_URL=***
CLIENT_X509_CERT_URL=***
EMAIL= ваш gmail
```

Все константы можно перенести в .env файл из json файла, который вы скачиваете при создании сервисного аккаунта в Google API.
Если у вас нет нужного json файла, интсрукцию по его получению можно найти, например, здесь: https://stackoverflow.com/questions/46287267/how-can-i-get-the-file-service-account-json-for-google-translate-api





