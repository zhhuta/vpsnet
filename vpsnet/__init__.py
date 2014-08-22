__author__ = 'zhhuta'

BASE_URL = "https://api.vps.net/"
HEADERS = {"Accept": "application/json", "Content-type": "application/json"}
from .api import Handler, set_default_handler

DEFAULT_HANDLER = None


def init(username=None, password=None, verify=True, base_url=BASE_URL):
    handler = Handler(base_url, username, password, verify)
    set_default_handler(handler)
    return handler

