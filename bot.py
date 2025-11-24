"""Main Telegram bot application."""

import logging
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
👋 Hello! I'm your Financial Analyst Bot!

I can help this group with:
📊 **Analytics** - Get insights about financial data
💬 **Chat** - Ask me anything about personal finance

**Group Commands:**
/analytics - View financial insights menu
/summary - Get quick financial summary
/help - Show all commands

**Note:** Analytics are shared with the group. For private AI conversations, DM me!
"""
    else:
        welcome_message = f"""
👋 Hello {user.first_name}! Welcome to your Financial Analyst Bot!

I can help you with:
📊 **Analytics** - Get insights about your financial data
💬 **Chat** - Ask me anything about personal finance

**Quick Commands:**
/analytics - View financial insights menu
/summary - Get quick financial summary
/chat - Start a conversation with me
/help - Show all commands

You can also just send me a message and I'll respond!
"""

    await update.message.reply_text(welcome_message)


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /help command."""
    chat = update.effective_chat
    bot_username = context.bot.username or "bot"

    if chat.type in ['group', 'supergroup']:
        help_text = f"""
🤖 **Financial Analyst Bot - Help**

**Analytics Commands:**
/analytics - Interactive analytics menu
/summary - Monthly financial summary
/balance - Account balance overview
/spending - Spending by category
/trends - Transaction trends
/top - Top transactions

**Chat in Groups:**
- Mention me: @{bot_username} your question
- Reply to my message
- Use /ask command

**General Commands:**
/start - Bot introduction
/help - Show this help message
/myid - Show your Telegram user ID

**Note:**
- Analytics are shared with the group
- Chat history is personal (use /clear to reset yours)
- For private conversations, DM me!
"""
    else:
        help_text = """
🤖 **Financial Analyst Bot - Help**

**Analytics Commands:**
/analytics - Interactive analytics menu
/summary - Monthly financial summary
/balance - Account balance overview
/spending - Spending by category
/trends - Transaction trends
/top - Top transactions

**Chat Commands:**
/chat - Start chatting with AI assistant
/clear - Clear chat history
/ask [question] - Ask a specific question

**General Commands:**
/start - Start the bot
/help - Show this help message
/myid - Show your Telegram user ID

**How to use:**
- Use commands for specific analytics
- Or simply send me a message and I'll respond as your AI assistant
- Click buttons in analytics menu for visual charts
"""

    await update.message.reply_text(help_text)


async def analytics_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show analytics menu with options."""
    chat = update.effective_chat

    keyboard = [
        [
            InlineKeyboardButton("📊 Summary", callback_data='analytics_summary'),
            InlineKeyboardButton("💰 Balance", callback_data='analytics_balance')
        ],
        [
            InlineKeyboardButton("🛒 Spending", callback_data='analytics_spending'),
            InlineKeyboardButton("📈 Trends", callback_data='analytics_trends')
        ],
        [
            InlineKeyboardButton("🔝 Top Transactions", callback_data='analytics_top'),
            InlineKeyboardButton("📉 Balance Trend", callback_data='analytics_balance_trend')
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    message_text = "📊 **Analytics Dashboard**\n\nChoose what you'd like to see:"

    # Add note for groups
    if chat.type in ['group', 'supergroup']:
        message_text += "\n\n_Note: Analytics show demo bank data shared with the group._"

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
            text = f"""
📊 **Monthly Summary - {summary['month']}**

💰 Total Income: ${summary['total_income']:,.2f}
💸 Total Expenses: ${summary['total_expenses']:,.2f}
📈 Net: ${summary['net']:,.2f}
🔢 Transactions: {summary['transaction_count']}
"""
            await query.edit_message_text(text, parse_mode='Markdown')

        elif action == 'balance':
            account_summary = AnalyticsEngine.get_account_summary()
            text = f"""
💰 **Account Balance Overview**

