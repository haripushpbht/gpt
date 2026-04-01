import base64
import os

import requests
import streamlit as st

st.set_page_config(page_title="Math + Physics Solver", page_icon="📘", layout="centered")

st.title("📘 Math & Physics Solver (Class 1–12)")
st.caption("Type question or upload image • OCR + AI step-by-step explanation")

api_url = os.getenv("BACKEND_URL", "http://localhost:8000")

question_text = st.text_area("Enter your question", height=130, placeholder="e.g., Solve 2x + 3 = 11")
uploaded_image = st.file_uploader("Upload question image", type=["png", "jpg", "jpeg", "webp"])

col1, col2 = st.columns(2)
with col1:
    class_level = st.slider("Class", min_value=1, max_value=12, value=8)
with col2:
    explanation_mode = st.selectbox(
        "Language mode",
        options=["english", "hindi", "bilingual"],
        format_func=lambda x: {
            "english": "English",
            "hindi": "Hindi",
            "bilingual": "Hindi + English",
        }[x],
    )

if st.button("Solve", type="primary", use_container_width=True):
    if not question_text.strip() and not uploaded_image:
        st.error("Please type a question or upload an image.")
    else:
        encoded_image = None
        if uploaded_image:
            encoded_image = base64.b64encode(uploaded_image.read()).decode("utf-8")

        payload = {
            "question_text": question_text,
            "image_base64": encoded_image,
            "class_level": class_level,
            "explanation_mode": explanation_mode,
        }

        with st.spinner("Solving... please wait"):
            try:
                response = requests.post(f"{api_url}/solve", json=payload, timeout=120)
                response.raise_for_status()
                data = response.json()
            except requests.RequestException as exc:
                st.error(f"Request failed: {exc}")
            else:
                if data.get("extracted_text"):
                    st.subheader("OCR Extracted Text")
                    st.code(data["extracted_text"])

                st.subheader("Step-by-step Solution")
                st.markdown(data["solution"])

                st.download_button(
                    label="Copy/Download Answer",
                    data=data["solution"],
                    file_name="solution.txt",
                    mime="text/plain",
                    use_container_width=True,
                )
