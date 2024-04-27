# src/data_preprocessing/find_match.py

import os
from langchain_pinecone import PineconeVectorStore
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Pinecone
from langchain_community.chat_models import ChatOpenAI
from langchain.chains.question_answering import load_qa_chain
from dotenv import load_dotenv

load_dotenv()

def find_match(requirements):
    index_name = "stihl"
    embeddings = OpenAIEmbeddings(openai_api_key=os.getenv("OPENAI_API_KEY"))

    OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
    PINECONE_API_KEY = os.environ.get('PINECONE_API_KEY')

    llm = ChatOpenAI(temperature=0, openai_api_key=OPENAI_API_KEY)
    chain = load_qa_chain(llm, chain_type="stuff")

    docsearch = Pinecone.from_existing_index(index_name, embeddings)

    query = f"Find me the top 2 products. These are my requirements : {requirements}"
    docs = docsearch.similarity_search(query)

    result = chain.run(input_documents=docs, question=query)
    print(result)
    return result



#print(find_match("Compact brushcutter offering comfort and efficiency in space-restricted urban gardens. It should feature a single-handed operation, a loop handle with a safety barrier, and a motor around 25 cm³ with a high power output."))
