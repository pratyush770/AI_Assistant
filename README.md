## AI Assistant
**AI Assistant** is a generative AI project built using **Langchain** and **LangGraph**. It provides a variety of features to assist users in various tasks, including chatbot interactions, text translation, code assistance, grammar checking, exam tutoring and url/pdf q&a. The assistant leverages state-of-the-art AI models, along with **LangGraph** and **Custom Tools**, to deliver intelligent and helpful responses in each of these areas.
## Features
1. **Chatbot (Enhanced with LangGraph and Custom Tools)**  
   Engage in interactive conversations with the AI to answer questions, provide recommendations, or have casual discussions. The integration of LangGraph enables advanced reasoning and dynamic workflows, while 
   custom tools allow the chatbot to perform tasks such as:
   - Fetching real-time search results using DuckDuckGoSearch.
   - Retrieving the current day using the get_current_day function.
   - Performing basic arithmetic operations (add, sub, mul, div) for quick calculations.
     
2. **Text Translator**  
   Translate text between multiple languages seamlessly.
3. **Code Assistant**  
   Get help with coding tasks, including writing, debugging, and explaining code in various programming languages.
4. **Grammar Check**  
   Analyze and improve your text by identifying and correcting grammar, spelling, and punctuation errors.
5. **Exam Tutor**  
   Prepare for exams with personalized tutoring. The AI can help you with practice questions, explanations, and study strategies.
6. **Q&A Tool**  
   Upload an URL or PDF file and ask questions about its content. The AI processes the document and provides answers based on the uploaded material.
## Technologies Used  
- **Python**: Core programming language for the application.
  
- **Langchain**: Framework for building applications with large language models (LLMs), enabling reasoning, memory, and tool integration.
- **LangGraph** : A library within the Langchain ecosystem that enhances the chatbot's ability to perform complex workflows and multi-step reasoning.
- **Langsmith**: Platform for debugging, testing, monitoring, and improving LLM-powered applications.
- **Streamlit**: Framework for deploying the web application.
- **PyPDFLoader / WebBaseLoader**: Libraries for loading and processing PDF files or web pages.
- **Vector Store (AstraDB)**: For storing embeddings of the uploaded documents to enable efficient retrieval and question-answering.
- **Embedding Models (HuggingFaceEmbeddings)**: To generate vector representations of the document content.
## How to Deploy
- Clone the repository by the following command: `git clone https://github.com/pratyush770/AI_Assistant.git`
  
- Create a **virtual environment** (venv) first and install all the packages using `pip install requirements.txt`.
- Create your **GroqCloud** account by visiting the following link: https://console.groq.com
- Click on the **API Keys** section and generate an API key by giving a name to it.
- Create a secret_key.py file and add `sec_key = "Your generated secret key"`.
- Create your **Langsmith** account by visiting the following link: https://www.langchain.com/langsmith
- Click on the **Settings** section and generate an API key by giving a description to it.
- In the secret_key.py add `langsmith_sec_key = "Your generated secret key"`.
- Visit the **Astra DB Console** using this link: https://www.datastax.com/products/datastax-astra
- Click on **TRY FOR FREE** and sign in using your google account.
- Click on **Create a Database** to create the database.
- In the secret_key.py add `ASTRA_DB_API_ENDPOINT_SEC = "Your astra db enpdoint"` and `ASTRA_DB_API_TOKEN_SEC = "Your astra db token"`.
- Create a github repository and make sure to add **secret_key.py** in .gitignore for security reasons.
- Create your **Streamlit** account by visiting the following link: https://streamlit.io/cloud
- Click on **Create app** button on the top right and then select **Deploy a public app from Github**.
- Select your **created repository, branch, main file path** and give **app url** if needed.
- Click on the **Advanced settings** and add the following configurations.
  - `GROQ_API_KEY = "Your groqcloud secret key"`
  - `LANGCHAIN_API_KEY = "Your langsmith secret key"`
  - `ASTRA_DB_API_ENDPOINT_SEC = "Your astra db endpoint"`
  - `ASTRA_DB_API_TOKEN_SEC = "Your astra db token"`
- Click on the **Deploy** button and you're done!
    
## Deployment  
The application is deployed on **Streamlit** and is accessible via the following link: **[AI Assistant](https://ai-assistant-python.streamlit.app/)**
