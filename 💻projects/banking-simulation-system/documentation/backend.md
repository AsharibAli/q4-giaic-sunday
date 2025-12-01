# Backend Product Requirements Document: Banking Simulation System

## 1. Overview

This document outlines the product requirements for the backend of the Banking Simulation System. The backend will be a RESTful API service responsible for business logic, data storage, and providing the necessary endpoints for the frontend application.

## 2. Tech Stack

- **Framework:** FastAPI
- **Language:** Python 3.11+
- **Package Manager & Venv:** UV
- **Database:** SQLite (for simplicity in this simulation) with `sqlalchemy` as the ORM.
- **Data Validation:** Pydantic

## 3. Core Features & API Endpoints

The API will be versioned, e.g., `/api/v1/...`.

### 3.1. User Authentication
- `POST /auth/register`: Register a new user.
  - Request Body: `{ "username": "...", "email": "...", "password": "..." }`
  - Response: `{ "message": "User created successfully" }`
  - Logic: Hashes the password, creates a new user in the database, and creates default checking and savings accounts for the user.
- `POST /auth/login`: Log in a user.
  - Request Body: `{ "username": "...", "password": "..." }`
  - Response: `{ "access_token": "...", "token_type": "bearer" }`
  - Logic: Verifies credentials and returns a JWT token.

### 3.2. Account Management
- `GET /accounts/`: Get all accounts for the logged-in user.
  - Authentication: Required (JWT)
  - Response: `[{ "account_id": "...", "account_type": "...", "balance": "..." }, ...]`
- `GET /accounts/{account_id}`: Get details for a specific account.
  - Authentication: Required (JWT)
  - Response: `{ "account_id": "...", "account_type": "...", "balance": "..." }`

### 3.3. Transaction Management
- `POST /transactions/deposit`: Deposit funds into an account.
  - Authentication: Required (JWT)
  - Request Body: `{ "account_id": "...", "amount": "..." }`
  - Response: `{ "message": "Deposit successful", "new_balance": "..." }`
- `POST /transactions/withdraw`: Withdraw funds from an account.
  - Authentication: Required (JWT)
  - Request Body: `{ "account_id": "...", "amount": "..." }`
  - Response: `{ "message": "Withdrawal successful", "new_balance": "..." }`
  - Logic: Checks for sufficient funds before processing.
- `POST /transactions/transfer`: Transfer funds between the user's accounts.
  - Authentication: Required (JWT)
  - Request Body: `{ "from_account_id": "...", "to_account_id": "...", "amount": "..." }`
  - Response: `{ "message": "Transfer successful" }`
  - Logic: Checks for sufficient funds in the source account.
- `GET /transactions/{account_id}`: Get transaction history for a specific account.
  - Authentication: Required (JWT)
  - Response: `[{ "transaction_id": "...", "type": "...", "amount": "...", "timestamp": "...", "balance_after_transaction": "..." }, ...]`

## 4. Database Schema

- **users**
  - `user_id` (PK, UUID)
  - `username` (String, unique)
  - `email` (String, unique)
  - `hashed_password` (String)
  - `created_at` (DateTime)
- **accounts**
  - `account_id` (PK, UUID)
  - `user_id` (FK to users)
  - `account_type` (String, e.g., "checking", "savings")
  - `balance` (Numeric)
  - `created_at` (DateTime)
- **transactions**
  - `transaction_id` (PK, UUID)
  - `account_id` (FK to accounts)
  - `transaction_type` (String, e.g., "deposit", "withdrawal", "transfer")
  - `amount` (Numeric)
  - `timestamp` (DateTime)
  - `balance_after_transaction` (Numeric)

## 5. Proposed Codebase Structure

```
/
├── main.py             # FastAPI app entry point
├── api/
│   ├── __init__.py
│   ├── v1/
│   │   ├── __init__.py
│   │   ├── endpoints/
│   │   │   ├── __init__.py
│   │   │   ├── auth.py
│   │   │   ├── accounts.py
│   │   │   └── transactions.py
│   │   └── api.py        # v1 router
├── core/
│   ├── __init__.py
│   ├── config.py         # Configuration settings
│   └── security.py       # Password hashing, JWT handling
├── crud/
│   ├── __init__.py
│   ├── user.py
│   ├── account.py
│   └── transaction.py    # Functions to interact with the database
├── db/
│   ├── __init__.py
│   ├── database.py       # Database session management
│   └── models.py         # SQLAlchemy models
├── schemas/
│   ├── __init__.py
│   ├── user.py
│   ├── account.py
│   └── transaction.py    # Pydantic schemas for request/response
└── tests/
    ├── ...
```
