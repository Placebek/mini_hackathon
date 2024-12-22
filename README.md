# mint_hackathon

1) Установите Alembic
pip install alembic

2) В корне вашего проекта выполните команду:
alembic init alembic

3) Настройте файл конфигурации alembic.ini и alembic/versions/env.py
Создание миграции:
alembic revision --autogenerate -m "message"

4) Чтобы применить миграцию к базе данных, выполните:
alembic upgrade head

Просмотр истории миграций: чтобы увидеть все примененные миграции
alembic history
