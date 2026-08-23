from extraction import find_app_number, find_file_type, find_dates, extract_text
from pathlib import Path

def test_find_app_number():
    assert find_app_number("Canadian Patent Application No. 3,215,487") == "3,215,487"
    assert find_app_number("Korean Patent Application No. 10-2025-0067812") == "10-2025-0067812"
    assert find_app_number("U.S. Patent Application No. 18/742,615") == "18/742,615"

def test_find_letter_type():
    assert find_file_type("forwards the first Office Action with Search Report") == "first Office Action"
    assert find_file_type("Property Office issued a Notice of Preliminary Rejection") == "Notice of Preliminary Rejection"
    assert find_file_type("to forward the first Office Action issued") == "first Office Action"

def test_find_dates():
    text_ca = """This letter, dated 2026-05-19, forwards the first Office Action issued by
the Canadian Intellectual Property Office on 2026-05-14 for Canadian Patent Application.
The official response deadline is 2026-09-14."""
    text_kr = """By this letter of 8 September 2026, we report that the Korean Intellectual
Property Office issued a Notice of Preliminary Rejection on 8 September 2026 concerning
Korean Patent Application. A response must be filed no later than 3 November 2026."""
    text_us = """We write on August 4, 2026 to forward the first Office Action issued by
the United States Patent and Trademark Office on July 21, 2026 in U.S. Patent Application.
The response is due on October 21, 2026."""
    assert find_dates(text_ca) == ('2026-05-19', '2026-05-14', '2026-09-14')
    assert find_dates(text_kr) == ('8 September 2026', '8 September 2026', '3 November 2026')
    assert find_dates(text_us) == ('August 4, 2026', 'July 21, 2026', 'October 21, 2026')

def test_extract_text():
    letter_path = Path(__file__).parent / "samples" / "letter1.pdf"
    assert "3,215,487" in extract_text(letter_path)