from typing import Any

from mcp.server import FastMCP
from dotenv import load_dotenv, find_dotenv
from cdg_client import CDGClient
from pathlib import Path
import logging
import os
import json

fh = logging.FileHandler('congress_api.log')
fh.setLevel(logging.DEBUG)
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# load environment variables from .env in project root
env_path = f"{Path(__file__).parent.parent}/.env"
logger.info("loading from %s", env_path)
dotenv_result = load_dotenv(env_path)
if not dotenv_result:
    logger.error(".env not found or not readable")

mcp = FastMCP("congress")

def format_bill(bill):
    return (f"{bill['type']} {bill['number']} ({bill['congress']}th Congress)\n"
            f"Latest Action: {bill['latestAction']['actionDate']} - {bill['latestAction']['text']}\n"
            f"Title: {bill['title']}\n"
            f"URL: {bill['url']}")

@mcp.tool()
async def get_bills() -> str:
    """Get recent bills from Congress.gov.
    
    Returns:
        str: A formatted list of recent bills.
    """
    url = "bill?limit=250"
    client = CDGClient()
    data,status = client.get(url)
    if status != 200:
        logger.error(status)
        return "Unable to fetch bills, or no bills found."

    return data


@mcp.tool()
async def get_bills_by_congress(congress: int) -> str:
    """Get bills filtered by congress number.
    
    Args:
        congress (int): The congressional session number.
    
    Returns:
        str: A formatted list of bills from the specified congress.
    """
    url = f"bill/{congress}?limit=250"
    client = CDGClient()
    data,status = client.get(url)
    if status != 200:
        logger.error(status)
        return "Unable to fetch bills, or no bills found."
    return data

@mcp.tool()
async def get_bills_by_congress_and_type(congress: int, bill_type: str) -> str:
    """Get bills filtered by congress number and bill type.
    
    Args:
        congress (int): The congressional session number.
        bill_type (str): The type of bill (e.g., HRES, HR, S).
    
    Returns:
        str: A formatted list of bills matching the criteria.
    """
    url = f"bill/{congress}/{bill_type.lower()}?limit=250"
    client = CDGClient()
    data, status = client.get(url)
    if status != 200:
        logger.error(status)
        return "Unable to fetch bills, or no bills found."
    return data

@mcp.tool()
async def get_bill_details(congress: int, bill_type: str, bill_number: int) -> str:
    """Get details of a specific bill.
    
    Args:
        congress (int): The congressional session number.
        bill_type (str): The type of bill.
        bill_number (int): The bill number.
    
    Returns:
        str: The details of the specified bill.
    """
    url = f"bill/{congress}/{bill_type.lower()}/{bill_number}"
    client = CDGClient()
    data, status = client.get(url)
    if status != 200:
        logger.error(status)
        return "Unable to fetch bill details."
    return data

@mcp.tool()
async def get_bill_actions(congress: int, bill_type: str, bill_number: int) -> str:
    """Get actions of a specific bill.
    
    Args:
        congress (int): The congressional session number.
        bill_type (str): The type of bill.
        bill_number (int): The bill number.
    
    Returns:
        str: A list of actions for the specified bill.
    """
    url = f"bill/{congress}/{bill_type.lower()}/{bill_number}/actions"
    client = CDGClient()
    data, status = client.get(url)
    if status != 200:
        logger.error(status)
        return "Unable to fetch bill actions."
    return data

@mcp.tool()
async def get_bill_amendments(congress: int, bill_type: str, bill_number: int) -> str:
    """Get amendments of a specific bill.
    
    Args:
        congress (int): The congressional session number.
        bill_type (str): The type of bill.
        bill_number (int): The bill number.
    
    Returns:
        str: A list of amendments for the specified bill.
    """
    url = f"bill/{congress}/{bill_type.lower()}/{bill_number}/amendments"
    client = CDGClient()
    data, status = client.get(url)
    if status != 200:
        logger.error(status)
        return "Unable to fetch bill amendments."
    return data

@mcp.tool()
async def get_bill_committees(congress: int, bill_type: str, bill_number: int) -> str:
    """Get committees associated with a specific bill.
    
    Args:
        congress (int): The congressional session number.
        bill_type (str): The type of bill.
        bill_number (int): The bill number.
    
    Returns:
        str: A list of committees for the specified bill.
    """
    url = f"bill/{congress}/{bill_type.lower()}/{bill_number}/committees"
    client = CDGClient()
    data, status = client.get(url)
    if status != 200:
        logger.error(status)
        return "Unable to fetch committees, or no committees found."
    return data

