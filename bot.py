"""Main Telegram bot application."""

import logging
import os
from threading import Thread
from flask import Flask
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ContextTypes,
    filters
)

from config import Config
from database import get_session
from database.models import TelegramUser
from analytics import AnalyticsEngine, ChartGenerator
from chatbot import GeminiChatbot

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Initialize components
chatbot = GeminiChatbot()
chart_generator = ChartGenerator()

# Telegram message length limit
MAX_MESSAGE_LENGTH = 4096


def split_message(text: str, max_length: int = MAX_MESSAGE_LENGTH) -> list[str]:
    """Split a long message into chunks that fit Telegram's limit."""
    if len(text) <= max_length:
        return [text]

    chunks = []
    current_chunk = ""

    # Split by paragraphs first to maintain readability
    paragraphs = text.split('\n\n')

    for paragraph in paragraphs:
        # If adding this paragraph exceeds limit, save current chunk and start new one
        if len(current_chunk) + len(paragraph) + 2 > max_length:
            if current_chunk:
                chunks.append(current_chunk.strip())
                current_chunk = ""

            # If paragraph itself is too long, split it
            if len(paragraph) > max_length:
                # Split by lines first
                lines = paragraph.split('\n')
                for line in lines:
                    # If line is still too long, force split by character
                    if len(line) > max_length:
                        while len(line) > 0:
                            if current_chunk and len(current_chunk) + len(line) > max_length:
                                chunks.append(current_chunk.strip())
                                current_chunk = ""

                            # Take as much as we can
                            available_space = max_length - len(current_chunk) - 1
                            if available_space <= 0:
                                chunks.append(current_chunk.strip())
                                current_chunk = ""
                                available_space = max_length

                            current_chunk += line[:available_space]
                            line = line[available_space:]
                        current_chunk += '\n'
                    else:
                        if len(current_chunk) + len(line) + 1 > max_length:
                            if current_chunk:
                                chunks.append(current_chunk.strip())
                            current_chunk = line + '\n'
                        else:
                            current_chunk += line + '\n'
            else:
                current_chunk = paragraph + '\n\n'
        else:
            current_chunk += paragraph + '\n\n'

    if current_chunk.strip():
        chunks.append(current_chunk.strip())

    return chunks


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /start command."""
    user = update.effective_user
    chat = update.effective_chat

    # Save user to database
    with get_session() as session:
        db_user = session.query(TelegramUser).filter(TelegramUser.telegram_id == user.id).first()
        if not db_user:
            db_user = TelegramUser(
                telegram_id=user.id,
                username=user.username,
                first_name=user.first_name,
                last_name=user.last_name
            )
            session.add(db_user)

    # Different message for groups vs private chats
    if chat.type in ['group', 'supergroup']:
        welcome_message = f"""
💼 **Your AI Business Intelligence Advisor is Online**

I deliver real-time strategic insights on your bank's operations - anytime, anywhere.

**What I Provide:**
📊 **Executive Dashboard** - Key metrics at your fingertips
💡 **Strategic Insights** - Ask me anything about your business
🎯 **Data-Driven Decisions** - Turn data into action

**Quick Access:**
/analytics - Executive dashboard
/summary - Business snapshot
/help - All capabilities

Transform conversations into strategic advantage. Just mention me or ask a question.
"""
    else:
        welcome_message = f"""
💼 **Welcome, {user.first_name}**

Your AI Business Intelligence Advisor - delivering strategic insights on demand.

**Strategic Intelligence at Your Command:**
📊 **Executive Dashboard** - Real-time business metrics
💡 **AI Advisor** - Ask strategic questions, get data-driven answers
🎯 **Instant Insights** - From customer trends to revenue opportunities

**Get Started:**
/analytics - View executive dashboard
/summary - Business performance snapshot
/chat - Activate AI advisor
/help - Explore all capabilities

