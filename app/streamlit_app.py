import streamlit as st
import sys
import os
from notes_formatter import NotesFormatter
import tempfile
import os as os_sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from content_generator import ContentGenerator
from example_generator import ExampleGenerator
from quiz_generator import QuizGenerator

st.set_page_config(
    page_title="AI Study Material Generator",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)


@st.cache_resource
def load_generators():
    return {
        "content": ContentGenerator(),
        "example": ExampleGenerator(),
        "quiz": QuizGenerator()
    }


generators = load_generators()

st.title("AI Study Material Generator")
st.write("Structured explanation • Difficulty-specific content • Real-world examples • Quiz")

topic = st.text_input("Topic", placeholder="e.g., Machine Learning, Photosynthesis")
level = st.selectbox("Difficulty", ["Beginner", "Intermediate", "Advanced"])

col_generate, col_examples, col_quiz = st.columns([2, 1, 1])

with col_generate:
    generate_button = st.button("Generate Study Material")

with col_examples:
    show_examples = st.checkbox("Include Examples", value=True)

with col_quiz:
    show_quiz = st.checkbox("Include Quiz", value=True)

# Clean up previous PDF if exists
if "study_material" in st.session_state:
    prev_data = st.session_state.study_material
    if prev_data.get("pdf_file") and os.path.exists(prev_data["pdf_file"]):
        try:
            os_sys.remove(prev_data["pdf_file"])
        except:
            pass  # Ignore errors during cleanup

if generate_button:
    if not topic.strip():
        st.error("Please enter a topic.")
    else:
        content = generators["content"].generate_content(topic, level)
        examples = generators["example"].generate_examples(topic, level) if show_examples else ""
        quiz_data = generators["quiz"].generate_quiz(topic, level) if show_quiz else []

        # Generate PDF in temporary file
        temp_pdf_filename = f"temp_study_material_{topic.replace(' ', '_')}_{level}.pdf"
        pdf_success = NotesFormatter.export_to_pdf(
            topic,
            level,
            content,
            examples,
            quiz_data,
            temp_pdf_filename
        )
        
        st.session_state.study_material = {
            "topic": topic,
            "level": level,
            "content": content,
            "examples": examples,
            "quiz": quiz_data,
            "pdf_file": temp_pdf_filename if pdf_success else None,
        }

if "study_material" in st.session_state:
    data = st.session_state.study_material

    st.subheader(f"{data['topic']} ({data['level']})")

    # PDF Download Section
    col1, col2 = st.columns([1, 1])
    with col1:
        if data.get("pdf_file") and os.path.exists(data["pdf_file"]):
            with open(data["pdf_file"], 'rb') as f:
                pdf_data = f.read()
            st.download_button(
                label="📥 Download as PDF",
                data=pdf_data,
                file_name=f"{data['topic'].replace(' ', '_')}_{data['level']}_Study_Material.pdf",
                mime="application/pdf"
            )
        else:
            st.info("PDF not available")

    with col2:
        st.download_button(
            label="📝 Download as Markdown",
            data=NotesFormatter.format_markdown(data['content'], data['examples'], data['quiz']),
            file_name=f"{data['topic'].replace(' ', '_')}_{data['level']}_Study_Material.md",
            mime="text/markdown"
        )

    st.markdown("### 📝 Structured Explanation")
    st.write(data["content"])

    st.markdown("### 💡 Real-World Examples")
    if data["examples"]:
        st.info(data["examples"])
    else:
        st.info("Examples not generated. Enable them above.")

    st.markdown("### ❓ Quiz")
    if data["quiz"]:
        for i, q in enumerate(data["quiz"], 1):
            st.markdown(f"**Question {i}:** {q['question']}")

            user_answer = st.radio(
                f"Select your answer for Q{i}",
                options=q["options"],
                key=f"q_{i}"
            )

            if st.button(f"Check Q{i}", key=f"check_{i}"):
                if q["options"].index(user_answer) == q["correct"]:
                    st.success("Correct!")
                else:
                    st.error(f"Incorrect. Correct answer: {q['options'][q['correct']]}")

                if "explanation" in q:
                    st.info(q["explanation"])

            st.divider()
    else:
        st.info("Quiz not generated. Enable it above.")
    # Cleanup PDF file when leaving the session
    if data.get("pdf_file") and os.path.exists(data["pdf_file"]):
        try:
            os_sys.remove(data["pdf_file"])
        except:
            pass  # Ignore errors during cleanup
else:
    st.info("Enter a topic, choose difficulty, and click 'Generate Study Material'.")