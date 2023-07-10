# Используйте базовый образ Python
FROM python:3.9

# Установите рабочую директорию внутри контейнера
WORKDIR /app

# Скопируйте файл зависимостей в контейнер
COPY requirements.txt .

# Установите зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Скопируйте все файлы проекта в контейнер
COPY . .

# Укажите порт, который будет использоваться приложением
EXPOSE 8000

# Запустите приложение с помощью uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
