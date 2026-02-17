# 🃏 Casino API

[![Python Version](https://img.shields.io/badge/python-3.11%2B-blue.svg)](https://www.python.org/)
[![Framework](https://img.shields.io/badge/framework-FastAPI-009688.svg)](https://fastapi.tiangolo.com/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](https://opensource.org/licenses/MIT)

An enterprise-level, real-money capable Blackjack backend built with **Python 3.11+**, **FastAPI**, and **SQLAlchemy**. This system implements clean architecture, SOLID principles, and strict atomic transaction handling for financial integrity.

## 🚀 Features

-   **Secure Wallet System:** Atomic balance updates with pessimistic database locking (`FOR UPDATE`) to prevent double-spending and race conditions.
-   **Pure Game Engine:** A decoupled `BlackjackEngine` using cryptographically secure RNG (`secrets` module).
-   **Persistent Sessions:** Multi-step game state management (Start -> Hit/Stand -> Settle).
-   **Clean Architecture:** Strict separation of concerns between Repositories, Services, and API Routes.
-   **Security:** JWT-based Authentication and full ownership validation for every game action.
-   **Database Migrations:** Managed by Alembic for safe schema evolution.

---

## 🏗 Project Structure

```text
app/
├── main.py              # App entry point & global exception handling
├── core/                # Configuration & Security (JWT/Bcrypt)
├── db/                  # Database session & Base model definitions
├── models/              # SQLAlchemy Models (User, Wallet, Game)
├── schemas/             # Pydantic v2 validation schemas
├── repositories/        # Data access layer (CRUD & Locking)
├── services/            # Business logic (Wallet & Blackjack orchestrators)
├── api/
│   ├── deps.py          # Dependency injection (Auth/DB)
│   └── routes/          # Versioned API endpoints
└── tests/               # Pytest suite
```

---

## 🛠 Tech Stack

-   **Runtime:** Python 3.11+
-   **Web Framework:** FastAPI (Asynchronous)
-   **Database:** PostgreSQL (via SQLAlchemy 2.0)
-   **Migrations:** Alembic
-   **Security:** Passlib (Bcrypt), Python-Jose (JWT)
-   **Validation:** Pydantic v2

---

## 🚦 Getting Started

### 1. Environment Setup
Clone the repository and create a `.env` file:
```bash
git clone https://github.com/your-repo/blackjack-api.git
cd blackjack-api
python -m venv venv
source venv/bin/activate  # venv\Scripts\activate on Windows
pip install -r requirements.txt
```

### 2. Configure Database
Update your database URL in `.env` file:
```env
DATABASE_URL=postgresql://user:password@localhost:5432/blackjack_db
SECRET_KEY=your_super_secret_key_here
```

### 3. Run Migrations
```bash
alembic revision --autogenerate -m "Initial schema"
alembic upgrade head
```

### 4. Start the Server
```bash
uvicorn app.main:app --reload
```
The API will be available at `http://localhost:8000`.
Access Interactive Documentation (Swagger) at `http://localhost:8000/api/docs`.

---

## 🃏 Blackjack Rules Implemented

-   **Standard Deck:** 52 cards (2-10 face value, J/Q/K = 10, Ace = 1 or 11).
-   **Dealer AI:** Must hit until score is 17 or higher.
-   **Payouts:**
    -   Natural Blackjack (Initial 21): **2.5x**
    -   Standard Win: **2x**
    -   Push (Tie): **Bet Returned**
    -   Bust/Loss: **0x**
-   **State Masking:** Dealer's second card and score are hidden from the API response until the player stands or busts.

---


## 🔐 Security & Integrity

-   **Financial Safety:** All wallet operations utilize database transactions. If a game action fails after funds are deducted, the transaction rolls back automatically.
-   **Authorization:** All game endpoints check for `game.user_id == current_user.id` to prevent unauthorized session manipulation.
-   **RNG:** Uses `secrets.choice` instead of `random.choice` to ensure outcomes are statistically unpredictable.

---

## 📝 API Response Format

All responses follow a standardized JSON structure for consistent frontend integration:

```json
{
    "success": true,
    "data": { ... },
    "message": "Action description"
}
```
