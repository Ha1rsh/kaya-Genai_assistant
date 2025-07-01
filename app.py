import streamlit as st
import requests
from fpdf import FPDF
from PIL import Image
from io import BytesIO
import base64
import os

# === Page Config ===
st.set_page_config(page_title="Kaya - GenAI Assistant", layout="wide")

# === Helper: Encode image to base64 ===
def get_image_base64(image_path):
    img = Image.open(image_path)
    buffered = BytesIO()
    img.save(buffered, format="PNG")
    img_bytes = buffered.getvalue()
    img_base64 = base64.b64encode(img_bytes).decode()
    return img_base64

# === Title with Kaya Avatar ===
image_path = r"C:\Users\harsh_\OneDrive\Desktop\GENAi\frontend\assets\kaya.png"
img_base64 = get_image_base64(image_path)

st.markdown(
    f"""
    <div style='display: flex; align-items: center; gap: 20px;'>
        <img src='data:image/png;base64,{img_base64}' width='80' height='80' style='border-radius: 50%;'/>
        <h1 style='margin: 0;'>Kaya: GenAI Assistant</h1>
    </div>
    """,
    unsafe_allow_html=True
)

# === PDF Creation Helper ===
def create_pdf(summary_text):
    # Remove non-latin characters to avoid encoding error
    safe_text = summary_text.encode('latin-1', 'ignore').decode('latin-1')
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_font("Arial", size=12)
    pdf.cell(0, 10, "Summary", ln=True, align="C")
    pdf.ln(10)
    pdf.multi_cell(0, 10, safe_text)
    return pdf.output(dest='S').encode('latin1')

# === Sidebar Upload ===
with st.sidebar:
    uploaded_file = st.file_uploader("Upload a PDF or TXT file", type=["pdf", "txt"])

# === Session State Init ===
if 'document_text' not in st.session_state:
    st.session_state.document_text = ""
if 'summary' not in st.session_state:
    st.session_state.summary = ""
if 'questions' not in st.session_state:
    st.session_state.questions = []
    st.session_state.answers = []
    st.session_state.evaluations = []
    st.session_state.current_index = 0

