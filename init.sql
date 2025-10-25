-- Файл инициализации базы данных PostgreSQL для AntiqueHub

-- Создание базы данных (если еще не создана)
CREATE DATABASE antiquehub;

-- Подключение к базе данных
\c antiquehub;

-- Создание таблицы пользователей
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    is_seller BOOLEAN DEFAULT FALSE,
    verified BOOLEAN DEFAULT FALSE,
    role VARCHAR(20) DEFAULT 'buyer',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Создание таблицы лотов
CREATE TABLE IF NOT EXISTS lots (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    price NUMERIC(12, 2) NOT NULL,
    currency VARCHAR(3) DEFAULT 'RUB',
    category VARCHAR(50),
    era VARCHAR(100),
    material VARCHAR(100),
    image_urls JSON,
    is_approved BOOLEAN DEFAULT FALSE,
    status VARCHAR(20) DEFAULT 'pending',
    seller_id INTEGER REFERENCES users(id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Создание таблицы заказов
CREATE TABLE IF NOT EXISTS orders (
    id SERIAL PRIMARY KEY,
    item_id INTEGER REFERENCES lots(id),
    buyer_id INTEGER REFERENCES users(id),
    status VARCHAR(20) DEFAULT 'created',
    payment_id VARCHAR(100),
    payment_provider VARCHAR(20),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Создание таблицы тикетов поддержки
CREATE TABLE IF NOT EXISTS support_tickets (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    subject VARCHAR(255) NOT NULL,
    message TEXT NOT NULL,
    category VARCHAR(20) NOT NULL,
    order_id INTEGER REFERENCES orders(id),
    status VARCHAR(20) DEFAULT 'new',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Создание индексов для улучшения производительности
CREATE INDEX IF NOT EXISTS idx_lots_seller_id ON lots(seller_id);
CREATE INDEX IF NOT EXISTS idx_lots_category ON lots(category);
CREATE INDEX IF NOT EXISTS idx_lots_status ON lots(status);
CREATE INDEX IF NOT EXISTS idx_orders_item_id ON orders(item_id);
CREATE INDEX IF NOT EXISTS idx_orders_buyer_id ON orders(buyer_id);
CREATE INDEX IF NOT EXISTS idx_support_tickets_user_id ON support_tickets(user_id);
CREATE INDEX IF NOT EXISTS idx_support_tickets_status ON support_tickets(status);