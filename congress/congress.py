"""
MDC API for Congress.gov
API docs https://api.congress.gov/#/
Requires an API key: https://api.congress.gov/sign-up/

"""
from typing import Any

from mcp.server import FastMCP
from dotenv import load_dotenv, find_dotenv
from cdg_client import CDGClient
from fdtreasury_client import FDTreasuryClient
from fred import FREDClient
from pathlib import Path
import logging
from removed_env_data_client import RemovedEnvDataClient
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

# @mcp.tool()
# def generate_jq_filter_command(field_query: str, example: Dict|List) -> str:
#     """Generates a JQ command useful for filtering objects or lists objects given a specific query for a filter

#     Example:

#     Args:
#         field_query (str): A name or a comma separated set of names of fields within an object to filter down to.
#         example (Dict|List): The example object that the jq command will be run on.

#     Returns:
#         str: A jq command that can be used to filter the responses of other tools.
#     """
#     if isinstance(example, dict):
        

@mcp.tool()
async def get_bills() -> str:
    """Get recent bills from Congress.gov.
    
    Returns:
        str: A formatted list of recent bills.
    """
    url = "bill?limit=100"
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
    url = f"bill/{congress}?limit=100"
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
    url = f"bill/{congress}/{bill_type.lower()}?limit=100"
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

@mcp.tool()
async def get_all_members() -> str:
    """Get a list of all congressional members.

    Returns:
        str: A list of all congressional members.
    """
    url = "member"
    client = CDGClient()
    data, status = client.get(url)
    if status != 200:
        logger.error(status)
        return "Unable to fetch members, or no data found."
    return data

@mcp.tool()
async def get_member_details(bioguide_id: str) -> str:
    """Get detailed information for a specific congressional member.

    Args:
        bioguide_id (str): The Bioguide ID of the member.

    Returns:
        str: Detailed information about the specified member.
    """
    url = f"member/{bioguide_id}"
    client = CDGClient()
    data, status = client.get(url)
    if status != 200:
        logger.error(status)
        return f"Unable to fetch details for member {bioguide_id}, or no data found."
    return data

@mcp.tool()
async def get_member_sponsored_legislation(bioguide_id: str) -> str:
    """Get the list of legislation sponsored by a specified congressional member.

    Args:
        bioguide_id (str): The Bioguide ID of the member.

    Returns:
        str: A list of legislation sponsored by the member.
    """
    url = f"member/{bioguide_id}/sponsored-legislation"
    client = CDGClient()
    data, status = client.get(url)
    if status != 200:
        logger.error(status)
        return f"Unable to fetch sponsored legislation for member {bioguide_id}, or no data found."
    return data

@mcp.tool()
async def get_member_cosponsored_legislation(bioguide_id: str) -> str:
    """Get the list of legislation cosponsored by a specified congressional member.

    Args:
        bioguide_id (str): The Bioguide ID of the member.

    Returns:
        str: A list of legislation cosponsored by the member.
    """
    url = f"member/{bioguide_id}/cosponsored-legislation"
    client = CDGClient()
    data, status = client.get(url)
    if status != 200:
        logger.error(status)
        return f"Unable to fetch cosponsored legislation for member {bioguide_id}, or no data found."
    return data

@mcp.tool()
async def get_members_by_congress(congress: int) -> str:
    """Get a list of members in a specific congressional session.

    Args:
        congress (int): The congressional session number.

    Returns:
        str: A list of members for the specified congress.
    """
    url = f"member/congress/{congress}?limit=40"
    client = CDGClient()
    data, status = client.get(url)
    if status != 200:
        logger.error(status)
        return f"Unable to fetch members for Congress {congress}, or no data found."
    return data

@mcp.tool()
async def get_members_by_state(state_code: str) -> str:
    """Get a list of members filtered by state.

    Args:
        state_code (str): The two-letter state abbreviation.

    Returns:
        str: A list of members representing the specified state.
    """
    url = f"member/{state_code}"
    client = CDGClient()
    data, status = client.get(url)
    if status != 200:
        logger.error(status)
        return f"Unable to fetch members for state {state_code}, or no data found."
    return data

@mcp.tool()
async def get_members_by_state_and_district(state_code: str, district: int) -> str:
    """Get a list of members filtered by state and district.

    Args:
        state_code (str): The two-letter state abbreviation.
        district (int): The congressional district number.

    Returns:
        str: A list of members representing the specified state and district.
    """
    url = f"member/{state_code}/{district}"
    client = CDGClient()
    data, status = client.get(url)
    if status != 200:
        logger.error(status)
        return f"Unable to fetch members for state {state_code}, district {district}, or no data found."
    return data

