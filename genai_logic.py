import os
import together
import asyncio
from concurrent.futures import ThreadPoolExecutor

# Use environment variable for API key
together.api_key = os.getenv("TOGETHER_API_KEY")
if not together.api_key:
    raise EnvironmentError("Set TOGETHER_API_KEY environment variable")

executor = ThreadPoolExecutor()

async def call_llm(prompt, max_tokens=700):
    loop = asyncio.get_event_loop()
    try:
        response = await loop.run_in_executor(
            executor,
            lambda: together.Complete.create(
                model="NousResearch/Nous-Hermes-2-Mixtral-8x7B-DPO",
                prompt=prompt,
                max_tokens=max_tokens,
                temperature=0.7,
                top_k=50,
                top_p=0.7,
                repetition_penalty=1.1,
                stop=["<|endoftext|>"]
            )
        )
        return response["choices"][0]["text"].strip()
    except Exception as e:
        print("❌ Model call error:", e)
        return ""

async def generate_summary(text: str) -> str:
    prompt = f"Summarize this text in 120–150 words:\n\n{text}\n\nSummary:"
    return await call_llm(prompt)

async def answer_question(context: str, question: str) -> str:
    prompt = f"Read the text below and answer the question with justification.\n\nText:\n{context}\n\nQuestion: {question}\nAnswer:"
    return await call_llm(prompt)

async def generate_questions_from_context(context: str) -> list:
    prompt = f"""
You are a helpful AI tutor. Read the following document and generate 5 high-quality challenge questions.
Return only the questions.

Document:
{context}

Questions:
1.
"""
    raw_output = await call_llm(prompt)
    print("❓ Question Generation Output:", raw_output)
    return [line.strip() for line in raw_output.split("\n") if line.strip().endswith("?")]

async def evaluate_answer(context: str, question: str, answer: str) -> str:
    prompt = (
        f"Evaluate the user's answer based on the context and question below.\n\n"
        f"Context: {context}\n"
        f"Question: {question}\n"
        f"User Answer: {answer}\n"
        f"Evaluation and feedback:"
    )
    return await call_llm(prompt)
