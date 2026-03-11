FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt /app/
RUN apt-get update && apt-get install -y default-libmysqlclient-dev build-essential && pip install --no-cache-dir -r requirements.txt
COPY . /app
EXPOSE 8000
CMD ["sh", "-c", "python manage.py migrate && python manage.py seed_mvp_data && python manage.py runserver 0.0.0.0:8000"]
