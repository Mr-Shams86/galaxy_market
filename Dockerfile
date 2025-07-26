FROM python:3.10-slim

# Устанавливаем netcat и зависимости
RUN apt-get update && apt-get install -y netcat-openbsd gcc libpq-dev && apt-get clean

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем зависимости
COPY requirements.txt .

# Устанавливаем зависимости Python
RUN pip install --no-cache-dir -r requirements.txt

# Копируем весь проект
COPY . .

# Делаем скрипт исполняемым
RUN chmod +x ./entrypoint.sh

# Запускаем
ENTRYPOINT ["./entrypoint.sh"]
