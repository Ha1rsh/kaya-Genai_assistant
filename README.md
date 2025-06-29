# Document-Aware GenAI Assistant

## Setup Instructions

1. Clone the repo
2. Create and activate a Python virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate   # Linux/macOS
   venv\Scripts\activate      # Windows
   genai_assistant/
├── app.py                   # Streamlit or Gradio UI
├── backend/
│   ├── summarizer.py
│   ├── qa_engine.py
│   ├── evaluator.py
│   ├── question_generator.py
│   └── utils.py
├── data/
│   └── uploads/             # Store uploaded documents
├── models/                  # Optional: store embedding or model logic
├── requirements.txt
└── README.md
