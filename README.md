# Analyst in Pocket - Executive AI Business Intelligence

**Your trusted AI business advisor, always available in your pocket.**

A premium B2B SaaS solution that delivers real-time strategic insights to bank CEOs and executives through Telegram. Combines powerful analytics dashboards with an AI advisor powered by Google Gemini - all accessible through simple conversations.

## Features

### 💼 Executive Dashboard
- **Portfolio Overview** - Real-time assets under management across all accounts
- **Transaction Intelligence** - Pattern analysis and operational flow insights
- **Expenditure Analysis** - Strategic spending breakdown with percentages
- **Business Performance** - Revenue, costs, and net position tracking
- **High-Value Monitoring** - Track largest transactions instantly
- **Interactive Visualizations** - Professional charts generated on-demand

### 🤖 AI Business Advisor
- **Strategic Conversations** - Ask anything about your bank's performance in natural language
- **Data-Driven Insights** - AI analyzes your real operational data
- **Executive-Level Communication** - Answers focused on business impact, not technical details
- **Context-Aware Intelligence** - Remembers conversation history for deeper analysis
- **24/7 Availability** - Your trusted advisor always in your pocket
- **Group Support** - Multiple executives can access insights in team channels

### 🎯 Built for Executives
- No technical jargon - pure business intelligence
- Instant insights without data analyst dependency
- Mobile-first design for executives on the go
- Secure, private conversations per executive
- Real-time operational metrics

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

## How to Use

### 🚀 Getting Started

1. **Start the bot** - Send `/start` to your bot in Telegram
2. **Access the dashboard** - Use `/analytics` for interactive metrics
3. **Ask questions** - Just message the bot naturally with your strategic questions

### 💬 Using the AI Business Advisor

#### In Private Chats

Simply message the bot with any strategic question:

**Example Conversations:**

```
Executive: What are our growth opportunities?
Bot: Based on your current portfolio of $487K across 5 active accounts
with a positive net position of $11.2K this month, I identify three key
growth opportunities:

1. Customer acquisition potential - Current transaction volume shows
   capacity for 20-30% more active accounts
2. Loan portfolio expansion - Only $125K in active loans suggests
   untapped lending revenue
3. Fee optimization - Current fee structure could be adjusted to increase
   revenue by an estimated 8-12%

Recommendation: Focus on customer acquisition first to maximize
transaction volume before adjusting pricing.
```

```
Executive: Analyze our loan portfolio risk
Bot: Current loan portfolio analysis:

Portfolio Value: $125,450
Active Loans: 3 accounts
Avg Loan Size: $41,817

Risk Assessment: LOW-MODERATE
- Payment consistency: 100% on-time in last 90 days
- Portfolio concentration: Well-diversified across customer base
- Default indicators: None detected

Strategic recommendation: Portfolio health is strong. Consider expanding
lending operations given the low-risk performance.
```

```
Executive: Show me where we're losing money
Bot: Cost analysis reveals key expenditure areas:

Total Operating Costs: $4,067.56 this period

Breakdown:
1. Loan Payments: $3,567.56 (87.7%) - Major outflow
2. Withdrawals: $500.00 (12.3%) - Operational costs

Strategic insight: Loan servicing represents your largest expense at
nearly 88% of costs. This is within normal banking operations, but
consider:
- Refinancing opportunities to reduce interest burden
- Revenue diversification to offset loan servicing costs
- Fee income optimization to improve net margins

Current net position is positive, but margin improvement opportunity
exists through revenue growth rather than cost cutting.
```

#### In Group Chats (Executive Teams)

The bot responds when you mention it or reply to its messages:

**Method 1: Mention the bot**
```
@your_bot_username What's our transaction volume trend?
```
**Important:**
- Replace `@your_bot_username` with your actual bot's username (the one you set in BotFather)
- Mention detection is case-insensitive - `@MyBot` and `@mybot` both work
- To find your bot's username: Check the bot's profile in Telegram or look for the username in BotFather

**Method 2: Reply to bot's message**
```
Bot: [Shows business snapshot]
Executive: [Replies] Break down the revenue sources
Bot: [Provides detailed revenue analysis]
```

**Method 3: Use /ask command**
```
/ask What customer segments are most profitable?
```

**Note:** Analytics are shared with the group, but each executive has private AI conversation history.

### 📊 Using the Executive Dashboard

#### Access the Dashboard
```
/analytics
```

This opens an interactive menu with these intelligence options:

1. **📊 Business Snapshot** - Monthly performance overview
   - Revenue vs operating costs
   - Net position with strategic assessment
   - Transaction volume metrics

2. **💼 Portfolio Overview** - Assets under management
   - Total portfolio value
   - Account breakdown by type
   - Customer distribution

