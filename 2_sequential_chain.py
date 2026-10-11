from langchain_huggingface import HuggingFaceEndpoint, ChatHuggingFace
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

import os
os.environ['LANGSMITH_PROJECT']= 'Sequential-LLM-Knight'

load_dotenv()

prompt1 = PromptTemplate(
    template='Generate a detailed report on {topic}',
    input_variables=['topic']
)

prompt2 = PromptTemplate(
    template='Generate a 5 pointer summary from the following text \n {text}',
    input_variables=['text']
)

llm = HuggingFaceEndpoint(
     repo_id="Qwen/Qwen3-4B-Instruct-2507",
     task="text-generation",
     max_new_tokens=412,
     temperature=0.7,)


model = ChatHuggingFace(llm=llm)


parser = StrOutputParser()

chain = prompt1 | model | parser | prompt2 | model | parser

config = {'tags':['Llm_app','Report_summarizers','Application'],
          'metadata':{'model1':'Qwen/Qwen3-4B-Instruct-2507',
                      'model2':'Qwen/Qwen3-4B-Instruct-2507',
                      'model1_temp':0.7
                      }}
result = chain.invoke({'topic': 'Where & How i can scrape Manufacturer/Producer in the Noida and Ghaziabad city in brief ?'})


print(result)
