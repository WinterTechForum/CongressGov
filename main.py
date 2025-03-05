from typing import Any

from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP
from dotenv import load_dotenv

load_dotenv()  # load environment variables from .env

# Initialize FastMCP server
mcp = FastMCP("congressgov")

# Constants
NWS_API_BASE = "https://api.congress.gov/v3/"
USER_AGENT = "weather-app/1.0"