-- Add placements and ad units tables
-- Placements represent advertising inventory (e.g., Digital Display, Print, Broadcast)
-- Ad Units are specific ad positions within placements

CREATE TABLE IF NOT EXISTS placements (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tenant_id UUID NOT NULL REFERENCES tenants(id) ON DELETE CASCADE,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    medium VARCHAR(50) NOT NULL,
    type VARCHAR(50),
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT unique_placement_name_per_tenant UNIQUE (tenant_id, name)
);

-- Create indexes on placements
CREATE INDEX idx_placements_tenant_id ON placements(tenant_id);
CREATE INDEX idx_placements_tenant_medium ON placements(tenant_id, medium);

-- Apply updated_at trigger to placements table
CREATE TRIGGER update_placements_updated_at
    BEFORE UPDATE ON placements
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- Create ad units table
CREATE TABLE IF NOT EXISTS ad_units (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tenant_id UUID NOT NULL REFERENCES tenants(id) ON DELETE CASCADE,
    placement_id UUID NOT NULL REFERENCES placements(id) ON DELETE CASCADE,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    dimensions VARCHAR(50),
    specifications JSONB DEFAULT '{}'::jsonb,
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT unique_ad_unit_name_per_placement UNIQUE (placement_id, name)
);

-- Create indexes on ad_units
CREATE INDEX idx_ad_units_tenant_id ON ad_units(tenant_id);
CREATE INDEX idx_ad_units_placement_id ON ad_units(placement_id);

-- Apply updated_at trigger to ad_units table
CREATE TRIGGER update_ad_units_updated_at
    BEFORE UPDATE ON ad_units
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();
