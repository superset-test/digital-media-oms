-- Add orders and line items tables
-- Orders represent advertising campaigns with associated advertisers and optional agencies
-- Line items are the individual ad placements within an order

CREATE TABLE IF NOT EXISTS orders (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tenant_id UUID NOT NULL REFERENCES tenants(id) ON DELETE CASCADE,
    advertiser_id UUID NOT NULL REFERENCES advertisers(id) ON DELETE RESTRICT,
    agency_id UUID REFERENCES agencies(id) ON DELETE RESTRICT,
    order_number VARCHAR(50) UNIQUE NOT NULL,
    order_name VARCHAR(255) NOT NULL,
    status VARCHAR(50) DEFAULT 'draft',
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    total_amount NUMERIC(15, 2) DEFAULT 0.00,
    currency VARCHAR(3) DEFAULT 'USD',
    payment_terms VARCHAR(100),
    notes TEXT,
    created_by UUID NOT NULL REFERENCES users(id) ON DELETE RESTRICT,
    approved_by UUID REFERENCES users(id) ON DELETE SET NULL,
    approved_at TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT valid_order_dates CHECK (end_date >= start_date),
    CONSTRAINT valid_total CHECK (total_amount >= 0),
    CONSTRAINT unique_order_number UNIQUE (order_number)
);

-- Create indexes on orders
CREATE INDEX idx_orders_tenant_id ON orders(tenant_id);
CREATE INDEX idx_orders_advertiser_id ON orders(advertiser_id);
CREATE INDEX idx_orders_agency_id ON orders(agency_id);
CREATE INDEX idx_orders_order_number ON orders(order_number);
CREATE INDEX idx_orders_status ON orders(tenant_id, status);
CREATE INDEX idx_orders_dates ON orders(tenant_id, start_date, end_date);

-- Apply updated_at trigger to orders table
CREATE TRIGGER update_orders_updated_at
    BEFORE UPDATE ON orders
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- Create line items table
CREATE TABLE IF NOT EXISTS line_items (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tenant_id UUID NOT NULL REFERENCES tenants(id) ON DELETE CASCADE,
    order_id UUID NOT NULL REFERENCES orders(id) ON DELETE CASCADE,
    ad_unit_id UUID NOT NULL REFERENCES ad_units(id) ON DELETE RESTRICT,
    rate_card_id UUID REFERENCES rate_cards(id) ON DELETE SET NULL,
    line_number INTEGER NOT NULL,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    quantity INTEGER NOT NULL DEFAULT 1,
    unit_price NUMERIC(15, 2) NOT NULL,
    discount_percentage NUMERIC(5, 2) DEFAULT 0.00,
    subtotal NUMERIC(15, 2) NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    status VARCHAR(50) DEFAULT 'pending',
    delivered_quantity INTEGER DEFAULT 0,
    notes TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT valid_line_item_dates CHECK (end_date >= start_date),
    CONSTRAINT valid_quantity CHECK (quantity > 0),
    CONSTRAINT valid_unit_price CHECK (unit_price >= 0),
    CONSTRAINT valid_discount CHECK (discount_percentage >= 0 AND discount_percentage <= 100),
    CONSTRAINT valid_subtotal CHECK (subtotal >= 0),
    CONSTRAINT valid_delivered CHECK (delivered_quantity >= 0),
    CONSTRAINT unique_line_number_per_order UNIQUE (order_id, line_number)
);

-- Create indexes on line_items
CREATE INDEX idx_line_items_tenant_id ON line_items(tenant_id);
CREATE INDEX idx_line_items_order_id ON line_items(order_id);
CREATE INDEX idx_line_items_ad_unit_id ON line_items(ad_unit_id);
CREATE INDEX idx_line_items_dates ON line_items(order_id, start_date, end_date);

-- Apply updated_at trigger to line_items table
CREATE TRIGGER update_line_items_updated_at
    BEFORE UPDATE ON line_items
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();
