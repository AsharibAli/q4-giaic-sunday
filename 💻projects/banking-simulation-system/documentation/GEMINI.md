# Project Overview

This project is a banking simulation system with a backend and a frontend.

The backend is a RESTful API service built with FastAPI (Python). It handles business logic, data storage, and provides endpoints for user authentication, account management, and transaction management. The database is SQLite, and SQLAlchemy is used as the ORM.

The frontend is a web application built with Next.js (React) and TypeScript. It is intended to be a single-page application that consumes the backend API to provide a user interface for the banking simulation. The frontend will use Tailwind CSS for styling.

# Building and Running

## Backend

To run the backend, you need to have Python and `uv` installed.

1.  **Navigate to the backend directory:**
    ```bash
    cd backend
    ```
2.  **Install dependencies:**
    ```bash
    uv sync
    ```
3.  **Run the development server:**
    ```bash
    uv run uvicorn main:app --reload
    ```

The API will be available at `http://127.0.0.1:8000`.

## Frontend

To run the frontend, you need to have Node.js and npm installed.

1.  **Navigate to the frontend directory:**
    ```bash
    cd frontend
    ```
2.  **Install dependencies:**
    ```bash
    npm install
    ```
3.  **Run the development server:**
    ```bash
    npm run dev
    ```

The frontend will be available at `http://localhost:3000`.

# Development Conventions

## Backend

The backend follows a modular structure, separating concerns into `api`, `core`, `crud`, `db`, and `schemas`.
-   **API Endpoints:** Defined in `backend/api/v1/endpoints/`.
-   **Database Models:** Defined in `backend/db/models.py`.
-   **Pydantic Schemas:** Defined in `backend/schemas/`.
-   **CRUD Operations:** Defined in `backend/crud/`.

## Frontend

The frontend is structured using the Next.js App Router.
-   **Pages:** The frontend is not yet implemented and contains the default Next.js template. The proposed structure in `documentation/frontend.md` suggests that pages will be organized in the `frontend/app/` directory.
-   **Components:** Reusable components from shadcn/ui are placed in `frontend/components/`.
-   **API Calls:** Functions for making API calls to the backend should be placed in `frontend/lib/api.ts`.
-   **Styling:** Tailwind CSS is used for styling.