3. **💸 Expenditure Analysis** - Where money flows out
   - Visual pie chart of spending categories
   - Percentage breakdown
   - Top cost centers

4. **📈 Transaction Patterns** - 90-day operational trends
   - Transaction flow over time
   - Type-based analysis
   - Seasonal patterns

5. **🎯 High-Value Transactions** - Top 10 by amount
   - Visual chart ranking
   - Transaction details
   - Type classification (revenue vs expense)

6. **📉 Portfolio Trend** - 90-day asset trajectory
   - Daily balance evolution
   - Growth/decline patterns
   - Performance tracking

#### Quick Commands

Skip the menu and get insights directly:

```
/summary   - Instant business performance snapshot
/balance   - Portfolio overview
/spending  - Expenditure analysis with charts
/trends    - Transaction pattern analysis
/top       - High-value transaction review
```

### 💡 Strategic Question Examples

**Growth & Revenue:**
- "What revenue opportunities exist in our current data?"
- "How can we increase profitability?"
- "Which customer segments should we focus on?"
- "What's our customer acquisition trend?"

**Risk Management:**
- "Analyze our portfolio risk exposure"
- "What are our default indicators?"
- "Show me concerning transaction patterns"
- "Evaluate loan portfolio health"

**Operational Efficiency:**
- "Where can we reduce costs without impacting service?"
- "What's our operational efficiency trend?"
- "Are we optimizing fee structures?"
- "Compare revenue vs expenses trend"

**Market Intelligence:**
- "What do transaction patterns tell us about customer behavior?"
- "Identify seasonal trends in our operations"
- "What's our competitive positioning based on these metrics?"
- "Forecast next quarter based on current trends"

### 🔄 Managing Conversations

**Clear conversation history:**
```
/clear
```
This resets the AI's memory of your conversation, useful when switching topics.

**Get your Executive ID:**
```
/myid
```
Shows your unique identifier for system administration.

**View all capabilities:**
```
/help
```

## Bot Commands Reference

### 🎯 Executive Commands
- `/start` - Welcome brief and bot introduction
- `/help` - Complete command reference and capabilities
- `/myid` - Display your Executive ID for system access

### 📊 Strategic Intelligence Commands
- `/analytics` - Interactive executive dashboard with all metrics
- `/summary` - Instant business performance snapshot (revenue, costs, net position)
- `/balance` - Portfolio overview (assets under management, account breakdown)
- `/spending` - Expenditure analysis with visual charts and percentages
- `/trends` - Transaction pattern analysis (90-day operational flow)
- `/top` - High-value transaction review (top 10 by amount)

### 💼 AI Advisor Commands
- `/chat` - Activate AI business advisor mode
- `/ask [question]` - Direct strategic inquiry (e.g., `/ask What are our growth opportunities?`)
- `/clear` - Reset conversation context

## Real-World Use Cases

### 📱 CEO on the Go
**Scenario:** CEO traveling to board meeting needs quick portfolio update

```
CEO: /summary
Bot: [Delivers business snapshot in 30 seconds]

CEO: What should I highlight to the board?
Bot: Focus on three key strengths:
1. Strong net position of $11.2K (up 15% from last period)
2. Portfolio growth to $487K across diversified accounts
3. Zero default indicators in loan portfolio

Opportunity area to address: Loan portfolio at only 25% of capacity
suggests untapped lending revenue potential.
```

### 👥 Executive Team Strategy Session
**Scenario:** Leadership team discussing Q4 strategy in group chat

```
CFO: @your_bot_username Show expenditure breakdown
Bot: [Sends chart and analysis showing 87.7% in loan servicing]

CEO: [Replies to bot] How does this compare to revenue?
Bot: Current revenue covers loan servicing with 35% margin for operations.
This is healthy but below industry standard of 45-50%. Consider...

COO: @your_bot_username What operational efficiencies can improve margins?
Bot: [Provides detailed efficiency analysis]
```

### 📈 Quick Decision Support
**Scenario:** CFO needs risk assessment before approving new loans

```
CFO: Analyze our current loan portfolio risk
Bot: [Delivers comprehensive risk analysis with payment patterns,
concentration metrics, and strategic recommendations]

CFO: What's our capacity for additional loans?
Bot: Based on current portfolio health (100% payment consistency) and
capital position, you have capacity for $350K-$400K in additional
lending without exceeding prudent risk thresholds.
```

### 🎯 Performance Monitoring
**Scenario:** Daily check on business metrics during coffee

```
Executive: Good morning, show me yesterday's highlights
Bot: [Delivers key metrics from previous day's activity]

Executive: Any concerning patterns?
Bot: [AI analyzes recent trends and flags any anomalies]
```

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

## Strategic Intelligence Available

