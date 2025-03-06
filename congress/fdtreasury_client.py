from urllib.parse import urljoin
import requests
import logging

API_VERSION = "v2"
ROOT_URL = "https://api.fiscaldata.treasury.gov/services/api/fiscal_service/"


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
            logger.error("failed getting FD Treasury Data  %s",e)
            return "FD Treasury API Failure",-1

class FDTreasuryClient:
    def __init__(
            self,
            api_version=API_VERSION,
            # response_format=RESPONSE_FORMAT,
            raise_on_error=True,
    ):
        self.base_url = urljoin(ROOT_URL, api_version) + "/"
        self._session = requests.Session()

        if raise_on_error:
            self._session.hooks = {
                "response": lambda r, *args, **kwargs: r.raise_for_status()
            }

    def __getattr__(self, method_name):
        """Find the session method dynamically and cache for later."""
        method = _MethodWrapper(self, method_name)
        self.__dict__[method_name] = method
        return method
