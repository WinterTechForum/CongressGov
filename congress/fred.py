import requests
from urllib.parse import urljoin, quote_plus
import os
import logging

ROOT_URL = "https://api.stlouisfed.org/fred/"
RESPONSE_FORMAT = "json"

class _MethodWrapper:
    """ Wrap request method to facilitate queries.  Supports requests signature. """

    def __init__(self, parent, http_method):
        self._parent = parent
        self._method = getattr(parent._session, http_method)

    def __call__(self, endpoint, *args, **kwargs):  # full signature passed here
        logger = logging.getLogger(__name__)

        response = self._method(
            urljoin(self._parent.base_url, endpoint), *args, **kwargs
        )
        logger.debug("%s %d",response.url, response.status_code)
        # unpack
        if response.headers.get("content-type", "").startswith("application/json"):
            return response.json(), response.status_code
        else:
            return response.content, response.status_code

class FREDClient:
    def __init__(
            self,
            api_key=os.environ.get("FRED_API_KEY"),
            response_format=RESPONSE_FORMAT,
            raise_on_error=False,
    ):
        self.base_url = ROOT_URL
        self._session = requests.Session()
        self._session.params = {"api_key": api_key, "file_type": response_format}

        if raise_on_error:
            self._session.hooks = {
                "response": lambda r, *args, **kwargs: r.raise_for_status()
            }

    def __getattr__(self, method_name):
        """Find the session method dynamically and cache for later."""
        method = _MethodWrapper(self, method_name)
        self.__dict__[method_name] = method
        return method
