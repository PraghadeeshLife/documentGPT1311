import os
from supabase.client import Client, create_client
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import SupabaseVectorStore
from langchain.document_loaders import TextLoader, PyMuPDFLoader
from langchain.chat_models import ChatOpenAI
from langchain.chains import RetrievalQA
from dotenv import load_dotenv

load_dotenv()

open_ai_api_key = os.getenv('OPENAI_API_KEY')
supabase_url = os.getenv('SUPABASE_URL')
supabase_key = os.getenv('SUPABASE_KEY')
supabase: Client = create_client(supabase_url, supabase_key)

def ingest_document(file_path):
  if ".txt" in file_path:
    print("Loaded the txt file")
    loader = TextLoader(file_path)
  elif ".pdf" in file_path:
    print("Loaded the pdf file")
    loader = PyMuPDFLoader(file_path)
  documents = loader.load()
  text_splitter = CharacterTextSplitter(chunk_size=2500, chunk_overlap=300)
  docs = text_splitter.split_documents(documents)
  embeddings = OpenAIEmbeddings(openai_api_key=open_ai_api_key)
  vector_store = SupabaseVectorStore.from_documents(docs, embeddings, client=supabase, table_name='documents')
  return vector_store

def retrieve_vector_store():
  embeddings = OpenAIEmbeddings(openai_api_key=open_ai_api_key)
  return SupabaseVectorStore(
    client=supabase,
    embedding=embeddings,
    table_name="documents",
    query_name="match_documents"
)

def generate_answer(query, vector_store):
  llm = ChatOpenAI(model_name='gpt-4',openai_api_key=open_ai_api_key)
  qa = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=vector_store.as_retriever())
  llm_response = qa(query)
  return (llm_response["result"])