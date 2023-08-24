import streamlit as st
import ocrspace
from PIL import Image
import io

st.title("Streamlit OCR App")

# Get your API_ENDPOINT and API_KEY from Streamlit Secrets
API_ENDPOINT = st.secrets['API_ENDPOINT']
API_KEY = st.secrets['API_KEY']

def resize_image(image, max_width=1024):
    width, height = image.size
    if width <= max_width:
        return image
    new_width = max_width
    new_height = int((new_width / width) * height)
    resized_image = image.resize((new_width, new_height))
    return resized_image

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
        # Convert the BytesIO object to an image
        image = Image.open(uploaded_file)
        resized_image = resize_image(image)
        resized_image.save("resized_image.jpg")

        if st.button("Run OCR"):
            # Provide the file path to the saved image
            response = api.ocr_file("resized_image.jpg")
            st.write("OCR Output:")
            st.write(response)
            st.image(uploaded_file, caption="Uploaded Image", use_column_width=True)
