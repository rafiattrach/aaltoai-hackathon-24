# aaltoai-hackathon-24
# Project Documentation

## Quick Overview
The project aimed to streamline the RFP process by automating the review and creation of client proposals. 
Utilizing the latest 247-page STIHL Catalogue 2024, we processed product descriptions with Langchain chunking and OpenAI Embeddings, storing them in a Pinecone Vector Database. 
Synthetically generated RFPs by GPT-4 were formatted into multiple file types, with key details extracted into JSON and similarly embedded. 
A RAG pipeline facilitated the retrieval of top product matches, leveraging GPT-4 for final selections, which were then composed into client emails using Microsoft's PHI3.

## Demo

https://github.com/rafiattrach/aaltoai-hackathon-24/assets/64313536/7e98ff79-2eec-476f-990f-65e7a48fcbbc

## Installation & Setup

#### Create Virtual Environment

  ```python
  python -m venv hackathon_ai
  ```

#### Activation

- **macOS/Linux**:

  ```bash
  source hackathon_ai/bin/activate
  ```
- **Windows**:

  ```powershell
  .\hackathon_ai\Scripts\activate
  ```

#### Installing Dependencies

Before running the project, you need to install all dependencies. To download the `requirements.txt` file, use the following command:

  ```python
  pip install -r requirements.txt
  ```

Additionally, to successfully run the web application as well as the scripts and notebooks that use the **OpenAI API** and the **Pinecone API**, you need to paste your own API key from OpenAI and from Pinecone into the `.env` file:

`OPENAI_API_KEY=<YOUR_OPENAI_KEY>`

`PINECONE_API_KEY=<YOUR_PINECONE_API_KEY>`

#### Web Application (Streamlit)

To run the web application after you have installed all the dependencies, you can run this command down below from the project root directory (**make sure you added the OpenAI key in the .env file!**):

  ```python
  streamlit run app/app.py 
  ```
