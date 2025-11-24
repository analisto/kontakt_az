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

        # System prompt for the analyst bot
        self.system_prompt = """You are a helpful financial analyst assistant. You help users understand their financial data,
provide insights about their spending habits, and answer questions about personal finance.

You have access to the user's banking data including transactions, accounts, and balances through the analytics system.
When users ask about their financial data, you should provide clear, actionable insights.

Be professional, friendly, and concise in your responses. Use emojis occasionally to make the conversation more engaging.
Focus on practical financial advice and data-driven insights."""

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

            # For simpler interaction, don't use chat history with Gemini API
            # Just send direct message with system context
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

Here is the current financial data:

{analytics_context}

User question: {user_message}

Please provide insights based on this data. Be specific and reference the actual numbers."""
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
