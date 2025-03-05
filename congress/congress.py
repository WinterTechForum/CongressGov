from typing import Any

import httpx
from mcp.server import FastMCP

mcp = FastMCP("congress")

CONGRESS_API_BASE="https://api.congress.gov/v3"
CONGRESS_API_KEY=<FILL IN>

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
    url = f"{CONGRESS_API_BASE}/bill?format=json&limit=250&api_key={CONGRESS_API_KEY}"
    data = await make_nws_request(url)

    if not data or "bills" not in data:
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
    url = f"{CONGRESS_API_BASE}/bill/{congress}?format=json&limit=250&api_key={CONGRESS_API_KEY}"
    return await fetch_and_format_bills(url)

@mcp.tool()
async def get_bills_by_congress_and_type(congress: int, bill_type: str) -> str:
    """Get bills filtered by congress number and bill type.
    
    Args:
        congress (int): The congressional session number.
        bill_type (str): The type of bill (e.g., HRES, HR, S).
    
    Returns:
        str: A formatted list of bills matching the criteria.
    """
    url = f"{CONGRESS_API_BASE}/bill/{congress}/{bill_type}?format=json&limit=250&api_key={CONGRESS_API_KEY}"
    return await fetch_and_format_bills(url)

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
    url = f"{CONGRESS_API_BASE}/bill/{congress}/{bill_type}/{bill_number}?format=json&api_key={CONGRESS_API_KEY}"
    return await fetch_and_format_bills(url)

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
    url = f"{CONGRESS_API_BASE}/bill/{congress}/{bill_type}/{bill_number}/actions?format=json&api_key={CONGRESS_API_KEY}"
    return await fetch_and_format_bills(url)

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
    url = f"{CONGRESS_API_BASE}/bill/{congress}/{bill_type}/{bill_number}/amendments?format=json&api_key={CONGRESS_API_KEY}"
    return await fetch_and_format_bills(url)

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
    url = f"{CONGRESS_API_BASE}/bill/{congress}/{bill_type}/{bill_number}/titles?format=json&api_key={CONGRESS_API_KEY}"
    return await fetch_and_format_bills(url)

async def fetch_and_format_bills(url: str) -> str:
    """Fetches and formats bill data from Congress.gov.
    
    Args:
        url (str): The API endpoint URL to fetch data from.
    
    Returns:
        str: The formatted response data or an error message.
    """
    data = await make_nws_request(url)
    if not data:
        return "No data available."
    return str(data)