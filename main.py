from typing import Any
import httpx
from mcp.server.fastmcp import FastMCP

# Initialize FastMCP server
mcp = FastMCP("congressgov")

# Constants
NWS_API_BASE = "https://api.congress.gov/v3/"
USER_AGENT = "weather-app/1.0"