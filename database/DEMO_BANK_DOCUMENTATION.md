# Demo Bank Database Documentation

## Overview
The `demo_bank` schema is a comprehensive banking database designed for demonstration purposes. It models core banking operations including customer management, loan processing, and transaction tracking.

---

## Schema Structure

### Entity Relationship Diagram (ERD) Description

```
customers (1) ----< (N) loans
customers (1) ----< (N) transactions
loans (1) ----< (N) transactions [optional relationship]
```

**Relationships:**
- One customer can have multiple loans (one-to-many)
- One customer can have multiple transactions (one-to-many)
- One loan can have multiple transactions (one-to-many, optional)

---

## Table: `customers`

### Purpose
Stores comprehensive information about bank customers, including personal details, contact information, account details, and KYC (Know Your Customer) compliance data.

### Columns

| Column Name | Data Type | Constraints | Description |
|-------------|-----------|-------------|-------------|
| `customer_id` | SERIAL | PRIMARY KEY | Unique identifier for each customer (auto-incremented) |
| `first_name` | VARCHAR(100) | NOT NULL | Customer's first name |
| `last_name` | VARCHAR(100) | NOT NULL | Customer's last name |
| `date_of_birth` | DATE | NOT NULL, CHECK | Customer's date of birth (must be 18+ years old) |
| `email` | VARCHAR(255) | UNIQUE, NOT NULL | Customer's email address (validated format) |
| `phone_number` | VARCHAR(20) | | Customer's phone number |
| `street_address` | VARCHAR(255) | | Street address |
| `city` | VARCHAR(100) | | City of residence |
| `state` | VARCHAR(100) | | State/province |
| `postal_code` | VARCHAR(20) | | Postal/ZIP code |
| `country` | VARCHAR(100) | DEFAULT 'USA' | Country of residence |
| `account_number` | VARCHAR(20) | UNIQUE, NOT NULL | Unique bank account number |
| `account_type` | VARCHAR(50) | NOT NULL, CHECK | Type of account: 'checking', 'savings', 'business', 'investment' |
| `account_balance` | DECIMAL(15, 2) | DEFAULT 0.00, NOT NULL | Current account balance (precision: 15 digits, 2 decimals) |
| `ssn_last_four` | CHAR(4) | | Last 4 digits of Social Security Number (for security) |
| `id_type` | VARCHAR(50) | CHECK | Type of ID: 'passport', 'drivers_license', 'national_id' |
| `id_number` | VARCHAR(50) | | ID document number |
| `account_status` | VARCHAR(20) | DEFAULT 'active', CHECK | Account status: 'active', 'inactive', 'suspended', 'closed' |
| `credit_score` | INTEGER | CHECK | Credit score (range: 300-850) |
| `created_at` | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | Timestamp when customer record was created |
| `updated_at` | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | Timestamp of last update (auto-updated via trigger) |
| `last_login` | TIMESTAMP | | Timestamp of customer's last login |

### Constraints

1. **Email Format Validation**: Ensures email follows standard format (username@domain.extension)
2. **Age Verification**: Customers must be at least 18 years old
3. **Unique Email**: No two customers can have the same email address
4. **Unique Account Number**: Each account number must be unique
5. **Credit Score Range**: Credit score must be between 300 and 850
6. **Account Type Enumeration**: Only allows specific account types
7. **Account Status Enumeration**: Only allows specific status values
8. **ID Type Enumeration**: Only allows specific ID types

### Indexes

- `idx_customers_email`: Fast lookup by email
- `idx_customers_account_number`: Fast lookup by account number
- `idx_customers_last_name`: Fast search by last name
- `idx_customers_account_status`: Filter by account status

### Business Rules

1. All customers must provide a valid email address
2. Customers must be at least 18 years old to open an account
3. Each customer is assigned a unique account number
4. Account balances are tracked with 2 decimal precision
5. The `updated_at` field is automatically updated on any record modification

---

## Table: `loans`

### Purpose
Stores information about loans issued to customers, including loan terms, payment schedules, status tracking, and collateral information.

### Columns

