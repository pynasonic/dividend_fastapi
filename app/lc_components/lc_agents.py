# agents.py
from langchain.agents import create_agent
from langchain_core.messages import HumanMessage

class AgentFactory:
    def __init__(self, model):
        self.model = model

    def create(self, *, tools=None, system_prompt=None):
        return create_agent(
            model=self.model,
            tools=tools or [],
            system_prompt=system_prompt,
        )


class BaseAgent:
    def __init__(self, agent):
        self.agent = agent

    async def invoke(self, prompt: str):
        return await self.agent.ainvoke(
            {"messages": [HumanMessage(content=prompt)]}
        )


class BasicAgent(BaseAgent):
    def __init__(self, factory: AgentFactory):
        agent = factory.create()
        super().__init__(agent)


class MathToolAgent(BaseAgent):
    def __init__(self, factory: AgentFactory, tools):
        agent = factory.create(
            tools=tools,
            system_prompt=(
                "You are an arithmetic wizard. "
                "Use your tools to calculate the square root and square of any number."
            ),
        )
        super().__init__(agent)


class TavilyWebSearchAgent(BaseAgent):
    def __init__(self, factory: AgentFactory, tools):
        agent = factory.create(
            tools=tools,
            system_prompt=(
                "How up to date is your training knowledge?"
            ),
        )
        super().__init__(agent)
