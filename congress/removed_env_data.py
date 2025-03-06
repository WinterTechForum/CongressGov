from mcp.server import FastMCP
from removed_env_data_client import RemovedEnvDataClient


mcp = FastMCP("removed_env_data")

@mcp.tool()
async def get_removed_env_data() -> str:
    """
    Gets environmental data removed from US Federal Websites
    """
    parsed_data = RemovedEnvDataClient.read_and_parse_csv()
    print(parsed_data)