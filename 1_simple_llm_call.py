from dotenv import load_dotenv
from langchain_huggingface import HuggingFaceEndpoint, ChatHuggingFace
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

# Simple one-line prompt
prompt = PromptTemplate.from_template("{question}")

llm = HuggingFaceEndpoint(
     repo_id="Qwen/Qwen3-4B-Instruct-2507",
     task="text-generation",
     max_new_tokens=256,
     temperature=0.2,)


model = ChatHuggingFace(llm=llm)
parser = StrOutputParser()

# Chain: prompt → model → parser
chain = prompt | model | parser

# Run it
result = chain.invoke({"question": "What is the population of jaipur"})
print(result)
