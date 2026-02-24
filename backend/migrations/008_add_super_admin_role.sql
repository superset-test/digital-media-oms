-- Add super-admin support and system tenant
-- This migration adds super-admin functionality and a system tenant for super-admins

-- Create system tenant for super-admins
INSERT INTO tenants (name, slug, is_active, settings)
VALUES ('System', 'system', true, '{}'::jsonb)
ON CONFLICT (slug) DO NOTHING;

-- Add is_super_admin column to users table
ALTER TABLE users ADD COLUMN IF NOT EXISTS is_super_admin BOOLEAN DEFAULT false;

-- Add invited_by_user_id column for audit trail
ALTER TABLE users ADD COLUMN IF NOT EXISTS invited_by_user_id UUID;

-- Add foreign key constraint for invited_by_user_id
ALTER TABLE users ADD CONSTRAINT fk_users_invited_by 
    FOREIGN KEY (invited_by_user_id) REFERENCES users(id) ON DELETE SET NULL;

-- Create index on is_super_admin for fast lookup
CREATE INDEX IF NOT EXISTS idx_users_super_admin ON users(is_super_admin) WHERE is_super_admin = true;

-- Create index on invited_by_user_id for audit queries
CREATE INDEX IF NOT EXISTS idx_users_invited_by ON users(invited_by_user_id) WHERE invited_by_user_id IS NOT NULL;

-- Add check constraint: super-admins must have role = 'super_admin'
ALTER TABLE users ADD CONSTRAINT chk_super_admin_role 
    CHECK (is_super_admin = false OR role = 'super_admin');

-- Update existing admin users to have proper role
-- (Note: this doesn't make them super-admins, just standardizes the role field)
UPDATE users SET role = 'admin' WHERE role IN ('admin', 'manager');

-- Add comment for documentation
COMMENT ON COLUMN users.is_super_admin IS 'Super-admins have access to all tenants and can manage tenants';
COMMENT ON COLUMN users.invited_by_user_id IS 'User ID of the admin who invited/created this user';
