# Використовуйте офіційний образ Python як базовий
FROM python:3.12.2

# Встановіть poetry
RUN pip install poetry

#Встановіть змінну середовища
ENV APP_HOME /app

# Встановіть робочу директорію всередині контейнера
WORKDIR $APP_HOME

# Копіюйте файли pyproject.toml та poetry.lock у контейнер
COPY pyproject.toml poetry.lock ./

# Встановіть залежності проекту
RUN poetry install --no-root
#
COPY . .
#
ENTRYPOINT ["python", "app.py"]