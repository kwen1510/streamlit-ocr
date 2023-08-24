import streamlit as st
import ocrspace
from PIL import Image
import io

st.title("Streamlit OCR App")

# Get your API_ENDPOINT and API_KEY from Streamlit Secrets
API_ENDPOINT = st.secrets['API_ENDPOINT']
API_KEY = st.secrets['API_KEY']

# Create an OCR API instance
api = ocrspace.API(endpoint=API_ENDPOINT, api_key=API_KEY, OCREngine=2, language='eng', scale=True)

# Add a radio button to choose between URL and file upload
source = st.radio("Select Source", ("URL", "Upload File"))

if source == "URL":
    # Get URL input from the user
    url = st.text_input("Enter the URL of the image:")

    if st.button("Run OCR"):
        if url:
            response = api.ocr_url(url)
            st.write("OCR Output:")
            st.write(response)
            st.image(url, use_column_width=True)
        else:
            st.warning("Please enter a valid URL.")

else:
    # Get file upload from the user
    uploaded_file = st.file_uploader("Upload an image:", type=["jpg", "png", "jpeg", "heic"])

    if uploaded_file is not None:
        # Save the uploaded file to a temporary location
        with open("uploaded_image.jpg", "wb") as f:
            f.write(uploaded_file.read())

        if st.button("Run OCR"):
            # Provide the file path to the saved image
            response = api.ocr_file("uploaded_image.jpg")
            st.write("OCR Output:")
            st.write(response)
            st.image(uploaded_file, caption="Uploaded Image", use_column_width=True)
