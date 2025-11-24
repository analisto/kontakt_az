# Financial Analyst Telegram Bot

A hybrid Telegram bot that combines pre-generated analytics insights with AI-powered chat capabilities using Google's Gemini API. Works with the `demo_bank` PostgreSQL schema.

## Features

### Analytics Features
- Account balance overview
- Transaction trends and patterns
- Spending breakdown by transaction type
- Monthly financial summaries
- Top transactions analysis
- Interactive charts and visualizations

### AI Chat Features
- Natural conversation with Gemini AI
- Context-aware financial advice
- Integration with your financial data
- Persistent chat history
- Smart detection of financial queries

## Quick Start with Docker (Recommended)

### Prerequisites
- Docker and Docker Compose installed
- Telegram Bot Token
- Google Gemini API Key
- PostgreSQL database with `demo_bank` schema

### Setup

1. **Configure environment variables**

Edit `.env` file:
```env
DATABASE_URL="postgresql://user:password@host:port/database"
TELEGRAM_BOT_TOKEN="your_bot_token"
GEMINI_API_KEY="your_gemini_api_key"
ADMIN_USER_IDS=""
```

2. **Deploy the bot**

```bash
# Make deploy script executable (first time only)
chmod +x deploy.sh

# Deploy
./deploy.sh
```

3. **Bot is now running!** Open Telegram and send `/start` to your bot.

### Docker Commands

```bash
# View logs
docker-compose logs -f

# Stop bot
docker-compose down

# Restart bot
docker-compose restart

# Rebuild and restart
docker-compose up -d --build
```

## Manual Setup (Without Docker)

### Prerequisites
- Python 3.11 or higher
- PostgreSQL database with `demo_bank` schema
- Telegram Bot Token
- Google Gemini API Key

### Installation

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Test setup
python test_bot.py

# Run bot
python bot.py
```

## Getting API Keys

### Telegram Bot Token
1. Open Telegram and search for `@BotFather`
2. Send `/newbot` and follow the instructions
3. Copy the token provided

### Gemini API Key
1. Visit https://makersuite.google.com/app/apikey
2. Create a new API key
3. Copy the key

## Database Schema

The bot uses the existing `demo_bank` PostgreSQL schema with the following tables:

- **customers** - Bank customer information and account details
- **transactions** - Financial transactions (deposits, withdrawals, transfers, loan payments)
- **loans** - Loan information
- **telegram_users** - Bot users (created automatically)
- **chat_history** - Conversation history (created automatically)

See `database/DEMO_BANK_DOCUMENTATION.md` for complete schema documentation.

## Bot Commands

### General Commands
- `/start` - Start the bot and see welcome message
- `/help` - Display all available commands

### Analytics Commands
- `/analytics` - Open interactive analytics dashboard
- `/summary` - Get quick monthly financial summary
- `/balance` - View account balance overview
- `/spending` - See spending breakdown by type
- `/trends` - View transaction trends
- `/top` - See top transactions

### Chat Commands
- `/chat` - Activate chat mode
- `/ask [question]` - Ask a specific question
- `/clear` - Clear chat history

## Usage Examples

### Analytics Dashboard
```
1. Send /analytics
2. Click any button to view insights
3. Receive charts and detailed breakdowns
```

### AI Chat
```
You: How much did I spend this month?
Bot: Based on your data, you spent $X this month on...

You: What's a good savings strategy?
Bot: Here are some strategies based on your current financial situation...
```

### Data-Aware Queries
The bot automatically detects financial questions and includes your actual data in the AI conversation.

## Project Structure

```
analyst_in_pocket/
├── bot.py                   # Main bot application
├── config.py                # Configuration management
├── requirements.txt         # Python dependencies
├── test_bot.py             # Test script
├── deploy.sh               # Docker deployment script
├── Dockerfile              # Docker image definition
├── docker-compose.yml      # Docker Compose configuration
│
├── database/               # Database layer
│   ├── connection.py       # Database connection handler
│   ├── models.py           # SQLAlchemy models
│   └── DEMO_BANK_DOCUMENTATION.md  # Schema documentation
│
├── analytics/              # Analytics engine
│   ├── insights.py         # Analytics insights generation
│   └── charts.py           # Chart generation
│
└── chatbot/                # AI chatbot
    └── gemini_client.py    # Gemini API integration
