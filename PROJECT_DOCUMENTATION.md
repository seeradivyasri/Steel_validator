# Steel Validation Command Center Documentation

## 1. Project Title & Overview

The **Steel Validation Command Center** is a non-invasive, local-first billing advisory platform engineered specifically for the iron and steel trading industry. It solves the critical real-world problem of revenue leakage and operational errors caused by manual data entry in Tally, where complex, multidimensional steel materials are often recorded with inconsistent shorthand and misspelled dimensions. By intercepting exported Tally invoices in real-time, the system mathematically cross-verifies entered weights against strict, dynamically managed material tolerances without impeding the live billing flow. Designed for inventory owners, auditors, and administrators, the system combines lightning-fast regex parsing with an offline Phi-3 Large Language Model to auto-detect discrepancies, flag high-risk anomalies for human review, and progressively learn the localized jargon used by operators.

## 2. Tech Stack

The system is built on a modern, asynchronous Python backend, optimized for offline environments, and pairs with a lightweight, reactive frontend.

### Backend & Core Logic
- **Language**: Python 3.10+
- **Web Framework**: FastAPI (Handles robust API routing, CORS middleware, and static file mounting)
- **ASGI Server**: Uvicorn (Provides high-performance asynchronous serving)
- **Data Validation & Serialization**: Pydantic (Enforces strict schemas for API requests and responses)
- **File System Observer**: Watchdog (Runs a continuous background daemon to monitor directories for file events)

### Database & Persistence
- **RDBMS**: SQLite (Primary local relational store)
- **ORM**: SQLAlchemy (Manages complex schema relationships like Invoices -> Items -> Validation Events)

### AI & Machine Learning
- **Inference Engine**: llama-cpp-python (v0.2.90) (Enables offline, CPU-bound execution of quantized LLMs)
- **Model Hub Connector**: huggingface-hub (v0.23.0) (Used via `download_model.py` to fetch the Phi-3-mini model once)

### Frontend & UI
- **Structure**: Vanilla HTML5
- **Reactivity & State Management**: Alpine.js (Handles asynchronous data fetching, model binding, and reactive DOM updates without a build step)
- **Styling**: TailwindCSS via CDN (Utility-first framework for rapid, responsive UI design)

### DevOps & Tooling
- **Environment Management**: python-dotenv (Injects `.env` configuration securely at runtime)
- **Testing**: pytest (Testing framework)

## 3. Architecture & Folder Structure

The application adopts a modular monolith architecture. The backend is cleanly separated into routers, core logic (engines), and database layers, while a distinct background daemon handles event-driven file processing.

```text
steel-validation-center/
├── backend/
│   ├── routers/             # Defines FastAPI route handlers grouped by domain (invoices, dashboard, materials, ai_queue).
│   ├── utils/               # Contains utility modules such as `cleanup.py` for automated data retention management.
│   ├── ai_engine.py         # Interfaces with `llama.cpp` to run offline inference for alias suggestions.
│   ├── database.py          # Configures the SQLAlchemy engine, SessionLocal factory, and `get_db` dependency.
│   ├── main.py              # The FastAPI entry point; handles startup hooks, middleware, and exception handling.
│   ├── models.py            # Contains declarative SQLAlchemy base classes (Invoice, MaterialBaseline, AILearningQueue, etc.).
│   ├── parser.py            # Implements deterministic regex rules to extract dimensions (e.g., 50x50x5) and known aliases.
│   ├── schemas.py           # Pydantic models (e.g., `InvoiceResponse`, `ResolveAction`) for strict API validation.
│   ├── seed.py              # Automates database initialization, reading from `seed/` CSVs to populate baselines and categories.
│   ├── settings.py          # Centralized configuration access for dynamically updated system settings (e.g., Calibration Mode).
│   ├── validation_engine.py # The core rules engine calculating expected weights, tolerances, and assigning severities.
│   └── watcher.py           # Watchdog observer running in a separate thread to detect, move, and process exported files.
├── data/                    # Local storage volumes utilized by `watcher.py` to trace document lifecycles.
│   ├── archive/             # Destination for successfully parsed and validated invoices.
│   ├── exports/             # The active drop-zone actively monitored by Watchdog for new Tally XML/JSON/CSV files.
│   └── failed/              # Quarantine zone for files that triggered irrecoverable parsing exceptions.
├── frontend/                # Statically served, zero-build-step frontend assets.
│   ├── admin.html           # UI for managing system settings and approving/rejecting AI learning suggestions.
│   ├── alerts.html          # Detailed tabular view for investigating historical flags.
│   └── index.html           # The main reactive dashboard displaying live incoming validation flags.
├── scripts/                 # Auxiliary tools (e.g., `download_model.py` to fetch the Hugging Face AI model).
├── seed/                    # Contains `Material_List.csv` and `Material_Category.csv` used by `seed.py` for initialization.
├── .env.example             # Defines the required environment variables format.
└── requirements.txt         # Explicit list of Python package dependencies.
```

