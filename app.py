
import streamlit as st
import fitz

from audio_processor import generate_audio
from ai_processor import translate_text, simplify_text


st.set_page_config(
    page_title="AccessDoc AI",
    page_icon="📄",
    layout="wide"
)

st.title("📄 AccessDoc AI")
st.subheader("Making Every Document Accessible")

st.write(
    "Upload public notices and institutional PDFs "
    "to make information easier for everyone to access."
)

uploaded_file = st.file_uploader(
    "Upload your PDF document",
    type=["pdf"]
)

if uploaded_file is not None:

    document = fitz.open(
        stream=uploaded_file.read(),
        filetype="pdf"
    )

    st.success("PDF uploaded successfully!")

    complete_text = ""

    for page_number, page in enumerate(document, start=1):

        extracted_text = page.get_text()

        complete_text += (
            f"\n--- Page {page_number} ---\n"
            f"{extracted_text}\n"
        )

        st.subheader(f"Page {page_number}")

        st.text_area(
            f"Extracted Text - Page {page_number}",
            extracted_text,
            height=200,
            key=f"page_{page_number}"
        )

    if complete_text.strip():

        st.download_button(
            "📥 Download Extracted Text",
            data=complete_text,
            file_name="accessible_document.txt",
            mime="text/plain"
        )

        st.divider()

        # AI DOCUMENT SIMPLIFICATION

        st.subheader("✨ AI Document Simplification")

        if st.button("Simplify into Easy English"):

            try:
                with st.spinner("Simplifying your document..."):

                    simplified_text = simplify_text(complete_text)

                if simplified_text and simplified_text.strip():

                    st.success("Document simplified successfully!")

                    st.text_area(
                        "Easy-to-Understand Document",
                        simplified_text,
                        height=300,
                        key="simplified_output"
                    )

                    st.download_button(
                        "📥 Download Simplified Document",
                        data=simplified_text,
                        file_name="simplified_document.txt",
                        mime="text/plain"
                    )

                else:
                    st.warning("No simplified text was returned.")

            except Exception as e:
                st.error(f"Simplification failed: {e}")

        st.divider()

        # TRANSLATION AND AUDIO

        st.subheader("🌐 Translation and Audio")

        language_options = {
            "English": ("English", "en"),
            "Hindi": ("Hindi", "hi"),
            "Telugu": ("Telugu", "te"),
            "Tamil": ("Tamil", "ta"),
            "Kannada": ("Kannada", "kn")
        }

        selected_language = st.selectbox(
            "Choose audio language",
            list(language_options.keys())
        )

        if st.button("Generate Audio"):

            try:
                if selected_language == "English":

                    translated_text = complete_text

                else:
                    with st.spinner("Translating document..."):

                        translated_text = translate_text(
                            complete_text,
                            target_language=language_options[selected_language][0]
                        )

                if not translated_text or not translated_text.strip():

                    st.error("Translation returned empty text.")

                else:

                    st.subheader("Translated Document")

                    st.text_area(
                        "Translated Text",
                        translated_text,
                        height=250,
                        key="translated_output"
                    )

                    with st.spinner("Generating audio..."):

                        audio = generate_audio(
                            translated_text,
                            language=language_options[selected_language][1]
                        )

                    if audio:

                        st.audio(
                            audio.getvalue(),
                            format="audio/mp3"
                        )

                        st.success("Audio generated successfully!")

            except Exception as e:
                st.error(f"Translation or audio generation failed: {e}")

    else:

        st.warning(
            "No text found. This PDF may contain scanned pages."
        )
