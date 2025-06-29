from langchain.llms import Together

llm = Together(model="mistralai/Mixtral-8x7B-Instruct-v0.1")

def generate_questions(text):
    prompt = f"""Generate 3 logic-based comprehension questions from this text:\n\n{text[:1500]}"""
    return llm(prompt).strip().split("\n")[:3]

