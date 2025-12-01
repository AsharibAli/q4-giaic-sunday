# Banking Simulation System

This project is a full-stack banking simulation system featuring a RESTful backend API and a modern web application frontend. It allows users to register, log in, view accounts, and perform basic transactions like deposits, withdrawals, and transfers.

## Tech Stack

- **Backend:** UV, Python, FastAPI, Pydantic, SQLAlchemy, SQLite 
- **Frontend:** Next.js, React, TypeScript, Tailwind CSS, shadcn/ui

## Getting Started

Follow these instructions to get a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

Make sure you have the following installed on your system:

- [Node.js](https://nodejs.org/en/download) 
- [Python](https://www.python.org/downloads/)
- [uv](https://docs.astral.sh/uv/getting-started/installation)

### Cloning the Repository

First, clone the repository to your local machine:

```bash
git clone https://github.com/asharibali/banking-simulation-system
cd banking-simulation-system
```

## Installation and Running

The project is split into two main parts: a `backend` service and a `frontend` application. You will need to run them in two separate terminals.

### Backend (API)

1.  **Navigate to the backend directory:**
    ```bash
    cd backend
    ```

2.  **Install Python dependencies:**
    ```bash
    uv sync
    ```

3.  **Run the development server:**
    ```bash
    uv run uvicorn main:app --reload
    ```

The backend API will be available at `http://127.0.0.1:8000`.

### Frontend (Web Application)

1.  **Navigate to the frontend directory:**
    ```bash
    cd frontend
    ```

2.  **Install Node.js dependencies:**
    ```bash
    npm install
    ```

3.  **Run the development server:**
    ```bash
    npm run dev
    ```

The frontend application will be available at `http://localhost:3000`.

## Contributions
Contributions are welcome! Feel free to submit issues or pull requests.

**Build with 💗 by Asharib Ali**