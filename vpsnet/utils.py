__author__ = 'zhhuta'

import json

import requests


from .exceptions import VpsNetError
import vpsnet.api


def check_handler(handler):
    if not isinstance(handler, vpsnet.api.Handler):
        raise VpsNetError("No credentials set. Please set credentials vpsnet.init('email','password')")


def request_handler(handler=vpsnet.api.DEFAULT_HANDLER, cs_id=None, name=None, data=None):
    """
        Wrapper for requests
        :param cs_id: Id of Cloud Server
        :param data:
        :param name: name of method that is predefined in METHODS
        :return: json object with CloudServer details
        """
    #print handler
    check_handler(handler)

    if cs_id is None:
        url = handler.base_url + handler.method[name]["url"]
    else:
        url = handler.base_url + handler.method[name]["url"] % cs_id

    if data is not False:
        data = json.dumps(data)
        params = {"auth": (handler.username, handler.password), "headers": handler.headers, "data": data,
                  "verify": handler.verify}
    else:
        params = {"auth": (handler.username, handler.password), "headers": handler.headers, "verify": handler.verify}

    if handler.method[name]['method'] is "GET":
        reply = requests.get(url, **params)
    elif handler.method[name]['method'] is "POST":
        reply = requests.post(url, **params)
    elif handler.method[name]['method'] is "PUT":
        reply = requests.put(url, **params)
    elif handler.method[name]['method'] is "DELETE":
        reply = requests.delete(url, **params)
        reply._content = '{"status":"deleted"}'
    else:
        raise VpsNetError("Unsuported metod")

    if reply.status_code != requests.codes.ok:
        reply.raise_for_status()

    try:
        respond = reply.json()
        return respond
    except ValueError:
        raise ValueError("The API server doesn't respond with a valid json")
    except requests.RequestException as e:
        raise RuntimeError(e)
