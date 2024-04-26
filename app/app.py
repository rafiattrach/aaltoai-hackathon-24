import streamlit as st
from PIL import Image
import os
import base64
from io import BytesIO

def image_to_base64(image):
    buffered = BytesIO()
    image.save(buffered, format="JPEG")
    img_str = base64.b64encode(buffered.getvalue()).decode()
    return img_str

# Set the title of the app
st.title("")

# Load your image
image_path = os.path.join('assets', 'jack.jpeg')
image = Image.open(image_path)

# Convert image to base64 for HTML embedding
image_base64 = image_to_base64(image)

# Create circular image and styled caption using Streamlit columns
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.markdown(f"""
        <style>
        .container {{
            display: flex;
            align-items: center;
            justify-content: center;
            flex-direction: column;
        }}
        img {{
            border-radius: 50%;
            width: 150px;
            height: 200px;
        }}
        .title {{
            font-weight: bold;
            font-size: 30px;
            margin-bottom: -20px; /* Negative margin to reduce space between title and description */
        }}
        .description {{
            font-size: 16px;
            text-align: center; /* Ensure text is centered under SPARROW */
        }}
        .initial {{
            font-weight: bold;
            color: #ff6699;
        }}
        </style>
        <div class="container">
            <img src="data:image/jpeg;base64,{image_base64}">
            <p class='title'>SPARROW</p>
            <br>
            <p class='description'>
                <span class='initial'>S</span>mart <span class='initial'>P</span>roposal <span class='initial'>A</span>ssistant for <span class='initial'>R</span>FP<br>
                <span class='initial'>R</span>esponse and <span class='initial'>O</span>ffer <span class='initial'>W</span>orkflow
            </p>
        </div>
        """, unsafe_allow_html=True)
