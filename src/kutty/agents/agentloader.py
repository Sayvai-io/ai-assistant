# Agent Loader Class
# Loads the agent from the agent file

from typing import List, Any
from rich import print as rprint
from langchain.agents import initialize_agent

class AgentLoader:
    """This class is used to load Agent"""
    
    def __init__(self, tools: Any, llm: Any):
        """Initializes the AgentLoader class"""
        self.tools = tools
        self.agent = None
        self.llm = llm
    
    def load_agent(self, agent_name: str, verbose: bool = False) -> str:
        """Loads the agent from the agent file"""
        self.agent = initialize_agent(self.tools, self.llm, agent_name, verbose)  
        rprint(f"[bold green]Agent {agent_name} loaded successfully![/bold green]")
        return self.agent
    
    def get_agent_template(self) -> List[str]:
        """Returns the agent template"""
        if self.agent is None:
            raise Exception("Agent not loaded")
        return self.agent.agent.llm_chain.prompt.template
    
    
        