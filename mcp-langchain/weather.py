from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Weather")

@mcp.tool()
async def get_weather(location: str)->str:
    """
    Get the weather for a given location
    """
    return "The weather is sunny"

if __name__ == "__main__":
    mcp.run(transport="streamable-http")
