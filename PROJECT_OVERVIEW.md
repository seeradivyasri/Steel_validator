# Project Overview

## 1. What This System Does — In One Paragraph

Billing operators in a steel trading business frequently enter material weights manually into Tally ERP, making it nearly impossible to catch errors or deliberate manipulation in real time. This system solves that problem by silently monitoring those Tally exports as they happen. It instantly checks the entered math against industry standard weights and tolerances. If something does not add up, it alerts the business owner immediately without interrupting the billing operators at all. Ultimately, it acts as a digital auditor that protects the company's revenue.

## 2. The Problem It Solves

Weight entry errors that go unnoticed for months can severely impact profit margins. Operators handling hundreds of invoices a day can easily mistype a digit or select the wrong material size, and because these documents are filed away immediately, the mistake is rarely caught until an audit happens much later.

Gradual financial leakage from consistent small discrepancies is another major threat. A few kilograms shaved off every invoice might seem insignificant on a single bill, but across thousands of transactions, it amounts to massive inventory losses that are incredibly difficult to trace.

Finally, business owners currently have no way to see billing accuracy without checking every single invoice manually. This lack of visibility forces owners to rely purely on trust, leaving them blind to both accidental errors and systemic, deliberate manipulation on the warehouse floor.

## 3. How It Works — Step by Step

1. The billing operator enters an invoice in Tally ERP as they normally would.
2. Tally automatically saves a copy of the invoice file into a specific folder on the computer.
3. The folder watcher instantly detects the new file and reads its contents.
4. The system attempts to match the typed material names against the master database.
5. If the material name is written in an unknown slang or shorthand, the artificial intelligence silently guesses what it means and saves the guess for the owner to review later.
6. For recognized materials, the system calculates the exact weight the steel should be based on its dimensions.
7. It compares the expected weight to what the operator actually typed.
8. If the difference is too large, the system generates an alert.
9. The operator sees a quick popup asking them for a reason, while the owner sees the discrepancy on their dashboard and takes action.

## 4. System Architecture

The system uses a tightly integrated design where a background process monitors files and feeds them to a central checking engine, which then saves the results for a web-based dashboard to display.

* The Folder Watcher: A background tool that constantly monitors the export folder for new Tally files. It exists to ensure that every single invoice is captured the moment it is saved.
* The Material Parser: A text analysis tool that breaks down messy, typed material names into clean dimensions and categories. It exists because operators rarely type product names exactly the same way twice.
* The Validation Engine: The core mathematical tool that calculates expected weights and checks for discrepancies. It exists to provide the actual auditing logic that catches errors.
* The Master Material Database: A local SQLite storage system holding all the correct weights, tolerances, and past invoices. It exists to serve as the single source of truth for the entire application.
* The Owner Dashboard: A web page that displays live alerts and daily accuracy metrics. It exists to give the business owner immediate, clear visibility into operations.
* The Operator Alert Popup: A small screen that appears when a discrepancy is caught, asking the operator to provide a reason. It exists to capture context from the warehouse floor before the operator forgets what happened.
* The Admin Panel: A control center for adjusting system settings. It exists so the owner can manage how the system behaves without needing a programmer.
* The AI Alias Learning Engine: An offline artificial intelligence that guesses the meaning of unknown material names. It exists to reduce the manual work of matching new slang terms to standard products.
* The Fine-Tuning Pipeline: A collection point for all the AI guesses that the owner has approved. It exists to gather the training data needed to eventually make the artificial intelligence smarter, though the automated training process is not yet fully built.

## 5. Technology Used

