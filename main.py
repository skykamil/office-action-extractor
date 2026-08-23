from pathlib import Path
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi import FastAPI, UploadFile, Request
from database import init_db, save_file, get_all_files
from extraction import extract_text, find_app_number, find_file_type, find_dates
from exceptions import FileAccessError, UnsupportedFileFormatError, CorruptedFileError, EmptyDocumentError

app = FastAPI()
init_db()

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.post("/upload")
async def upload_files(files: list[UploadFile]):
    uploaded_files = []
    for file in files:
        if file.filename is None:
            raise FileAccessError("File not selected")
        contents = await file.read()
        safe_filename = Path(file.filename).name
        with open(safe_filename, "wb") as f:
            f.write(contents)
        try:
            text = extract_text(safe_filename)
            save_file(find_file_type(text), find_app_number(text), *find_dates(text))
            uploaded_files.append({"file_type": find_file_type(text), "application_number": find_app_number(text)})
        finally:
            Path(safe_filename).unlink(missing_ok=True)
    return uploaded_files

@app.get("/files")
async def get_files():
    files = get_all_files()
    return files

@app.get("/")
async def get_form():
    return FileResponse("static/index.html")

@app.exception_handler(FileAccessError)
async def file_access_error(request: Request, exc: FileAccessError):
    return JSONResponse(
        status_code=404,
        content={"message": str(exc)}
    )

@app.exception_handler(UnsupportedFileFormatError)
async def unsupported_file(request: Request, exc: UnsupportedFileFormatError):
    return JSONResponse(
        status_code=415,
        content={"message": str(exc)}
    )

@app.exception_handler(CorruptedFileError)
async def corrupted_file(request: Request, exc: CorruptedFileError):
    return JSONResponse(
        status_code=400,
        content={"message": str(exc)}
    )

@app.exception_handler(EmptyDocumentError)
async def empty_document(request: Request, exc: EmptyDocumentError):
    return JSONResponse(
        status_code=400,
        content={"message": str(exc)}
    )