| Column Name | Data Type | Constraints | Description |
|-------------|-----------|-------------|-------------|
| `loan_id` | SERIAL | PRIMARY KEY | Unique identifier for each loan (auto-incremented) |
| `customer_id` | INTEGER | NOT NULL, FOREIGN KEY | References the customer who owns the loan |
| `loan_number` | VARCHAR(20) | UNIQUE, NOT NULL | Unique loan identification number |
| `loan_type` | VARCHAR(50) | NOT NULL, CHECK | Type: 'personal', 'mortgage', 'auto', 'student', 'business', 'home_equity' |
| `loan_purpose` | TEXT | | Description of loan purpose |
| `principal_amount` | DECIMAL(15, 2) | NOT NULL, CHECK | Original loan amount (must be > 0) |
| `interest_rate` | DECIMAL(5, 2) | NOT NULL, CHECK | Annual interest rate (0-100%) |
| `loan_term_months` | INTEGER | NOT NULL, CHECK | Loan duration in months (must be > 0) |
| `monthly_payment` | DECIMAL(15, 2) | NOT NULL | Required monthly payment amount |
| `outstanding_balance` | DECIMAL(15, 2) | NOT NULL, DEFAULT 0.00 | Current amount owed |
| `total_paid` | DECIMAL(15, 2) | DEFAULT 0.00 | Total amount paid to date |
| `application_date` | DATE | NOT NULL, DEFAULT CURRENT_DATE | Date loan application was submitted |
| `approval_date` | DATE | | Date loan was approved |
| `disbursement_date` | DATE | | Date loan funds were disbursed |
| `first_payment_date` | DATE | | Date of first payment |
| `maturity_date` | DATE | | Date loan is fully due |
| `loan_status` | VARCHAR(20) | DEFAULT 'pending', CHECK | Status: 'pending', 'approved', 'active', 'paid_off', 'defaulted', 'rejected' |
| `payment_status` | VARCHAR(20) | DEFAULT 'current', CHECK | Payment status: 'current', 'late', 'defaulted', 'grace_period' |
| `days_past_due` | INTEGER | DEFAULT 0 | Number of days payment is overdue |
| `collateral_type` | VARCHAR(100) | | Type of collateral (if secured loan) |
| `collateral_value` | DECIMAL(15, 2) | | Estimated value of collateral |
| `loan_officer_name` | VARCHAR(200) | | Name of loan officer handling the loan |
| `loan_officer_id` | VARCHAR(50) | | ID of loan officer |
| `created_at` | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | Timestamp when loan record was created |
| `updated_at` | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | Timestamp of last update (auto-updated via trigger) |
| `last_payment_date` | DATE | | Date of most recent payment |

### Constraints

1. **Positive Principal**: Principal amount must be greater than zero
2. **Valid Interest Rate**: Interest rate must be between 0 and 100
3. **Positive Term**: Loan term must be greater than zero
4. **Loan Type Enumeration**: Only allows specific loan types
5. **Loan Status Enumeration**: Only allows specific status values
6. **Payment Status Enumeration**: Only allows specific payment status values
7. **Foreign Key to Customers**: Ensures loan is linked to valid customer (RESTRICT on delete, CASCADE on update)

### Indexes

- `idx_loans_customer_id`: Fast lookup of loans by customer
- `idx_loans_loan_number`: Fast lookup by loan number
- `idx_loans_loan_status`: Filter by loan status
- `idx_loans_loan_type`: Filter by loan type
- `idx_loans_payment_status`: Filter by payment status

### Business Rules

1. Loans must be associated with an existing customer
2. Loan amounts must be positive values
3. Interest rates are expressed as annual percentage rates (APR)
4. Outstanding balance should decrease as payments are made
5. The system tracks payment history and delinquency
6. Secured loans should have collateral information
7. Deleting a customer is restricted if they have loans (referential integrity)

---

## Table: `transactions`

### Purpose
Stores all financial transactions for customers, including deposits, withdrawals, transfers, and loan-related transactions. Provides complete audit trail of all account activity.

### Columns