* Python: Programming Language. It is the core language used to write the entire backend logic. It was chosen for its excellent data processing and artificial intelligence capabilities.
* FastAPI: Web Framework. It handles the communication between the backend logic and the web dashboard. It was chosen because it is incredibly fast and easy to build with.
* Uvicorn: Web Server. It runs the FastAPI application and serves it to the browser. It was chosen because it handles multiple requests simultaneously without slowing down.
* SQLite: Database. It stores all the system's data locally in a single file. It was chosen because it requires no complex installation and keeps all data strictly on the local machine.
* SQLAlchemy: Database Tool. It allows the Python code to talk to the database easily. It was chosen to make writing and reading data safer and more organized.
* Pydantic: Data Validation Tool. It ensures that any data moving through the system is formatted correctly. It was chosen to prevent crashes caused by unexpected or missing information.
* Watchdog: File Monitoring Tool. It tells the system the exact millisecond a new file appears in a folder. It was chosen because it is highly reliable for background monitoring.
* Llama.cpp and Hugging Face Hub: Artificial Intelligence Tools. They run the offline AI model directly on the local computer's processor. They were chosen to ensure the AI could work without sending any private billing data to the internet.
* Alpine.js: Frontend Tool. It manages the interactive elements on the web dashboard. It was chosen because it is lightweight and doesn't require complex build steps.
* Tailwind CSS: Design Tool. It provides the visual styling for the web pages. It was chosen to rapidly build a clean, professional interface.

## 6. Key Features

* Real-time invoice monitoring: The system watches the export folder and processes files the moment they appear. The owner experiences instant updates, ensuring that no problematic invoice slips by unnoticed before the truck leaves the yard.
* Regex-based material parsing: A pattern matching system that breaks down messy text into numbers and standard names. The operator can type however they want, and the system still understands it, which provides immense value by not forcing operators to change their habits.
* Confidence scoring: The system grades how sure it is that it identified the right material. The owner can see this score, helping them decide whether to trust the system's math or manually review the invoice.
* Severity classification: Invoices are tagged as Passed, Warning, High Risk, or Requires Audit based on how far off the weight is. This allows the owner to quickly prioritize which alerts need immediate attention.
* Automatic suppression of tiny deviations: If a weight difference is only a few kilograms below the threshold, the system ignores it. This prevents the owner from being spammed with alerts for acceptable, minor rusting or scale differences.
* Calibration Mode: A temporary setting where the system stays quiet and learns the local terminology without generating alerts. It ensures that when the system is finally turned on, it is highly accurate and not disruptive.
* AI alias suggestion and human approval flow: When the system encounters a completely new word, the AI guesses what it means, but waits for the owner to approve it. This protects the business from AI mistakes while still automating the learning process over time.
* Fine-tuning pipeline: The system collects all the corrected AI guesses into a specific database table. While the automated retraining script isn't fully built yet, this ensures the valuable data is safely stored for future AI upgrades.
* 90-day auto-cleanup: A utility script automatically deletes old invoices and files after three months. This ensures the local computer does not run out of storage space over time, keeping the system maintenance-free.
* Operator shift tracking: When an operator interacts with a popup alert, their action is logged as an operator intervention. This provides accountability, letting the owner see exactly how discrepancies are being handled on the floor.
* Audit log: Every time a flag is resolved, a permanent record is created explaining who closed it and why. This gives the owner a complete, tamper-proof history of all billing issues and how they were handled.

## 7. What the Owner Sees — Dashboard Walkthrough

When you open the dashboard, you see a clean, professional control center designed for immediate visibility. At the top, a metrics bar highlights your pending alerts, the number of high-risk items today, your total invoice count, and a calculation of potential financial leakage in kilograms. Below that, discrepancy cards feed in automatically, showing exactly what the operator entered versus what the system mathematically expected, complete with a severity badge. You can use simple dropdown filters to narrow down alerts by date or severity level. When you are ready to handle an alert, you have three clear action buttons to either mark it as safe, log it as an entry error, or escalate it for a full audit review. From the top navigation, you can access the Admin Panel to toggle system settings, or click into the AI Suggestions tab to review and approve the intelligent guesses the system has made about unknown materials.

## 8. What the Operator Experiences

From the billing operator's perspective, the system is almost entirely invisible during normal, accurate billing. They continue their daily routine of entering weights and generating invoices in Tally exactly as they always have, without any slowdowns or new software to learn.