@mcp.tool()
async def get_members_by_congress_state_and_district(congress: int, state_code: str, district: int) -> str:
    """Get a list of members filtered by congress, state, and district.

    Args:
        congress (int): The congressional session number.
        state_code (str): The two-letter state abbreviation.
        district (int): The congressional district number.

    Returns:
        str: A list of members matching the specified criteria.
    """
    url = f"member/congress/{congress}/{state_code}/{district}"
    client = CDGClient()
    data, status = client.get(url)
    if status != 200:
        logger.error(status)
        return f"Unable to fetch members for Congress {congress}, state {state_code}, district {district}, or no data found."
    return data



@mcp.tool()
async def get_debt_outstanding() -> str:
    """Get info about outstanding debt. Updated once per fiscal year"""
    url = "accounting/od/debt_outstanding"
    client = FDTreasuryClient()
    data, status = client.get(url)
    if status != 200:
        logger.error(status)
        return "Unable to fetch details for the current congress, or no data found."
    return data

@mcp.tool()
async def get_outstanding_gold_reserves() -> str:
    """Get info about outstanding gold reserves."""
    url = "accounting/od/gold_reserve"
    client = FDTreasuryClient()
    data, status = client.get(url)
    if status != 200:
        logger.error(status)
        return "Unable to fetch details for the current congress, or no data found."
    return data

@mcp.tool()
async def get_daily_treasury_statement() -> str:
    """
    This table represents the Treasury General Account balance.
    Additional detail on changes to the Treasury General Account can be found in the Deposits and Withdrawals of Operating Cash table.
    All figures are rounded to the nearest million.
    """
    url = "accounting/dts/operating_cash_balance"
    client = FDTreasuryClient()
    data, status = client.get(url)
    if status != 200:
        logger.error(status)
        return "Unable to fetch the daily treasury statement, or no data found."
    return data


@mcp.tool()
async def get_daily_treasury_operating_cash_activities() -> str:
    """
    This table represents deposits and withdrawals from the Treasury General Account.
    A summary of changes to the Treasury General Account can be found in the Operating Cash Balance table.
    All figures are rounded to the nearest million.
    """
    client = FDTreasuryClient()
    data, status = client.get("accounting/dts/deposits_withdrawals_operating_cash")
    if status != 200:
        logger.error(status)
        return "Unable to fetch details on deposits and withdrawls, or no data found."
    return data


@mcp.tool()
async def get_public_debt_transactions() -> str:
    """
    This table represents the issues and redemption of marketable and nonmarketable securities.
    All figures are rounded to the nearest million.
    """
    client = FDTreasuryClient()
    data, status = client.get("accounting/dts/public_debt_transactions")
    if status != 200:
        logger.error(status)
        return "Unable to fetch details of public debt transactions, or no data found."
    return data

@mcp.tool()
async def get_fred_data_releases() -> str:
    """
    Get all releases of economic data from the Federal Reserve Bank of St. Louis.
    :return: a list of releases of economic data
    """
    client = FREDClient()
    data, status = client.get("releases")
    if status != 200:
        logger.error(status)
        return "Unable to fetch FRED economic data releases, or no data found."
    return data

@mcp.tool()
async def get_fred_release_series(release_id: str) -> str:
    """
    Get the series on a release of economic data from the Federal Reserve Bank of St. Louis.
    :return: the series on a release of economic data
    """
    client = FREDClient()
    data, status = client.get("release/series",params={"release_id": release_id})
    if status != 200:
        logger.error(status)
        return "Unable to fetch FRED economic data sources, or no data found."
    return data

@mcp.tool()
async def get_all_committees() -> str:
    """Get a list of all congressional committees.

    Returns:
        str: A list of all congressional committees.
    """
    url = "committee?limit=40"
    client = CDGClient()
    data, status = client.get(url)
    if status != 200:
        logger.error(status)
        return "Unable to fetch committees, or no data found."
    return data

@mcp.tool()
async def get_committees_by_chamber(chamber: str) -> str:
    """Get a list of congressional committees filtered by chamber.

    Args:
        chamber (str): The chamber of Congress ("house" or "senate").

    Returns:
        str: A list of committees for the specified chamber.
    """
    url = f"committee/{chamber}?limit=40"
    client = CDGClient()
    data, status = client.get(url)
    if status != 200:
        logger.error(status)
        return f"Unable to fetch committees for the {chamber} chamber, or no data found."
    return data

@mcp.tool()
async def get_committees_by_congress(congress: int) -> str:
    """Get a list of congressional committees filtered by congress.

    Args:
        congress (int): The congressional session number.

    Returns:
        str: A list of committees for the specified congress.
    """
    url = f"committee/{congress}?limit=40"
    client = CDGClient()
    data, status = client.get(url)
    if status != 200:
        logger.error(status)
        return f"Unable to fetch committees for Congress {congress}, or no data found."
    return data