## 4. How It Works — Core Processes

The primary functionality centers on an asynchronous, event-driven pipeline that intercepts files, parses chaotic text, mathematically validates it, and delegates unknown edge-cases to AI.

1. **Detection & Ingestion (`backend/watcher.py`)**: 
   When an operator exports a file (JSON, CSV, or XML) to `data/exports`, the `InvoiceFileHandler` detects the file creation event. To ensure the file is fully written before processing, a brief timer is triggered. The file is then parsed using dedicated parsers (`parse_json`, `parse_csv`, `parse_xml`).
2. **Entity Initialization**:
   A local database session is opened. The system generates an `Invoice` record (status: Pending) and links the parsed line items (`InvoiceItem`).
3. **Material Resolution (`backend/parser.py`)**:
   For every line item, the engine calls `resolve_material(raw_text)`.
   - `extract_dimensions()` utilizes complex regex to strip metric units and identify multi-dimensional signatures (e.g., matching `50X50` or concatenated `5050` to `[50.0, 50.0]`).
   - `extract_alias()` attempts to match the string against known material categories (e.g., "ANGLE", "ISMB").
   - The engine queries active `MaterialBaseline` records, scoring matches based on alias overlaps and precise dimensional intersections. A confidence score >= 70.0 locks in a match.
4. **Tolerance Validation (`backend/validation_engine.py`)**:
   If a material is confidently resolved, `validate_invoice_item()` executes. It multiplies the matched baseline's `unit_weight` by the invoice `quantity`. It then calculates upper and lower bounds using the baseline's `tolerance_min_pct` and `tolerance_max_pct`. Based on the entered weight's deviation, the item is stamped with a `SeverityEnum` (e.g., `Passed`, `Warning`, `HighRisk`, `RequiresAudit`).
5. **AI Delegation (`backend/ai_engine.py`)**:
   If `resolve_material()` yields an `UnknownMaterial` and the global `calibration_mode` is enabled, the system forks a background daemon thread (`_run_ai_suggestion_in_background`). The text is passed to the localized Phi-3-mini model, which generates a structured JSON guess of the material category and alias. This guess is safely written to the `AILearningQueue` table with a `Pending` status—ensuring the live regex parser is never automatically polluted by AI hallucinations.
6. **Dashboard Interaction (`frontend/index.html` & `frontend/admin.html`)**:
   Items that fail validation generate a `DashboardFlag`. The Alpine.js frontend continuously polls FastAPI routes (e.g., `/api/dashboard/flags`). In the admin panel, an owner reviews the `AILearningQueue`. If approved, the AI's suggested alias is permanently appended to the respective `MaterialBaseline`, enabling the deterministic regex parser to automatically catch the localized shorthand in future transactions.

## 5. Local Setup & Installation

Follow these exact terminal commands to clone, configure, and boot the Command Center.

### Prerequisites
- Python 3.10+
- Sufficient RAM (Minimum 4GB; 8GB+ if running the local LLM).

### Installation & Execution

```bash
# 1. Navigate to your desired workspace and clone the repository (if applicable)
# git clone <repository_url>
cd steel-validation-center

# 2. Install the required Python dependencies
pip install -r requirements.txt

# 3. Prepare the environment configuration
cp .env.example .env

# 4. Initialize the database schema (SQLite) and seed the baseline tables
python backend/seed.py

# 6. (Optional) Download the ~2.4GB Phi-3-mini AI model from Hugging Face for offline alias generation
python scripts/download_model.py

# 7. Start the FastAPI application with hot-reloading
uvicorn backend.main:app --reload
```

