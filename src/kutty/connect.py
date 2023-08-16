""" Using Langchain Going to Generate a Server that can be used to shcedule meetings """
# Importing the required libraries
import os
import langchain
from langchain.llms import OpenAI
from 

with open("openai_api_key.txt", "r") as f:
    OPEN_AI_KEY = f.read()

with open("serpapi_api_key.txt", "r") as f:
    SERP_API_KEY = f.read()

os.environ["OPENAI_API_KEY"] = OPEN_AI_KEY
os.environ["SERPAPI_API_KEY"] = SERP_API_KEY

llm = OpenAI(temperature=0)

# Creating a function that will be used to generate the response


    

