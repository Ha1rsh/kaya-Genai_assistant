import streamlit as st
from backend import utils, summarizer, qa_engine, question_generator, evaluator

st.set_page_config(page_title="Kaya - Doc-Aware Assistant", layout="wide")
st.title("📄 Kaya - Document-Aware GenAI Assistant")

# Put your Together API key here securely or load from env vars
API_KEY = "bd694cf39d025dcdaa6be4f4dbefa45281af00eb6640ca804ed339ff5dc09c0"

uploaded_file = st.file_uploader("Upload a PDF or TXT document", type=["pdf", "txt"])

if uploaded_file is not None:
    # Extract text from uploaded document
    text = utils.extract_text_from_file(uploaded_file)

    # Show summary
    st.subheader("📌 Auto Summary")
    summary = summarizer.summarize_text(text)
    st.write(summary)

    # Split text into chunks
    chunks = utils.get_text_chunks(text)

    # Build vectorstore with API key
    vectorstore = utils.build_vectorstore(chunks, api_key=API_KEY)

    # Choose interaction mode
    mode = st.radio("Choose Interaction Mode", ["Ask Anything", "Challenge Me"])

    if mode == "Ask Anything":
        question = st.text_input("Ask your question here:")
        if question:
            answer, source = qa_engine.answer_question(question, vectorstore)
            st.markdown(f"**Answer:** {answer}")
            st.markdown(f"**Justification:** {source}")

    elif mode == "Challenge Me":
        questions = question_generator.generate_questions(text)
        for i, q in enumerate(questions, 1):
            st.subheader(f"Q{i}. {q}")
            user_ans = st.text_input(f"Your Answer for Q{i}")
            if user_ans:
                feedback = evaluator.evaluate_answer(q, user_ans, vectorstore)
                st.markdown(f"**Feedback:** {feedback}")

else:
    st.info("Please upload a PDF or TXT file to start.")
