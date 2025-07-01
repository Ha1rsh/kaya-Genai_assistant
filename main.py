from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from backend.genai_logic import (
    generate_summary,
    answer_question,
    generate_questions_from_context,
    evaluate_answer,
)
from backend.document_utils import extract_text_from_file

app = FastAPI()

# Allow frontend access (CORS)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/upload/")
async def upload_document(file: UploadFile = File(...)):
    contents = await file.read()
    text = extract_text_from_file(file.filename, contents)
    summary = await generate_summary(text)
    return {"text": text, "summary": summary}


@app.post("/answer/")
async def answer_endpoint(payload: dict):
    context = payload.get("context", "")
    question = payload.get("question", "")
    if not context or not question:
        return {"answer": "Invalid input."}
    answer = await answer_question(context, question)
    return {"answer": answer}

@app.post("/generate_questions/")
async def generate_questions_endpoint(payload: dict):
    context = payload.get("context", "")
    if not context:
        return {"questions": []}
    questions = await generate_questions_from_context(context)
    return {"questions": questions}

@app.post("/evaluate_answer/")
async def evaluate_endpoint(payload: dict):
    context = payload.get("context", "")
    question = payload.get("question", "")
    answer = payload.get("answer", "")
    evaluation = await evaluate_answer(context, question, answer)
    return {"evaluation": evaluation}