*Your trusted advisor in your pocket. Ask me anything about your bank's performance.*
"""

    await update.message.reply_text(welcome_message)


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /help command."""
    chat = update.effective_chat
    bot_username = context.bot.username or "bot"

    if chat.type in ['group', 'supergroup']:
        help_text = f"""
💼 **Executive Command Center**

**Strategic Intelligence:**
/analytics - Executive dashboard with interactive metrics
/summary - Business performance snapshot
/balance - Portfolio overview
/spending - Expenditure analysis
/trends - Market & transaction patterns
/top - Highest-value transactions

**AI Advisory Access:**
- Mention me: @{bot_username} [your strategic question]
- Reply to my insights for deeper analysis
- /ask [question] - Direct inquiry

**System:**
/start - Welcome brief
/help - Command reference
/myid - Your executive ID

**Intelligence Note:**
All metrics reflect real-time bank operations. AI conversations are private to each executive.
"""
    else:
        help_text = """
💼 **Executive Command Center**

**Strategic Dashboard:**
/analytics - Interactive executive dashboard
/summary - Business performance snapshot
/balance - Portfolio overview
/spending - Expenditure analysis by category
/trends - Transaction & market patterns
/top - High-value transaction review

**AI Business Advisor:**
/chat - Activate AI advisory mode
/clear - Reset conversation context
/ask [question] - Direct strategic inquiry

**System:**
/start - Welcome brief
/help - Command reference
/myid - Your executive ID

**How to Use:**
Simply message me any strategic question about your bank's performance. I analyze the data and deliver actionable insights instantly.

*Example: "What are our growth opportunities?" or "Analyze loan portfolio risk"*
"""

    await update.message.reply_text(help_text)


async def analytics_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show analytics menu with options."""
    chat = update.effective_chat

    keyboard = [
        [
            InlineKeyboardButton("📊 Business Snapshot", callback_data='analytics_summary'),
            InlineKeyboardButton("💼 Portfolio Overview", callback_data='analytics_balance')
        ],
        [
            InlineKeyboardButton("💸 Expenditure Analysis", callback_data='analytics_spending'),
            InlineKeyboardButton("📈 Transaction Patterns", callback_data='analytics_trends')
        ],
        [
            InlineKeyboardButton("🎯 High-Value Transactions", callback_data='analytics_top'),
            InlineKeyboardButton("📉 Portfolio Trend", callback_data='analytics_balance_trend')
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    message_text = "💼 **Executive Dashboard**\n\nSelect strategic intelligence:"

    # Add note for groups
    if chat.type in ['group', 'supergroup']:
        message_text += "\n\n_Real-time operational metrics for executive decision-making._"

    await update.message.reply_text(
        message_text,
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )


async def handle_analytics_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle analytics button callbacks."""
    query = update.callback_query
    await query.answer()

    action = query.data.replace('analytics_', '')

    try:
        if action == 'summary':
            summary = AnalyticsEngine.get_monthly_summary()
            net_emoji = "📈" if summary['net'] >= 0 else "📉"
            text = f"""
💼 **Business Performance - {summary['month']}**

💰 Revenue: ${summary['total_income']:,.2f}
💸 Operating Expenses: ${summary['total_expenses']:,.2f}
{net_emoji} Net Position: ${summary['net']:,.2f}
📊 Transaction Volume: {summary['transaction_count']}

*Strategic Position: {"Strong positive cashflow" if summary['net'] >= 0 else "Cost optimization opportunity"}*
"""
            await query.edit_message_text(text, parse_mode='Markdown')

        elif action == 'balance':
            account_summary = AnalyticsEngine.get_account_summary()
            text = f"""
💼 **Portfolio Overview**

🏦 Total Assets Under Management: ${account_summary['total_balance']:,.2f}
📋 Active Customer Accounts: {account_summary['account_count']}

**Portfolio Breakdown:**
"""
            for acc in account_summary['accounts']:
                text += f"\n• Account {acc['account_number']} | {acc['type'].title()}: ${acc['balance']:,.2f}"

            await query.edit_message_text(text, parse_mode='Markdown')

        elif action == 'spending':
            spending = AnalyticsEngine.get_spending_by_type()

            # Send chart
            chart = chart_generator.create_spending_by_category_chart(spending)
            await query.message.reply_photo(photo=chart, caption="💸 **Expenditure Analysis** - Strategic spending breakdown")

            # Also send text summary
            text = "**Operating Expenditure Breakdown:**\n\n"
            total_spending = sum(spending.values())
            for i, (trans_type, amount) in enumerate(
                sorted(spending.items(), key=lambda x: x[1], reverse=True)[:10], 1
            ):
                display_name = trans_type.replace('_', ' ').title()
                percentage = (amount / total_spending * 100) if total_spending > 0 else 0
                text += f"{i}. {display_name}: ${amount:,.2f} ({percentage:.1f}%)\n"

            await query.message.reply_text(text, parse_mode='Markdown')

        elif action == 'trends':
            df = AnalyticsEngine.get_transaction_trends(days=30)
            chart = chart_generator.create_transaction_trend_chart(df)
            await query.message.reply_photo(
                photo=chart,
                caption="📈 **Transaction Pattern Analysis** - 90-day operational flow"
            )

        elif action == 'balance_trend':
            df = AnalyticsEngine.get_daily_balance_trend(days=90)
            chart = chart_generator.create_balance_trend_chart(df)
            await query.message.reply_photo(
                photo=chart,
                caption="📊 **Portfolio Performance Trend** - 90-day asset trajectory"
            )

        elif action == 'top':
            transactions = AnalyticsEngine.get_top_transactions(limit=10)
            chart = chart_generator.create_top_transactions_chart(transactions)
            await query.message.reply_photo(photo=chart, caption="🎯 **High-Value Transaction Review** - Top 10 by volume")

            # Also send text list
            text = "**Strategic Transaction Review:**\n\n"
            for i, t in enumerate(transactions, 1):
                emoji = "📈" if 'deposit' in t['type'] or 'credit' in t['type'] else "📉"
                text += f"{i}. {emoji} ${t['amount']:,.2f} | {t['category']}\n"
                text += f"   {t['description']} | {t['date']}\n\n"

            await query.message.reply_text(text, parse_mode='Markdown')

    except Exception as e:
        logger.error(f"Error in analytics callback: {e}")
        await query.message.reply_text(
            f"Sorry, I encountered an error: {str(e)}"
        )


