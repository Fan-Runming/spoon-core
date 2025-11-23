# test_agent.py（可选）
import asyncio
from relationship_spark_agent import create_default_relationship_agent

async def main():
    agent = create_default_relationship_agent()
    res = await agent.generate_spark(
        scene="stay_in_touch",
        context="We met at a hackathon and built an AI music project together. "
                "It's been 2 months and we haven't talked since the demo day."
    )
    print(res)

if __name__ == "__main__":
    asyncio.run(main())
