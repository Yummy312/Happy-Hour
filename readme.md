# Happy Hour FastAPI Project

### Описание проекта

Проект предоставляет конечные точки для операций CRUD (создание, чтение, обновление, удаление) над предприятиями и продуктами.



### Технологический стек

- ⚡ [**FastAPI**](https://fastapi.tiangolo.com) для бекенда на Python.
    - 🧰 [SQLAlchemy](https://sqlmodel.tiangolo.com) для работы с SQL-базой данных (ORM).
    - 🔍 [Pydantic](https://docs.pydantic.dev), используемый FastAPI, для валидации данных и управления настройками.
    - 💾 [PostgreSQL](https://www.postgresql.org) в качестве SQL-базы данных.
- 🐋 [Docker Compose](https://www.docker.com) для разработки и продакшена.
- ✅ Тесты с [Pytest](https://pytest.org).



#### Установка Python и виртуальное окружение
Для установки Python с помощью pip у вас уже должен быть установлен Python. pip обычно включается в установки Python, начиная с версии Python 3.4 и выше.



```shell
pip install python==3.9.13
```

- Создание виртуальной среды для Windows:

```shell
python -m venv myvenv
```

- Активация виртуальной среды для macOS и Linux:

```shell
source venv/bin/activate
```

#### Установка зависимостей

```shell
pip install -r requirements.txt
```


#### Структура проекта
  - app/
    - `main.py`                      запуска FastAPI
    - companies/
      - `models.py`                   хранение моделей таблиц
      - `router.py`                   эндпоинты
      - `dao.py`                      содержит класс для работы с базой данных CRUD (наследуется от BaseDao)
      - `schemas.py`                  для валидации данных (схемы) компаний
    - dao/                             
      - `base.py`                     содержит класс BaseDao                 
    - products/
      - `models.py`                   хранения моделей таблиц
      - `router.py`                   группировки эндпоинтов
      - `dao.py`                      для работы с базой данных (наследуется от BaseDao)
      - `schemas.py`                  для валидации данных (схемы) продуктов
    - tests/                          Папка для общих тестов проекта
    - `config.py`                     Содержит класс, который работает с переменными оркужения из файла .env
    - `database.py`                   Подключение к БД
    - `exceptions.py`                 Включает исключения
    - `migrations`                    Содержит файл миграции и необходимые настройки для Alembic




#### Запуск тестов

```shell
pytest
```


## Полезно знать
```Python
# app/config.py
from typing import Literal

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    MODE: Literal["DEV", "TEST", "PROD",] = "PROD"
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASS: str
    DB_NAME: str

    @property
    def get_database_url(self) -> str:
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    TEST_DB_HOST: str
    TEST_DB_PORT: int
    TEST_DB_USER: str
    TEST_DB_PASS: str
    TEST_DB_NAME: str

    @property
    def get_test_database_url(self) -> str:
        return f"postgresql+asyncpg://{self.TEST_DB_USER}:{self.TEST_DB_PASS}@{self.TEST_DB_HOST}:{self.TEST_DB_PORT}/{self.TEST_DB_NAME}"

    class Config:
        env_file = ".env"


settings = Settings()

```
Данный файл представляет собой определение класса Settings, который используется для загрузки настроек из переменных окружения в вашем приложении.

Использование переменной MODE позволяет определить режим работы вашего приложения и соответственно выбирать необходимые настройки, включая конфигурацию базы данных.

Например, если MODE равен TEST, то будет использваться тестовая база данных. Это может быть полезно для проведения автоматических тестов без воздействия на основные данные в рабочей базе данных.


### Настроить
Прежде чем разворачивать приложение, убедитесь, что вы создали файл `.env` и скопировали переменные окружения ниже. Обязательно внесите изменения в значения переменных окружения, чтобы они соответствовали вашей конфигурации. Например, укажите свой собственный пароль для доступа к базе данных, если он отличается от предоставленного.


```plaintext
MODE=DEV

DB_HOST=localhost
DB_PORT=5432
DB_USER=myuser
DB_PASS=mypassword
DB_NAME=db

TEST_DB_HOST=localhost
TEST_DB_PORT=5432
TEST_DB_USER=myuser
TEST_DB_PASS=mypassword
TEST_DB_NAME=db_test
```


#### Database Schema


В базе данных будут созданы две таблицы: "Company" и "Product". Эти таблицы связаны отношением "один ко многим", что означает, что у одной компании может быть несколько продуктов.
![Alt текст](./images/schema_db.png 'Schema of database')








## Контакты
Если у вас есть какие-либо вопросы или предложения, пожалуйста, свяжитесь со мной:

- **Email:** kurmusheuv.nurzhigit@gmail.com
- **Телефон:** +996500755887
- **Telegram:**  @Nurzhigit312