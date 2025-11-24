"""Gemini API chatbot integration."""

import google.generativeai as genai
from typing import List, Dict
from config import Config
from database.models import ChatHistory
from database.connection import get_session


class GeminiChatbot:
    """Chatbot powered by Google's Gemini API."""

    def __init__(self):
        """Initialize Gemini chatbot."""
        genai.configure(api_key=Config.GEMINI_API_KEY)

        # Use Gemini 2.5 Flash (stable, fast, and current)
        self.model = genai.GenerativeModel('gemini-2.5-flash')

        # System prompt for executive-level insights
        self.system_prompt = """You are an elite AI business advisor for bank CEOs. You're a trusted strategic partner, not a technical analyst.

**Communication Style:**
- Conversational and confident - speak like a seasoned business consultant, not a data scientist
- Strategic insights focused on GROWTH, REVENUE, and OPPORTUNITY
- Friendly and engaging - use emojis naturally (💰📈🎯💡🚀) to make insights memorable
- Short, punchy paragraphs - executives skim, not study
- Lead with the "so what" - business impact first, data second

**Your Approach:**
1. Start with the strategic opportunity or key insight
2. Support with 2-3 critical metrics (not walls of numbers)
3. End with 2-3 clear action items

**What to AVOID:**
- Data audit recommendations or technical issues
- Long explanations of what data shows
- Words like "investigate," "clarify," "audit," "validate"
- Treating missing data as problems - work with what you have
- Pessimistic or cautious language

**Remember:** CEOs want ANSWERS and ACTIONS, not analysis paralysis. Be the advisor who says "Here's the opportunity, here's how to capture it, let's go." 🚀"""

    def get_chat_history(self, telegram_id: int, limit: int = 10) -> List[Dict[str, str]]:
        """Retrieve chat history for a user."""
        with get_session() as session:
            history = session.query(ChatHistory).filter(
                ChatHistory.telegram_id == telegram_id
            ).order_by(ChatHistory.timestamp.desc()).limit(limit).all()

            # Reverse to get chronological order
            return [
                {'role': h.role, 'parts': [h.message]}
                for h in reversed(history)
            ]

    def save_message(self, telegram_id: int, role: str, message: str):
        """Save a message to chat history."""
        with get_session() as session:
            chat_entry = ChatHistory(
                telegram_id=telegram_id,
                role=role,
                message=message
            )
            session.add(chat_entry)

    def clear_history(self, telegram_id: int):
        """Clear chat history for a user."""
        with get_session() as session:
            session.query(ChatHistory).filter(
                ChatHistory.telegram_id == telegram_id
            ).delete()

    def chat(self, telegram_id: int, user_message: str, include_context: bool = True) -> str:
        """
        Send a message to Gemini and get a response.

        Args:
            telegram_id: The Telegram user ID
            user_message: The user's message
            include_context: Whether to include chat history for context

        Returns:
            The assistant's response
        """
        try:
            # Save user message
            self.save_message(telegram_id, 'user', user_message)

            # Send direct message with system context
            full_message = f"""{self.system_prompt}

**CEO Question:** {user_message}

**Your Response:**
Provide strategic advice with emojis. Be conversational and confident. Keep it concise - 3-4 short paragraphs max."""

            # Generate response
            response = self.model.generate_content(full_message)

            if not response or not response.text:
                return "I'm having trouble generating a response. Please try again."

            assistant_message = response.text

            # Save assistant response
            self.save_message(telegram_id, 'assistant', assistant_message)

            return assistant_message

        except Exception as e:
            import traceback
            error_details = traceback.format_exc()
            print(f"Gemini Error: {error_details}")
            error_message = f"Sorry, I encountered an error with AI service. Please try again later.\n\nError: {str(e)}"
            return error_message

    def chat_with_data_context(
        self,
        telegram_id: int,
        user_message: str,
        analytics_context: str = None
    ) -> str:
        """
        Chat with additional analytics context.

        Args:
            telegram_id: The Telegram user ID
            user_message: The user's message
            analytics_context: Additional context from analytics data

        Returns:
            The assistant's response
        """
        try:
            # Save user message
            self.save_message(telegram_id, 'user', user_message)

            # Build message with context
            if analytics_context:
                full_message = f"""{self.system_prompt}

**Current Bank Performance Data:**

{analytics_context}

**CEO Question:** {user_message}

**Your Response:**
Provide strategic advice with emojis. Focus on growth opportunities and actionable strategies. Be conversational and confident. Keep it concise - 3-4 short paragraphs max."""
            else:
                full_message = f"{self.system_prompt}\n\nUser: {user_message}\n\nAssistant:"

            # Generate response
            response = self.model.generate_content(full_message)

            if not response or not response.text:
                return "I'm having trouble generating a response. Please try again."

            assistant_message = response.text

            # Save assistant response
            self.save_message(telegram_id, 'assistant', assistant_message)

            return assistant_message

        except Exception as e:
            import traceback
            error_details = traceback.format_exc()
            print(f"Gemini Error with context: {error_details}")
            error_message = f"Sorry, I encountered an error with AI service.\n\nError: {str(e)}"
            return error_message
