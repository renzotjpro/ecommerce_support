-- ============================================
-- E-COMMERCE SUPPORT DATABASE SCHEMA
-- Complete SQL Schema for Supabase PostgreSQL
-- ============================================

-- ============================================
-- 1. CUSTOMERS TABLE
-- ============================================
CREATE TABLE IF NOT EXISTS customers (
    id SERIAL PRIMARY KEY,
    customer_id VARCHAR(100) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    name VARCHAR(255) NOT NULL,
    phone VARCHAR(50),
    address TEXT,
    city VARCHAR(100),
    state VARCHAR(100),
    postal_code VARCHAR(20),
    country VARCHAR(100) DEFAULT 'USA',
    is_active BOOLEAN DEFAULT TRUE,
    loyalty_points INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Add comments for documentation
COMMENT ON TABLE customers IS 'Stores customer information and profiles';
COMMENT ON COLUMN customers.customer_id IS 'Unique customer identifier used in the application';
COMMENT ON COLUMN customers.loyalty_points IS 'Customer loyalty/reward points';

-- ============================================
-- 2. INVENTORY TABLE
-- ============================================
CREATE TABLE IF NOT EXISTS inventory (
    id SERIAL PRIMARY KEY,
    product_id VARCHAR(100) UNIQUE NOT NULL,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    price DECIMAL(10, 2) NOT NULL CHECK (price >= 0),
    category VARCHAR(100),
    stock_quantity INTEGER DEFAULT 0 CHECK (stock_quantity >= 0),
    reserved_quantity INTEGER DEFAULT 0 CHECK (reserved_quantity >= 0),
    low_stock_threshold INTEGER DEFAULT 10,
    sku VARCHAR(100) UNIQUE,
    brand VARCHAR(100),
    weight_kg DECIMAL(8, 2),
    dimensions VARCHAR(100),
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Add comments
COMMENT ON TABLE inventory IS 'Product inventory and stock management';
COMMENT ON COLUMN inventory.reserved_quantity IS 'Stock reserved during checkout process';
COMMENT ON COLUMN inventory.low_stock_threshold IS 'Alert threshold for low stock notifications';

-- ============================================
-- 3. ORDERS TABLE
-- ============================================
CREATE TABLE IF NOT EXISTS orders (
    id SERIAL PRIMARY KEY,
    order_id VARCHAR(100) UNIQUE NOT NULL,
    customer_id VARCHAR(100) NOT NULL,
    items JSONB NOT NULL,
    total DECIMAL(10, 2) NOT NULL CHECK (total >= 0),
    subtotal DECIMAL(10, 2),
    tax DECIMAL(10, 2) DEFAULT 0,
    shipping_cost DECIMAL(10, 2) DEFAULT 0,
    discount DECIMAL(10, 2) DEFAULT 0,
    status VARCHAR(50) DEFAULT 'pending',
    payment_status VARCHAR(50) DEFAULT 'pending',
    payment_method VARCHAR(50),
    tracking_number VARCHAR(100),
    carrier VARCHAR(50),
    expected_delivery DATE,
    shipped_date TIMESTAMP,
    delivered_date TIMESTAMP,
    notes TEXT,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id) ON DELETE CASCADE
);

-- Add check constraint for valid order status
ALTER TABLE orders ADD CONSTRAINT valid_order_status 
CHECK (status IN ('pending', 'processing', 'shipped', 'delivered', 'cancelled', 'refunded'));

ALTER TABLE orders ADD CONSTRAINT valid_payment_status
CHECK (payment_status IN ('pending', 'paid', 'failed', 'refunded', 'partial_refund'));

-- Add comments
COMMENT ON TABLE orders IS 'Customer orders and order history';
COMMENT ON COLUMN orders.items IS 'JSON array of order items with product details';
COMMENT ON COLUMN orders.status IS 'Order fulfillment status';
COMMENT ON COLUMN orders.payment_status IS 'Payment processing status';

-- ============================================
-- 4. REFUNDS TABLE
-- ============================================
CREATE TABLE IF NOT EXISTS refunds (
    id SERIAL PRIMARY KEY,
    refund_id VARCHAR(100) UNIQUE,
    order_id VARCHAR(100) NOT NULL,
    amount DECIMAL(10, 2) NOT NULL CHECK (amount >= 0),
    reason TEXT,
    status VARCHAR(50) DEFAULT 'pending',
    refund_method VARCHAR(50),
    processed_by VARCHAR(100),
    approved_date TIMESTAMP,
    completed_date TIMESTAMP,
    created_at TIMESTAMP DEFAULT NOW(),
    FOREIGN KEY (order_id) REFERENCES orders(order_id) ON DELETE CASCADE
);

-- Add check constraint for valid refund status
ALTER TABLE refunds ADD CONSTRAINT valid_refund_status
CHECK (status IN ('pending', 'approved', 'processing', 'completed', 'rejected'));

-- Add comments
COMMENT ON TABLE refunds IS 'Refund requests and processing';
COMMENT ON COLUMN refunds.status IS 'Current status of refund request';

-- ============================================
-- 5. RESERVATIONS TABLE
-- ============================================
CREATE TABLE IF NOT EXISTS reservations (
    id SERIAL PRIMARY KEY,
    product_id VARCHAR(100) NOT NULL,
    customer_id VARCHAR(100) NOT NULL,
    quantity INTEGER NOT NULL CHECK (quantity > 0),
    status VARCHAR(50) DEFAULT 'active',
    order_id VARCHAR(100),
    expires_at TIMESTAMP NOT NULL,
    created_at TIMESTAMP DEFAULT NOW(),
    released_at TIMESTAMP,
    FOREIGN KEY (product_id) REFERENCES inventory(product_id) ON DELETE CASCADE,
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id) ON DELETE CASCADE,
    FOREIGN KEY (order_id) REFERENCES orders(order_id) ON DELETE SET NULL
);

