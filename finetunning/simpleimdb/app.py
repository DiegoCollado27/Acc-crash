import os

#install requirements.txt in the terminal

os.system('pip install -r requirements.txt')

from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings
from langchain_openai import ChatOpenAI
from langchain.schema import StrOutputParser
from langchain.prompts import PromptTemplate
from openai import OpenAI
from transformers import pipeline
import numpy as np





load_dotenv()
secret_string= os.getenv('OPENAI_API_KEY')

#create simple langchain QA from question of user

engine = "ft:gpt-3.5-turbo-1106:sinensia:movies:9PDh7plA"
client = OpenAI(api_key=secret_string)
llm = ChatOpenAI(model=engine, temperature=0, openai_api_key=secret_string)

prompt = PromptTemplate.from_template(
    """
you are an imdb expert and you have to answer the following question about movies:

{input}

answer the question in a concise way, if you don't know the answer say you don't know.

answer:

"""
)

chain = prompt | llm | StrOutputParser()

transcriber = pipeline("automatic-speech-recognition", model="openai/whisper-base.en")

#make a sinmple gradio interface that can input text or voice and output text

def voice_to_text(audio):
    sr, y = audio
    y = y.astype(np.float32)
    y /= np.max(np.abs(y))

    question = transcriber({"sampling_rate": sr, "raw": y})["text"]
    return answer_question(question)

def answer_question(question):
    return chain.invoke({"input": question})

# interface with two inputs, one for text and one for voice and one output for text
import gradio as gr

iface = gr.Interface(fn=lambda text, audio: answer_question(text) if text else voice_to_text(audio), inputs=[gr.Textbox(lines=2, placeholder="Ask a question about movies"), gr.Audio()], outputs="text")

iface.launch()
