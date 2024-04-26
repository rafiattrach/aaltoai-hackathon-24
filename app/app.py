import streamlit as st
from io import BytesIO
import base64
from PIL import Image
import sys
import pandas as pd
import os

# Adding path to import custom modules from different directories
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(os.path.join(parent_dir, 'src', 'data_preprocessing'))
sys.path.append(os.path.join(parent_dir, 'src', 'data_processing'))

from extraction import extract_text_from_pdf, extract_text_from_docx, generate_description_with_gpt4
from json_creation import create_json_from_text

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
            <span style="font-weight:bold;color:#ff4d4d;">S</span>mart <span style="font-weight:bold;color:#ff4d4d;">P</span>roposal <span style="font-weight:bold;color:#ff4d4d;">A</span>ssistant for <span style="font-weight:bold;color:#ff4d4d;">R</span>FP<br>
            <span style="font-weight:bold;color:#ff4d4d;">R</span>esponse and <span style="font-weight:bold;color:#ff4d4d;">O</span>ffer <span style="font-weight:bold;color:#ff4d4d;">W</span>orkflow
        </p>
    </div>
    """, unsafe_allow_html=True)

# File uploader and text input
uploaded_file = st.file_uploader("Upload your RFP file", type=['pdf', 'docx', 'jpeg', 'jpg', 'png'])
text_input = st.text_area("Or paste your text here", disabled=uploaded_file is not None)

process_button = st.button('Process Document')

if process_button:
    if uploaded_file:
        with open(uploaded_file.name, "wb") as f:
            f.write(uploaded_file.getbuffer())
        file_path = uploaded_file.name
        
        if uploaded_file.type == "application/pdf":
            extracted_text = extract_text_from_pdf(file_path)
        elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
            extracted_text = extract_text_from_docx(file_path)
        elif uploaded_file.type in ["image/jpeg", "image/png"]:
            extracted_text = generate_description_with_gpt4(file_path)
        os.remove(file_path)
    elif text_input:
        extracted_text = text_input

    if extracted_text:
        json_result = create_json_from_text(extracted_text)
        if json_result and all(json_result.values()):
            st.markdown("## **Key RFP Information**")
            st.write("")  # Adds an extra line for spacing
            # Transpose the DataFrame for display
            data_df = pd.DataFrame({
                'Property': ['Due Date', 'Email', 'Requirements'],
                'Value': [json_result['dueDate'], json_result['email'], json_result['reqs']]
            })
            # Render DataFrame as HTML table without index
            st.write(data_df.to_html(index=False, header=False), unsafe_allow_html=True)
        else:
            error_image_path = os.path.join(assets_dir, 'confused.jpeg')
            error_image = Image.open(error_image_path)
            st.markdown(
                f'<div style="display: flex; flex-direction: column; align-items: center; text-align: center;">'
                f'<img src="data:image/jpeg;base64,{image_to_base64(error_image)}" style="width: 300px;">'
                f'<p>The text does not have all the RPF requirements! Please try again. Make sure to include an email address, due date, and specific requirements.</p>'
                f'</div>',
                unsafe_allow_html=True
            )
    else:
        st.error("Failed to extract or process text.")
