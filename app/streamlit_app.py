import streamlit as st
import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from generation.content_generator import ContentGenerator
from generation.example_generator import ExampleGenerator
from generation.quize_generator import QuizGenerator
from generation.notes_formatter import NotesFormatter

# Page configuration
st.set_page_config(
    page_title="AI Study Material Generator",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        color: #1E40AF;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #6B7280;
        text-align: center;
        margin-bottom: 2rem;
    }
    .stButton>button {
        width: 100%;
        background-color: #3B82F6;
        color: white;
        font-weight: bold;
        padding: 0.5rem 1rem;
        border-radius: 0.5rem;
        border: none;
    }
    .stButton>button:hover {
        background-color: #2563EB;
    }
    .quiz-box {
        background-color: #F3F4F6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if 'history' not in st.session_state:
    st.session_state.history = []
if 'current_content' not in st.session_state:
    st.session_state.current_content = None

# Initialize generators
@st.cache_resource
def load_generators():
    return {
        'content': ContentGenerator(),
        'example': ExampleGenerator(),
        'quiz': QuizGenerator(),
        'formatter': NotesFormatter()
    }

generators = load_generators()

# Header
st.markdown('<div class="main-header">📚 AI Study Material Generator</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Create personalized study materials with AI-powered content generation</div>', unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.header("⚙️ Settings")
    
    st.subheader("📝 Generate Material")
    topic = st.text_input("Enter Topic", placeholder="e.g., Machine Learning, Photosynthesis")
    level = st.selectbox("Difficulty Level", ["Beginner", "Intermediate", "Advanced"])
    
    generate_button = st.button("🚀 Generate Study Material", use_container_width=True)
    
    st.divider()
    
    st.subheader("📖 Features")
    show_examples = st.checkbox("Include Examples", value=True)
    show_quiz = st.checkbox("Include Quiz", value=True)
    
    st.divider()
    
    if st.session_state.history:
        st.subheader("📜 History")
        for i, item in enumerate(st.session_state.history[:5]):
            if st.button(f"📄 {item['topic']} ({item['level']})", key=f"history_{i}"):
                st.session_state.current_content = item
                st.rerun()

# Main content area
if generate_button and topic:
    with st.spinner("🔄 Generating study material..."):
        # Generate content
        content = generators['content'].generate_content(topic, level)
        examples = generators['example'].generate_examples(topic, level) if show_examples else ""
        quiz_data = generators['quiz'].generate_quiz(topic, level) if show_quiz else []
        
        # Store in session state
        current_content = {
            'topic': topic,
            'level': level,
            'content': content,
            'examples': examples,
            'quiz': quiz_data,
            'timestamp': st.session_state.get('timestamp', ''),
        }
        
        st.session_state.current_content = current_content
        st.session_state.history.insert(0, current_content)
        st.session_state.history = st.session_state.history[:10]  # Keep last 10
        
        st.success("✅ Study material generated successfully!")
        st.rerun()

elif generate_button and not topic:
    st.error("⚠️ Please enter a topic!")

# Display content
if st.session_state.current_content:
    content_data = st.session_state.current_content
    
    # Title and metadata
    col1, col2, col3 = st.columns([3, 1, 1])
    with col1:
        st.title(f"📖 {content_data['topic']}")
        st.caption(f"Level: {content_data['level']}")
    
    with col2:
        # Export options
        markdown_content = generators['formatter'].format_markdown(
            content_data['content'],
            content_data['examples'],
            content_data.get('quiz', [])
        )
        st.download_button(
            label="📥 Download MD",
            data=markdown_content,
            file_name=f"{content_data['topic'].replace(' ', '_')}_notes.md",
            mime="text/markdown"
        )
    
    with col3:
        pdf_filename = f"{content_data['topic'].replace(' ', '_')}_notes.pdf"
        if st.button("📄 Export PDF"):
            success = generators['formatter'].export_to_pdf(
                content_data['topic'],
                content_data['level'],
                content_data['content'],
                content_data['examples'],
                content_data.get('quiz', []),
                pdf_filename
            )
            if success:
                with open(pdf_filename, "rb") as pdf_file:
                    st.download_button(
                        label="📥 Download PDF",
                        data=pdf_file,
                        file_name=pdf_filename,
                        mime="application/pdf"
                    )
                os.remove(pdf_filename)
    
    st.divider()
    
    # Content sections
    tab1, tab2, tab3 = st.tabs(["📝 Explanation", "💡 Examples", "❓ Quiz"])
    
    with tab1:
        st.markdown("### Detailed Explanation")
        st.write(content_data['content'])
    
    with tab2:
        if content_data['examples']:
            st.markdown("### Real-World Examples")
            st.info(content_data['examples'])
        else:
            st.info("No examples generated. Enable examples in settings.")
    
    with tab3:
        if content_data.get('quiz'):
            st.markdown("### Test Your Knowledge")
            for i, q in enumerate(content_data['quiz'], 1):
                with st.container():
                    st.markdown(f"**Question {i}:** {q['question']}")
                    
                    # Display options
                    user_answer = st.radio(
                        f"Select your answer for Q{i}:",
                        options=q['options'],
                        key=f"q_{i}",
                        label_visibility="collapsed"
                    )
                    
                    if st.button(f"Check Answer Q{i}", key=f"check_{i}"):
                        if q['options'].index(user_answer) == q['correct']:
                            st.success("✅ Correct!")
                        else:
                            st.error(f"❌ Incorrect. The correct answer is: {q['options'][q['correct']]}")
                        
                        if 'explanation' in q:
                            st.info(f"💡 {q['explanation']}")
                    
                    st.divider()
        else:
            st.info("No quiz generated. Enable quiz in settings.")

else:
    # Welcome message
    st.info("👈 Enter a topic in the sidebar and click 'Generate Study Material' to get started!")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("### 🎯 Features")
        st.markdown("""
        - AI-powered content generation
        - Multiple difficulty levels
        - Real-world examples
        - Interactive quizzes
        - PDF & Markdown export
        """)
    
    with col2:
        st.markdown("### 📚 Difficulty Levels")
        st.markdown("""
        - **Beginner**: Simple explanations
        - **Intermediate**: Detailed analysis
        - **Advanced**: Expert-level content
        """)
    
    with col3:
        st.markdown("### 💡 Example Topics")
        st.markdown("""
        - Machine Learning
        - Photosynthesis
        - Quantum Physics
        - Data Structures
        - Economics
        """)