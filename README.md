# Kaya: GenAI Assistant 🤖📄

Kaya is an AI-powered document-aware assistant that can **summarize**, **answer questions**, and **generate logic-based challenges** from any uploaded PDF or TXT document. Built using Streamlit and FastAPI, Kaya helps you interact with research material in a smart, intuitive way.
---

## 🚀 Features

- 📥 Upload `.pdf` or `.txt` files  
- 📌 Get concise summaries (~150 words)  
- 💬 Ask context-aware questions from the document  
- 🧠 Challenge yourself with logic-based questions  
- 📤 Export summary as downloadable PDF  
- 🖼️ Clean UI with interactive icons and avatars

---

## 🛠️ Tech Stack

- [Python 3.8+](https://www.python.org/)
- [Streamlit](https://streamlit.io/)
- [Together API](https://together.xyz/)
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
├── backend/ # FastAPI logic: summarization, QA, evaluation
│ └── main.py 
│ └── genai_logic.py
│ └── document_utils.py
│
├── frontend/ # Streamlit app UI
│ ├── app.py
│ └── assets/
│ ├── kaya.png # Kaya avatar
│ ├── question.png # Ask Anything icon
│ └── student.png # Challenge Me icon
│
├── requirements.txt
└── README.md
