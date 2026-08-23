from exceptions import FileAccessError, UnsupportedFileFormatError, CorruptedFileError, EmptyDocumentError
from pdfplumber.utils.exceptions import PdfminerException
from pathlib import Path
import pdfplumber
import re

DATE_PATTERN = r"(\d{4}-\d{2}-\d{2}|\d{1,2} \w+ \d{4}|\w+ \d+, \d{4})"

LETTER_DATE_PATTERN = rf"(We write on|this letter of|This letter, dated) {DATE_PATTERN}"
OA_DATE_PATTERN = rf"issued [\w\s]+ on {DATE_PATTERN}"
DUE_DATE_PATTERN = rf"response [\w\s]+ (than|is|on) {DATE_PATTERN}"

def extract_text(filepath):
    if Path(filepath).suffix not in ('.pdf',):
        raise UnsupportedFileFormatError("Only PDF files are supported.")
    try:
        with pdfplumber.open(filepath) as pdf:
            text = ""
            for page in pdf.pages:
                text += page.extract_text()
            if text == "":
                raise EmptyDocumentError("Text not found")
            return text
    except FileNotFoundError:
        raise FileAccessError("File not found")
    except PdfminerException:
        raise CorruptedFileError("File is corrupted")
        

def find_app_number(text):
    app_number = None

    if match := re.search(r"(\d+,\d{3},\d{3}|\d{2}-20\d{2}-\d{7}|\d{2}\/\d{3},\d{3})", text):
        app_number = match.group(1)
    return app_number

def find_file_type(text):
    letter_type = None
    if match := re.search(r"(first office action|notice of preliminary rejection)", text, flags=re.I):
        letter_type = match.group(1)
    return letter_type

def find_dates(text):
    letter_date = None
    oa_date = None
    due_date = None

    if match := re.search(LETTER_DATE_PATTERN, text, flags=re.I):
        letter_date = match.group(2)
    if match := re.search(OA_DATE_PATTERN, text, flags=re.I):
        oa_date = match.group(1)
    if match := re.search(DUE_DATE_PATTERN, text, flags=re.I):
        due_date = match.group(2)

    return letter_date, oa_date, due_date