### 1. 💼 Business Performance Dashboard
**What it shows:**
- Revenue (deposits, transfers in, loan disbursements, interest credits, refunds)
- Operating Expenses (withdrawals, transfers out, loan payments, fees)
- Net Position (positive = growth, negative = optimization opportunity)
- Transaction Volume (operational activity indicator)

**Strategic Value:** Understand overall business health and cash flow position at a glance

### 2. 🏦 Portfolio Intelligence
**What it shows:**
- Total Assets Under Management across all customer accounts
- Account distribution by type (checking, savings, business, investment)
- Individual account performance breakdown
- Customer portfolio composition

**Strategic Value:** Monitor total capital position and portfolio diversification

### 3. 💸 Expenditure Intelligence
**What it shows:**
- Operating cost breakdown by category
- Visual pie chart for quick pattern recognition
- Percentage distribution showing where money flows
- Top cost centers requiring attention

**Strategic Value:** Identify cost optimization opportunities and spending patterns

### 4. 📈 Transaction Pattern Analysis
**What it shows:**
- 90-day transaction flow trends
- Revenue vs expense patterns over time
- Type-based transaction analysis
- Seasonal and cyclical patterns

**Strategic Value:** Predict future performance and identify operational trends

### 5. 📊 Portfolio Performance Tracking
**What it shows:**
- Daily balance evolution over 90 days
- Growth trajectory visualization
- Peak and trough identification
- Performance momentum indicators

**Strategic Value:** Monitor capital growth and identify inflection points

### 6. 🎯 High-Value Transaction Intelligence
**What it shows:**
- Top 10 largest transactions by amount
- Transaction type classification (revenue/expense)
- Detailed descriptions and dates
- Visual ranking chart

**Strategic Value:** Monitor significant capital movements and major business events

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

The AI advisor's communication style and expertise can be customized by editing the `system_prompt` in `chatbot/gemini_client.py:21-39`.

**Current configuration:**
- Executive-level strategic communication
- Focus on business impact over technical details
- Data-driven recommendations with actionable insights
- Professional, confident tone suitable for C-suite

**To customize:**
```python
self.system_prompt = """Your custom advisor personality here..."""
```

**Example customizations:**
- Adjust formality level
- Add industry-specific expertise
- Change focus areas (risk vs growth vs efficiency)
- Modify recommendation style

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

## Strategic Roadmap

### 🚀 Coming Soon

**Enhanced Predictive Analytics**
- ML-powered revenue forecasting
- Risk prediction models
- Customer behavior predictions
- Market trend analysis

**Executive Reporting**
- Scheduled automated reports (daily/weekly/monthly)
- Custom KPI dashboards
- Board presentation exports (PDF/PowerPoint)
- Excel/CSV data exports for deeper analysis

**Advanced Intelligence**
- Competitor benchmarking
- Multi-bank portfolio management
- Real-time alerts for critical metrics
- Custom threshold notifications

**Enterprise Features**
- Role-based access control
- Multi-language support for global operations
- White-label deployment options
- Integration with other banking systems

**Enhanced Visualizations**
- Interactive drill-down charts
- Comparison views (YoY, MoM)
- Customizable dashboard layouts
- Real-time metric streaming

## Why Choose Analyst in Pocket?

### 💎 Value Proposition

**For Bank CEOs:**
- **Instant Intelligence** - Strategic insights in seconds, not hours
- **Always Available** - Your AI advisor works 24/7, wherever you are
- **No Technical Barrier** - Business language, not IT jargon
- **Data-Driven Confidence** - Make decisions backed by real data
- **Cost Efficient** - Fraction of the cost of hiring a full-time analyst

**Business Impact:**
- ⏱️ **Save 10+ hours/week** on data analysis and reporting
- 📊 **Make faster decisions** with instant access to insights
- 💰 **Identify revenue opportunities** hidden in your data
- 🎯 **Reduce risk** with continuous portfolio monitoring
- 📈 **Improve margins** through data-driven optimization

**Technical Excellence:**
- 🔒 **Secure** - Private conversations, encrypted connections
- ⚡ **Fast** - Sub-second response times for most queries
- 🎨 **Professional** - Executive-quality charts and reports
- 🔄 **Real-time** - Always synced with your latest data
- 📱 **Mobile-First** - Designed for executives on the move

### 🎯 Perfect For

- Bank CEOs and C-Suite Executives
- Financial Institution Leadership Teams
- Board Members requiring quick insights
- CFOs and Financial Controllers
- Risk Management Officers
- Operations Directors

### 💼 Use It For

- Board meeting preparation
- Daily performance monitoring
- Strategic planning sessions
- Risk assessment reviews
- Investor presentations
- Quarterly business reviews
- Ad-hoc analysis requests
