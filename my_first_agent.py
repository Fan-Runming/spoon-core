import os
from spoon_ai.agents import SpoonReactAI
from spoon_ai.chat import ChatBot
from spoon_ai.tools.crypto_tools import get_crypto_tools

# Create your first agent
def create_agent():
    # Configure LLM
    llm = ChatBot(
        # Pick up provider/model from env to support Gemini out of the box.
        # Example: set DEFAULT_LLM_PROVIDER=gemini and GEMINI_API_KEY=***
        llm_provider=os.getenv("LLM_PROVIDER") or os.getenv("DEFAULT_LLM_PROVIDER") or "gemini",
        model_name=os.getenv("LLM_MODEL") or "gemini-2.5-pro",
        temperature=0.3
    )

    # Create agent with tools
    agent = SpoonReactAI(
        llm=llm,
        tools=[*get_crypto_tools()]  # requires `pip install -e toolkit`
    )

    return agent

# Test the agent
async def main():
    agent = create_agent()

    # Framework handles all errors automatically
    response = await agent.run("Hello! What can you help me with?")
    response = await agent.run("What's the current price of Bitcoin?")

    return response

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())