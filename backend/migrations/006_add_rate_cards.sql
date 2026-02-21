-- Add rate cards table
-- Rate cards define pricing for ad units with effective dates

CREATE TABLE IF NOT EXISTS rate_cards (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tenant_id UUID NOT NULL REFERENCES tenants(id) ON DELETE CASCADE,
    ad_unit_id UUID NOT NULL REFERENCES ad_units(id) ON DELETE CASCADE,
    name VARCHAR(255) NOT NULL,
    effective_date DATE NOT NULL,
    expiration_date DATE,
    base_rate NUMERIC(15, 2) NOT NULL,
    currency VARCHAR(3) DEFAULT 'USD',
    rate_type VARCHAR(50) NOT NULL,
    minimum_quantity INTEGER DEFAULT 1,
    discount_percentage NUMERIC(5, 2) DEFAULT 0.00,
    notes TEXT,
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT valid_rate CHECK (base_rate >= 0),
    CONSTRAINT valid_discount CHECK (discount_percentage >= 0 AND discount_percentage <= 100),
    CONSTRAINT valid_date_range CHECK (expiration_date IS NULL OR expiration_date >= effective_date)
);

-- Create indexes on rate_cards
CREATE INDEX idx_rate_cards_tenant_id ON rate_cards(tenant_id);
CREATE INDEX idx_rate_cards_ad_unit_id ON rate_cards(ad_unit_id);
CREATE INDEX idx_rate_cards_effective_date ON rate_cards(ad_unit_id, effective_date);

-- Apply updated_at trigger to rate_cards table
CREATE TRIGGER update_rate_cards_updated_at
    BEFORE UPDATE ON rate_cards
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();
