# Руководство по развертыванию AntiqueHub

## Системные требования

- Docker и Docker Compose
- Git

## Локальное развертывание

### 1. Клонирование репозитория

```bash
git clone <repository-url>
cd antiquehub
```

### 2. Настройка переменных окружения

Скопируйте файл `.env.example` в `.env` и заполните необходимые значения:

```bash
cp .env.example .env
```

Отредактируйте файл `.env` и укажите свои значения для:
- `SECRET_KEY` - секретный ключ для JWT
- `YOOKASSA_SHOP_ID` и `YOOKASSA_SECRET_KEY` - данные для интеграции с ЮKassa
- `STRIPE_SECRET_KEY` и `STRIPE_WEBHOOK_SECRET` - данные для интеграции со Stripe

### 3. Запуск приложения

```bash
docker-compose up -d
```

После запуска приложение будет доступно по адресам:
- Фронтенд: http://localhost:3000
- Бэкенд API: http://localhost:8000
- Документация API: http://localhost:8000/docs

### 4. Остановка приложения

```bash
docker-compose down
```

## Развертывание в production

### Настройка базы данных

Для production рекомендуется использовать отдельный сервер базы данных PostgreSQL.

### Настройка веб-сервера

Для production рекомендуется использовать Nginx в качестве reverse proxy.

Пример конфигурации Nginx:

```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://localhost:3000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    location /api/ {
        proxy_pass http://localhost:8000/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

### Настройка SSL

Рекомендуется использовать Let's Encrypt для получения SSL сертификата.

### Масштабирование

Для масштабирования можно использовать несколько инстансов бэкенда и фронтенда с балансировкой нагрузки.

## Резервное копирование

Регулярно создавайте резервные копии базы данных:

```bash
docker exec antiquehub_db pg_dump -U antique_user antiquehub > backup.sql
```

## Мониторинг

Рекомендуется настроить мониторинг для отслеживания состояния приложения:
- Доступность сервисов
- Использование ресурсов
- Логи ошибок