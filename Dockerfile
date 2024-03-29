#Використовуємо офіційний образ Python
FROM python:3.12.2
#
ENV APP_HOME /app
#
WORKDIR $APP_HOME
#
COPY . .
#
ENTRYPOINT ["python", "app.py"]