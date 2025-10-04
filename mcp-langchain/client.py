from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent
from langchain_groq import ChatGroq

from dotenv import load_dotenv
load_dotenv()

import asyncio

async def main():
    client = MultiServerMCPClient({
        "math":{
            "command": "python",
            "args": ["mathserver.py"],
            "transport": "stdio"
        },
        "weather":{
            "url": "http://localhost:8000/mcp",
            "transport": "streamable_http"
        }
    })

    import os
    os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")

    tools = await client.get_tools()
    #print(tools)
    model = ChatGroq(model="qwen-qwq-32b")
    agent = create_react_agent(model, tools)

    math_response = await agent.ainvoke({
        "messages": [{"role": "user", "content": "What is (10 + 8) x 20?"}]
    })

    # Grab the messages key
    # Grab the last message
    # Grab its content
    print("Math Response:", math_response["messages"][-1].content)

    weather_response = await agent.ainvoke({
        "messages":[{"role":"user", "content":"what is the weather of California?"}]
    })
    print("Weather response:", weather_response['messages'][-1].content)

asyncio.run(main()) # run the async main function 