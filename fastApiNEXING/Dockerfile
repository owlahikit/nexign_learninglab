# Используем базовый образ Python
FROM python:3.8-slim

# Устанавливаем рабочую директорию внутри контейнера
WORKDIR /app

# Копируем файлы проекта в рабочую директорию контейнера
COPY best.pt .
COPY Dockerfile .
COPY model.py .
COPY model.joblib .
COPY requirements.txt .
COPY server.py .
COPY yolov8m-seg.pt .

# Устанавливаем зависимости Python
RUN pip install -r requirements.txt

# Определяем команду для запуска приложения
CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "8000"]
