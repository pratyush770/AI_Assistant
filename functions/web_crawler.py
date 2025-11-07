import os
import streamlit as st
from langchain_community.document_loaders import WebBaseLoader
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
def get_embeddings():
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
def get_vector_store(_embeddings):
    """Centralized function to create the vector store."""
    return AstraDBVectorStore(
        collection_name="astradb_langchain",
        embedding=_embeddings,
        api_endpoint=ASTRA_DB_API_ENDPOINT,
        token=ASTRA_DB_APPLICATION_TOKEN,
        namespace=ASTRA_DB_KEYSPACE,
    )


def is_vector_store_initialized(vector_store, url):
    """Check if the vector store already contains data for the given url."""
    try:
        # perform a test query to see if any data exists
        return len(vector_store.similarity_search("the", k=1, filter={"source": url})) > 0
    except Exception:
        return False


def initialize_vector_store(url, vector_store):
    """Initialize the vector store for the given URL."""
    # print(f"Initializing vector store for url: {url}")
    loader = WebBaseLoader(url)
    documents = loader.load()  # creates list of documents
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    docs = text_splitter.split_documents(documents)  # splits the documents into chunk size of 1000
    vector_store.add_documents(documents=docs)
    return vector_store


def query_vector_store(vector_store, query, url):
    """Query the vector store for the given query."""
    retriever = vector_store.as_retriever(
        search_type="similarity",
        search_kwargs={"k": 3}
    )
    relevant_docs = retriever.invoke(query, filter={"source": url})  # retrieve relevant documents based on the query
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
    url = input("Enter the url of the webpage you want to index: ").strip()  # prompt the user to enter a url
    embeddings = get_embeddings()  # get centralized embeddings
    vector_store = get_vector_store(embeddings)  # get centralized vector store
    if not is_vector_store_initialized(vector_store, url):  # check if the vector store is already initialized
        vector_store = initialize_vector_store(url, vector_store)
    else:
        print("Vector store already initialized for this url. Skipping data addition.")
    while True:
        query = input("Enter your query (or type 'exit' to quit): ").strip()
        if query.lower() == "exit":
            print("Exiting the program.")
            break
        # query the vector store and display the result
        result = query_vector_store(vector_store, query, url)
        print(result)
