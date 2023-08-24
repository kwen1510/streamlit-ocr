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
        # Convert the BytesIO object to an image
        image = Image.open(uploaded_file)
        
        # Check and correct image orientation
        if hasattr(image, '_getexif'):
            exif = image._getexif()
            if exif is not None and 274 in exif:
                orientation = exif[274]
                if orientation == 3:
                    image = image.rotate(180, expand=True)
                elif orientation == 6:
                    image = image.rotate(270, expand=True)
                elif orientation == 8:
                    image = image.rotate(90, expand=True)
        
        # Check image size and resize if necessary
        max_file_size_kb = 1024
        img_byte_array = io.BytesIO()
        image.save(img_byte_array, format='JPEG')
        
        if len(img_byte_array.getvalue()) / 1024 > max_file_size_kb:
            image.thumbnail((800, 800))  # Adjust the size as needed
            img_byte_array = io.BytesIO()
            image.save(img_byte_array, format='JPEG')

        if st.button("Run OCR"):
            # Provide the file path to the saved image
            response = api.ocr_file("uploaded_image.jpg")
            st.write("OCR Output:")
            st.write(response)
            st.image(uploaded_file, caption="Uploaded Image", use_column_width=True)
