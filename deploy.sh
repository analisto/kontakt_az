#!/bin/bash

# Deployment script for Analyst in Pocket Telegram Bot

set -e

echo "🚀 Deploying Analyst in Pocket Bot..."

# Check if .env file exists
if [ ! -f .env ]; then
    echo "❌ Error: .env file not found!"
    echo "Please create .env file with required environment variables."
    exit 1
fi

# Check required environment variables
echo "✅ Checking environment variables..."
source .env

if [ -z "$TELEGRAM_BOT_TOKEN" ]; then
    echo "❌ Error: TELEGRAM_BOT_TOKEN not set in .env"
    exit 1
fi

if [ -z "$GEMINI_API_KEY" ]; then
    echo "❌ Error: GEMINI_API_KEY not set in .env"
    exit 1
fi

if [ -z "$DATABASE_URL" ]; then
    echo "❌ Error: DATABASE_URL not set in .env"
    exit 1
fi

echo "✅ Environment variables configured"

# Build Docker image
echo "🔨 Building Docker image..."
docker-compose build

# Stop existing container if running
echo "🛑 Stopping existing container (if any)..."
docker-compose down || true

# Start the bot
echo "▶️  Starting bot..."
docker-compose up -d

# Show logs
echo "📋 Bot logs:"
docker-compose logs --tail=50 -f

# Deployment complete
echo ""
echo "✅ Deployment complete!"
echo "To view logs: docker-compose logs -f"
echo "To stop bot: docker-compose down"
echo "To restart bot: docker-compose restart"