However, if they enter a weight that significantly deviates from the mathematical expectation, a small alert popup appears on their screen. This screen simply informs them that a discrepancy was detected and asks them to provide a reason for the unusual weight before they move on.

They are presented with a simple reason code dropdown menu, allowing them to quickly select common explanations like "Supplier Variation" or "Custom Fabrication." This exists so that the business owner has immediate context for the error directly from the warehouse floor, preventing unnecessary interrogations later in the day.

## 9. Data and Privacy

All data is stored strictly on the local computer hosting the system inside a secure, local database file. The system does not connect to the cloud or the internet to process invoices; it only requires an internet connection once during the initial setup to download the artificial intelligence model. It is designed as a read-only advisory tool, meaning it cannot modify, delete, or interfere with any of your original Tally data. Access to the dashboard is restricted to devices on your local network, ensuring that only you and your authorized staff can view the financial alerts. Finally, to ensure your computer does not run out of storage, the system includes a 90-day auto-cleanup feature that permanently deletes old records, keeping your data footprint small and manageable.

## 10. Current Status and What Was Built

Backend: A fully operational, high-speed routing and validation engine is completely built and functioning. It successfully monitors folders, parses files, calculates weights, and saves all data to the local database.

Frontend: A responsive, real-time dashboard is fully built and deployed. The metrics bar, the live alert feed, the action buttons, the admin settings, and the operator popup screen are all functional and connected to the backend.

AI Layer: The offline artificial intelligence engine is built and working. It successfully loads the model, processes unknown material strings, generates guesses, and holds them in a queue for the owner to approve.

Fine-Tuning Pipeline: The data collection aspect of the pipeline is built; the system successfully stores every human-approved AI guess in the database. However, the automated script to mathematically retrain the AI model on this new data does not currently exist in the codebase.

## 11. Limitations and Known Boundaries

This system is strictly an advisory tool. It does not prevent an operator from finalizing a wrong bill in Tally; it only flags the error after it is exported. Furthermore, the system will never automatically classify a discrepancy as confirmed fraud. It strictly highlights mathematical errors, leaving the final judgment call entirely up to the business owner. Its mathematical accuracy depends entirely on the quality and correctness of the data provided in the initial master material spreadsheet. While the artificial intelligence is helpful, it can suggest wrong aliases, which is exactly why the human approval step is mandatory before the system permanently learns a new word. To avoid overwhelming the owner with false alarms, Calibration Mode must be run for a few weeks so the system can learn the specific, localized terminology your warehouse uses. Finally, because this is a privacy-first system, it works on your local network only; you cannot check your dashboard from a mobile phone while away from the office without a specialized network setup.

## 12. Glossary

* Tally ERP: The accounting and inventory software used by the business to generate bills.
* Regex: A pattern matching system that searches text for specific structures, like looking for numbers formatted as dimensions.
* Confidence Score: A percentage grade that tells you how sure the system is that it matched the right product.
* Severity Level: A category tag (like Warning or High Risk) that indicates how severe a weight difference is.
* Calibration Mode: A learning phase where the system stays quiet and memorizes your local warehouse slang instead of sending alerts.
* GGUF model: A specialized file format that allows large artificial intelligence programs to run quickly on standard, everyday computers.
* Fine-Tuning: The process of teaching an artificial intelligence new, highly specific information to make it smarter over time.
* LoRA: A technical method used to efficiently fine-tune an artificial intelligence without requiring a supercomputer.
* Alias: A slang term or abbreviation that an operator types instead of the official product name.
* Material Baseline: The official master record of a product, containing its correct dimensions and acceptable weight ranges.
* Validation Engine: The core calculator in the software that compares the typed weight against the expected mathematical weight.
* Dashboard Flag: A visual alert that pops up on the owner's screen when an error is caught.
* Audit Log: A permanent, unchangeable record of every alert and how it was resolved by the staff.
* Watchdog: A background software tool that instantly notices when a new file is saved to a folder.
* SQLite: The specific local database technology used to safely store all the system's information on your computer.

## 13. Technical File Overview

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

Document generated from live codebase on 2026-06-21.
