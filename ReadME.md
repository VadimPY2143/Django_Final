# 🏡 BookingSite — Платформа для бронювання помешкань

**BookingSite** — це сучасна веб-платформа для бронювання житла. Сервіс дозволяє користувачам переглядати доступні варіанти, здійснювати бронювання, обробляти платежі через PayPal, а також отримувати повідомлення в реальному часі про статуси бронювань.

---

## Стек технологій

- **Backend**: [Python](https://www.python.org/), [Django](https://www.djangoproject.com/)
- **Асинхронні задачі**: [Celery](https://docs.celeryq.dev/), [Redis](https://redis.io/)
- **База даних**: [PostgreSQL](https://www.postgresql.org/)
- **Система оплати**: [PayPal](https://developer.paypal.com/tools/sandbox/)
- **Контейнери**: [Docker](https://www.docker.com/), [Docker Compose](https://docs.docker.com/compose/)

---

## 🔧 Установка (локально через Docker)

### 1. Клонування репозиторію

```bash
git clone https://https://github.com/VadimPY2143/Django_Final
```

### 2. Налаштування .env

```bash
EMAIL_BACKEND='django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST='smtp.example.com'
EMAIL_HOST_USER='your-email@example.com'
EMAIL_HOST_PASSWORD='your-email-password'
EMAIL_PORT=587
EMAIL_USE_TLS=True

PAYPAL_RECEIVER_EMAIL='your-paypal-biz@example.com'
PAYPAL_TEST=True
PAYPAL_CLIENT_ID='your-paypal-client-id'
PAYPAL_CLIENT_SECRET='your-paypal-client-secret'

POSTGRES_DB=example_db
POSTGRES_USER=example_user
POSTGRES_PASSWORD=example_password
POSTGRES_HOST=db
POSTGRES_PORT=5432
```

### 3. Запуск сервісів

```bash
docker-compose up --build
```

### 4. Застосування міграцій

```bash
docker-compose exec django python manage.py migrate
```

---
## Проєкт запущений
- 🌐 **Головна сторінка**: [http://localhost:8000](http://localhost:8000)  
- 🔐 **Адмінка Django**: [http://localhost:8000/admin](http://localhost:8000/admin)

---


##  Контакти

- 👨‍💻 **Розробник**: Вадим  
- 📍 **Місто**: Львів, Україна  
- ✉️ **Email**: vadimpapusha2310@gmail.com
- 🐙 **GitHub**: [VadimPY2143](https://github.com/VadimPY2143)  
