-- Test data for AntiqueHub database

-- Insert test users
INSERT INTO users (email, hashed_password, is_seller, verified, role, created_at) VALUES
('buyer1@example.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj/RK.PZvO.S', true, true, 'buyer', NOW()),
('buyer2@example.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj/RK.PZvO.S', false, true, 'buyer', NOW()),
('seller1@example.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj/RK.PZvO.S', true, true, 'seller', NOW()),
('seller2@example.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj/RK.PZvO.S', true, true, 'seller', NOW()),
('admin@example.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj/RK.PZvO.S', false, true, 'admin', NOW());

-- Insert test lots
INSERT INTO lots (title, description, price, currency, category, era, material, image_urls, is_approved, status, seller_id, created_at) VALUES
('Antique Wooden Chair', 'Beautiful antique wooden chair from the 18th century, excellent condition.', 12000.00, 'RUB', 'Furniture', '18th Century', 'Wood', '["/images/chair1.jpg"]', true, 'approved', 3, NOW()),
('Vintage Silver Necklace', 'Elegant silver necklace with intricate design, circa 1920s.', 8500.00, 'RUB', 'Jewelry', '1920s', 'Silver', '["/images/necklace1.jpg"]', true, 'approved', 3, NOW()),
('Classic Oil Painting', 'Original oil painting by a lesser-known artist from the 19th century.', 45000.00, 'RUB', 'Art', '19th Century', 'Canvas', '["/images/painting1.jpg"]', true, 'approved', 4, NOW()),
('Antique Porcelain Vase', 'Delicate porcelain vase with hand-painted flowers, Qing Dynasty.', 32000.00, 'RUB', 'Decorative', 'Qing Dynasty', 'Porcelain', '["/images/vase1.jpg"]', true, 'approved', 4, NOW()),
('Vintage Leather Armchair', 'Luxurious leather armchair from the 1950s, recently restored.', 18000.00, 'RUB', 'Furniture', '1950s', 'Leather', '["/images/armchair1.jpg"]', true, 'approved', 3, NOW()),
('Antique Bronze Statue', 'Small bronze statue from the Art Deco period, excellent condition.', 25000.00, 'RUB', 'Sculpture', 'Art Deco', 'Bronze', '["/images/statue1.jpg"]', true, 'approved', 4, NOW()),
('Vintage Wooden Desk', 'Magnificent wooden desk from the early 20th century, solid oak construction.', 35000.00, 'RUB', 'Furniture', 'Early 1900s', 'Oak', '["/images/desk1.jpg"]', true, 'approved', 3, NOW()),
('Antique Clock', 'Ornate grandfather clock from the Victorian era, still functional.', 55000.00, 'RUB', 'Decorative', 'Victorian Era', 'Wood', '["/images/clock1.jpg"]', true, 'approved', 4, NOW());

-- Insert test orders
INSERT INTO orders (item_id, buyer_id, status, payment_id, payment_provider, created_at) VALUES
(1, 1, 'paid', 'pay_123456789', 'stripe', NOW()),
(3, 2, 'shipped', 'pay_987654321', 'yookassa', NOW());

-- Insert test support tickets
INSERT INTO support_tickets (user_id, subject, message, category, order_id, status, created_at) VALUES
(1, 'Question about delivery', 'When will my item be delivered?', 'delivery', 1, 'resolved', NOW()),
(2, 'Issue with payment', 'I was charged twice for my purchase', 'payment', 2, 'in_progress', NOW());