| Column Name | Data Type | Constraints | Description |
|-------------|-----------|-------------|-------------|
| `transaction_id` | SERIAL | PRIMARY KEY | Unique identifier for each transaction (auto-incremented) |
| `customer_id` | INTEGER | NOT NULL, FOREIGN KEY | References the customer account |
| `loan_id` | INTEGER | FOREIGN KEY | Optional reference to loan (for loan-related transactions) |
| `transaction_reference` | VARCHAR(50) | UNIQUE, NOT NULL | Unique transaction reference number |
| `transaction_type` | VARCHAR(50) | NOT NULL, CHECK | Type: 'deposit', 'withdrawal', 'transfer_in', 'transfer_out', 'loan_disbursement', 'loan_payment', 'interest_credit', 'fee_debit', 'refund', 'reversal' |
| `amount` | DECIMAL(15, 2) | NOT NULL, CHECK | Transaction amount (must be > 0) |
| `currency` | VARCHAR(3) | DEFAULT 'USD' | Currency code (ISO 4217) |
| `balance_before` | DECIMAL(15, 2) | NOT NULL | Account balance before transaction |
| `balance_after` | DECIMAL(15, 2) | NOT NULL | Account balance after transaction |
| `description` | TEXT | | Transaction description |
| `notes` | TEXT | | Additional notes or comments |
| `transaction_method` | VARCHAR(50) | CHECK | Method: 'cash', 'check', 'wire_transfer', 'ach', 'debit_card', 'credit_card', 'online', 'mobile_app', 'atm' |
| `counterparty_account` | VARCHAR(50) | | Account number of other party (for transfers) |
| `counterparty_name` | VARCHAR(200) | | Name of other party |
| `counterparty_bank` | VARCHAR(200) | | Bank of other party |
| `branch_code` | VARCHAR(20) | | Branch where transaction occurred |
| `atm_id` | VARCHAR(50) | | ATM ID (for ATM transactions) |
| `ip_address` | INET | | IP address (for online transactions) |
| `device_id` | VARCHAR(100) | | Device identifier (for mobile/online) |
| `transaction_status` | VARCHAR(20) | DEFAULT 'completed', CHECK | Status: 'pending', 'processing', 'completed', 'failed', 'reversed', 'cancelled' |
| `transaction_date` | DATE | NOT NULL, DEFAULT CURRENT_DATE | Date of transaction |
| `transaction_time` | TIMESTAMP | NOT NULL, DEFAULT CURRENT_TIMESTAMP | Exact timestamp of transaction |
| `posted_date` | DATE | | Date transaction posted to account |
| `value_date` | DATE | | Date transaction value takes effect |
| `created_at` | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | Timestamp when record was created |
| `processed_by` | VARCHAR(100) | | User/system that processed transaction |
| `authorized_by` | VARCHAR(100) | | User who authorized transaction |
| `is_flagged` | BOOLEAN | DEFAULT FALSE | Flag for suspicious/unusual transactions |
| `flag_reason` | TEXT | | Reason for flagging (if flagged) |

### Constraints

1. **Positive Amount**: Transaction amount must be greater than zero
2. **Balance Calculation Validation**: Ensures balance_after is correctly calculated based on transaction type
   - Credit transactions (deposits, transfers in): balance_after = balance_before + amount
   - Debit transactions (withdrawals, payments): balance_after = balance_before - amount
3. **Transaction Type Enumeration**: Only allows specific transaction types
4. **Transaction Method Enumeration**: Only allows specific transaction methods
5. **Transaction Status Enumeration**: Only allows specific status values
6. **Foreign Key to Customers**: Links to valid customer (RESTRICT on delete, CASCADE on update)
7. **Foreign Key to Loans**: Optional link to loan (SET NULL on delete, CASCADE on update)

### Indexes

- `idx_transactions_customer_id`: Fast lookup by customer
- `idx_transactions_loan_id`: Fast lookup of loan-related transactions
- `idx_transactions_transaction_date`: Time-based queries
- `idx_transactions_transaction_type`: Filter by transaction type
- `idx_transactions_transaction_status`: Filter by status
- `idx_transactions_reference`: Fast lookup by reference number
- `idx_transactions_flagged`: Partial index for flagged transactions
- `idx_transactions_customer_date`: Composite index for customer transaction history

### Business Rules

