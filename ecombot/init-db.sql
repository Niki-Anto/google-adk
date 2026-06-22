-- Create schema
CREATE SCHEMA IF NOT EXISTS om;

-- om_order table
CREATE TABLE om.om_order (
    order_id      VARCHAR(50) PRIMARY KEY,
    offer         VARCHAR(255),
    status        VARCHAR(50),
    creation_date VARCHAR(20)
);

-- om_delivery table
CREATE TABLE om.om_delivery (
    delivery_id    VARCHAR(50),
    order_id       VARCHAR(50),
    status         VARCHAR(50),
    completed_date VARCHAR(20),
    scheduled_date VARCHAR(20)
);

-- Seed order data
INSERT INTO om.om_order (order_id, offer, status, creation_date) VALUES
('ORD-2026-00001', 'LG TV',                        'COMPLETED',  '2026-01-10'),
('ORD-2026-00002', 'Samsung Galaxy S25 128GB',      'PROCESSING', '2026-02-14'),
('ORD-2026-00003', 'iPhone 16 Pro 256GB',           'PENDING',    '2026-03-05'),
('ORD-2026-00004', 'Haier Washing Machine',         'CANCELLED',  '2026-04-20'),
('ORD-2026-00005', 'Xiaomi 14T 256GB + Case',       'SHIPPED',    '2026-05-30');

-- Seed delivery data
INSERT INTO om.om_delivery (delivery_id, order_id, status, completed_date, scheduled_date) VALUES
('DEL-2026-00001', 'ORD-2026-00001', 'DELIVERED',  '2026-01-13', '2026-01-12'),
('DEL-2026-00002', 'ORD-2026-00002', 'IN_TRANSIT', '',           '2026-02-17'),
('DEL-2026-00003', 'ORD-2026-00003', 'PENDING',    '',           '2026-03-08'),
('DEL-2026-00004', 'ORD-2026-00004', 'CANCELLED',  '',           '2026-04-23'),
('DEL-2026-00005', 'ORD-2026-00005', 'SHIPPED',    '',           '2026-06-02');