# === File Upload Handling ===
if uploaded_file:
    res = requests.post("http://localhost:8000/upload/", files={"file": uploaded_file})
    if res.status_code != 200:
        st.error(f"Server error {res.status_code}: {res.text}")
        st.stop()
    try:
        data = res.json()
        if not data:
            st.error("❌ Response JSON is empty. Please check the backend.")
            st.stop()
    except ValueError:
        st.error("❌ Response was not JSON.")
        st.stop()

    st.session_state.summary = data.get("summary", "")
    st.session_state.document_text = data.get("text", "")
    st.success("✅ File uploaded!")

    # === Summary Display & Download ===
    if st.session_state.summary:
        st.markdown("### 📌 Summary")
        st.write(st.session_state.summary)

        pdf_bytes = create_pdf(st.session_state.summary)
        st.download_button(
            label="📥 Download Summary as PDF",
            data=pdf_bytes,
            file_name="summary.pdf",
            mime="application/pdf",
        )

    # === Mode Selection with Image Icons ===
    st.markdown("### 🔍 Select Your Interaction Mode")

    ask_icon = r"C:\Users\harsh_\OneDrive\Desktop\GENAi\frontend\assets\ask_icon.png"
    challenge_icon = r"C:\Users\harsh_\OneDrive\Desktop\GENAi\frontend\assets\brain_icon.png"

    def get_mode_option_html(img_path, label):
        if os.path.exists(img_path):
            icon_base64 = get_image_base64(img_path)
            return f"<img src='data:image/png;base64,{icon_base64}' width='25' style='vertical-align:middle;'/> <span style='vertical-align:middle;'>{label}</span>"
        else:
            return label

    ask_option_html = get_mode_option_html(ask_icon, "Ask Anything")
    challenge_option_html = get_mode_option_html(challenge_icon, "Challenge Me")

    mode = st.radio(
        "Mode",
        options=["Ask Anything", "Challenge Me"],
        index=0,
        format_func=lambda opt: ask_option_html if opt == "Ask Anything" else challenge_option_html,
    )

    # === Ask Anything Mode ===
    if "Ask Anything" in mode:
        ask_img_path = r"C:\Users\harsh_\OneDrive\Desktop\GENAi\frontend\assets\question.png"
        if os.path.exists(ask_img_path):
            ask_img_base64 = get_image_base64(ask_img_path)
            st.markdown(
                f"""
                <div style='text-align: center; margin-bottom: 20px;'>
                    <img src='data:image/png;base64,{ask_img_base64}' width='120' />
                    <h3>Ask me anything about the document!</h3>
                </div>
                """,
                unsafe_allow_html=True
            )

        question = st.text_input("Ask a question about the document:")
        if st.button("Submit Question") and question:
            with st.spinner("Thinking..."):
                answer_res = requests.post("http://localhost:8000/answer/", json={
                    "context": st.session_state.document_text,
                    "question": question
                })
                if answer_res.status_code == 200:
                    try:
                        answer_json = answer_res.json()
                        answer = answer_json.get("answer", "No answer received.")
                        st.markdown(f"**Answer:** {answer}")
                    except ValueError:
                        st.error("❌ Answer response was not JSON.")
                else:
                    st.error(f"Error getting answer: {answer_res.status_code}")

    # === Challenge Me Mode ===
    elif "Challenge Me" in mode:
        student_img_path = r"C:\Users\harsh_\OneDrive\Desktop\GENAi\frontend\assets\student.png"
        if os.path.exists(student_img_path):
            emoji_base64 = get_image_base64(student_img_path)
            st.markdown(
                f"""
                <div style='text-align: center; margin-bottom: 20px;'>
                    <img src='data:image/png;base64,{emoji_base64}' width='120' />
                    <h3>Ready to challenge your brain?</h3>
                </div>
                """,
                unsafe_allow_html=True
            )

        if st.button("🧠 Generate Challenge Questions"):
            with st.spinner("Generating questions..."):
                q_res = requests.post("http://localhost:8000/generate_questions/", json={
                    "context": st.session_state.document_text
                })
                if q_res.status_code == 200:
                    try:
                        q_json = q_res.json()
                        if q_json:
                            st.session_state.questions = q_json.get("questions", [])
                            st.session_state.answers = [""] * len(st.session_state.questions)
                            st.session_state.evaluations = [""] * len(st.session_state.questions)
                            st.session_state.current_index = 0
                        else:
                            st.error("❌ Questions response JSON is empty.")
                    except ValueError:
                        st.error("❌ Questions response was not JSON.")
                else:
                    st.error(f"Error generating questions: {q_res.status_code}")

        if st.session_state.questions:
            idx = st.session_state.current_index
            question = st.session_state.questions[idx]
            st.markdown(f"### Q{idx + 1}: {question}")

            answer = st.text_area("Your Answer", value=st.session_state.answers[idx], key=f"answer_{idx}")
            st.session_state.answers[idx] = answer

            if st.button("✅ Submit Answer", key=f"submit_{idx}"):
                with st.spinner("Evaluating..."):
                    eval_res = requests.post("http://localhost:8000/evaluate_answer/", json={
                        "context": st.session_state.document_text,
                        "question": question,
                        "answer": answer
                    })
                    if eval_res.status_code == 200:
                        try:
                            eval_json = eval_res.json()
                            st.session_state.evaluations[idx] = eval_json.get("evaluation", "No evaluation received.")
                        except ValueError:
                            st.error("❌ Evaluation response was not JSON.")
                    else:
                        st.error(f"Error evaluating answer: {eval_res.status_code}")

            if st.session_state.evaluations[idx]:
                st.markdown(f"**Evaluation:** {st.session_state.evaluations[idx]}")

            col1, col2 = st.columns(2)
            if col1.button("⬅️ Previous") and idx > 0:
                st.session_state.current_index -= 1
            if col2.button("➡️ Next") and idx < len(st.session_state.questions) - 1:
                st.session_state.current_index += 1

else:
    st.info("📂 Please upload a PDF or TXT file to begin.")
