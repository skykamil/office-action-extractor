# Office Action Extractor

[![Python application](https://github.com/skykamil/office-action-extractor/actions/workflows/python-app.yml/badge.svg)](https://github.com/skykamil/office-action-extractor/actions/workflows/python-app.yml)

A tool for automatically extracting key data (letter type, application number, key dates) from patent Office Action letters (PDF) and storing them in a database, with a simple web interface for uploading files and reviewing results.

## Features

- Text extraction from PDF files (regex-based)
- Supports multiple date and application number formats (tested on USPTO, Canadian, and Korean documents)
- Multi-file upload
- Results stored in SQLite
- Simple web interface (upload form + results table)
- Custom exception hierarchy with clear, mapped HTTP error responses (unsupported format, corrupted file, missing file, empty document)
- Uploaded files are sanitized against path traversal and deleted after processing — nothing is kept on disk beyond the request

## Requirements

- Python 3.12+ (tested on 3.14)

## Tech Stack

- Python
- FastAPI + Uvicorn
- SQLite3
- pdfplumber
- pytest
- HTML / CSS / JavaScript (frontend)

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/skykamil/office-action-extractor.git
   cd office-action-extractor
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the server:
   ```bash
   uvicorn main:app --reload
   ```
4. Open in your browser:
   ```
   http://127.0.0.1:8000/
   ```

## Usage

Upload one or more PDF Office Action letters through the web interface, or via the API directly. Extracted data is saved to the database and can be viewed in the results table.

The repository includes three sample letters (`samples/letter1.pdf`, `samples/letter2.pdf`, `samples/letter3.pdf`) covering USPTO, Canadian, and Korean formats — upload them to see the extractor working without needing your own documents.

## Sample Documents

The included `samples/letter1.pdf`, `samples/letter2.pdf`, and `samples/letter3.pdf` are synthetic documents generated for demonstration and testing purposes only — they do not represent real Office Actions and contain no data from actual cases or clients. Each file carries a visible header marking it as a synthetic training sample. Law firm names, client names, application numbers, and dates are all fictional.

The three samples deliberately cover different jurisdictions and formats: USPTO (`18/742,615`, dates as `July 21, 2026`), Canadian (`3,215,487`, ISO dates), and Korean (`10-2025-0067812`, dates as `3 September 2026`). Each letter also contains two distinct deadlines — the official response due date and an earlier internal date for client instructions — so the extractor has to distinguish between them rather than match the first date it finds.

## API Endpoints

| Method | Path      | Description                                                        |
|--------|-----------|---------------------------------------------------------------------|
| GET    | `/`       | Web interface                                                      |
| POST   | `/upload` | Upload one or more files (`multipart/form-data`), returns extracted results |
| GET    | `/files`  | Returns all saved records from the database                        |

## Extracted Fields

- letter type (`file_type`)
- application number (`application_number`)
- letter date (`file_date`)
- Office Action issue date (`oa_start_date`)
- response due date (`due_date`)

## Project Structure

| File | Description |
|---|---|
| `main.py` | FastAPI app: endpoints, exception handling |
| `extraction.py` | Text and data extraction from files (regex) |
| `database.py` | SQLite: initialization, saving, reading |
| `exceptions.py` | Custom exception hierarchy |
| `static/index.html` | Frontend (upload form + results table) |
| `samples/` | Synthetic sample Office Action letters (USPTO, Canadian, Korean) |
| `test_extraction.py` | Pytest tests for extraction logic |

## Testing

```bash
pytest -v
```

## License

MIT — see [LICENSE](LICENSE). This covers the code and the synthetic sample documents in `samples/`.

## Limitations

- PDF only — no DOCX or scanned/OCR support
- Each uploaded file is a separate database record — no grouping of multiple documents into a single case
- Regex patterns tuned only for USPTO, Canadian, and Korean formats — other jurisdictions (e.g. EPO, Chinese CNIPA) may require additional patterns