from secret_key import sec_key
import os
from langchain_huggingface import HuggingFaceEndpoint
from langchain_core.prompts import PromptTemplate
from langchain.schema.runnable import RunnableSequence

# sec_key = st.secrets["HUGGINGFACEHUB_API_TOKEN"]
os.environ['HUGGINGFACEHUB_API_TOKEN'] = sec_key

repo_id = "mistralai/Mistral-7B-Instruct-v0.2"
llm = HuggingFaceEndpoint(
    repo_id=repo_id, temperature=0.6,
    model_kwargs={"max_length": 128, "token": sec_key}
)


def generate_prompt(query):
    template = f"""
    Question: {query}
    Provide the most relevant and concise answer.
    """
    prompt = PromptTemplate(template=template, input_variables=["query"])
    sequence = RunnableSequence(first=prompt, last=llm)
    response = sequence.invoke({"query": query})
    return response


if __name__ == "__main__":
    print(generate_prompt("What is gen ai"))
