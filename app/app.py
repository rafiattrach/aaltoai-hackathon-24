import streamlit as st
from io import BytesIO
import base64
from PIL import Image
import sys
import os

# Assuming app.py is in root/app and extraction.py is in root/src/data_preprocessing
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(os.path.join(parent_dir, 'src', 'data_preprocessing'))

from extraction import extract_text_from_pdf, extract_text_from_docx, generate_description_with_gpt4

# Function to convert image to base64 for HTML embedding
def image_to_base64(image):
    buffered = BytesIO()
    image.save(buffered, format="JPEG")
    img_str = base64.b64encode(buffered.getvalue()).decode()
    return img_str

# Streamlit application setup
#st.title("Smart Proposal Assistant for RFP Response and Offer Workflow")

# Display logo and branding
assets_dir = os.path.join(current_dir, 'assets')  # Ensure this directory points correctly
image_path = os.path.join(assets_dir, 'jack.jpeg')
image = Image.open(image_path)
image_base64 = image_to_base64(image)
st.markdown(f"""
    <div style="display:flex;align-items:center;justify-content:center;flex-direction:column;">
        <img src="data:image/jpeg;base64,{image_base64}" style="border-radius:50%;width:150px;height:200px;">
        <p style="font-weight:bold;font-size:30px;margin-bottom:-20px;">SPARROW</p>
        <br>
        <p style="font-size:16px;text-align:center;">
            <span style="font-weight:bold;color:#ff6699;">S</span>mart <span style="font-weight:bold;color:#ff6699;">P</span>roposal <span style="font-weight:bold;color:#ff6699;">A</span>ssistant for <span style="font-weight:bold;color:#ff6699;">R</span>FP<br>
            <span style="font-weight:bold;color:#ff6699;">R</span>esponse and <span style="font-weight:bold;color:#ff6699;">O</span>ffer <span style="font-weight:bold;color:#ff6699;">W</span>orkflow
        </p>
    </div>
    """, unsafe_allow_html=True)

# File uploader
uploaded_file = st.file_uploader("Upload your RFP file", type=['pdf', 'docx', 'jpeg', 'jpg', 'png'])

# Text area, disabled if a file is uploaded
if uploaded_file is None:
    text_input = st.text_area("Or paste your text here")
else:
    text_input = st.text_area("Or paste your text here", "", disabled=True)

if st.button('Extract Text'):
    if uploaded_file is not None:
        # Save the uploaded file temporarily
        with open(uploaded_file.name, "wb") as f:
            f.write(uploaded_file.getbuffer())
        file_path = uploaded_file.name
        
        # Process the file based on its type
        if uploaded_file.type == "application/pdf":
            extracted_text = extract_text_from_pdf(file_path)
        elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
            extracted_text = extract_text_from_docx(file_path)
        elif uploaded_file.type in ["image/jpeg", "image/png"]:
            extracted_text = generate_description_with_gpt4(file_path)
        st.write(extracted_text)
        os.remove(file_path)
    elif text_input:
        st.write("Entered Text:")
        st.write(text_input)