async def summary_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Get quick financial summary."""
    try:
        text = AnalyticsEngine.get_insights_text()
        # Split message if too long
        message_chunks = split_message(text)
        for chunk in message_chunks:
            await update.message.reply_text(chunk, parse_mode='Markdown')
    except Exception as e:
        await update.message.reply_text(f"Error generating summary: {str(e)}")


async def chat_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Start chat mode."""
    await update.message.reply_text(
        "💼 **AI Business Advisor Activated**\n\n"
        "Ask me anything about your bank's performance:\n\n"
        "• Revenue opportunities and growth strategies\n"
        "• Risk assessment and portfolio analysis\n"
        "• Customer behavior and transaction patterns\n"
        "• Operational efficiency insights\n"
        "• Market trends and competitive positioning\n\n"
        "*I transform your data into strategic intelligence.*\n\n"
        "Use /clear to reset conversation context."
    )


async def my_id_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show user's Telegram ID."""
    user = update.effective_user

    info_text = f"""
🆔 **Executive Access Credentials**

**Executive ID:** `{user.id}`
**Username:** @{user.username if user.username else 'Not configured'}
**Name:** {user.first_name} {user.last_name if user.last_name else ''}

💼 **About Executive ID:**
- Your unique secure identifier
- Required for system administration access
- Independent of username

⚙️ **Grant System Admin Access:**
Add your Executive ID to .env configuration:
```
ADMIN_USER_IDS="{user.id}"
```

For multiple administrators:
```
ADMIN_USER_IDS="{user.id},123456789,987654321"
```
"""

    await update.message.reply_text(info_text, parse_mode='Markdown')


