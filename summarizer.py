from langchain_community.llms import Together
from langchain.chains.summarize import load_summarize_chain
from langchain.docstore.document import Document

llm = Together(
    model="mistralai/Mistral-7B-Instruct-v0.1",  # ✅ Serverless model
    temperature=0.7,
    max_tokens=300
)

chain = load_summarize_chain(llm, chain_type="stuff")

def summarize_text(text):
    try:
        doc = Document(page_content=text)
        summary = chain.run([doc])
        return summary[:150]
    except Exception as e:
        raise RuntimeError(f"Unexpected error during summarization: {e}")





