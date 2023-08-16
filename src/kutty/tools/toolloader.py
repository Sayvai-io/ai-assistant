#Tools file for langchain
from pydantic import BaseModel
from langchain.agents import load_tools

class ToolLoader(BaseModel):
    
    """ This class is used to load the tools """
    def __init__(self, tools: list):
        """ This is the constructor of the class """
        self.tools = load_tools(tools)
        
    def get_descriptions(self):
        """ This method is used to get the descriptions of the tools """
        return [tool.description for tool in self.tools]
    
    def get_names(self):
        """ This method is used to get the names of the tools """
        return [tool.name for tool in self.tools]