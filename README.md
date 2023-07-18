# FastAPIJWTAuth

## О проекте:
В проекте реализовано создание пользователя, аутентификация по JWT-токену, CRUD постов. 
Также пользователь может поставить лайк или дизлайк посту, при условии, что он не автор поста.

## Технологии:
- FastAPI
- Pydantic
- Pyjwt
- SQLAlchemy
- Alembic


## Установка:
- Скопировать проект с гитхаб
- Создать и активировать виртуальную среду
- Установить зависимости (```pip install -r requirements.txt``` либо через poetry)
- Подключить базу Postgres (название базы: jwtblog)
- Создать файл .env и добавить в него DATABASE_URL (```DATABASE_URL='postgresql://postgres:anna@localhost/jwt_blog'```)
- Отдать команду применить миграции (```alembic upgrade head```)
- Запустить приложение локально (```python application.py```)

Healthcheck доступен здесь: http://localhost:8000/ping
Документация здесь: http://localhost:8000/api/v1/docs