-- Add multi-tenancy support
-- This migration adds tenants table and updates users to be tenant-scoped

-- Create tenants table
CREATE TABLE IF NOT EXISTS tenants (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255) NOT NULL,
    slug VARCHAR(100) UNIQUE NOT NULL,
    is_active BOOLEAN DEFAULT true,
    settings JSONB DEFAULT '{}'::jsonb,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes on tenants
CREATE INDEX idx_tenants_slug ON tenants(slug);
CREATE INDEX idx_tenants_active ON tenants(is_active) WHERE is_active = true;

-- Apply updated_at trigger to tenants table
CREATE TRIGGER update_tenants_updated_at
    BEFORE UPDATE ON tenants
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- Create a default tenant for existing data
INSERT INTO tenants (name, slug, is_active)
VALUES ('Default Tenant', 'default', true)
ON CONFLICT (slug) DO NOTHING;

-- Add tenant_id column to users table
ALTER TABLE users ADD COLUMN IF NOT EXISTS tenant_id UUID;

-- Set tenant_id for existing users to the default tenant
UPDATE users
SET tenant_id = (SELECT id FROM tenants WHERE slug = 'default')
WHERE tenant_id IS NULL;

-- Make tenant_id NOT NULL and add foreign key constraint
ALTER TABLE users ALTER COLUMN tenant_id SET NOT NULL;
ALTER TABLE users ADD CONSTRAINT fk_users_tenant_id 
    FOREIGN KEY (tenant_id) REFERENCES tenants(id) ON DELETE CASCADE;

-- Add role column to users
ALTER TABLE users ADD COLUMN IF NOT EXISTS role VARCHAR(50) DEFAULT 'user';

-- Update existing admin users to have admin role
UPDATE users SET role = 'admin' WHERE is_super_admin = true;

-- Remove is_super_admin column (replaced by role system)
ALTER TABLE users DROP COLUMN IF EXISTS is_super_admin;

-- Create composite index for tenant-scoped email lookups
CREATE INDEX idx_users_tenant_email ON users(tenant_id, email);
CREATE INDEX idx_users_tenant_id ON users(tenant_id);

-- Drop the old unique email constraint and create a new one scoped to tenant
ALTER TABLE users DROP CONSTRAINT IF EXISTS users_email_key;
CREATE UNIQUE INDEX idx_users_tenant_email_unique ON users(tenant_id, email);
