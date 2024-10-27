# Начальный образ Python
FROM python:3.12-slim as base

# Переменные окружения для Python
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Устанавливаем рабочую директорию
WORKDIR /app

# Установка зависимостей через requirements.txt с кэшированием pip
RUN --mount=type=cache,target=/root/.cache/pip \
    --mount=type=bind,source=requirements.txt,target=/app/requirements.txt \
    python -m pip install -r /app/requirements.txt

# Установка protoc для работы с .proto файлами
RUN apt-get update && apt-get install -y \
    unzip \
    wget && \
    wget https://github.com/protocolbuffers/protobuf/releases/download/v21.12/protoc-21.12-linux-x86_64.zip && \
    unzip protoc-21.12-linux-x86_64.zip -d /usr/local && \
    rm protoc-21.12-linux-x86_64.zip

RUN apt-get update && apt-get install -y grpcurl

# Копирование всех файлов проекта
COPY . /app

# Указываем порт
EXPOSE 8084

# Запуск через скрипт startup.sh
ENTRYPOINT ["sh", "./startup.sh"]
