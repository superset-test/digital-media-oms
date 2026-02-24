-- Add contacts table
-- Contacts must be associated with either an agency OR an advertiser (but not both)

CREATE TABLE IF NOT EXISTS contacts (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tenant_id UUID NOT NULL REFERENCES tenants(id) ON DELETE CASCADE,
    agency_id UUID REFERENCES agencies(id) ON DELETE CASCADE,
    advertiser_id UUID REFERENCES advertisers(id) ON DELETE CASCADE,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    title VARCHAR(100),
    email VARCHAR(255) NOT NULL,
    phone VARCHAR(50),
    mobile VARCHAR(50),
    notes TEXT,
    is_primary BOOLEAN DEFAULT false,
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT contact_must_have_agency_or_advertiser 
        CHECK (
            (agency_id IS NOT NULL AND advertiser_id IS NULL) OR 
            (agency_id IS NULL AND advertiser_id IS NOT NULL)
        )
);

-- Create indexes on contacts
CREATE INDEX idx_contacts_tenant_id ON contacts(tenant_id);
CREATE INDEX idx_contacts_agency_id ON contacts(agency_id);
CREATE INDEX idx_contacts_advertiser_id ON contacts(advertiser_id);
CREATE INDEX idx_contacts_email ON contacts(email);

-- Apply updated_at trigger to contacts table
CREATE TRIGGER update_contacts_updated_at
    BEFORE UPDATE ON contacts
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();
