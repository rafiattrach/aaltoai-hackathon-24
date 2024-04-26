import glob
from pypdf import PdfReader
from docx import Document
import base64
import requests
import os
from dotenv import load_dotenv

load_dotenv()


def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')


def generate_description_with_gpt4(image_path):
    api_key = os.getenv('OPENAI_API_KEY')
    base64_image = encode_image(image_path)

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    payload = {
        "model": "gpt-4-turbo",
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "Extract the text from the image."
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}"
                        }
                    }
                ]
            }
        ],
        "max_tokens": 300
    }

    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
    if response.status_code == 200:
        try:
            response_data = response.json()
            return response_data['choices'][0]['message']['content']
        except (KeyError, IndexError) as e:
            print(f"Error extracting description: {e}")
            return "Failed to extract description"
    else:
        print(f"API request failed with status code {response.status_code}")
        return "Failed to extract description"


def append_to_file(file_path, text):
    if text and text != "Failed to extract description":
        with open(file_path, 'a', encoding='utf-8') as file:
            file.write('\n' + text)


def find_files(directory, extensions):
    files = []
    for ext in extensions:
        files.extend(glob.glob(os.path.join(directory, f'*.{ext}')))
    return files


def extract_text_from_pdf(pdf_path):
    reader = PdfReader(pdf_path)
    text = []
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text.append(page_text)
    return "\n".join(text)


def extract_text_from_docx(file_path):
    doc = Document(file_path)
    full_text = []
    for para in doc.paragraphs:
        full_text.append(para.text)
    return '\n'.join(full_text)


def main():
    directory = "../../data/test"
    output_file_path = '../../data/test/output/extracted_text.txt'

    # Process images
    images = find_files(directory, ['png', 'jpg', 'jpeg'])
    for image_url in images:
        print(f"Processing image: {image_url}")
        description = generate_description_with_gpt4(image_url)
        if description:
            append_to_file(output_file_path, description)

    # Process PDFs
    pdf_files = find_files(directory, ['pdf'])
    for pdf_path in pdf_files:
        extracted_text = extract_text_from_pdf(pdf_path)
        append_to_file(output_file_path, extracted_text)

    # Process DOCX files
    docx_files = find_files(directory, ['docx'])
    for file_path in docx_files:
        extracted_text = extract_text_from_docx(file_path)
        append_to_file(output_file_path, extracted_text)

    print(f"All files processed. Text saved to {output_file_path}")


if __name__ == "__main__":
    main()
