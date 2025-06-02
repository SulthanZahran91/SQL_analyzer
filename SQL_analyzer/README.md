# SQL Query Analyzer

## Overview

The SQL Query Analyzer is a web-based tool designed to help developers and analysts understand, debug, and refactor complex SQL queries. It parses SQL scripts, extracts key components such as Common Table Expressions (CTEs), temporary tables, table variables, and subqueries (optional), and presents them in an organized manner. This allows users to gain clearer insights into the structure and flow of their SQL code.

## Features

-   **SQL Parsing**: Breaks down SQL queries into their fundamental components.
-   **Component Extraction**: Identifies CTEs, temporary tables, table variables, and subqueries.
-   **Individual Component Queries**: Generates separate, runnable queries for each extracted component.
-   **Component Statistics**: Provides a summary of the number and types of components found.
-   **File Upload**: Supports uploading `.sql` or `.txt` files containing SQL scripts.
-   **SQL Input with Syntax Highlighting**: Offers a code editor with syntax highlighting for direct SQL input.
-   **Include Subqueries Option**: Allows users to choose whether to extract subqueries as distinct components.
-   **Dark/Light Theme Support**: Provides theme options for user interface preference.
-   **Responsive Design**: Adapts to different screen sizes for usability on various devices.

## Technologies Used

-   **Frontend**:
    -   Vue.js 3
    -   Vite (Build Tool)
    -   Pinia (State Management)
    -   Tailwind CSS (Styling)
    -   Codemirror (SQL Editor with Syntax Highlighting)
-   **Backend**:
    -   Python 3
    -   FastAPI (Web Framework)
-   **SQL Parsing Logic**:
    -   Custom Python-based parser (`sql_parser.py` located in the backend).

## Project Structure

The project is organized into two main directories:

-   `SQL_analyzer/`: Contains the Vue.js frontend application.
-   `SQL_analyzer_backend/`: Contains the Python FastAPI backend server and SQL parsing logic.

## Prerequisites

-   **Node.js**: Latest LTS version recommended.
-   **bun**: For frontend package management and running scripts (alternative to npm/yarn).
-   **Python**: Version 3.8 or higher.
-   **pip**: Python package installer.

## Recommended IDE Setup

-   [VSCode](https://code.visualstudio.com/)
-   [Volar](https://marketplace.visualstudio.com/items?itemName=Vue.volar) (ensure Vetur is disabled if previously installed).

## Setup and Installation

### Backend (`SQL_analyzer_backend/`)

1.  **Navigate to the backend directory**:
    ```bash
    cd SQL_analyzer_backend
    ```
2.  **Create and activate a virtual environment** (optional but highly recommended):
    ```bash
    python -m venv venv
    # On Windows
    # venv\Scripts\activate
    # On macOS/Linux
    # source venv/bin/activate
    ```
3.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

### Frontend (`SQL_analyzer/`)

1.  **Navigate to the frontend directory**:
    ```bash
    cd SQL_analyzer
    ```
    (If you are in `SQL_analyzer_backend`, you'd use `cd ../SQL_analyzer`)

2.  **Install dependencies**:
    ```bash
    bun install
    ```

## Running the Application

### Backend

1.  Ensure you are in the `SQL_analyzer_backend` directory.
2.  If you created a virtual environment, make sure it's activated.
3.  Start the FastAPI server:
    ```bash
    uvicorn main:app --reload --port 8000
    ```
    The backend will typically be available at `http://localhost:8000`.

### Frontend

1.  Ensure you are in the `SQL_analyzer` directory.
2.  Start the Vite development server:
    ```bash
    bun dev
    ```
    The frontend will typically be available at `http://localhost:5173` and will proxy API requests to the backend.

## API Documentation

Once the backend is running, you can access the automatically generated API documentation:

-   **Swagger UI**: `http://localhost:8000/docs`
-   **ReDoc**: `http://localhost:8000/redoc`

## User Guide

For detailed instructions on how to use the application's features, please refer to the [User Guide](./USER_GUIDE.md).

## How It Works

1.  The user inputs an SQL query directly into the text editor or uploads an SQL file via the frontend interface.
2.  The frontend application sends the SQL query string (and any options like "include subqueries") to the backend API.
3.  The FastAPI backend receives the request and uses its custom SQL parser to analyze the query.
4.  The parser extracts components (CTEs, temp tables, etc.), generates individual queries for them, and calculates statistics.
5.  The backend sends the processed results (components, queries, statistics, formatted output) back to the frontend.
6.  The frontend displays these results in their respective tabs (Results, Statistics, Formatted View).

## Linting

To check the frontend code for linting issues:

1.  Navigate to the `SQL_analyzer` directory.
2.  Run:
    ```bash
    bun lint
    ```

## Building for Production (Frontend)

1.  Navigate to the `SQL_analyzer` directory.
2.  Run:
    ```bash
    bun run build
    ```
    This will create a `dist` folder with the production-ready static assets.

## Contributing

Contributions are welcome! If you have suggestions for improvements or encounter any issues, please feel free to open an issue or submit a pull request.

## License

This project is currently unlicensed. Consider adding a license like MIT if you wish to share it under specific terms.
