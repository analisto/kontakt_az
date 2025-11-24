"""Database models for the Analyst Bot."""

from datetime import datetime, date
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text, Numeric, Date, Boolean, CHAR, BigInteger
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class TelegramUser(Base):
    """Telegram bot user model (separate from bank users)."""

    __tablename__ = 'telegram_users'
    __table_args__ = {'schema': 'demo_bank'}

    id = Column(Integer, primary_key=True)
    telegram_id = Column(BigInteger, unique=True, nullable=False)  # BigInteger for Telegram IDs
    username = Column(String(255))
    first_name = Column(String(255))
    last_name = Column(String(255))
    created_at = Column(DateTime, default=datetime.utcnow)
    last_active = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"<TelegramUser(telegram_id={self.telegram_id}, username={self.username})>"


class Customer(Base):
    """Bank customer model - maps to existing customers table."""

    __tablename__ = 'customers'
    __table_args__ = {'schema': 'demo_bank', 'extend_existing': True}

    customer_id = Column(Integer, primary_key=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    date_of_birth = Column(Date, nullable=False)
    email = Column(String, nullable=False)
    phone_number = Column(String)
    street_address = Column(String)
    city = Column(String)
    state = Column(String)
    postal_code = Column(String)
    country = Column(String, default='USA')
    account_number = Column(String, nullable=False)
    account_type = Column(String, nullable=False)
    account_balance = Column(Numeric, nullable=False, default=0.00)
    ssn_last_four = Column(CHAR(4))
    id_type = Column(String)
    id_number = Column(String)
    account_status = Column(String, default='active')
    credit_score = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_login = Column(DateTime)

    transactions = relationship("Transaction", back_populates="customer")
    loans = relationship("Loan", back_populates="customer")

    def __repr__(self):
        return f"<Customer(id={self.customer_id}, name={self.first_name} {self.last_name})>"


class Transaction(Base):
    """Transaction model - maps to existing transactions table."""

    __tablename__ = 'transactions'
    __table_args__ = {'schema': 'demo_bank', 'extend_existing': True}

    transaction_id = Column(Integer, primary_key=True)
    customer_id = Column(Integer, ForeignKey('demo_bank.customers.customer_id'), nullable=False)
    loan_id = Column(Integer, ForeignKey('demo_bank.loans.loan_id'))
    transaction_reference = Column(String, nullable=False)
    transaction_type = Column(String, nullable=False)
    amount = Column(Numeric, nullable=False)
    currency = Column(String, default='USD')
    balance_before = Column(Numeric, nullable=False)
    balance_after = Column(Numeric, nullable=False)
    description = Column(Text)
    notes = Column(Text)
    transaction_method = Column(String)
    counterparty_account = Column(String)
    counterparty_name = Column(String)
    counterparty_bank = Column(String)
    branch_code = Column(String)
    atm_id = Column(String)
    transaction_status = Column(String, default='completed')
    transaction_date = Column(Date, nullable=False, default=date.today)
    transaction_time = Column(DateTime, nullable=False, default=datetime.utcnow)
    posted_date = Column(Date)
    value_date = Column(Date)
    created_at = Column(DateTime, default=datetime.utcnow)
    processed_by = Column(String)
    authorized_by = Column(String)
    is_flagged = Column(Boolean, default=False)
    flag_reason = Column(Text)

    customer = relationship("Customer", back_populates="transactions")
    loan = relationship("Loan", back_populates="transactions")

    def __repr__(self):
        return f"<Transaction(id={self.transaction_id}, type={self.transaction_type}, amount={self.amount})>"


class Loan(Base):
    """Loan model - maps to existing loans table."""

    __tablename__ = 'loans'
    __table_args__ = {'schema': 'demo_bank', 'extend_existing': True}

    loan_id = Column(Integer, primary_key=True)
    customer_id = Column(Integer, ForeignKey('demo_bank.customers.customer_id'), nullable=False)
    loan_number = Column(String, nullable=False)
    loan_type = Column(String, nullable=False)
    loan_purpose = Column(Text)
    principal_amount = Column(Numeric, nullable=False)
    interest_rate = Column(Numeric, nullable=False)
    loan_term_months = Column(Integer, nullable=False)
    monthly_payment = Column(Numeric, nullable=False)
    outstanding_balance = Column(Numeric, nullable=False, default=0.00)
    total_paid = Column(Numeric, default=0.00)
    application_date = Column(Date, nullable=False, default=date.today)
    approval_date = Column(Date)
    disbursement_date = Column(Date)
    first_payment_date = Column(Date)
    maturity_date = Column(Date)
    loan_status = Column(String, default='pending')
    payment_status = Column(String, default='current')
    days_past_due = Column(Integer, default=0)
    collateral_type = Column(String)
    collateral_value = Column(Numeric)
    loan_officer_name = Column(String)
    loan_officer_id = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_payment_date = Column(Date)

    customer = relationship("Customer", back_populates="loans")
    transactions = relationship("Transaction", back_populates="loan")

    def __repr__(self):
        return f"<Loan(id={self.loan_id}, number={self.loan_number}, balance={self.outstanding_balance})>"


class ChatHistory(Base):
    """Chat history model for storing conversation context."""

    __tablename__ = 'chat_history'
    __table_args__ = {'schema': 'demo_bank'}

    id = Column(Integer, primary_key=True)
    telegram_id = Column(BigInteger, nullable=False)  # BigInteger for Telegram IDs
    role = Column(String(50))  # user, assistant
    message = Column(Text)
    timestamp = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<ChatHistory(telegram_id={self.telegram_id}, role={self.role})>"
