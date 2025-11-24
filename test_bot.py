"""Test script to verify bot setup."""

print("🔍 Testing bot setup...\n")

# Test 1: Configuration
print("1️⃣ Testing configuration...")
try:
    from config import Config
    Config.validate()
    print("✅ Configuration validated")
    print(f"   - Database URL: {Config.DATABASE_URL[:50]}...")
    print(f"   - Telegram Token: {'*' * 20}{Config.TELEGRAM_BOT_TOKEN[-10:]}")
    print(f"   - Gemini API Key: {'*' * 20}{Config.GEMINI_API_KEY[-10:]}")
except Exception as e:
    print(f"❌ Configuration failed: {e}")
    exit(1)

# Test 2: Database Connection
print("\n2️⃣ Testing database connection...")
try:
    from database import get_session
    from database.models import Customer, Transaction, TelegramUser

    with get_session() as session:
        customer_count = session.query(Customer).count()
        transaction_count = session.query(Transaction).count()

        print(f"✅ Database connected successfully")
        print(f"   - Customers: {customer_count}")
        print(f"   - Transactions: {transaction_count}")

        # Try to get sample data
        sample_customer = session.query(Customer).first()
        if sample_customer:
            print(f"   - Sample customer: {sample_customer.first_name} {sample_customer.last_name}")
except Exception as e:
    print(f"❌ Database connection failed: {e}")
    import traceback
    traceback.print_exc()
    exit(1)

# Test 3: Analytics Engine
print("\n3️⃣ Testing analytics engine...")
try:
    from analytics import AnalyticsEngine

    summary = AnalyticsEngine.get_account_summary()
    print(f"✅ Analytics engine working")
    print(f"   - Total balance: ${summary['total_balance']:,.2f}")
    print(f"   - Active accounts: {summary['account_count']}")

    monthly = AnalyticsEngine.get_monthly_summary()
    print(f"   - Monthly income: ${monthly['total_income']:,.2f}")
    print(f"   - Monthly expenses: ${monthly['total_expenses']:,.2f}")
except Exception as e:
    print(f"❌ Analytics engine failed: {e}")
    import traceback
    traceback.print_exc()
    exit(1)

# Test 4: Chart Generator
print("\n4️⃣ Testing chart generator...")
try:
    from analytics import ChartGenerator
    chart_gen = ChartGenerator()
    print("✅ Chart generator initialized")
except Exception as e:
    print(f"❌ Chart generator failed: {e}")
    exit(1)

# Test 5: Gemini Chatbot
print("\n5️⃣ Testing Gemini chatbot...")
try:
    from chatbot import GeminiChatbot
    chatbot = GeminiChatbot()
    print("✅ Gemini chatbot initialized")
except Exception as e:
    print(f"❌ Gemini chatbot failed: {e}")
    import traceback
    traceback.print_exc()
    exit(1)

# Test 6: Bot Imports
print("\n6️⃣ Testing bot imports...")
try:
    import bot
    print("✅ Bot module imported successfully")
except Exception as e:
    print(f"❌ Bot import failed: {e}")
    import traceback
    traceback.print_exc()
    exit(1)

print("\n" + "="*50)
print("✅ All tests passed! Bot is ready to run.")
print("="*50)
print("\nTo start the bot:")
print("  • Locally: python bot.py")
print("  • Docker: ./deploy.sh")
print("\nTo test with Telegram:")
print(f"  1. Open Telegram")
print(f"  2. Search for your bot")
print(f"  3. Send /start command")
