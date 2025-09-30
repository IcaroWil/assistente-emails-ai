import io
from fastapi import UploadFile
from pypdf import PdfReader

async def text_from_upload(file: UploadFile) -> str:
    content_type = file.content_type or ""
    name = (file.filename or "").lower()

    if content_type == "text/plain" or name.endswith(".txt"):
        text = (await file.read()).decode("utf-8", errors="ignore")
        return text

    if content_type == "application/pdf" or name.endswith(".pdf"):
        data = await file.read()
        reader = PdfReader(io.BytesIO(data))
        pages = [page.extract_text() or "" for page in reader.pages]
        return "\n".join(pages)

    return (await file.read()).decode("utf-8", errors="ignore")
