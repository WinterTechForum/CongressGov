"""
    CDG Client - An example client for the Congress.gov API.

    @copyright: 2022, Library of Congress
    @license: CC0 1.0

"""
from urllib.parse import urljoin
import os
import requests
import logging

API_VERSION = "v3"
ROOT_URL = "https://api.congress.gov/"
RESPONSE_FORMAT = "json"


class _MethodWrapper:
    """ Wrap request method to facilitate queries.  Supports requests signature. """

    def __init__(self, parent, http_method):
        self._parent = parent
        self._method = getattr(parent._session, http_method)

    def __call__(self, endpoint, *args, **kwargs):  # full signature passed here
        logger = logging.getLogger(__name__)
        try:
            response = self._method(
                urljoin(self._parent.base_url, endpoint), *args, **kwargs
            )
            logger.debug("%s %d",response.url, response.status_code)
            # unpack
            if response.headers.get("content-type", "").startswith("application/json"):
                return response.json(), response.status_code
            else:
                return response.content, response.status_code
        except Exception as e:
            logger.error("failed getting bills  %s",e)
            return "API Failure",-1

class CDGClient:
    """ A simple client to interface with Congress.gov.

    Usage example:
    response, status_code = client.get("bill/117")
    print(f"Status Code: {status_code}")

    if status_code == 200:
        # Print the first bill in the response
        bills = response.get("bills", [])
        if bills:
            print("\nFirst Bill Details:")
            first_bill = bills[0]
            print(f"Number: {first_bill.get('number')}")
            print(f"Title: {first_bill.get('title')}")
            print(f"Type: {first_bill.get('type')}")
            print(f"Congress: {first_bill.get('congress')}")
    """

    def __init__(
            self,
            api_version=API_VERSION,
            response_format=RESPONSE_FORMAT,
            raise_on_error=True,
    ):
        self.base_url = urljoin(ROOT_URL, api_version) + "/"
        self._session = requests.Session()

        api_key=os.environ["CONGRESS_API_KEY"]
        
        # do not use url parameters, even if offered, use headers
        self._session.params = {"format": response_format}
        self._session.headers.update({"x-api-key": api_key})

        if raise_on_error:
            self._session.hooks = {
                "response": lambda r, *args, **kwargs: r.raise_for_status()
            }

    def __getattr__(self, method_name):
        """Find the session method dynamically and cache for later."""
        method = _MethodWrapper(self, method_name)
        self.__dict__[method_name] = method
        return method
