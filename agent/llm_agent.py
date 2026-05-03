from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from dotenv import load_dotenv
import os

load_dotenv()

# Initialize LLM
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

def run_prompt(prompt_text, user_input):
    prompt = PromptTemplate(
        input_variables=["input"],
        template=prompt_text
    )

    formatted_prompt = prompt.format(input=user_input)

    response = llm.invoke(formatted_prompt)

    return response.content
