import pdfplumber
import io

def extract_text_from_file(filename: str, content: bytes) -> str:
    if filename.endswith(".pdf"):
        text = ""
        with pdfplumber.open(io.BytesIO(content)) as pdf:
            for page in pdf.pages:
                text += page.extract_text() or ""
        return text
    elif filename.endswith(".txt"):
        return content.decode("utf-8")
    else:
        raise ValueError("Unsupported file type")
