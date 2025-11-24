"""Analytics insights generation module."""

from datetime import datetime, timedelta, date
from typing import Dict, List, Any
import pandas as pd
from sqlalchemy import func, desc
from database.models import Transaction, Customer
from database.connection import get_session


class AnalyticsEngine:
    """Engine for generating analytics insights."""

    @staticmethod
    def get_account_summary() -> Dict[str, Any]:
        """Get summary of all customer accounts."""
        with get_session() as session:
            customers = session.query(Customer).filter(
                Customer.account_status == 'active'
            ).all()

            total_balance = sum(float(c.account_balance) for c in customers)
            account_count = len(customers)

            return {
                'total_balance': total_balance,
                'account_count': account_count,
                'accounts': [
                    {
                        'account_number': c.account_number,
                        'type': c.account_type,
                        'balance': float(c.account_balance),
                        'customer': f"{c.first_name} {c.last_name}"
                    }
                    for c in customers
                ]
            }

    @staticmethod
    def get_transaction_trends(days: int = 30) -> pd.DataFrame:
        """Get transaction trends for the specified number of days."""
        with get_session() as session:
            start_date = date.today() - timedelta(days=days)

            transactions = session.query(Transaction).filter(
                Transaction.transaction_date >= start_date,
                Transaction.transaction_status == 'completed'
            ).all()

            if not transactions:
                return pd.DataFrame()

            df = pd.DataFrame([
                {
                    'date': t.transaction_date,
                    'amount': float(t.amount),
                    'type': t.transaction_type,
                    'description': t.description or 'No description'
                }
                for t in transactions
            ])

            df['date'] = pd.to_datetime(df['date'])
            return df

    @staticmethod
    def get_spending_by_type(days: int = 30) -> Dict[str, float]:
        """Get spending breakdown by transaction type."""
        with get_session() as session:
            start_date = date.today() - timedelta(days=days)

            # Get debit-type transactions (money going out)
            debit_types = ['withdrawal', 'transfer_out', 'loan_payment', 'fee_debit']

            results = session.query(
                Transaction.transaction_type,
                func.sum(Transaction.amount).label('total')
            ).filter(
                Transaction.transaction_date >= start_date,
                Transaction.transaction_type.in_(debit_types),
                Transaction.transaction_status == 'completed'
            ).group_by(Transaction.transaction_type).all()

            return {
                trans_type: float(total)
                for trans_type, total in results
            }

    @staticmethod
    def get_monthly_summary() -> Dict[str, Any]:
        """Get current month's financial summary."""
        with get_session() as session:
            # Get first day of current month
            now = date.today()
            first_day = date(now.year, now.month, 1)

            transactions = session.query(Transaction).filter(
                Transaction.transaction_date >= first_day,
                Transaction.transaction_status == 'completed'
            ).all()

            # Credit types (money coming in)
            credit_types = ['deposit', 'transfer_in', 'loan_disbursement', 'interest_credit', 'refund']
            # Debit types (money going out)
            debit_types = ['withdrawal', 'transfer_out', 'loan_payment', 'fee_debit']

            total_income = sum(
                float(t.amount) for t in transactions
                if t.transaction_type in credit_types
            )
            total_expenses = sum(
                float(t.amount) for t in transactions
                if t.transaction_type in debit_types
            )

            return {
                'month': now.strftime('%B %Y'),
                'total_income': total_income,
                'total_expenses': total_expenses,
                'net': total_income - total_expenses,
                'transaction_count': len(transactions)
            }

    @staticmethod
    def get_top_transactions(limit: int = 10, transaction_type: str = None) -> List[Dict[str, Any]]:
        """Get top transactions by amount."""
        with get_session() as session:
            query = session.query(Transaction).filter(
                Transaction.transaction_status == 'completed'
            )

            if transaction_type:
                query = query.filter(Transaction.transaction_type == transaction_type)

            transactions = query.order_by(desc(Transaction.amount)).limit(limit).all()

            return [
                {
                    'id': t.transaction_id,
                    'amount': float(t.amount),
                    'type': t.transaction_type,
                    'category': t.transaction_type.replace('_', ' ').title(),
                    'description': t.description or 'No description',
                    'date': t.transaction_date.strftime('%Y-%m-%d')
                }
                for t in transactions
            ]

    @staticmethod
    def get_daily_balance_trend(days: int = 30) -> pd.DataFrame:
        """Get daily balance trends."""
        with get_session() as session:
            start_date = date.today() - timedelta(days=days)

            transactions = session.query(Transaction).filter(
                Transaction.transaction_date >= start_date,
                Transaction.transaction_status == 'completed'
            ).order_by(Transaction.transaction_time).all()

            if not transactions:
                return pd.DataFrame()

            df = pd.DataFrame([
                {
                    'date': t.transaction_date,
                    'balance': float(t.balance_after)
                }
                for t in transactions
            ])

            df['date'] = pd.to_datetime(df['date'])
            # Get last balance of each day
            df = df.groupby(df['date'].dt.date).last().reset_index()
            return df

    @staticmethod
    def get_insights_text() -> str:
        """Generate a text-based insights summary."""
        summary = AnalyticsEngine.get_monthly_summary()
        account_summary = AnalyticsEngine.get_account_summary()
        spending = AnalyticsEngine.get_spending_by_type()

        text = f"""
📊 **Financial Insights Summary**

**This Month ({summary['month']})**
💰 Total Income: ${summary['total_income']:,.2f}
💸 Total Expenses: ${summary['total_expenses']:,.2f}
📈 Net: ${summary['net']:,.2f}
🔢 Transactions: {summary['transaction_count']}

**Account Overview**
🏦 Total Balance: ${account_summary['total_balance']:,.2f}
📋 Active Accounts: {account_summary['account_count']}

**Top Spending by Type**
"""
        for i, (trans_type, amount) in enumerate(sorted(spending.items(), key=lambda x: x[1], reverse=True)[:5], 1):
            display_name = trans_type.replace('_', ' ').title()
            text += f"{i}. {display_name}: ${amount:,.2f}\n"

        return text.strip()
