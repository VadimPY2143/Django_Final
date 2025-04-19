FROM python:3.11

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

RUN apt-get update && apt-get install -y \
    libpq-dev gcc python3-dev && \
    apt-get clean

COPY requirements.txt /app/

RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

COPY . /app/

CMD ["sh", "-c", "python manage.py makemigrations && python manage.py migrate && python manage.py runserver localhost:8000"]

#CMD ["python", "manage.py", "runserver", "localhost:8000"]
