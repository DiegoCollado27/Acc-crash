
from langchain_anthropic import ChatAnthropic
from langchain_core.output_parsers import StrOutputParser
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv
import os

load_dotenv()

model = ChatAnthropic(model='claude-2.1',
                      anthropic_api_key=os.getenv("ANTHROPIC_API_KEY"))

parser = StrOutputParser()
prompt_template = PromptTemplate.from_template("Cuéntame un chiste de padre")
prompt_template.format()

chain = prompt_template | model | parser

print(chain.invoke({}))