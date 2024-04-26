# json_creation.py

import json
import openai
import os
from dotenv import load_dotenv

load_dotenv()

def create_json_from_text(text):
    api_key = os.getenv("OPENAI_API_KEY")
    openai.api_key = api_key
    model = "gpt-4"
    prompt = (
        "Extract and format the provided text into a JSON object with specific details. "
        "Identify the following elements from the text: \n"
        "1. Email Address: Look for a string containing an 'at' symbol (@), and ensure it is in a standard email format. \n"
        "2. Due Date: Search for a date that specifies a deadline and format it appropriately. \n"
        "3. Specific Requirements: Summarize any detailed requirements related to the request mentioned in the text. \n"
        "Structure the output as a JSON object with three key-value pairs: 'email', 'dueDate', and 'reqs'."
    )

    try:
        response = openai.chat.completions.create(
            model=model,
            messages=[
                {"role": "user", "content": text},
                {"role": "system", "content": prompt}
            ],
            max_tokens=150
        )
        response_data = json.loads(response.choices[0].message.content)
        return response_data
    except Exception as e:
        print(f"Failed to generate JSON: {e}")
        return None

