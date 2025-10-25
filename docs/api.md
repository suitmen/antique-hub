# AntiqueHub API Documentation

## Введение

Это документация для REST API платформы AntiqueHub - маркетплейса для продажи антиквариата.

## Базовый URL

```
http://localhost:8000/api
```

## Аутентификация

Большинство endpoints требуют аутентификации с помощью JWT токенов.

### Получение токена

```
POST /token
```

**Параметры:**
- `username` (string): email пользователя
- `password` (string): пароль пользователя

**Ответ:**
```json
{
  "access_token": "string",
  "token_type": "bearer"
}
```

## Пользователи

### Регистрация пользователя

```
POST /users/
```

**Параметры:**
- `email` (string): email пользователя
- `password` (string): пароль пользователя

**Ответ:**
```json
{
  "id": 1,
  "email": "user@example.com",
  "is_seller": false,
  "verified": false,
  "role": "buyer",
  "created_at": "2023-01-01T00:00:00"
}
```

### Получение списка пользователей

```
GET /users/
```

**Параметры:**
- `skip` (integer, optional): количество пропущенных записей (по умолчанию: 0)
- `limit` (integer, optional): максимальное количество записей (по умолчанию: 100)

**Ответ:**
```json
[
  {
    "id": 1,
    "email": "user@example.com",
    "is_seller": false,
    "verified": false,
    "role": "buyer",
    "created_at": "2023-01-01T00:00:00"
  }
]
```

### Получение пользователя по ID

```
GET /users/{user_id}
```

**Ответ:**
```json
{
  "id": 1,
  "email": "user@example.com",
  "is_seller": false,
  "verified": false,
  "role": "buyer",
  "created_at": "2023-01-01T00:00:00"
}
```

## Лоты

### Создание лота

```
POST /lots/
```

**Требуется аутентификация**

**Параметры:**
- `title` (string): название лота
- `description` (string): описание лота
- `price` (number): цена
- `currency` (string, optional): валюта (по умолчанию: "RUB")
- `category` (string): категория
- `era` (string): эпоха
- `material` (string): материал
- `image_urls` (array of strings, optional): URL изображений

**Ответ:**
```json
{
  "id": 1,
  "title": "Антикварная ваза",
  "description": "Красивая ваза из фарфора",
  "price": 10000,
  "currency": "RUB",
  "category": "ceramics",
  "era": "19th",
  "material": "фарфор",
  "image_urls": ["http://example.com/image1.jpg"],
  "is_approved": false,
  "status": "pending",
  "seller_id": 1,
  "created_at": "2023-01-01T00:00:00"
}
```

### Получение списка лотов

```
GET /lots/
```

**Параметры:**
- `skip` (integer, optional): количество пропущенных записей (по умолчанию: 0)
- `limit` (integer, optional): максимальное количество записей (по умолчанию: 100)

**Ответ:**
```json
[
  {
    "id": 1,
    "title": "Антикварная ваза",
    "description": "Красивая ваза из фарфора",
    "price": 10000,
    "currency": "RUB",
    "category": "ceramics",
    "era": "19th",
    "material": "фарфор",
    "image_urls": ["http://example.com/image1.jpg"],
    "is_approved": false,
    "status": "pending",
    "seller_id": 1,
    "created_at": "2023-01-01T00:00:00"
  }
]
```

### Получение лота по ID

```
GET /lots/{lot_id}
```

**Ответ:**
```json
{
  "id": 1,
  "title": "Антикварная ваза",
  "description": "Красивая ваза из фарфора",
  "price": 10000,
  "currency": "RUB",
  "category": "ceramics",
  "era": "19th",
  "material": "фарфор",
  "image_urls": ["http://example.com/image1.jpg"],
  "is_approved": false,
  "status": "pending",
  "seller_id": 1,
  "created_at": "2023-01-01T00:00:00"
}
```

## Заказы

### Создание заказа

```
POST /orders/
```

**Требуется аутентификация**

**Параметры:**
- `item_id` (integer): ID лота

**Ответ:**
```json
{
  "id": 1,
  "item_id": 1,
  "buyer_id": 1,
  "status": "created",
  "payment_id": null,
  "payment_provider": null,
  "created_at": "2023-01-01T00:00:00"
}
```

### Получение списка заказов

```
GET /orders/
```

**Требуется аутентификация**

**Параметры:**
- `skip` (integer, optional): количество пропущенных записей (по умолчанию: 0)
- `limit` (integer, optional): максимальное количество записей (по умолчанию: 100)

**Ответ:**
```json
[
  {
    "id": 1,
    "item_id": 1,
    "buyer_id": 1,
    "status": "created",
    "payment_id": null,
    "payment_provider": null,
    "created_at": "2023-01-01T00:00:00"
  }
]
```

## Платежи

### Инициализация платежа

```
POST /payments/init
```

**Требуется аутентификация**

**Параметры:**
- `item_id` (integer): ID лота
- `currency` (string): валюта платежа

**Ответ:**
```json
{
  "provider": "yookassa",
  "payment_id": "12345",
  "redirect_url": "https://yookassa.ru/payment/12345"
}
```

## Техподдержка

### Создание тикета

```
POST /support/tickets
```

**Требуется аутентификация**

**Параметры:**
- `subject` (string): тема тикета
- `message` (string): сообщение
- `category` (string): категория (payment, item, account, delivery)
- `order_id` (integer, optional): ID заказа

**Ответ:**
```json
{
  "id": 1,
  "user_id": 1,
  "subject": "Проблема с оплатой",
  "message": "Оплата не прошла",
  "category": "payment",
  "order_id": 1,
  "status": "new",
  "created_at": "2023-01-01T00:00:00"
}
```

### Получение списка тикетов

```
GET /support/tickets
```

**Требуется аутентификация**

**Параметры:**
- `skip` (integer, optional): количество пропущенных записей (по умолчанию: 0)
- `limit` (integer, optional): максимальное количество записей (по умолчанию: 100)

**Ответ:**
```json
[
  {
    "id": 1,
    "user_id": 1,
    "subject": "Проблема с оплатой",
    "message": "Оплата не прошла",
    "category": "payment",
    "order_id": 1,
    "status": "new",
    "created_at": "2023-01-01T00:00:00"
  }
]