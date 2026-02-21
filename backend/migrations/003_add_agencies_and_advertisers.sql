-- Add agencies and advertisers tables
-- These represent the core business entities in the ad management system

-- Create agencies table
CREATE TABLE IF NOT EXISTS agencies (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tenant_id UUID NOT NULL REFERENCES tenants(id) ON DELETE CASCADE,
    name VARCHAR(255) NOT NULL,
    address TEXT,
    city VARCHAR(100),
    state VARCHAR(100),
    postal_code VARCHAR(20),
    country VARCHAR(100),
    phone VARCHAR(50),
    email VARCHAR(255),
    website VARCHAR(255),
    notes TEXT,
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT unique_agency_name_per_tenant UNIQUE (tenant_id, name)
);

-- Create indexes on agencies
CREATE INDEX idx_agencies_tenant_id ON agencies(tenant_id);
CREATE INDEX idx_agencies_tenant_active ON agencies(tenant_id, is_active) WHERE is_active = true;

-- Apply updated_at trigger to agencies table
CREATE TRIGGER update_agencies_updated_at
    BEFORE UPDATE ON agencies
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- Create advertisers table
CREATE TABLE IF NOT EXISTS advertisers (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tenant_id UUID NOT NULL REFERENCES tenants(id) ON DELETE CASCADE,
    name VARCHAR(255) NOT NULL,
    industry VARCHAR(100),
    address TEXT,
    city VARCHAR(100),
    state VARCHAR(100),
    postal_code VARCHAR(20),
    country VARCHAR(100),
    phone VARCHAR(50),
    email VARCHAR(255),
    website VARCHAR(255),
    notes TEXT,
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT unique_advertiser_name_per_tenant UNIQUE (tenant_id, name)
);

-- Create indexes on advertisers
CREATE INDEX idx_advertisers_tenant_id ON advertisers(tenant_id);
CREATE INDEX idx_advertisers_tenant_active ON advertisers(tenant_id, is_active) WHERE is_active = true;

-- Apply updated_at trigger to advertisers table
CREATE TRIGGER update_advertisers_updated_at
    BEFORE UPDATE ON advertisers
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();
