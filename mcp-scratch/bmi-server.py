from fastmcp import FastMCP

mcp = FastMCP("BMI Server")

# Register the BMI calculation tool
# The @mcp.tool decorator exposes this function as an MCP tool

@mcp.tool  
async def calculate_bmi(weight_kg: float, height_m: float) -> float:
    """
    Calculate Body Mass Index (BMI) given weight in kilograms and height in meters.

    Args:
        weight_kg: Weight in kilograms (must be > 0)
        height_m: Height in meters (must be > 0)

    Returns:
        BMI value rounded to 2 decimal places

    Raises:
        ValueError: If either weight or height is less than or equal to zero
    """
    if weight_kg <= 0 or height_m <= 0:
        raise ValueError("Weight and height must both be greater than zero.")
    return round(weight_kg / (height_m ** 2), 2)

# Run the server when executed directly (not when imported as a module)
if __name__ == "__main__":
    mcp.run()  # STDIO by default

"""
When using 'stdio' transport, anything printed to stdout that is not a 
structured MCP JSON-RPC message will corrupt the communication channel, 
causing the client to immediately close the connection.
"""