### Environment Variables (`.env`)
You must populate the `.env` file with accurate local paths and credentials:
- `DATABASE_URL`: The connection string for SQLAlchemy (uses SQLite by default, e.g., `sqlite:///./steel_validation.db`).
- `EXPORT_FOLDER_PATH`: The absolute or relative path Watchdog will monitor for new Tally exports (default: `./data/exports`).
- `ARCHIVE_FOLDER_PATH`: Directory where successfully processed invoices are moved (default: `./data/archive`).
- `FAILED_FOLDER_PATH`: Directory where unparseable or corrupted files are quarantined (default: `./data/failed`).
- `SUPPRESSION_THRESHOLD_KG`: A numeric threshold (e.g., `5`). If a weight deviation (in KG) is smaller than this value, it is classified as `AutoIgnored` to reduce alert fatigue.
- `ADMIN_SECRET_TOKEN`: A plaintext security token required to execute sensitive API actions.

*Gotchas:* Ensure that the directories specified in the environment variables exist and possess adequate read/write permissions for the Python process, otherwise Watchdog will silently fail to move processed files.

## 6. Future Scope

Based on a strict analysis of the current implementation, here are three actionable, high-impact improvements:

1. **Implement Alembic for Idempotent Database Migrations**
   *Rationale:* `backend.main:app` relies on `Base.metadata.create_all(bind=engine)` via `init_db()`. While this successfully creates missing tables, it cannot detect schema modifications (like adding a column to `InvoiceItem`), making future development fragile without a proper migration tool like Alembic.
2. **Expose the Retry Queue & Dead-Letter Queue to the Frontend**
   *Rationale:* `watcher.py` implements an in-memory `_retry_queue` for transient DB errors and moves irrecoverable files to `FAILED_FOLDER_PATH`. Building a dedicated "Failed Invoices" view in the UI would allow operators to manually inspect, correct, and replay these files without requiring direct filesystem access.
3. **Upgrade Frontend Security with JWT Authentication**
   *Rationale:* The application currently relies on a static `ADMIN_SECRET_TOKEN` for administrative tasks, but the main dashboard (`index.html`) relies purely on CORS middleware for protection. Implementing robust JWT-based session handling would properly secure sensitive billing anomaly data from unauthorized network access.

## 7. Technical File Overview

While the system is designed to be seamless for the business, it is powered by a strictly organized collection of files. Here is the exact role of every operational file in the software:

* backend/models.py: Defines the structure of the database tables where invoices and materials are saved.
* backend/main.py: The starting point of the software that launches the web server and the background monitoring process.
* backend/watcher.py: The background tool that constantly observes the export folder for newly saved Tally invoices.
* backend/parser.py: The text analysis script that breaks down messy typed material names into clean numbers and categories.
* backend/validation_engine.py: The core calculator that runs the math to compare entered weights against expected standard weights.
* backend/ai_engine.py: The artificial intelligence interface that guesses the meaning of unknown material names completely offline.
* backend/settings.py: The control center file that manages temporary system states, like whether Calibration Mode is currently active.
* backend/database.py: The connection manager that allows the Python software to securely talk to the local SQLite database.
* backend/routers/ai_queue.py: The web pathway that handles approving or rejecting the artificial intelligence's guesses.
* backend/routers/dashboard.py: The web pathway that sends the live metrics and discrepancy alerts to the owner's screen.
* backend/routers/invoices.py: The web pathway that provides historical data about past processed invoices.
* backend/routers/materials.py: The web pathway used to search and update the master list of steel products.
* backend/routers/reason_codes.py: The web pathway that supplies the dropdown options for operators explaining an error.
* backend/utils/cleanup.py: The automated maintenance script that permanently deletes files and database records older than 90 days.
* backend/utils/confidence.py: The scoring system that grades how mathematically certain the system is about a material match.
* backend/utils/suppression.py: The filtering rule that ignores tiny weight differences below the acceptable threshold.
* frontend/index.html: The main visual dashboard where the business owner watches live validation alerts.
* frontend/admin.html: The visual control panel where the owner adjusts settings and trains the artificial intelligence.
* frontend/alerts.html: The small visual popup screen that operators see when they make a billing mistake.
* seed/Material_List.csv: The master spreadsheet containing all the correct industry weights and dimensions for steel products.
* seed/Material_Category.csv: The list grouping similar steel products together, like all pipes or all beams.
* scripts/download_model.py: The one-time setup tool used to pull the artificial intelligence brain from the internet to the local computer.
* requirements.txt: The official list of third-party software packages the system needs installed to run.
* .env: The active configuration file that securely holds local database connections, folder paths, and system settings.
