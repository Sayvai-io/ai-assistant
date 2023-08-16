""" Using Langchain Going to Generate a Server that can be used to shcedule meetings """
# Importing the required libraries
import os
import langchain
from pydantic import BaseModel
from langchain.llms import OpenAI
from agents.agentloader import AgentLoader
from tools.toolloader import ToolLoader
from langchain.chat_models import ChatOpenAI


with open("../../openai_api_key.txt", "r") as f:
    OPEN_AI_KEY = f.read()

with open("../../serp_api_key.txt", "r") as f:
    SERP_API_KEY = f.read()

os.environ["OPENAI_API_KEY"] = OPEN_AI_KEY
os.environ["SERPAPI_API_KEY"] = SERP_API_KEY

llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo-0613")

class LangchainServer:
    def __init__(self):
        self.llm = llm
        self.tools = ["serpapi", "llm-math"]
        self.agent = None
    
    def load_agent_and_tools(self, agent_name: str, tool_names: str) -> str:
        # loading agents
        tool_object = ToolLoader(tool_names, llm=self.llm)
        self.tools = tool_object.get_tools()
        agent_object = AgentLoader(tools=self.tools, llm=llm, agent_name=agent_name)
        self.agent = agent_object.get_agent()
        return "Agent Loaded Successfully"
    
    def get_response(self, message: str) -> str:        
        # This function is used to get the response from the agent 
        if self.agent is None:
            raise Exception("Agent Not Loaded")
        return self.agent.run(message)

if __name__ == "__main__":
    server = LangchainServer()
    server.load_agent_and_tools(agent_name="zero-shot-react-description", tool_names=["serpapi", "llm-math"])
    print(server.get_response("What is the square root of 4?"))
    


