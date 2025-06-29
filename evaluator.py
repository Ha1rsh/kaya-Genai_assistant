from langchain.llms import Together

llm = Together(model="mistralai/Mixtral-8x7B-Instruct-v0.1")

def evaluate_answer(question, user_answer, vectorstore):
    context = vectorstore.similarity_search(question, k=1)[0].page_content
    prompt = f"""Q: {question}\nUser Answer: {user_answer}\nReference: {context}\nEvaluate the user's answer and justify based on reference."""
    return llm(prompt).strip()

