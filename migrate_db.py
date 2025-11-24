"""Database migration script to fix telegram_id column type."""

import psycopg2
from config import Config

def migrate():
    """Migrate database to use BIGINT for telegram_id."""

    print("🔄 Starting database migration...")

    # Remove schema parameter for psycopg2
    db_url = Config.DATABASE_URL.replace('&schema=demo_bank', '')

    try:
        conn = psycopg2.connect(db_url)
        conn.autocommit = True
        cur = conn.cursor()

        print("✅ Connected to database")

        # Drop existing tables if they exist
        print("🗑️  Dropping old telegram_users and chat_history tables...")
        cur.execute("""
            DROP TABLE IF EXISTS demo_bank.chat_history CASCADE;
            DROP TABLE IF EXISTS demo_bank.telegram_users CASCADE;
        """)
        print("✅ Old tables dropped")

        # Create telegram_users table with BIGINT
        print("📋 Creating telegram_users table...")
        cur.execute("""
            CREATE TABLE demo_bank.telegram_users (
                id SERIAL PRIMARY KEY,
                telegram_id BIGINT UNIQUE NOT NULL,
                username VARCHAR(255),
                first_name VARCHAR(255),
                last_name VARCHAR(255),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_active TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        print("✅ telegram_users table created")

        # Create chat_history table with BIGINT
        print("📋 Creating chat_history table...")
        cur.execute("""
            CREATE TABLE demo_bank.chat_history (
                id SERIAL PRIMARY KEY,
                telegram_id BIGINT NOT NULL,
                role VARCHAR(50),
                message TEXT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        print("✅ chat_history table created")

        # Create indexes for better performance
        print("📊 Creating indexes...")
        cur.execute("""
            CREATE INDEX idx_telegram_users_telegram_id ON demo_bank.telegram_users(telegram_id);
            CREATE INDEX idx_chat_history_telegram_id ON demo_bank.chat_history(telegram_id);
            CREATE INDEX idx_chat_history_timestamp ON demo_bank.chat_history(timestamp);
        """)
        print("✅ Indexes created")

        cur.close()
        conn.close()

        print("\n" + "="*50)
        print("✅ Migration completed successfully!")
        print("="*50)
        print("\nYou can now run the bot:")
        print("  python bot.py")

    except Exception as e:
        print(f"\n❌ Migration failed: {e}")
        import traceback
        traceback.print_exc()
        return False

    return True

if __name__ == '__main__':
    migrate()
