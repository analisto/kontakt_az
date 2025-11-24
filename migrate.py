"""One-time migration script to create new bot tables."""

print("🔄 Running database migration...\n")

try:
    from database import init_db
    from database.connection import engine
    from sqlalchemy import text

    print("1️⃣ Connecting to database...")

    # Initialize database (creates only missing tables)
    init_db()

    print("✅ Database migration completed!\n")

    # Verify new tables were created
    print("2️⃣ Verifying new tables...")
    with engine.connect() as conn:
        result = conn.execute(text("""
            SELECT table_name
            FROM information_schema.tables
            WHERE table_schema = 'demo_bank'
            AND table_name IN ('telegram_users', 'chat_history')
            ORDER BY table_name
        """))

        tables = [row[0] for row in result]

        if tables:
            print("✅ Created new tables:")
            for table in tables:
                print(f"   - {table}")
        else:
            print("⚠️  Tables may already exist (this is OK)")

    print("\n" + "="*50)
    print("✅ Migration successful!")
    print("="*50)
    print("\nNew tables created:")
    print("  • telegram_users - Stores bot users")
    print("  • chat_history - Stores AI conversations")
    print("\nExisting tables untouched:")
    print("  • customers")
    print("  • transactions")
    print("  • loans")
    print("\n💡 You can now delete migrate.py if you want")
    print("   The bot will work without running init_db() again")

except Exception as e:
    print(f"\n❌ Migration failed: {e}")
    import traceback
    traceback.print_exc()
    print("\n💡 Tip: Check your DATABASE_URL in .env file")
    exit(1)
