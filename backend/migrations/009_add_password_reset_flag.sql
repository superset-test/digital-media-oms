-- Add password reset requirement flag
-- This migration adds must_change_password column for forcing password reset on first login

-- Add must_change_password column to users table
ALTER TABLE users ADD COLUMN IF NOT EXISTS must_change_password BOOLEAN DEFAULT false;

-- Create index for users who must change password
CREATE INDEX IF NOT EXISTS idx_users_must_change_password 
    ON users(must_change_password) WHERE must_change_password = true;

-- Add comment for documentation
COMMENT ON COLUMN users.must_change_password IS 'User must change password on next login (e.g., after invitation)';
