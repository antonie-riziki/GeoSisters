import streamlit as st 
import sys
import os
import google.generativeai as genai


from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key = os.getenv("GOOGLE_API_KEY"))


def generate_auto_message(prompt):

    model = genai.GenerativeModel("gemini-1.5-flash", 
        system_instruction = '''

        	You are an AI Assistant specialized in generating professional, concise, and clear alert messages for a community outreach platform called CommUnity Africa. Your task is to generate {prompt} message based on the context provided by the user.

			Instructions:
			1. The message must be relevant, engaging, and easy to understand by a diverse audience.
			2. Maintain a professional and respectful tone.
			3. Keep the message between 20 to 50 words.
			4. If the alert is about emergencies, warnings, or updates, ensure urgency is reflected politely.
			5. If the alert is promotional, ensure it’s friendly and actionable.

			Respond with ONLY the generated alert message. Do not include explanations or preambles.

			Example Inputs:
			- "Weather Alert - Heavy rains expected"
			- "Promo Alert - New product launch"
			- "Health Update - Free clinic services"

			Example Outputs:
			- "🌧️ Weather Alert: Heavy rains are expected in your area today. Please stay indoors and avoid unnecessary travel. Stay safe!"
			- "🎉 Exciting News! Our new product line is now available. Visit our store today and enjoy exclusive launch offers."
			- "🏥 Health Alert: Free clinic services are available this Saturday at the Community Center. Take advantage of this opportunity for a free health check-up."


        '''
)
    response = model.generate_content(
    prompt,
    generation_config = genai.GenerationConfig(
        max_output_tokens=1000,
        temperature=0.1,
    )
)

    return st.text_area(label="", value=response.text)



import os
import glob
import getpass
import warnings
from typing import List, Union
from dotenv import load_dotenv
from langchain_community.document_loaders import (
    PyPDFLoader, CSVLoader
)
from langchain_core.prompts import PromptTemplate
from langchain.chains import RetrievalQA
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain.docstore.document import Document
warnings.filterwarnings("ignore")



load_dotenv()

GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")

if not GOOGLE_API_KEY:
  GOOGLE_API_KEY = getpass.getpass("Enter you Google Gemini API key: ")



def load_model():
  """
  Func loads the model and embeddings
  """
  model = ChatGoogleGenerativeAI(
      model="models/gemini-1.5-pro-001",
      google_api_key=GOOGLE_API_KEY,
      temperature=0.4,
      convert_system_message_to_human=True
  )
  embeddings = GoogleGenerativeAIEmbeddings(
      # model="models/embedding-004",
      model="models/text-embedding-004",
      google_api_key=GOOGLE_API_KEY
  )
  return model, embeddings


def load_documents(source_dir: str):
    """
    Load documents from multiple sources
    """
    documents = []

    file_types = {
      "*.pdf": PyPDFLoader,
      "*.cvs": CSVLoader
    }

    for pattern, loader in file_types.items():
        for file_path in glob.glob(os.path.join(source_dir, pattern)):
          documents.extend(loader(file_path).load())

        return documents


def create_vector_store(docs: List[Document], embeddings, chunk_size: int = 10000, chunk_overlap: int = 200):
  """
  Create vector store from documents
  """
  text_splitter = RecursiveCharacterTextSplitter(
      chunk_size=chunk_size,
      chunk_overlap=chunk_overlap
  )
  splits = text_splitter.split_documents(docs)
  return Chroma.from_documents(splits, embeddings).as_retriever(search_kwargs={"k": 5})




PROMPT_TEMPLATE = """
  Use the following pieces of context to answer the question at the end.
  If you don't know the answer, just say that you don't know, don't try to make up an answer.

  {context}

  Question: {question}
  Answer:"""



def get_qa_chain(source_dir):
  """Create QA chain with proper error handling"""

  try:
    docs = load_documents(source_dir)
    if not docs:
      raise ValueError("No documents found in the specified sources")

    llm, embeddings = load_model()
    # if not llm or not embeddings:model_type: str = "gemini",
    #   raise ValueError(f"Model {model_type} not configured properly")

    retriever = create_vector_store(docs, embeddings)

    prompt = PromptTemplate(
        template=PROMPT_TEMPLATE,
        input_variables=["context", "question"]
    )

    return RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=retriever,
        return_source_documents=True,
        chain_type_kwargs={"prompt": prompt}
    )
  except Exception as e:
    st.write(f"Error initializing QA system: {e}")
    return None



def query_system(query: str, qa_chain):
  if not qa_chain:
    return st.write("System not initialized properly")

  try:
    result = qa_chain({"query": query})
    if not result["result"] or "don't know" in result["result"].lower():
      return st.write("The answer could not be found in the provided documents")
    return st.write(f"Answer: {result['result']}\nSources: {[s.metadata['source'] for s in result['source_documents']]}")
  except Exception as e:
    return st.write(f"Error processing query: {e}")


# content_dir = "./src/agrof_health_paper.pdf"


# get_qa_chain(
#     source_dir=content_dir
# )


# query = "What are the most important impacts of tree-based interventions on health and wellbeing?"

# print(query_system(query, qa_chain))
    