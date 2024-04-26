import json
import time
import openai
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")


def generate(model, text, prompt, correction=False):
    """Generate structured JSON from text using OpenAI's GPT-4 via chat completions."""
    try:
        messages = [{"role": "user", "content": text}]
        if correction:
            messages.append(
                {"role": "system", "content": "Fix the format of the invalid json to a valid structured json: " + text})
        else:
            messages.append({"role": "system", "content": prompt})

        response = openai.chat.completions.create(
            model=model,
            messages=[
                {"role": "user", "content": text},
                {"role": "system", "content": prompt}
            ],
            max_tokens=150,
            temperature=0.7,
            top_p=1
        )
        response_text = response.choices[0].message.content
        response_data = json.loads(response_text)
        return response_data
    except json.JSONDecodeError:
        if not correction:
            print("fizing json")
            return generate(model, response_text, prompt, correction=True)
        else:
            print("Failed to correct JSON format after second attempt.")
            return {}
    except Exception as e:
        print(f"Failed to generate description: {e}")
        return {}


def read_text_file(file_path):
    """Read the contents of a text file."""
    with open(file_path, 'r') as file:
        return file.read()


file_path = "../../data/test/output/extracted_text.txt"
text = read_text_file(file_path)
prompt = (
    "Extract and format the provided text into a JSON object with specific details. "
    "Identify the following elements from the text: \n"
    "1. Email Address: Look for a string containing an 'at' symbol (@), and ensure it is in a standard email format. \n"
    "2. Due Date: Search for a date that specifies a deadline and format it appropriately. \n"
    "3. Specific Requirements: Summarize any detailed requirements related to the request mentioned in the text. \n"
    "Structure the output as a JSON object with three key-value pairs: 'email', 'dueDate', and 'reqs'. "
    "Use these exact keys, and ensure there is no subkey or nesting within the JSON object. If any information is missing, "
    "leave the corresponding value empty.  \n"
)


start_time = time.time()

model = "gpt-4"
print(f"Model: {model}")
print(f"Processing text from: {file_path}")
json_response = generate(model, text, prompt)

json_output_path = '../../data/test/output/structured_output.json'
with open(json_output_path, 'w') as json_file:
    json.dump(json_response, json_file, indent=4)

elapsed_time = time.time() - start_time
print(f"\n\nText processed in {elapsed_time:.2f} seconds")
print(f"Output saved to {json_output_path}")
