from langchain.vectorstores import FAISS
from langchain.embeddings.base import Embeddings
from langchain.docstore.document import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from together import Together
import fitz
import os

class TogetherEmbeddings(Embeddings):
    def __init__(self, model_name: str, api_key: str):
        self.model_name = model_name
        self.client = Together(api_key="bd694cf39d025dcdaa6be4f4dbefa45281af00eb664c0ca804ed339ff5dc09c0")

    def embed_documents(self, texts):
        embeddings = []
        for text in texts:
            response = self.client.embeddings.create(
                model=self.model_name,
                input=text,
            )
            embedding = response.data[0].embedding
            embeddings.append(embedding)
        return embeddings

    def embed_query(self, text):
        response = self.client.embeddings.create(
            model=self.model_name,
            input=text,
        )
        return response.data[0].embedding

def build_vectorstore(chunks, api_key=None):
    if api_key is None:
        api_key = os.getenv("TOGETHER_API_KEY")
        if not api_key:
            raise ValueError("API key must be provided or set in TOGETHER_API_KEY environment variable")

    # Use a proper embedding model from Together
    embeddings = TogetherEmbeddings(
        model_name="togethercomputer/m2-bert-80M-8k-retrieval",  # embedding model
        api_key=api_key
    )
    docs = [Document(page_content=chunk) for chunk in chunks]
    return FAISS.from_documents(docs, embeddings)

def extract_text_from_file(file):
    ext = file.name.split('.')[-1].lower()
    if ext == "pdf":
        doc = fitz.open(stream=file.read(), filetype="pdf")
        text = "\n".join([page.get_text() for page in doc])
        doc.close()
        return text
    elif ext == "txt":
        return file.read().decode("utf-8")
    else:
        raise ValueError("Unsupported file format")

def get_text_chunks(text, chunk_size=500, chunk_overlap=50):
    splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    return splitter.split_text(text)
