"""Create invite and notification tables."""
import sqlite3

db_path = 'data/research_platform.db'
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Create invites table
cursor.execute('''
CREATE TABLE IF NOT EXISTS invites (
    id TEXT PRIMARY KEY,
    code TEXT UNIQUE NOT NULL,
    workspace_id TEXT NOT NULL,
    created_by_id TEXT NOT NULL,
    accepted_by_id TEXT,
    role TEXT DEFAULT 'viewer',
    status TEXT DEFAULT 'pending',
    max_uses INTEGER DEFAULT 1,
    use_count INTEGER DEFAULT 0,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    expires_at DATETIME,
    accepted_at DATETIME,
    FOREIGN KEY (workspace_id) REFERENCES workspaces(id) ON DELETE CASCADE,
    FOREIGN KEY (created_by_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (accepted_by_id) REFERENCES users(id) ON DELETE SET NULL
)
''')

# Create notifications table
cursor.execute('''
CREATE TABLE IF NOT EXISTS notifications (
    id TEXT PRIMARY KEY,
    user_id TEXT NOT NULL,
    type TEXT DEFAULT 'system',
    title TEXT NOT NULL,
    message TEXT NOT NULL,
    link TEXT,
    workspace_id TEXT,
    document_id TEXT,
    from_user_id TEXT,
    is_read INTEGER DEFAULT 0,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    read_at DATETIME,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
)
''')

# Create indexes
cursor.execute('CREATE INDEX IF NOT EXISTS idx_invites_code ON invites(code)')
cursor.execute('CREATE INDEX IF NOT EXISTS idx_invites_workspace ON invites(workspace_id)')
cursor.execute('CREATE INDEX IF NOT EXISTS idx_notifications_user ON notifications(user_id)')
cursor.execute('CREATE INDEX IF NOT EXISTS idx_notifications_unread ON notifications(user_id, is_read)')

conn.commit()
conn.close()
print("Tables created successfully!")