async def clear_chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Clear chat history."""
    user_id = update.effective_user.id
    chatbot.clear_history(user_id)
    await update.message.reply_text("✅ Chat history cleared!")


async def ask_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /ask command with question."""
    user_id = update.effective_user.id

    if not context.args:
        await update.message.reply_text(
            "Please provide a question. Example:\n/ask What is a good savings rate?"
        )
        return

    question = ' '.join(context.args)

    # Get analytics context
    analytics_context = AnalyticsEngine.get_insights_text()

    # Get AI response
    response = chatbot.chat_with_data_context(
        user_id,
        question,
        analytics_context=analytics_context
    )

    # Split message if too long and send in chunks
    message_chunks = split_message(response)
    for chunk in message_chunks:
        await update.message.reply_text(chunk)


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle regular messages."""
    user_id = update.effective_user.id
    user_message = update.message.text
    chat = update.effective_chat

    # In groups, only respond if bot is mentioned or replied to
    if chat.type in ['group', 'supergroup']:
        bot_username = context.bot.username
        # Check if message is a reply to bot or mentions bot
        is_reply_to_bot = (
            update.message.reply_to_message and
            update.message.reply_to_message.from_user.id == context.bot.id
        )
        is_mentioned = f"@{bot_username}" in user_message.lower() if bot_username else False

        # Only respond if mentioned or replied to
        if not (is_reply_to_bot or is_mentioned):
            return

        # Remove bot mention from message
        if is_mentioned and bot_username:
            user_message = user_message.replace(f"@{bot_username}", "").strip()

    # Show typing indicator
    await update.message.chat.send_action(action="typing")

    # Get analytics context for financial questions
    analytics_context = None
    financial_keywords = [
        'spending', 'balance', 'transaction', 'account', 'money', 'financial',
        'loan', 'revenue', 'sales', 'portfolio', 'customer', 'growth',
        'profit', 'cost', 'expense', 'income', 'performance', 'strategy'
    ]

    if any(keyword in user_message.lower() for keyword in financial_keywords):
        analytics_context = AnalyticsEngine.get_insights_text()

    # Get AI response (always use user_id for personal history)
    if analytics_context:
        response = chatbot.chat_with_data_context(
            user_id,
            user_message,
            analytics_context=analytics_context
        )
    else:
        response = chatbot.chat(user_id, user_message)

    # Split message if too long and send in chunks
    message_chunks = split_message(response)
    for chunk in message_chunks:
        # In groups, reply to the message for context
        if chat.type in ['group', 'supergroup']:
            await update.message.reply_text(chunk)
        else:
            await update.message.reply_text(chunk)


async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle errors."""
    logger.error(f"Update {update} caused error {context.error}")


def run_health_server():
    """Run a simple health check server for Render."""
    app = Flask(__name__)

    @app.route('/')
    @app.route('/health')
    def health():
        return {'status': 'ok', 'service': 'analyst_in_pocket_bot'}, 200

    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)


def main():
    """Start the bot."""
    # Validate configuration
    try:
        Config.validate()
    except ValueError as e:
        logger.error(f"Configuration error: {e}")
        return

    # Start health check server in background thread (for Render)
    if os.environ.get('RENDER'):
        health_thread = Thread(target=run_health_server, daemon=True)
        health_thread.start()
        logger.info("Health check server started")

    # Create application
    application = Application.builder().token(Config.TELEGRAM_BOT_TOKEN).build()

    # Add command handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("myid", my_id_command))
    application.add_handler(CommandHandler("analytics", analytics_menu))
    application.add_handler(CommandHandler("summary", summary_command))
    application.add_handler(CommandHandler("chat", chat_command))
    application.add_handler(CommandHandler("clear", clear_chat))
    application.add_handler(CommandHandler("ask", ask_command))

    # Add callback handler for analytics buttons
    application.add_handler(CallbackQueryHandler(handle_analytics_callback, pattern='^analytics_'))

    # Add message handler for chat
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Add error handler
    application.add_error_handler(error_handler)

    # Start bot
    logger.info("Starting bot...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == '__main__':
    main()
