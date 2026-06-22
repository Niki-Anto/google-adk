import os
from pathlib import Path
from dotenv import load_dotenv
from google.adk.agents.llm_agent import Agent
from google.adk.models.lite_llm import LiteLlm
from google.adk.tools.mcp_tool import MCPToolset, StreamableHTTPConnectionParams
from routing import FAST_MODEL

load_dotenv()
model = FAST_MODEL
instruction = (Path(__file__).parent / "order_assistance_instructions.txt").read_text().strip()

mcp_tools = MCPToolset(
    connection_params=StreamableHTTPConnectionParams(
        url=os.getenv("MCP_URL"),
        timeout=300
    )
)

order_assistance = Agent(
    model=LiteLlm(model=model),
    name='order_assistance',
    description='Your are order assistant for Lashi agent.',
    instruction=instruction,
    tools=[mcp_tools]
)