-- Add check constraint for valid reservation status
ALTER TABLE reservations ADD CONSTRAINT valid_reservation_status
CHECK (status IN ('active', 'completed', 'released', 'expired'));

-- Add comments
COMMENT ON TABLE reservations IS 'Temporary stock reservations during checkout';
COMMENT ON COLUMN reservations.expires_at IS 'Reservation expires after 15 minutes';

-- ============================================
-- 6. STOCK MOVEMENTS TABLE (Audit Trail)
-- ============================================
CREATE TABLE IF NOT EXISTS stock_movements (
    id SERIAL PRIMARY KEY,
    product_id VARCHAR(100) NOT NULL,
    quantity_change INTEGER NOT NULL,
    reason VARCHAR(255),
    movement_type VARCHAR(50),
    previous_stock INTEGER,
    new_stock INTEGER,
    reference_id VARCHAR(100),
    performed_by VARCHAR(100),
    timestamp TIMESTAMP DEFAULT NOW(),
    FOREIGN KEY (product_id) REFERENCES inventory(product_id) ON DELETE CASCADE
);

-- Add check constraint for valid movement types
ALTER TABLE stock_movements ADD CONSTRAINT valid_movement_type
CHECK (movement_type IN ('sale', 'return', 'restock', 'adjustment', 'damage', 'reservation', 'release'));

-- Add comments
COMMENT ON TABLE stock_movements IS 'Audit log of all inventory changes';
COMMENT ON COLUMN stock_movements.movement_type IS 'Type of stock movement';
COMMENT ON COLUMN stock_movements.reference_id IS 'Reference to order_id or other related entity';