```

## Analytics Available

1. **Monthly Summary**
   - Total income (deposits, transfers in, etc.)
   - Total expenses (withdrawals, payments, fees)
   - Net savings
   - Transaction count

2. **Account Overview**
   - Total balance across all accounts
   - Individual account balances
   - Account types (checking, savings, business, investment)

3. **Spending Analysis**
   - Breakdown by transaction type
   - Pie chart visualization
   - Top spending categories

4. **Transaction Trends**
   - Daily transaction patterns
   - 30-day trends by type
   - Income vs. expenses over time

5. **Balance Trends**
   - Daily balance changes
   - 30-day balance history

6. **Top Transactions**
   - Largest transactions by amount
   - Filter by type
   - With descriptions and dates

## Testing

Run the test script to verify everything is configured correctly:

```bash
python test_bot.py
```

The test checks:
- Configuration validation
- Database connectivity
- Analytics engine
- Chart generator
- Gemini chatbot
- Bot imports

## Development

### Adding New Analytics

1. Add method to `analytics/insights.py`:
```python
@staticmethod
def get_new_insight(days: int = 30) -> Dict[str, Any]:
    with get_session() as session:
        # Query database
        results = session.query(Transaction).filter(...).all()
        return {'data': results}
```

2. Add chart in `analytics/charts.py`:
```python
def create_new_chart(self, data: Dict) -> io.BytesIO:
    fig, ax = plt.subplots()
    # Create visualization
    return self._save_plot_to_bytes()
```

3. Add command handler in `bot.py`:
```python
async def new_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    data = AnalyticsEngine.get_new_insight()
    chart = chart_generator.create_new_chart(data)
    await update.message.reply_photo(photo=chart)
```

### Customizing AI Behavior

Edit `system_prompt` in `chatbot/gemini_client.py` to change the AI assistant's personality and behavior.

## Troubleshooting

### Database Connection Issues
```bash
# Test connection manually
python -c "from database import get_session; print('Connected!' if get_session() else 'Failed')"
```

### Bot Not Starting
- Check `.env` file exists and has all required variables
- Verify Telegram token is correct
- Check database is accessible
- Run `python test_bot.py` to diagnose issues

### Gemini API Errors
- Verify API key is valid
- Check quota limits at https://makersuite.google.com
- Ensure internet connectivity

### Docker Issues
```bash
# View detailed logs
docker-compose logs --tail=100 bot

# Check container status
docker-compose ps

# Restart with fresh build
docker-compose down && docker-compose up -d --build
```

## Security Best Practices

- Never commit `.env` file to version control
- Keep API keys secure and rotate regularly
- Use environment variables for all sensitive data
- Restrict admin commands to authorized users only
- Review chat history permissions

## Performance Tips

- The bot creates charts on-demand; larger datasets may take longer
- Chat history is stored in database; clear periodically if needed
- Database queries are optimized with indexes (see schema documentation)
- Docker deployment includes automatic restart on failure

## Deployment Options

### Option 1: Docker (Recommended)
```bash
./deploy.sh
```

### Option 2: Docker Compose
```bash
docker-compose up -d
```

### Option 3: Systemd Service (Linux)
```bash
# Create service file
sudo nano /etc/systemd/system/analyst-bot.service

# Enable and start
sudo systemctl enable analyst-bot
sudo systemctl start analyst-bot
```

### Option 4: Manual
```bash
python bot.py
```

## Monitoring

### View Logs
```bash
# Docker
docker-compose logs -f

# Manual
# Logs are printed to stdout
```

### Health Check
```bash
# Check if bot is responding
# Send /start command to bot in Telegram
```

## Contributing

To add features:
1. Create new branch
2. Add feature in appropriate module
3. Test with `python test_bot.py`
4. Update documentation
5. Submit pull request

## License

This project is provided as-is for educational and personal use.

## Support

For issues:
1. Run `python test_bot.py` to diagnose
2. Check logs for error messages
3. Verify all environment variables are set
4. Consult `database/DEMO_BANK_DOCUMENTATION.md` for schema details

## What's Next?

- Add more chart types (histogram, scatter plots)
- Implement spending predictions using ML
- Add budget tracking and alerts
- Create scheduled reports
- Multi-language support
- Export data to CSV/Excel
