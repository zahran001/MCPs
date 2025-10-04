from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Math") # server name

# return type is -> int
# based on the docstring, LLM will be able to understand which tool to specifically use
@mcp.tool()
def add(a: int, b: int) -> int:
    """
    Add two numbers together
    """
    return a + b

@mcp.tool()
def Multiply(a: int, b: int) -> int:
    """
    Multiply two numbers
    """
    return a * b


# The transport="stdio" argument tells the server to:
# Use standard input/output to receive and respond to tool function calls
if __name__ == "__main__":
    mcp.run(transport="stdio")