-- ============================================
-- 7. CONVERSATIONS TABLE
-- ============================================
CREATE TABLE IF NOT EXISTS conversations (
    id SERIAL PRIMARY KEY,
    customer_id VARCHAR(100) NOT NULL,
    message TEXT NOT NULL,
    role VARCHAR(50) NOT NULL,
    agent_name VARCHAR(100),
    sentiment VARCHAR(50),
    timestamp TIMESTAMP DEFAULT NOW(),
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id) ON DELETE CASCADE
);

-- Add check constraint for valid roles
ALTER TABLE conversations ADD CONSTRAINT valid_conversation_role
CHECK (role IN ('user', 'assistant', 'system', 'triage', 'billing', 'support', 'inventory'));

-- Add comments
COMMENT ON TABLE conversations IS 'Customer conversation history with support agents';
COMMENT ON COLUMN conversations.role IS 'Message sender role (user/assistant/agent)';
COMMENT ON COLUMN conversations.agent_name IS 'Name of the agent that handled the message';

-- ============================================
-- 8. PRODUCT CATEGORIES TABLE (Optional)
-- ============================================
CREATE TABLE IF NOT EXISTS product_categories (
    id SERIAL PRIMARY KEY,
    category_name VARCHAR(100) UNIQUE NOT NULL,
    description TEXT,
    parent_category VARCHAR(100),
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Add comments
COMMENT ON TABLE product_categories IS 'Product category definitions';

-- ============================================
-- INDEXES FOR PERFORMANCE
-- ============================================

-- Customers indexes
CREATE INDEX IF NOT EXISTS idx_customers_email ON customers(email);
CREATE INDEX IF NOT EXISTS idx_customers_customer_id ON customers(customer_id);
CREATE INDEX IF NOT EXISTS idx_customers_created_at ON customers(created_at);

-- Inventory indexes
CREATE INDEX IF NOT EXISTS idx_inventory_product_id ON inventory(product_id);
CREATE INDEX IF NOT EXISTS idx_inventory_category ON inventory(category);
CREATE INDEX IF NOT EXISTS idx_inventory_stock ON inventory(stock_quantity);
CREATE INDEX IF NOT EXISTS idx_inventory_sku ON inventory(sku);
CREATE INDEX IF NOT EXISTS idx_inventory_active ON inventory(is_active);

-- Orders indexes
CREATE INDEX IF NOT EXISTS idx_orders_order_id ON orders(order_id);
CREATE INDEX IF NOT EXISTS idx_orders_customer ON orders(customer_id);
CREATE INDEX IF NOT EXISTS idx_orders_status ON orders(status);
CREATE INDEX IF NOT EXISTS idx_orders_created_at ON orders(created_at);
CREATE INDEX IF NOT EXISTS idx_orders_tracking ON orders(tracking_number);

-- Refunds indexes
CREATE INDEX IF NOT EXISTS idx_refunds_order ON refunds(order_id);
CREATE INDEX IF NOT EXISTS idx_refunds_status ON refunds(status);
CREATE INDEX IF NOT EXISTS idx_refunds_created_at ON refunds(created_at);

-- Reservations indexes
CREATE INDEX IF NOT EXISTS idx_reservations_customer ON reservations(customer_id);
CREATE INDEX IF NOT EXISTS idx_reservations_product ON reservations(product_id);
CREATE INDEX IF NOT EXISTS idx_reservations_status ON reservations(status);
CREATE INDEX IF NOT EXISTS idx_reservations_expires ON reservations(expires_at);

-- Stock movements indexes
CREATE INDEX IF NOT EXISTS idx_stock_movements_product ON stock_movements(product_id);
CREATE INDEX IF NOT EXISTS idx_stock_movements_timestamp ON stock_movements(timestamp);
CREATE INDEX IF NOT EXISTS idx_stock_movements_type ON stock_movements(movement_type);

-- Conversations indexes
CREATE INDEX IF NOT EXISTS idx_conversations_customer ON conversations(customer_id);
CREATE INDEX IF NOT EXISTS idx_conversations_timestamp ON conversations(timestamp);
CREATE INDEX IF NOT EXISTS idx_conversations_role ON conversations(role);

-- ============================================
-- FUNCTIONS AND TRIGGERS
-- ============================================

-- Function to update 'updated_at' timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Trigger for customers table
CREATE TRIGGER update_customers_updated_at BEFORE UPDATE ON customers
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Trigger for inventory table
CREATE TRIGGER update_inventory_updated_at BEFORE UPDATE ON inventory
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Trigger for orders table
CREATE TRIGGER update_orders_updated_at BEFORE UPDATE ON orders
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- ============================================
-- INITIAL DATA - PRODUCT CATEGORIES
-- ============================================

INSERT INTO product_categories (category_name, description) VALUES
('Electronics', 'Electronic devices and gadgets'),
('Clothing', 'Apparel and fashion items'),
('Home & Kitchen', 'Home appliances and kitchen equipment'),
('Sports & Outdoors', 'Sports equipment and outdoor gear'),
('Books', 'Books and educational materials'),
('Toys & Games', 'Toys, games, and entertainment'),
('Health & Beauty', 'Health, beauty, and personal care products'),
('Automotive', 'Automotive parts and accessories')
ON CONFLICT (category_name) DO NOTHING;

-- ============================================
-- VIEWS FOR COMMON QUERIES
-- ============================================

-- View: Available inventory (excluding reserved stock)
CREATE OR REPLACE VIEW available_inventory AS
SELECT 
    product_id,
    name,
    category,
    price,
    stock_quantity,
    reserved_quantity,
    (stock_quantity - reserved_quantity) AS available_quantity,
    low_stock_threshold,
    CASE 
        WHEN (stock_quantity - reserved_quantity) <= 0 THEN 'Out of Stock'
        WHEN (stock_quantity - reserved_quantity) <= low_stock_threshold THEN 'Low Stock'
        ELSE 'In Stock'
    END AS stock_status
FROM inventory
WHERE is_active = TRUE;

-- View: Customer order summary
CREATE OR REPLACE VIEW customer_order_summary AS
SELECT 
    c.customer_id,
    c.name,
    c.email,
    COUNT(o.id) AS total_orders,
    SUM(o.total) AS total_spent,
    MAX(o.created_at) AS last_order_date
FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id
GROUP BY c.customer_id, c.name, c.email;

-- View: Low stock products
CREATE OR REPLACE VIEW low_stock_products AS
SELECT 
    product_id,
    name,
    category,
    (stock_quantity - reserved_quantity) AS available_quantity,
    low_stock_threshold,
    stock_quantity,
    reserved_quantity
FROM inventory
WHERE (stock_quantity - reserved_quantity) <= low_stock_threshold
  AND is_active = TRUE
ORDER BY available_quantity ASC;

-- ============================================
-- PERMISSIONS (Optional - for RLS)
-- ============================================

-- Enable Row Level Security (RLS) if needed
-- ALTER TABLE customers ENABLE ROW LEVEL SECURITY;
-- ALTER TABLE orders ENABLE ROW LEVEL SECURITY;
-- etc...

-- ============================================
-- COMPLETION MESSAGE
-- ============================================

DO $$
BEGIN
    RAISE NOTICE '✅ Database schema created successfully!';
    RAISE NOTICE 'Tables created: customers, inventory, orders, refunds, reservations, stock_movements, conversations, product_categories';
    RAISE NOTICE 'Indexes created for optimal performance';
    RAISE NOTICE 'Triggers added for automatic timestamp updates';
    RAISE NOTICE 'Views created for common queries';
    RAISE NOTICE '';
    RAISE NOTICE '📊 Next steps:';
    RAISE NOTICE '1. Run setup_inventory_data.py to populate sample products';
    RAISE NOTICE '2. Test the database with your Python application';
    RAISE NOTICE '3. Deploy to Hugging Face Spaces';
END $$;