1. All transactions must be linked to a valid customer
2. Transaction amounts must be positive (direction indicated by transaction_type)
3. Balance calculations must be accurate and verified
4. Each transaction has a unique reference number
5. Transactions maintain before/after balance snapshots for audit trail
6. Suspicious transactions can be flagged for review
7. Loan-related transactions should reference the loan_id when applicable
8. System tracks transaction method and channel for analytics

---

## Views

### 1. `customer_account_summary`

**Purpose:** Provides a high-level summary of each customer's account status, including loans and transaction activity.

**Columns:**
- `customer_id`: Customer identifier
- `first_name`, `last_name`: Customer name
- `email`: Contact email
- `account_number`: Bank account number
- `account_type`: Type of account
- `account_balance`: Current balance
- `account_status`: Account status
- `total_loans`: Count of active loans
- `total_loan_balance`: Sum of outstanding loan balances
- `total_transactions`: Count of all transactions
- `customer_since`: Date customer joined

**Use Cases:**
- Customer service representatives getting quick overview
- Dashboard displays
- Account management reports

---

### 2. `active_loans_summary`

**Purpose:** Shows all active and approved loans with key details and customer information.

**Columns:**
- `loan_id`, `loan_number`: Loan identifiers
- `loan_type`: Type of loan
- `customer_id`, `customer_name`: Customer details
- `principal_amount`: Original loan amount
- `outstanding_balance`: Current balance owed
- `interest_rate`: Annual interest rate
- `monthly_payment`: Required payment
- `loan_status`, `payment_status`: Current status
- `days_past_due`: Delinquency tracking
- `disbursement_date`, `maturity_date`: Loan timeline

**Use Cases:**
- Loan portfolio management
- Collections monitoring
- Risk assessment reports
- Loan officer dashboards

---

### 3. `recent_transactions`

**Purpose:** Displays recent transactions across all customers for monitoring and reporting.

**Columns:**
- `transaction_id`, `transaction_reference`: Transaction identifiers
- `customer_id`, `customer_name`, `account_number`: Customer details
- `transaction_type`: Type of transaction
- `amount`, `currency`: Transaction value
- `description`: Transaction description
- `transaction_date`, `transaction_time`: When it occurred
- `transaction_status`: Current status
- `is_flagged`: Fraud flag indicator

**Use Cases:**
- Real-time transaction monitoring
- Fraud detection
- Customer service inquiries
- Audit and compliance reviews

---

## Triggers

### `update_updated_at_column()`

**Purpose:** Automatically updates the `updated_at` timestamp whenever a record is modified.

**Applied To:**
- `customers` table
- `loans` table

**Functionality:**
When any UPDATE operation occurs on these tables, the trigger automatically sets `updated_at` to the current timestamp, ensuring accurate tracking of record modifications without manual intervention.

---

## Sample Data

The schema includes sample data for demonstration purposes:

### Customers
- 5 sample customers with diverse account types (checking, savings, business, investment)
- Realistic personal information and credit scores
- Various locations across the United States

### Loans
- 5 sample loans covering different loan types (auto, mortgage, business, personal, student)
- Different stages of repayment
- Realistic interest rates and payment schedules

### Transactions
- 10 sample transactions demonstrating various transaction types
- Includes deposits, withdrawals, and loan payments
- Shows balance changes and different transaction methods

---

## Security and Compliance Features

### 1. **Data Privacy**
- Only last 4 digits of SSN stored (not full SSN)
- Email validation to ensure proper format
- Age verification (18+ requirement)

### 2. **Audit Trail**
- All tables include `created_at` timestamps
- `updated_at` automatically maintained via triggers
- Transaction table maintains complete history with balance snapshots

### 3. **Fraud Detection**
- `is_flagged` and `flag_reason` fields in transactions
- Partial index on flagged transactions for efficient queries
- IP address and device tracking for online transactions

### 4. **Referential Integrity**
- Foreign key constraints prevent orphaned records
- RESTRICT on delete prevents accidental data loss
- CASCADE on update maintains data consistency

### 5. **Data Validation**
- CHECK constraints ensure data quality
- Enumerated types for status fields
- Positive amount constraints
- Balance calculation validation

---

## Common Queries