@mcp.tool()
async def get_bill_cosponsors(congress: int, bill_type: str, bill_number: int) -> str:
    """Get cosponsors of a specific bill.
    
    Args:
        congress (int): The congressional session number.
        bill_type (str): The type of bill.
        bill_number (int): The bill number.
    
    Returns:
        str: A list of cosponsors for the specified bill.
    """
    url = f"bill/{congress}/{bill_type.lower()}/{bill_number}/cosponsors"
    client = CDGClient()
    data, status = client.get(url)
    if status != 200:
        logger.error(status)
        return "Unable to fetch cosponsors, or no cosponsors found."
    return data

@mcp.tool()
async def get_bill_related(congress: int, bill_type: str, bill_number: int) -> str:
    """Get related bills to a specific bill.
    
    Args:
        congress (int): The congressional session number.
        bill_type (str): The type of bill.
        bill_number (int): The bill number.
    
    Returns:
        str: A list of related bills for the specified bill.
    """
    url = f"bill/{congress}/{bill_type.lower()}/{bill_number}/relatedbills"
    client = CDGClient()
    data, status = client.get(url)
    if status != 200:
        logger.error(status)
        return "Unable to fetch related bills, or no related bills found."
    return data

@mcp.tool()
async def get_bill_subjects(congress: int, bill_type: str, bill_number: int) -> str:
    """Get legislative subjects of a specific bill.
    
    Args:
        congress (int): The congressional session number.
        bill_type (str): The type of bill.
        bill_number (int): The bill number.
    
    Returns:
        str: A list of legislative subjects for the specified bill.
    """
    url = f"bill/{congress}/{bill_type.lower()}/{bill_number}/subjects"
    client = CDGClient()
    data, status = client.get(url)
    if status != 200:
        logger.error(status)
        return "Unable to fetch subjects, or no subjects found."
    return data

@mcp.tool()
async def get_bill_summaries(congress: int, bill_type: str, bill_number: int) -> str:
    """Get summaries of a specific bill.
    
    Args:
        congress (int): The congressional session number.
        bill_type (str): The type of bill.
        bill_number (int): The bill number.
    
    Returns:
        str: A list of summaries for the specified bill.
    """
    url = f"bill/{congress}/{bill_type.lower()}/{bill_number}/summaries"
    client = CDGClient()
    data, status = client.get(url)
    if status != 200:
        logger.error(status)
        return "Unable to fetch summaries, or no summaries found."
    return data

@mcp.tool()
async def get_bill_text(congress: int, bill_type: str, bill_number: int) -> str:
    """Get text versions of a specific bill.
    
    Args:
        congress (int): The congressional session number.
        bill_type (str): The type of bill.
        bill_number (int): The bill number.
    
    Returns:
        str: A list of text versions for the specified bill.
    """
    url = f"bill/{congress}/{bill_type.lower()}/{bill_number}/text"
    client = CDGClient()
    data, status = client.get(url)
    if status != 200:
        logger.error(status)
        return "Unable to fetch bill text, or no text versions found."
    return data

@mcp.tool()
async def get_bill_titles(congress: int, bill_type: str, bill_number: int) -> str:
    """Get titles of a specific bill.
    
    Args:
        congress (int): The congressional session number.
        bill_type (str): The type of bill.
        bill_number (int): The bill number.
    
    Returns:
        str: A list of titles for the specified bill.
    """
    url = f"bill/{congress}/{bill_type.lower()}/{bill_number}/titles"
    client = CDGClient()
    data, status = client.get(url)
    if status != 200:
        logger.error(status)
        return "Unable to fetch titles, or no titles found."
    return data

@mcp.tool()
async def get_all_congresses() -> str:
    """Get a list of all congresses and congressional sessions.

    Returns:
        str: A list of congresses and congressional sessions.
    """
    url = "congress"
    client = CDGClient()
    data, status = client.get(url)
    if status != 200:
        logger.error(status)
        return "Unable to fetch congress list, or no data found."
    return data

@mcp.tool()
async def get_congress_details(congress: int) -> str:
    """Get detailed information about a specific congress.

    Args:
        congress (int): The congressional session number.

    Returns:
        str: Detailed information about the specified congress.
    """
    url = f"congress/{congress}"
    client = CDGClient()
    data, status = client.get(url)
    if status != 200:
        logger.error(status)
        return f"Unable to fetch details for Congress {congress}, or no data found."
    return data

@mcp.tool()
async def get_current_congress() -> str:
    """Get detailed information about the current congress.

    Returns:
        str: Detailed information about the current congress.
    """
    url = "congress/current"
    client = CDGClient()
    data, status = client.get(url)
    if status != 200:
        logger.error(status)
        return "Unable to fetch details for the current congress, or no data found."
    return data


if __name__ == "__main__":
    logger.info("Running congress API")
    mcp.run(transport='stdio')
