from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_ollama import OllamaLLM
import streamlit as st

model = OllamaLLM(model="llama3.1:8b")

template = "Translate the following into {language}"
prompt = ChatPromptTemplate.from_messages(
    [("system", template), ("user", "{text}")]
)

parser = StrOutputParser()

chain = prompt | model | parser

st.title("Language Translator using Ollama")

# Create input fields for users to type the text and the target translation language
input_text = st.text_input("Type the Word or Sentence", "Hello")
input_language = st.text_input("Translation Language", "Swedish")

# Define a button that will trigger the translation process
if st.button("Translate"):
    try:
        # Invoke the chain of prompt, model, and parser to generate the translated output
        translated_output = chain.invoke({"language": input_language, "text": input_text})

        # Display the translated output in the app
        st.write("**Translated output:**", translated_output)
    except Exception as e:
        # Handle errors and display error message if translation fails
        st.error(f"Error During Translation: {e}")