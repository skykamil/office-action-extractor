import importlib
from pathlib import Path
import pytest
from fastapi.testclient import TestClient

@pytest.fixture
def client(monkeypatch):
    import database

    monkeypatch.setattr(database, "init_db", lambda: None)
    main = importlib.import_module("main")

    saved_records = []

    def fake_save_file(*args):
        saved_records.append(args)

    monkeypatch.setattr(main, "save_file", fake_save_file)

    return TestClient(main.app), saved_records


def test_rejected_upload_does_not_modify_existing_file(client, tmp_path, monkeypatch):
    test_client, _ = client
    monkeypatch.chdir(tmp_path)

    existing_file = tmp_path / "collision.txt"
    existing_file.write_text("ORIGINAL CONTENT")

    captured_paths = []

    import main

    original_extract_text = main.extract_text

    def capture_path(filepath):
        captured_paths.append(filepath)
        return original_extract_text(filepath)

    monkeypatch.setattr(main, "extract_text", capture_path)

    response = test_client.post(
        "/upload",
        files={"files": ("collision.txt", b"UPLOADED CONTENT", "text/plain")},
    )

    assert response.status_code == 415
    assert existing_file.read_text() == "ORIGINAL CONTENT"
    assert len(captured_paths) == 1
    assert not captured_paths[0].exists()

def test_same_filename_uploads_are_isolated_and_cleaned_up(client, tmp_path, monkeypatch):
    test_client, saved_records = client

    sample_path = Path(__file__).parent / "samples" / "letter1.pdf"
    pdf_contents = sample_path.read_bytes()
    monkeypatch.chdir(tmp_path)

    existing_file = tmp_path / "same.pdf"
    existing_file.write_bytes(b"ORIGINAL CONTENT")

    captured_paths = []

    import main

    original_extract_text = main.extract_text

    def capture_path(filepath):
        captured_paths.append(filepath)
        return original_extract_text(filepath)

    monkeypatch.setattr(main, "extract_text", capture_path)

    response = test_client.post(
        "/upload",
        files=[
            ("files", ("same.pdf", pdf_contents, "application/pdf")),
            ("files", ("same.pdf", pdf_contents, "application/pdf")),
        ],
)

    assert response.status_code == 200
    assert len(response.json()) == 2
    assert len(saved_records) == 2
    assert len(captured_paths) == 2
    assert captured_paths[0] != captured_paths[1]
    assert captured_paths[0].parent != captured_paths[1].parent
    assert not captured_paths[0].exists()
    assert not captured_paths[1].exists()
    assert existing_file.read_bytes() == b"ORIGINAL CONTENT"