### Get customer with their loans and total balance
```sql
SELECT
    c.customer_id,
    c.first_name || ' ' || c.last_name as customer_name,
    c.account_balance,
    COUNT(l.loan_id) as loan_count,
    SUM(l.outstanding_balance) as total_loan_balance
FROM demo_bank.customers c
LEFT JOIN demo_bank.loans l ON c.customer_id = l.customer_id
WHERE c.account_status = 'active'
GROUP BY c.customer_id;
```

### Get all transactions for a customer
```sql
SELECT *
FROM demo_bank.transactions
WHERE customer_id = 1
ORDER BY transaction_time DESC;
```

### Find loans that are past due
```sql
SELECT *
FROM demo_bank.loans
WHERE payment_status IN ('late', 'defaulted')
  AND loan_status = 'active'
ORDER BY days_past_due DESC;
```

### Get flagged transactions for review
```sql
SELECT *
FROM demo_bank.transactions
WHERE is_flagged = TRUE
ORDER BY transaction_time DESC;
```

### Calculate total deposits and withdrawals for a customer
```sql
SELECT
    customer_id,
    SUM(CASE WHEN transaction_type IN ('deposit', 'transfer_in') THEN amount ELSE 0 END) as total_deposits,
    SUM(CASE WHEN transaction_type IN ('withdrawal', 'transfer_out') THEN amount ELSE 0 END) as total_withdrawals
FROM demo_bank.transactions
WHERE customer_id = 1
  AND transaction_status = 'completed'
GROUP BY customer_id;
```

---

## Deployment Instructions

### Step 1: Connect to your PostgreSQL database
```bash
psql $DATABASE_URL
```

### Step 2: Execute the schema file
```bash
psql $DATABASE_URL -f demo_bank_schema.sql
```

Or from within psql:
```sql
\i demo_bank_schema.sql
```

### Step 3: Verify the schema
```sql
-- Set search path
SET search_path TO demo_bank;

-- List all tables
\dt

-- Verify sample data
SELECT COUNT(*) FROM customers;
SELECT COUNT(*) FROM loans;
SELECT COUNT(*) FROM transactions;

-- Test a view
SELECT * FROM customer_account_summary;
```

---

## Maintenance and Best Practices

### 1. **Regular Backups**
- Schedule regular backups of the demo_bank schema
- Test restore procedures periodically

### 2. **Index Maintenance**
- Monitor index usage and performance
- Rebuild indexes if fragmentation occurs
- Consider additional indexes based on query patterns

### 3. **Data Archival**
- Consider archiving old transactions after a retention period
- Maintain separate archive tables for historical data

### 4. **Performance Monitoring**
- Monitor slow queries using PostgreSQL logs
- Use EXPLAIN ANALYZE for query optimization
- Track table sizes and growth patterns

### 5. **Security**
- Regularly review and update permissions
- Audit access logs
- Keep PostgreSQL version updated
- Use SSL connections for database access

---

## Extension Ideas

### Future Enhancements
1. **Cards Table**: Credit/debit card management
2. **Beneficiaries Table**: Account beneficiaries
3. **Statements Table**: Monthly statement generation
4. **Alerts Table**: Customer notification preferences
5. **Branch Table**: Bank branch information
6. **Employee Table**: Bank employee management
7. **Audit Log Table**: Detailed audit trail for compliance
8. **Interest Calculations**: Automated interest posting
9. **Payment Schedule Table**: Detailed loan amortization
10. **Document Storage**: Links to uploaded documents (KYC, loan docs)

---

## Support and Questions

For issues or questions regarding this schema:
1. Review the SQL file comments for inline documentation
2. Check PostgreSQL documentation for specific data types or functions
3. Review the entity relationships diagram section for table relationships
4. Examine the sample data to understand expected formats

---

## Version History

- **v1.0** (2024-10-27): Initial schema creation
  - Created customers, loans, and transactions tables
  - Added indexes and constraints
  - Implemented views for common queries
  - Added triggers for auto-updating timestamps
  - Included sample data for demonstration

---

## License and Usage

This schema is provided for demonstration and educational purposes. Feel free to modify and extend it for your specific needs.
