import time
import json
import os
from pathlib import Path

from backend.database import init_db
from backend.watcher import start_watcher, ARCHIVE_FOLDER, EXPORT_FOLDER, FAILED_FOLDER

print("Initializing local SQLite DB...")
init_db()

print("Starting Watchdog service...")
start_watcher()

test_file = EXPORT_FOLDER / "test_invoice_002.json"
if test_file.exists():
    test_file.unlink()
test_data = {
    "invoice_number": "INV-TEST-001",
    "operator_id": "00000000-0000-0000-0000-000000000000",
    "shift_id": "11111111-1111-1111-1111-111111111111",
    "items": [
        {
            "raw_material_text": "ANG 50x50x5",
            "entered_weight": 500.0,
            "quantity": 10.0,
            "unit": "pieces"
        }
    ]
}

print(f"Dropping file: {test_file.name}...")
with open(test_file, 'w', encoding='utf-8') as f:
    json.dump(test_data, f, indent=2)

print("Waiting for Watchdog to detect and process...")
time.sleep(3)

# Verify
archived_files = list(ARCHIVE_FOLDER.glob("test_invoice_002*"))
failed_files = list(FAILED_FOLDER.glob("test_invoice_002*"))

if archived_files:
    print(f"\nSUCCESS! File was successfully processed and moved to ARCHIVE:\n   {archived_files[0]}")
elif failed_files:
    print(f"\nFAILED! File was moved to FAILED directory:\n   {failed_files[0]}")
else:
    if test_file.exists():
        print("\nPENDING! File is still in the EXPORTS directory. Watchdog might be delayed.")
    else:
        print("\nUNKNOWN! File disappeared but is not in ARCHIVE or FAILED.")