@mcp.tool()
async def get_committees_by_congress_and_chamber(congress: int, chamber: str) -> str:
    """Get a list of congressional committees filtered by congress and chamber.

    Args:
        congress (int): The congressional session number.
        chamber (str): The chamber of Congress ("house" or "senate").

    Returns:
        str: A list of committees matching the criteria.
    """
    url = f"committee/{congress}/{chamber}?limit=40"
    client = CDGClient()
    data, status = client.get(url)
    if status != 200:
        logger.error(status)
        return f"Unable to fetch committees for Congress {congress} in the {chamber} chamber, or no data found."
    return data

@mcp.tool()
async def get_committee_details(chamber: str, committee_code: str) -> str:
    """Get detailed information about a specific congressional committee.

    Args:
        chamber (str): The chamber of Congress ("house" or "senate").
        committee_code (str): The committee's unique code.

    Returns:
        str: Detailed information about the specified committee.
    """
    url = f"committee/{chamber}/{committee_code}"
    client = CDGClient()
    data, status = client.get(url)
    if status != 200:
        logger.error(status)
        return f"Unable to fetch details for committee {committee_code} in the {chamber} chamber, or no data found."
    return data

@mcp.tool()
async def get_committee_bills(chamber: str, committee_code: str) -> str:
    """Get a list of legislation associated with a specified congressional committee.

    Args:
        chamber (str): The chamber of Congress ("house" or "senate").
        committee_code (str): The committee's unique code.

    Returns:
        str: A list of bills associated with the specified committee.
    """
    url = f"committee/{chamber}/{committee_code}/bills?limit=40"
    client = CDGClient()
    data, status = client.get(url)
    if status != 200:
        logger.error(status)
        return f"Unable to fetch bills for committee {committee_code} in the {chamber} chamber, or no data found."
    return data

@mcp.tool()
async def get_committee_reports(chamber: str, committee_code: str) -> str:
    """Get a list of committee reports associated with a specified congressional committee.

    Args:
        chamber (str): The chamber of Congress ("house" or "senate").
        committee_code (str): The committee's unique code.

    Returns:
        str: A list of committee reports associated with the specified committee.
    """
    url = f"committee/{chamber}/{committee_code}/reports?limit=40"
    client = CDGClient()
    data, status = client.get(url)
    if status != 200:
        logger.error(status)
        return f"Unable to fetch reports for committee {committee_code} in the {chamber} chamber, or no data found."
    return data

@mcp.tool()
async def get_committee_nominations(chamber: str, committee_code: str) -> str:
    """Get a list of nominations associated with a specified congressional committee.

    Args:
        chamber (str): The chamber of Congress ("house" or "senate").
        committee_code (str): The committee's unique code.

    Returns:
        str: A list of nominations associated with the specified committee.
    """
    url = f"committee/{chamber}/{committee_code}/nominations?limit=40"
    client = CDGClient()
    data, status = client.get(url)
    if status != 200:
        logger.error(status)
        return f"Unable to fetch nominations for committee {committee_code} in the {chamber} chamber, or no data found."
    return data

@mcp.tool()
async def get_committee_house_communications(chamber: str, committee_code: str) -> str:
    """Get a list of House communications associated with a specified congressional committee.

    Args:
        chamber (str): The chamber of Congress ("house" or "senate").
        committee_code (str): The committee's unique code.

    Returns:
        str: A list of House communications associated with the specified committee.
    """
    url = f"committee/{chamber}/{committee_code}/house-communication?limit=40"
    client = CDGClient()
    data, status = client.get(url)
    if status != 200:
        logger.error(status)
        return f"Unable to fetch House communications for committee {committee_code} in the {chamber} chamber, or no data found."
    return data

@mcp.tool()
async def get_committee_senate_communications(chamber: str, committee_code: str) -> str:
    """Get a list of Senate communications associated with a specified congressional committee.

    Args:
        chamber (str): The chamber of Congress ("house" or "senate").
        committee_code (str): The committee's unique code.

    Returns:
        str: A list of Senate communications associated with the specified committee.
    """
    url = f"committee/{chamber}/{committee_code}/senate-communication?limit=40"
    client = CDGClient()
    data, status = client.get(url)
    if status != 200:
        logger.error(status)
        return f"Unable to fetch Senate communications for committee {committee_code} in the {chamber} chamber, or no data found."
    return data


# TODO: Move this to removed_env_data.py
@mcp.tool()
async def get_removed_env_data() -> dict:
    """
    Gets environmental data removed from US Federal Websites
    """
    return RemovedEnvDataClient.read_and_parse_csv()

if __name__ == "__main__":
    logger.info("Running congress API")
    mcp.run(transport='stdio')
