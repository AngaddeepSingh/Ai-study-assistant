import streamlit as st
from generator import generate_study_materials
from utils import extract_text_from_pdf, extract_text_from_url

st.set_page_config(page_title="AI Study Assistant", layout="centered")
st.title("Flashcard Generator")
st.write("Generate key concepts and active-recall flashcards from lecture notes, textbooks, PDFs, or web articles.")

# This ensures that text fetched from a PDF or URL isn't wiped out when you click other buttons
if "study_text" not in st.session_state:
    st.session_state.study_text = ""

# Create clean interactive tabs for different input methods
tab1, tab2, tab3 = st.tabs(["Paste Text", "Upload PDF", "Web Link"])

with tab1:
    pasted_text = st.text_area("Paste your lecture notes or textbook excerpts here:", height=200)
    if st.button("Use Pasted Text"):
        if pasted_text.strip():
            st.session_state.study_text = pasted_text
            st.success("Pasted text loaded successfully!")
        else:
            st.warning("The text box is empty.")

with tab2:
    uploaded_pdf = st.file_uploader("Upload a study guide or chapter PDF", type=["pdf"])
    if uploaded_pdf is not None:
        if st.button("Process PDF"):
            with st.spinner("Extracting text from PDF..."):
                try:
                    raw_pdf_text = extract_text_from_pdf(uploaded_pdf)
                    # Apply a safe 20,000 character limit
                    MAX_CHARS = 20000
                    if len(raw_pdf_text) > MAX_CHARS:
                        raw_pdf_text = raw_pdf_text[:MAX_CHARS]
                        st.warning(f"PDF was long! Trimmed to first {MAX_CHARS:,} characters.")
                    
                    st.session_state.study_text = raw_pdf_text
                    st.success(f"Successfully extracted text from `{uploaded_pdf.name}`!")
                except Exception as e:
                    st.error(f"Could not read PDF: {e}")

with tab3:
    url_input = st.text_input("Enter article or study guide URL:")
    if st.button("Fetch Webpage Content"):
        if url_input:
            with st.spinner("Fetching and cleaning webpage..."):
                try:
                    raw_url_text = extract_text_from_url(url_input)
                    # Apply a safe 20,000 character limit
                    MAX_CHARS = 20000
                    if len(raw_url_text) > MAX_CHARS:
                        raw_url_text = raw_url_text[:MAX_CHARS]
                        st.warning(f"Webpage was long! Trimmed to first {MAX_CHARS:,} characters.")
                        
                    st.session_state.study_text = raw_url_text
                    st.success("Successfully fetched and cleaned webpage content!")
                except Exception as e:
                    st.error(f"Could not fetch URL: {e}")
        else:
            st.warning("Please enter a URL first.")

# Show a status banner letting you know what's locked in and ready
if st.session_state.study_text:
    st.info(f"**Ready for generation!** ({len(st.session_state.study_text):,} characters loaded)")

print("---")

# Master Generate Button
if st.button("Generate Study Materials"):
    if not st.session_state.study_text.strip():
        st.warning("Please load or paste text, process a PDF, or fetch a URL first.")
    else:
        with st.spinner("Processing materials with Gemini..."):
            try:
                data = generate_study_materials(st.session_state.study_text)
                
                st.subheader("Key Concepts")
                for concept in data.key_concepts:
                    st.write(f"- {concept}")
                    
                st.subheader("Flashcards")
                for i, card in enumerate(data.flashcards, 1):
                    with st.expander(f"Card {i}: {card.question}"):
                        st.write(f"**Answer:** {card.answer}")
            except Exception as e:
                st.error(f"An error occurred: {e}")