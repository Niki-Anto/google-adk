from pathlib import Path
from google.adk.agents.llm_agent import Agent
from google.adk.models.lite_llm import LiteLlm
import warnings
from tools.rag import retrieve_relevant_chunks
from order_assist_agent import order_assistance
from routing import FAST_MODEL, DEEP_MODEL, classify_query
from google.adk.agents.callback_context import CallbackContext
from google.adk.models.llm_request import LlmRequest
from google.adk.models.llm_response import LlmResponse
import json
from langsmith.integrations.google_adk import configure_google_adk


warnings.filterwarnings("ignore", category=UserWarning, module="pydantic")


# ADK calls this BEFORE the agent processes the user message
#def before_agent_callback(callback_context: CallbackContext):
#    print(">>> current event is about to run")

# ADK calls this AFTER the agent has finished responding
#def after_agent_callback(callback_context: CallbackContext):
#    print(">>> current event is just finished")

#def before_model_callback(callback_context: CallbackContext, llm_request: LlmRequest):
#    print("\n========== LLM REQUEST ==========")
#    print(json.dumps(llm_request.model_dump(), indent=2, default=str))
#    print("=================================\n")

#def after_model_callback(callback_context: CallbackContext, llm_response: LlmResponse):
#    print("\n========== LLM RESPONSE ==========")
#    print(json.dumps(llm_response.model_dump(), indent=2, default=str))
#    print("==================================\n")


instruction = (Path(__file__).parent / "root_agent_instruction.txt").read_text().strip()

configure_google_adk()

root_agent = Agent(
    model=LiteLlm(model=FAST_MODEL),
    name='Lashi',
    description='Your are an ecombot and supports the customer about sales platform for an **electronics e-commerce store** which includes phones, TV decoders, accessories and washing machines ',
    instruction=instruction,
    tools=[retrieve_relevant_chunks],
    sub_agents=[order_assistance],
    before_agent_callback=None,
    after_agent_callback=None,
    before_model_callback=None,
    after_model_callback=None
)
