# 📄 Kaya - Document-Aware GenAI Assistant

Kaya is a local, document-aware GenAI assistant built with **Streamlit**, **LangChain**, **Together AI**, and **FAISS**. Upload PDF/TXT files, generate summaries, ask contextual questions, or challenge yourself with AI-generated quizzes based on the document content.

---

## 🚀 Features

- ✅ Upload and read **PDF** or **TXT** documents
- ✅ Generate a **summary** using LLMs
- ✅ Create a **vector store** using `FAISS`
- ✅ Perform **semantic search** and **Q&A**
- ✅ Test yourself with **auto-generated questions**
- ✅ Evaluate your answers with **AI feedback**

---

## 🛠️ Tech Stack

- [Python 3.8+](https://www.python.org/)
- [Streamlit](https://streamlit.io/)
- [LangChain](https://github.com/langchain-ai/langchain)
- [Together API](https://together.xyz/)
- [FAISS](https://github.com/facebookresearch/faiss)
- [PyMuPDF (`fitz`)](https://github.com/pymupdf/PyMuPDF)
- `.env` config via `python-dotenv`

---

## 📦 Installation

```bash
git clone https://github.com/your-username/kaya.git
cd kaya

python -m venv venv
# Activate the virtual environment:
# Windows
venv\Scripts\activate
# Mac/Linux
source venv/bin/activate

pip install -r requirements.txt
kaya/
├── app.py                   # Streamlit app interface
├── .env                     # API keys (not tracked in Git)
├── backend/
│   ├── utils.py             # Text extraction, chunking, vectorstore
│   ├── summarizer.py        # Summarization logic
│   ├── qa_engine.py         # Q&A logic
│   ├── question_generator.py# MCQ generation
│   └── evaluator.py         # Answer evaluation
├── requirements.txt         # Python dependencies
└── README.md                # Project documentation
