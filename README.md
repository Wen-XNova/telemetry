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
LayerTechnologyFrameworkFastAPI, PydanticDatabaseSQLite, SQLAlchemy (Async), aiosqliteFrontendHTML5, Tailwind CSS, Vanilla JS, Jinja2ConcurrencyPython asyncio, FastAPI BackgroundTasks
