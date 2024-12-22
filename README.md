# mint_hackathon

<!-- Установите Alembic -->
pip install alembic

<!-- В корне вашего проекта выполните команду: -->
alembic init alembic

<!-- Настройте файл конфигурации alembic.ini и alembic/versions/env.py -->
<!-- Создание миграции: -->
alembic revision --autogenerate -m "message"

<!-- Чтобы применить миграцию к базе данных, выполните: -->
alembic upgrade head

<!-- Просмотр истории миграций: чтобы увидеть все примененные миграции -->
alembic history
