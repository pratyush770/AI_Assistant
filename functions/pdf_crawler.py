import os
import streamlit as st
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
# from secret_key import ASTRA_DB_API_TOKEN_SEC, ASTRA_DB_API_ENDPOINT_SEC, sec_key
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_astradb import AstraDBVectorStore

sec_key = st.secrets["GROQ_API_KEY"]
astra_db_api_endpoint = st.secrets["ASTRA_DB_API_ENDPOINT_SEC"]
astra_db_application_token = st.secrets["ASTRA_DB_API_TOKEN_SEC"]
# os.environ['GROQ_API_KEY'] = sec_key  # secret_key set as environment variable
# os.environ['ASTRA_DB_API_ENDPOINT_SEC'] = ASTRA_DB_API_ENDPOINT_SEC
# os.environ['ASTRA_DB_API_TOKEN_SEC'] = ASTRA_DB_API_TOKEN_SEC
langsmith_sec_key = st.secrets["LANGSMITH_API_KEY"]
os.environ["LANGSMITH_API_KEY"] = langsmith_sec_key
os.environ['LANGCHAIN_TRACING_V2'] = "true"
os.environ['LANGCHAIN_PROJECT'] = "AI Assistant"

# configuration for Astra DB
ASTRA_DB_API_ENDPOINT = astra_db_api_endpoint
ASTRA_DB_APPLICATION_TOKEN = astra_db_application_token
ASTRA_DB_KEYSPACE = "AstraDb_Langchain"

# initialize llm
llm = ChatGroq(
    model="qwen/qwen3-32b",  # model name
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2,
    api_key=sec_key
)


# centralized embedding configuration
@st.cache_resource(show_spinner=False)
def get_embeddings_pdf():
    """Centralized function to create embeddings."""
    model_name = "sentence-transformers/multi-qa-MiniLM-L6-cos-v1"
    model_kwargs = {'device': 'cpu'}  # use local CPU instead of GPU
    encode_kwargs = {'normalize_embeddings': False}  # avoid computation
    return HuggingFaceEmbeddings(
        model_name=model_name,
        model_kwargs=model_kwargs,
        encode_kwargs=encode_kwargs
    )


# centralized vector store initialization
@st.cache_resource(show_spinner=False)
def get_vector_store_pdf(_embeddings):
    """Centralized function to create the vector store."""
    return AstraDBVectorStore(
        collection_name="astradb_langchain",
        embedding=_embeddings,
        api_endpoint=ASTRA_DB_API_ENDPOINT,
        token=ASTRA_DB_APPLICATION_TOKEN,
        namespace=ASTRA_DB_KEYSPACE,
    )


def is_vector_store_initialized_pdf(vector_store, pdf_name):
    """Check if the vector store already contains data for the given pdf."""
    try:
        # perform a test query to see if any data exists
        return len(vector_store.similarity_search("the", k=1, filter={"source": pdf_name})) > 0
    except Exception:
        return False


def initialize_vector_store_pdf(pdf_name, pdf_text, vector_store):
    """Initialize the vector store for the given PDF."""
    print(f"Initializing vector store for PDF: {pdf_name}")
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    docs = text_splitter.split_text(pdf_text)  # Split the PDF text into chunks
    vector_store.add_texts(texts=docs, metadatas=[{"source": pdf_name}] * len(docs))
    return vector_store


def query_vector_store_pdf(vector_store, query, pdf_name):
    """Query the vector store for the given query."""
    retriever = vector_store.as_retriever(
        search_type="similarity",
        search_kwargs={"k": 3}
    )
    relevant_docs = retriever.invoke(query, filter={"source": pdf_name})  # retrieve relevant documents based on the query
    content = " ".join(doc.page_content for doc in relevant_docs)
    template = """
        Answer the query asked by the user, taking the document into consideration.
        Query: {query}
        Document: {content}
    """
    prompt_template = ChatPromptTemplate.from_template(template)
    chain = prompt_template | llm | StrOutputParser()
    result = chain.invoke({"query": query, "content": content})
    return result


if __name__ == "__main__":
    # Prompt the user to upload a PDF file
    pdf_file_path = input("Enter the path to the PDF file you want to index: ").strip()
    if not os.path.exists(pdf_file_path):
        print("File not found. Please provide a valid file path.")
        exit()

    # Extract text from the PDF file
    loader = PyPDFLoader(pdf_file_path)
    documents = loader.load()  # Load the PDF content
    pdf_text = "\n".join(doc.page_content for doc in documents)  # Combine all pages into a single string
    pdf_name = os.path.basename(pdf_file_path)  # Use the file name as the source identifier

    # Get centralized embeddings and vector store
    embeddings = get_embeddings_pdf()
    vector_store = get_vector_store_pdf(embeddings)

    # Check if the vector store is already initialized for this PDF
    if not is_vector_store_initialized_pdf(vector_store, pdf_name):
        vector_store = initialize_vector_store_pdf(pdf_name, pdf_text, vector_store)
    else:
        print("Vector store already initialized for this PDF. Skipping data addition.")

    # Continuously prompt the user for queries
    while True:
        query = input("Enter your query (or type 'exit' to quit): ").strip()
        if query.lower() == "exit":
            print("Exiting the program.")
            break

        # Query the vector store and display the result
        result = query_vector_store_pdf(vector_store, query, pdf_name)
        print(result)

