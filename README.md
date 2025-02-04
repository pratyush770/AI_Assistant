## AI Assistant
**AI Assistant** is a generative AI project built using **Langchain**. It provides a variety of features to assist users in various tasks, including chatbot interactions, text translation, code assistance, grammar checking, and exam tutoring. The assistant leverages state-of-the-art AI models to deliver intelligent and helpful responses in each of these areas.
## Features
1. **Chatbot**  
   Engage in interactive conversations with the AI to answer questions, provide recommendations, or have casual discussions.

2. **Text Translator**  
   Translate text between multiple languages seamlessly.
3. **Code Assistant**  
   Get help with coding tasks, including writing, debugging, and explaining code in various programming languages.
4. **Grammar Check**  
   Analyze and improve your text by identifying and correcting grammar, spelling, and punctuation errors.
5. **Exam Tutor**  
   Prepare for exams with personalized tutoring. The AI can help you with practice questions, explanations, and study strategies.
## Technologies Used  
- **Python**: Core programming language for the application.
  
- **Langchain**: Advanced language processing for generating names and menu items.  
- **Streamlit**: Framework for deploying the web application.
## How to Deploy
- Clone the repository by the following command: `git clone https://github.com/pratyush770/AI_Assistant.git`
  
- Create a **virtual environment** (venv) first and install all the necessary packages using **pip install requriements.txt**.
- Create your **GroqCloud** account by visiting the following link: https://console.groq.com
- Click on the **API Keys** section and generate an API key by giving a name to it.
- Create a secret_key.py file and add `sec_key = "Your generated secret key"`.
- Create your **Langsmith** account by visiting the following link: https://www.langchain.com/langsmith
- Click on the **Settings** section and generate an API key by giving a description to it.
- In the secret_key.py add `langsmith_sec_key = "Your generated secret key"`.
- Create a github repository and make sure to add secret_key.py in .gitignore for security reasons.
- Create your **Streamlit** account by visiting the following link: https://streamlit.io/cloud
- Click on **Create app** button on the top right and then select **Deploy a public app from Github**.
- Select your **created repository, branch, main file path** and give **app url** if needed.
- Click on the **Advanced settings** and add the following configurations.
  - `GROQ_API_KEY = "Your groqcloud secret key"`
  - `LANGCHAIN_API_KEY = "Your langsmith secret key"`
- Click on the **Deploy** button and you're done!
    
## Deployment  
The application is deployed on **Streamlit** and is accessible via the following link:  
[Live Demo] https://ai-assistant-python.streamlit.app/
