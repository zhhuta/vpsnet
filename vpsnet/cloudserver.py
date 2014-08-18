__version__ = '0.0.1 alpha'
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
    """
    Singleton class for keep auth
    """
    def __init__(self, username, password):
        self.username = username
        self.password = password


class vpsnetError(Exception):
    """
    Class for printing errors.
    """
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)


class Operation():
    """
    Class that contain methods
    """
    def get_cloudserevrs(self):
        """
        Get an list of all cloudserver assigned to account
        :return: array of json objects with cloudserver details
        """
        reply = self._request(name="get_all")
        return reply

    def get_cs_property(self, cs_id):
        """
        Get details of cloudserver with specific id
        :param cs_id: ID of cloudserver assigned at control.vps.net
        :return: json object with cloudserver details
        """
        reply = self._request(cs_id, name="get_cs_property")
        return reply

    def creat(self, data=None):
        """
        Creta CloudServer with params specified at data dict
        :param data: dict with CloudServer params
        example:
        data = {"virtual_machine": {
                "label": label,
                "fqdn": fqdn,
                "system_template_id": template,
                "cloud_id": cloud,
                "backups_enabled": 'false',
                "rsync_backups_enabled": 'false',
                "slices_required": nodes
        :return: json object with cloudserver details
        """
        data = json.dums(data)
        reply = self._request(data=data, name="create_cs")
        return reply

    def shutdown(self, cs_id):
        """
        Shutdown cloudserver with id
        :param cs_id:
        :return: json object with cloudserver details
        """
        reply = self._request(cs_id, name="shutdown_cs")
        return reply

    def reboot(self, cs_id):
        """
        Reboot cloudserver with id
        :param cs_id:
        :return: json object with cloudserver details
        """
        reply = self._request(cs_id, name="reboot_cs")
        return reply

    def statup(self, cs_id):
        """
        StartUP cloudserver with id
        :param cs_id:
        :return: cloudserver with id
        """
        reply = self._request(cs_id, name="starup_cs")
        return reply

    def poweroff(self, cs_id):
        """
        PowerOff cloudserver with id
        :param cs_id:
        :return: cloudserver with id
        """
        reply = self._request(cs_id, name="power_off_cs")
        return reply

    def rebuild(self, cs_id, data):
        """ Reinstall/Rebuild cloudserver with id
        :param cs_id:
        example
        data = { "virtual_machine" : {"system_template_id": 4302 } }
        :return: cloudserver with id
        """
        data = json.dumps(data)
        reply = self._request(cs_id, data, name="rebuild_cs")
        return reply


    def _request(self, cs_id=None, data=False, name=None):
        """
        Wrapper for requests
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



