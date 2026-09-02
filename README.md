<img width="1295" height="832" alt="telemetry" src="https://github.com/user-attachments/assets/a326cdf6-6f8a-402a-acdd-ef65bdf0e205" />

# Telemetry Ingestion Engine

An asynchronous data pipeline and monitoring dashboard engineered to handle device telemetry. The architecture leverages decoupled background tasks for database write operations, ensuring the ingestion endpoints remain highly available and responsive under load.

## Architectural Highlights:
* Asynchronous I/O: Fully non-blocking architecture from API routing down to the database layer utilizing aiosqlite and SQLAlchemy 2.0.
* Decoupled Processing: Incoming metric payloads are immediately acknowledged and handed off to background workers, protecting the main event loop from I/O latency.
* Strict Payload Validation: Enforces data integrity at the boundary using Pydantic schemas before any database interaction occurs.
* Batch Ingestion: Supports bulk CSV processing for rapid historical data backfilling or offline sensor syncs.
* Real-Time Observation: Integrated Jinja2 and Tailwind CSS dashboard for live monitoring and direct CRUD operations on sensor data.

## Technology Stack
| Layer | Technology |
| :--- | :--- |
| **Framework** | FastAPI, Pydantic |
| **Database** | SQLite, SQLAlchemy (Async), `aiosqlite` |
| **Frontend** | HTML5, Tailwind CSS, Vanilla JS, Jinja2 |
| **Concurrency** | Python `asyncio`, FastAPI `BackgroundTasks` |

## Local Development Setup

1. **Clone the repository and navigate to the project root:**
   ```bash
   git clone [https://github.com/your-username/telemetry-pipeline.git](https://github.com/your-username/telemetry-pipeline.git)
   cd telemetry-pipeline
   ```

2. **Initialize and activate a virtual environment:**
   ```bash
   python -m venv .venv
   
   # Windows
   .\.venv\Scripts\activate
   # Unix/MacOS
   source .venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Launch the application:**
   ```bash
   uvicorn src.main:app --reload
   ```

5. **Access the interfaces:**
   * **Dashboard:** `http://localhost:8080/`
   * **Interactive API Docs (Swagger UI):** `http://localhost:8080/docs`

## Core API Reference

The API is versioned under `/api/v1` and strictly returns structured JSON.

| Method | Endpoint | Function |
| :--- | :--- | :--- |
| `POST` | `/api/v1/ingest` | Queues a single telemetry payload for background processing. |
| `POST` | `/api/v1/ingest/batch` | Accepts a `.csv` file upload for bulk record ingestion. |
| `GET` | `/api/v1/metrics` | Retrieves the 50 most recent telemetry records. |
| `PUT` | `/api/v1/metrics/{id}` | Updates an existing metric record in place. |
| `DELETE` | `/api/v1/metrics/{id}` | Removes a specific metric record from the database. |

## Project Structure

```text
├── src/
│   ├── api/v1/
│   │   └── endpoints/       # API route definitions
│   ├── db/                  # Database session configuration and repository pattern
│   ├── models/              # SQLAlchemy ORM definitions
│   ├── schemas/             # Pydantic validation structures
│   ├── services/            # Background workers and business logic
│   ├── templates/           # Jinja2 HTML views
│   └── main.py              # Application factory and lifespan configuration
├── .gitignore
├── requirements.txt
└── README.md
```
