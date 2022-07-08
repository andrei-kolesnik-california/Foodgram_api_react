FROM python:3.7-slim

# Создать директорию вашего приложения.
workdir /django

# Скопировать с локального компьютера файл зависимостей
# в директорию /app.
COPY requirements.txt .

# Выполнить установку зависимостей внутри контейнера.
RUN pip3 install -r requirements.txt --no-cache-dir

# Скопировать содержимое директории /api_yamdb c локального компьютера
# в директорию /app.
COPY . .

# Выполнить запуск сервера разработки при старте контейнера.
# CMD ["gunicorn", "api_foodgram.wsgi:application", "--bind", "0:8000" ]