""" Using Langchain Going to Generate a Server that can be used to shcedule meetings """
# Importing the required libraries
import os
import langchain
from langchain.llms import OpenAI
from agents.agentloader import AgentLoader
from tools.toolloader import ToolLoader

with open("openai_api_key.txt", "r") as f:
    OPEN_AI_KEY = f.read()

with open("serpapi_api_key.txt", "r") as f:
    SERP_API_KEY = f.read()

os.environ["OPENAI_API_KEY"] = OPEN_AI_KEY
os.environ["SERPAPI_API_KEY"] = SERP_API_KEY

llm = OpenAI(temperature=0)

class LangchainServer:
    def __init__(self):
        self.llm = llm
        self.tools = ["serpapi", "llm-math"]
        self.agent = None
    
    def load_agent_and_tools(self, agent_name: str, tool_names: str) -> str:
        self.tools = ToolLoader(tool_names)
        agent_object = AgentLoader(tools=self.tools, llm=llm, agent_name=agent_name)
        self.agent = agent_object.get_agent()
        return "Agent Loaded Successfully"
    
    def get_response(self, message: str) -> str:
        if self.agent is None:
            raise Exception("Agent Not Loaded")
        return self.agent.run(message)

if __name__ == "__main__":
    server = LangchainServer()
    server.load_agent_and_tools("test", ["serpapi", "llm-math"])
    print(server.get_response("What is the square root of 4?"))
    


