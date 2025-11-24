#!/bin/bash

# Startup script for the bot - handles migration and startup

set -e

echo "🚀 Starting Analyst Bot..."

# Check if migration is needed
echo "🔍 Checking database..."
python -c "
from database import get_session
from database.models import TelegramUser
try:
    with get_session() as session:
        session.query(TelegramUser).first()
    print('✅ Database ready')
except Exception as e:
    if 'does not exist' in str(e) or 'relation' in str(e).lower():
        print('⚠️  Tables not found, running migration...')
        import subprocess
        subprocess.run(['python', 'migrate_db.py'], check=True)
    else:
        print(f'⚠️  Database issue: {e}')
        print('Running migration to be safe...')
        import subprocess
        subprocess.run(['python', 'migrate_db.py'], check=True)
"

# Start the bot
echo "▶️  Starting bot..."
python bot.py
