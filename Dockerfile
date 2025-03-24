# Используем официальный образ Python
FROM python:3.12

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем файлы проекта
COPY . .

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем .env в контейнер
COPY .env .env

# Открываем порт (если приложение работает на 5000 порту)
EXPOSE 5000

# Запуск приложения
CMD ["python", "main.py"]