from typing import Any

from mcp.server import FastMCP
from dotenv import load_dotenv, find_dotenv
from cdg_client import CDGClient
from pathlib import Path
import logging

# load environment variables from .env in project root
dotenv_result = load_dotenv(Path(__file__).parent.parent / '.env')
if not dotenv_result:
    logging.error(".env not found or not readable")

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

    if status != 200 or "bills" not in data:
        logging.error(status)
        return "Unable to fetch bills, or no bills found."

    if not data["bills"]:
        return "No recent bills found."

    bills = [format_bill(bill) for bill in data["bills"]]
    return "\n---\n".join(bills)

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
    if status != 200 or "bills" not in data:
        logging.error(status)
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
    url = f"bill/{congress}/{bill_type}?limit=250"
    client = CDGClient()
    data,status = client.get(url)
    if status != 200 or "bills" not in data:
        logging.error(status)
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
    url = f"bill/{congress}/{bill_type}/{bill_number}"
    client = CDGClient()
    data,status = client.get(url)
    if status != 200 or "bills" not in data:
        logging.error(status)
        return "Unable to fetch bills, or no bills found."
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
    url = f"bill/{congress}/{bill_type}/{bill_number}/actions"
    client = CDGClient()
    data,status = client.get(url)
    if status != 200 or "bills" not in data:
        logging.error(status)
        return "Unable to fetch bills, or no bills found."
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
    url = f"bill/{congress}/{bill_type}/{bill_number}/amendments"
    client = CDGClient()
    data,status = client.get(url)
    if status != 200 or "bills" not in data:
        logging.error(status)
        return "Unable to fetch bills, or no bills found."
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
    url = f"bill/{congress}/{bill_type}/{bill_number}/titles"
    client = CDGClient()
    data,status = client.get(url)
    if status != 200 or "bills" not in data:
        logging.error(status)
        return "Unable to fetch bills, or no bills found."
    return data

if __name__ == "__main__":
    mcp.run(transport='stdio')