🏦 Total Balance: ${account_summary['total_balance']:,.2f}
📋 Active Accounts: {account_summary['account_count']}

**Accounts:**
"""
            for acc in account_summary['accounts']:
                text += f"\n• {acc['account_number']} ({acc['type']}): ${acc['balance']:,.2f}"

            await query.edit_message_text(text, parse_mode='Markdown')

        elif action == 'spending':
            spending = AnalyticsEngine.get_spending_by_type()

            # Send chart
            chart = chart_generator.create_spending_by_category_chart(spending)
            await query.message.reply_photo(photo=chart, caption="📊 Spending by Type")

            # Also send text summary
            text = "**Top Spending by Type:**\n\n"
            for i, (trans_type, amount) in enumerate(
                sorted(spending.items(), key=lambda x: x[1], reverse=True)[:10], 1
            ):
                display_name = trans_type.replace('_', ' ').title()
                text += f"{i}. {display_name}: ${amount:,.2f}\n"

            await query.message.reply_text(text, parse_mode='Markdown')

        elif action == 'trends':
            df = AnalyticsEngine.get_transaction_trends(days=30)
            chart = chart_generator.create_transaction_trend_chart(df)
            await query.message.reply_photo(
                photo=chart,
                caption="📈 Transaction Trends (Last 30 Days)"
            )

        elif action == 'balance_trend':
            df = AnalyticsEngine.get_daily_balance_trend(days=30)
            chart = chart_generator.create_balance_trend_chart(df)
            await query.message.reply_photo(
                photo=chart,
                caption="📉 Balance Trend (Last 30 Days)"
            )

        elif action == 'top':
            transactions = AnalyticsEngine.get_top_transactions(limit=10)
            chart = chart_generator.create_top_transactions_chart(transactions)
            await query.message.reply_photo(photo=chart, caption="🔝 Top 10 Transactions")

            # Also send text list
            text = "**Top 10 Transactions:**\n\n"
            for i, t in enumerate(transactions, 1):
                emoji = "💰" if t['type'] == 'credit' else "💸"
                text += f"{i}. {emoji} ${t['amount']:,.2f} - {t['category'] or 'N/A'}\n"
                text += f"   {t['description'] or 'No description'} ({t['date']})\n\n"

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
        await update.message.reply_text(text, parse_mode='Markdown')
    except Exception as e:
        await update.message.reply_text(f"Error generating summary: {str(e)}")


async def chat_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Start chat mode."""
    await update.message.reply_text(
        "💬 Chat mode activated! Send me any message and I'll respond.\n\n"
        "You can ask me about:\n"
        "• Personal finance tips\n"
        "• Understanding your spending\n"
        "• Financial planning advice\n"
        "• Or anything else!\n\n"
        "Use /clear to reset our conversation."
    )


async def my_id_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show user's Telegram ID."""
    user = update.effective_user

    info_text = f"""
🆔 **Your Telegram Information**

**User ID:** `{user.id}`
**Username:** @{user.username if user.username else 'Not set'}
**Name:** {user.first_name} {user.last_name if user.last_name else ''}

💡 **What is User ID?**
- Your unique Telegram identifier
- Used for admin permissions in bots
- Different from your username

📝 **To set as admin:**
Add this to your .env file:
```
ADMIN_USER_IDS="{user.id}"
```

For multiple admins, separate with commas:
```
ADMIN_USER_IDS="{user.id},123456789"
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

    await update.message.reply_text(response)


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
    financial_keywords = ['spending', 'balance', 'transaction', 'account', 'money', 'financial']

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

    # In groups, reply to the message for context
    if chat.type in ['group', 'supergroup']:
        await update.message.reply_text(response)
    else:
        await update.message.reply_text(response)


async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle errors."""
    logger.error(f"Update {update} caused error {context.error}")


def main():
    """Start the bot."""
    # Validate configuration
    try:
        Config.validate()
    except ValueError as e:
        logger.error(f"Configuration error: {e}")
        return

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
