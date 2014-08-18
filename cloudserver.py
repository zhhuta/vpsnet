__version__ = '0.1beta'
__author__ = 'zhhuta'

BASE_URL = "https://api.vps.net/"
HEADERS = {"Accept": "application/json", "Content-type": "application/json"}

METHODS = {
    "get_all": {"url": "virtual_machines.api10json", "method": "GET"},
    "get_cs_property": {"url": "virtual_machines/%s.api10json", "method": "GET"},
    "create_cs": {"url": "virtual_machines.api10json", "method": "POST"},
    "shutdown_cs": {"url": "virtual_machines/%s/shutdown.api10json", "method": "POST"},
    "reboot_cs": {"url": "virtual_machines/%s/reboot.api10json", "method": "POST"},
    "starup_cs": {"url": "virtual_machines/%s/power_on.api10json", "method": "POST"},
    "poweroff_cs": {"url": "virtual_machines/%s/power_off.api10json", "method": "POST"},
    "rebuild_cs": {"url": "virtual_machines/%s/rebuild.api10json", "method": "POST"},
    "rebuild_cs_net": {"url": "virtual_machines/%s/rebuild_network.api10json", "method": "POST"},
    "edit_cs": {"url": "virtual_machines/%s.api10json", "method": "PUT"}
}

import requests
import json


def singleton(class_):
    instances = {}

    def getinstance(*args, **kwargs):
        if class_ not in instances:
            instances[class_] = class_(*args, **kwargs)
        return instances[class_]

    return getinstance


@singleton
class vpsnetAuth():
    def __init__(self, username, password):
        self.username = username
        self.password = password


class vpsnetError(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)


class Operation():
    def get_cloudserevrs(self):
        reply = self._request(name="get_all")
        return reply

    def get_cs_property(self, cs_id):
        reply = self._request(cs_id, name="get_cs_property")
        return reply

    def creat(self, data=None):
        data = json.dums(data)
        reply = self._request(data=data, name="create_cs")
        return reply

    def shutdown(self, cs_id):
        reply = self._request(cs_id, name="shutdown_cs")
        return reply

    def reboot(self, cs_id):
        reply = self._request(cs_id, name="reboot_cs")
        return reply

    def statup(self, cs_id):
        reply = self._request(cs_id, name="starup_cs")
        return reply

    def poweroff(self, cs_id):
        reply = self._request(cs_id, name="power_off_cs")
        return reply

    def rebuild(self, cs_id):
        reply = self._request(cs_id, name="rebuild_cs")
        return reply

    def __getattr__(self, item):
        if item in METHODS.keys():
            print METHODS[item]
        else:
            raise AttributeError


    def _request(self, cs_id=None, data=False, name=None):
        """

        :param cs_id: Id of Cloud Server
        :param data:
        :param name: name of method that is predefined in METHODS
        :return: json with
        """
        params = {}

        if cs_id is None:
            url = BASE_URL + METHODS[name]["url"]
        else:
            url = BASE_URL + METHODS[name]["url"] % cs_id

        if data is not False:
            data = json.dumps(data)
            params = {"auth": (vpsnetAuth().username, vpsnetAuth().password), "headers": HEADERS, "data": data,
                      "verify": False}
        else:
            params = {"auth": (vpsnetAuth().username, vpsnetAuth().password), "headers": HEADERS, "verify": False}

        if METHODS[name]['method'] is "GET":
            reply = requests.get(url, **params)
        elif METHODS[name]['method'] is "POST":
            reply = requests.post(url, **params)
        elif METHODS[name]['method'] is "PUT":
            reply = requests.put(url, **params)
        else:
            raise vpsnetError("Unsuported metod")
        if reply.status_code != requests.codes.ok:
            reply.raise_for_status()

        try:
            respond = reply.json()
            return respond
        except ValueError:
            raise ValueError("The API server doesn't respond with a valid json")
        except requests.RequestException as e:
            raise RuntimeError(e)



