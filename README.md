# Steel Validation Command Center

## What is this?
The Steel Validation Command Center is a non-invasive, local-first billing advisory platform engineered specifically for the iron and steel trading industry. It monitors Tally invoice exports in real-time, detecting revenue leakage and operational errors. By mathematically cross-verifying entered weights against strict, dynamically managed material tolerances, it flags high-risk anomalies without impeding the live billing flow. It combines lightning-fast regex parsing with an offline Phi-3 AI model to automatically detect discrepancies and progressively learn localized warehouse jargon.

## Prerequisites
- Python 3.10+
- pip
- Sufficient RAM (Minimum 4GB; 8GB+ if running the local LLM).

## Setup in 4 steps
1. `pip install -r requirements.txt`
2. Create an `.env` file in the root directory and configure it (e.g., set `DATABASE_URL=sqlite:///./steel_validation.db`)
3. `python backend/seed.py`
4. `uvicorn backend.main:app --reload`

## Open the app
http://localhost:8000/app

## How Tally integration works
To integrate the system, set Tally to auto-export invoices as XML, JSON, or CSV files into the directory specified by your `EXPORT_FOLDER_PATH` environment variable. The background watchdog service actively monitors this folder. When a file drops, the system waits for a brief timer to ensure it is fully written, then parses it instantly and processes it through the validation engine.

## AI Alias Learning Engine

### What it does
When Calibration Mode is ON and the regex parser cannot identify a material string (an `UnknownMaterial`), the system forks a background daemon thread. The offline Phi-3-mini model quietly guesses the material category and alias, and saves that guess in the `AILearningQueue` table with a `Pending` status. This ensures the live regex parser is never automatically polluted by AI hallucinations.

### Why you must approve
The AI can be wrong. It might look at a strange abbreviation and guess the wrong material. If a wrong answer went into weight calculations, the numbers would be incorrect. Your manual approval step catches mistakes before they cause financial damage and permanently appends the correct alias to the `MaterialBaseline`.

### The weekly workflow
1. Go to Admin Panel → AI Suggestions tab
2. Turn Calibration Mode ON
3. Drop Tally files as normal
4. Come back at end of day — review what the AI suggested
5. For each suggestion: select the correct material from the dropdown, edit the alias if needed, click Approve
6. After a few weeks, the regex parser automatically catches all your local words based on your approvals — turn Calibration Mode OFF

### Setup (one-time)
Run `python scripts/download_model.py`.
Downloads ~2.4GB from Hugging Face (an AI model hosting website). After download, runs 100% offline. Hugging Face is never used again. Restart the server after downloading.

### Hardware
4GB+ free RAM, 4 CPU cores, no GPU required, no internet required after the initial download.

### If model not downloaded
The system works exactly as before — regex only. The validation engine continues running at lightning speed without the AI fallback, with zero crashes or impact on performance.

## Calibration mode
It is highly recommended to use Calibration Mode for the first 1–2 weeks of deployment. While enabled, the AI alias learning engine activates for unknown materials, saving them silently in the queue. Alert popups for unknown materials are suppressed during this learning phase so that operators are not disrupted.

## What this system will never do
- Modify Tally data (It is strictly a read-only advisory tool)
- Block billing operations
- Classify anything as confirmed fraud automatically (It only highlights mathematical errors; the business owner always makes the final judgment call)
- Require internet connectivity (after the initial one-time model download)

## Performance targets
- Invoice processing < 2 seconds
- Dashboard load < 1 second
- Folder detection latency < 500ms
