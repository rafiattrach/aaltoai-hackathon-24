import ollama

def extract_name_from_email(email):
    """Extracts the first part of the email and capitalizes it to use as a name."""
    name_part = email.split('@')[0]  # Take the part before '@'
    # Split by possible delimiters and take the first part as the name
    return name_part.split('.')[0].capitalize()  # Assumes format like 'john.doe@example.com'

def generate_email(model, data_json):
    """Generate an email from given JSON data using a specified model."""
    # Extract name from the email for a more personalized greeting
    name = extract_name_from_email(data_json['email'])

    text_representation = f"Create one single Email based on this template, dont use any placeholders in the email and keep it short but impressive (good sales)! Only use the information in this prompt and don't repeat information! Here it goes: Dear {name},\nBased on your requirements and the due date of {data_json['dueDate']}, we propose the following solutions: {data_json['matchedResults']}.\nPlease let us know if you need further information or if you would like to proceed with any of these options.\nBest regards STIHL Junior Sales Manager Rajna."
    
    stream = ollama.chat(
        model=model,
        messages=[{'role': 'user', 'content': text_representation}],
        stream=True
    )
    
    email_content = ""
    for chunk in stream:
        if 'message' in chunk and 'content' in chunk['message']:
            email_content += chunk['message']['content']
    
    return email_content
'''
def main():
    # Example JSON input
    example_json = {
        "dueDate": "2023-05-01",
        "email": "john.doe@example.com",
        "reqs": "USB-C, HDMI support",
        "matchedResults": "Product A, Product B"
    }
    model = "phi3"
    email = generate_email(model, example_json)
    print(email)

if __name__ == "__main__":
    main()
'''