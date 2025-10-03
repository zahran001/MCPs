from openai import OpenAI # to create the openAI client and talk to the API/LLM

from mcp.client.session import ClientSession
from mcp.client.stdio import stdio_client, StdioServerParameters

import os
import json
import asyncio
import sys # Import sys to get the executable path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get the absolute path of the server script
server_script_path = os.path.abspath("bmi-server.py")

server_params = StdioServerParameters(
    # Use sys.executable for the command.
    # This provides the full, absolute path to the Python interpreter 
    # running the client (e.g., the one in 'myenv'), guaranteeing the correct environment is used.
    command=sys.executable,
    # Use the absolute path for the script argument.
    args=[server_script_path]
)
# command: The executable command used to launch the server process.
# args: A list of string arguments passed to the command.

# Create the LLM client so that we can talk to that particular OpenAI LLM API
def llm_client(message: str):
    """
    Send a message to the LLM and return the response.
    """
    # Initialize the OpenAI client
    openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    # Send the message to the LLM
    response = openai_client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", 
            "content": "You are an intelligent assistant. You will execute tasks as prompted."},
            {"role": "user",
            "content": message}
        ],
        max_tokens=250,
        temperature=0.2 # creativity level
    )

    # Extract and return the response content
    return response.choices[0].message.content.strip()
    

# We will essentially create a method that returns a well-structured prompt (user query + how we want the prompt to return a response)
# This prompt is specifically for talking to the server and the tools it exposes
def get_prompt_to_identify_tool_and_arguments(query, tools):
    tools_description = "\n".join([f"{tool.name}, {tool.description}, {tool.inputSchema} " for tool in tools])
    
    return ("You are a helpful assistant with access to these tools:\n\n"
            f"{tools_description}\n"
            "Choose the appropriate tool based on the user's question.\n"
            f"User's question: {query}\n"
            "If no tool is needed, respond with 'No tool needed'.\n"
            "IMPORTANT: When you choose a tool, respond in the following JSON format:\n"
            "For numeric arguments, use JSON numbers (no quotes).\n"
            "{\n"
            '  "tool": "tool-name",\n'
            '  "arguments": {\n'
            '    "argument-name": "value",\n'
            "   }\n"
            "}\n\n")

# Our goal is to write a simple prompt and send that prompt to the LLM - LLM will identify the 
# tool and necessary arguments it needs to pass for that particular tool


# how tools work
# run method - instantiate the client and create a session, identify the server, get all the tools it has access to 
# and essentially it can pass those tools to the above method that we need to create the prompt
async def run(query: str):
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            
            # initialize the client session
            await session.initialize()

            # get the list of tools
            tools = await session.list_tools()
            # we ask the server for the list of tools it has access to
            # in our case, it will return the calculate bmi function that we exposed earlier

            print("Tools available: ", tools)

            prompt = get_prompt_to_identify_tool_and_arguments(query, tools.tools)
            print("Prompt to identify tool and arguments:\n", prompt)

            llm_response = llm_client(prompt)
            print("LLM response:\n", llm_response)

            # how to execute the tool
            # capture the response from the LLM into a dictionary
            tool_call = json.loads(llm_response)

            result = await session.call_tool(tool_call["tool"], arguments=tool_call["arguments"])
            print(result)
            print("Tool call result:\n", result.content[0].text)


if __name__ == "__main__":
    query = "Calculate the BMI for a person with weight 70kg and height 175cm."
    asyncio.run(run(query))


