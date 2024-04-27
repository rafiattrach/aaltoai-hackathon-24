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
from find_match import find_match
from generate_email import generate_email

def display_error_image(assets_dir, placeholder):
    error_image_path = os.path.join(assets_dir, 'confused.jpeg')
    error_image = Image.open(error_image_path)
    placeholder.image(error_image, caption="The text does not have all the RFP requirements! Please try again. Make sure to include an email address, due date, and specific requirements.")

def image_to_base64(image):
    buffered = BytesIO()
    image.save(buffered, format="JPEG")
    img_str = base64.b64encode(buffered.getvalue()).decode()
    return img_str

# Display logo and branding
assets_dir = os.path.join(current_dir, 'assets')
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

uploaded_file = st.file_uploader("Upload your RFP file", type=['pdf', 'docx', 'jpeg', 'jpg', 'png'])
text_input = st.text_area("Or paste your text here", disabled=uploaded_file is not None)

if not uploaded_file and not text_input:
    st.error("Please upload a file or enter text to extract.")
else:
    if st.button('Extract from Document'):
        with st.spinner('Processing...'):
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
                # Check if any key values are empty and display error image if so
                if not all(json_result.values()):  # This checks if any value in the dictionary is empty
                    error_placeholder = st.empty()
                    display_error_image(assets_dir, error_placeholder)
                else:
                    st.session_state['extracted_data'] = json_result
                    st.success('Extraction complete!')

    if 'extracted_data' in st.session_state:
        json_result = st.session_state['extracted_data']
        st.markdown("## **Key RFP Information**")
        data_df = pd.DataFrame({
            'Property': ['Due Date', 'Email', 'Requirements'],
            'Value': [json_result['dueDate'], json_result['email'], json_result['reqs']]
        })
        st.write(data_df.to_html(index=False, header=False), unsafe_allow_html=True)
        st.write("")

        if st.button('Find Match'):
            with st.spinner('Finding matches...'):
                prefixed_requirements = f"These are my requirements: {json_result['reqs']}"
                match_result = find_match(prefixed_requirements)
                st.session_state['matched_results'] = match_result
                st.success('Match finding complete!')

        if 'matched_results' in st.session_state:
            st.markdown("**Matched Products:**")
            st.write(st.session_state['matched_results'])
            st.write("")

            if st.button("Generate Email"):
                with st.spinner('Generating email...'):
                    email_data = {
                        'dueDate': json_result['dueDate'],
                        'email': json_result['email'],
                        'reqs': json_result['reqs'],
                        'matchedResults': st.session_state['matched_results']
                    }
                    email_text = generate_email('phi3', email_data)
                    st.session_state['email_text'] = email_text
                    st.success('Email generated!')

                if 'email_text' in st.session_state:
                    st.text_area("Editable Generated Email", value=st.session_state['email_text'], height=300)
