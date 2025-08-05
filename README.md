## AI Assistant
**AI Assistant** is a generative AI project built using **Langchain** and **LangGraph**. It provides a variety of features to assist users in various tasks, including chatbot interactions, text translation, code assistance, grammar checking, exam tutoring and url/pdf q&a. The assistant leverages state-of-the-art AI models, along with **LangGraph**, to deliver intelligent and helpful responses in each of these areas.
## Features
1. **Chatbot (Enhanced with LangGraph)**  
   Engage in interactive conversations with the AI to answer questions, provide recommendations, or have casual discussions. The integration of LangGraph enables advanced reasoning and dynamic workflows.
     
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
- **Azure Kubernetes Service (AKS)**: For container orchestration and deployment of the application.
- **Docker**: For containerizing the application.
- **PyPDFLoader / WebBaseLoader**: Libraries for loading and processing PDF files or web pages.
- **Vector Store (AstraDB)**: For storing embeddings of the uploaded documents to enable efficient retrieval and question-answering.
- **Embedding Models (HuggingFaceEmbeddings)**: To generate vector representations of the document content.
- **Clever Cloud Database** : SQL database for managing user authentication (login and sign-up).
## How to Deploy
### Prerequisites
1. Azure CLI: Install the Azure CLI from **[here](https://learn.microsoft.com/en-us/cli/azure/install-azure-cli-windows?view=azure-cli-latest&pivots=msi)**.
   
2. Kubernetes CLI (kubectl): Install kubectl from **[here](https://kubernetes.io/docs/tasks/tools/install-kubectl-windows/)**.
3. Docker: Install Docker from **[here](https://docs.docker.com/desktop/setup/install/windows-install/)**.
    
### Deployment Steps
1. Clone the repository using the following command: `git clone https://github.com/pratyush770/AI_Assistant.git`.
   
2. Create a virtual environment and install all dependencies using the requirements.txt file.
3. Create your **GroqCloud** account by visiting the following link: **[GroqCloud](https://console.groq.com)**.
4. Create a secret_key.py file and add `sec_key = "Your generated secret key"`.
5. Create your **Langsmith** account by visiting the following link: **[Langsmith](https://www.langchain.com/langsmith)**.
6. In the secret_key.py add `langsmith_sec_key = "Your generated secret key"`.
7. Visit the **Astra DB Console** using this link: **[Astra DB](https://www.datastax.com/products/datastax-astra)**
8. In the secret_key.py add `ASTRA_DB_API_ENDPOINT_SEC = "Your astra db enpdoint"` and `ASTRA_DB_API_TOKEN_SEC = "Your astra db token"`.
9. Visit **Clever Cloud** and login for storing user details using this link: **[Clever Cloud](https://console.clever-cloud.com)**
10. Create an **add on** and select on **MySQL** and create a database.
11. In the secret_key.py add the following database details.
    - ```
      HOST = "Your db host name"
      USER = "Your db user name"
      PASSWORD = "Your db password"
      DATABASE = "Your db name"
      ```
12. Create a .dockerignore file to exclude sensitive files:
    - ```
      .streamlit/secrets.toml
      secret_key.py```
13. Build the Docker image using the following command:
    - `docker build -t ai-assistant:latest`
14. Push the image to a container registry (e.g. Azure Container Registry):
    - ```
      az acr login --name <your-acr-name>`
      docker tag ai-assistant:latest <your-acr-name>.azurecr.io/ai-assistant:latest
      docker push <your-acr-name>.azurecr.io/ai-assistant:latest
      ```
15. Login to azure cli using the command: `az login`.
16. Set the default resource group using the command: `az configure --defaults group=<your-resource-group>`.
17. Get AKS credentials using the command: `az aks get-credentials --name <your-aks-cluster-name>`.
18. Update the deployment.yaml file to use the Docker image from your container registry:
    - ```
      spec:
       containers:
       - name: ai-assistant
         image: <your-acr-name>.azurecr.io/ai-assistant:latest
         imagePullPolicy: Always
      ```
19. Apply the Kubernetes manifests:
    - ```
      kubectl apply -f deployment.yaml
      kubectl apply -f service.yaml
      ```
20. Check the status of the pods using the command: `kubectl get pods`.
21. Access the application via the service's external IP using the command: `kubectl get svc`.

## Deployment
The application is deployed on Azure Kubernetes Service (AKS) and is accessible via the external IP provided by the Kubernetes service through the link: **[AI Assistant](http://ai-assistant.cloud/)**.
