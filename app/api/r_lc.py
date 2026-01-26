# app/api/lc_routes.py
from fastapi import APIRouter

from app.schemas.sch_lc import AgentRequest

from app.lc_components.lc_container import LCContainer

lcRou = APIRouter()
container = LCContainer()

@lcRou.post("/agent_basic", summary="Wage Agent 1.1")
async def agent_basic(payload: AgentRequest):
    prompt = payload.prompt
    return await container.basic_agent.invoke(prompt)


@lcRou.post("/agent_math", summary="Wage Agent 1.1")
async def agent_math(payload: AgentRequest):
    prompt = payload.prompt
    return await container.math_agent.invoke(prompt)



@lcRou.post("/agent_tavily", summary="Wage Agent 1.1")
async def agent_tavily(payload: AgentRequest):
    prompt = payload.prompt
    return await container.tavily_agent.invoke(prompt)
