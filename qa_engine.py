from langchain.chains import RetrievalQA
from langchain.llms import Together

llm = Together(model="mistralai/Mixtral-8x7B-Instruct-v0.1")

def answer_question(question, vectorstore):
    qa = RetrievalQA.from_chain_type(llm=llm, retriever=vectorstore.as_retriever())
    result = qa({"query": question})
    return result["result"], "Answer based on top retrieved chunk."



