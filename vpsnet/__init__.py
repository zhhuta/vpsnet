from vpsnet.cloudserver import vpsnetAuth, Operation

BASE_URL = "https://api.vps.net/"
HEADERS = {"Accept": "application/json", "Content-type": "application/json"}

METHODS = {
    "get_all": {"url": "virtual_machines.api10json", "method": "GET"},
    "get_cs_property": {"url": "virtual_machines/%s.api10json", "method": "GET"},
    "search": {"url": "virtual_machines.api10json?search=%s", "method": "GET"},
    "create_cs": {"url": "virtual_machines.api10json", "method": "POST"},
    "create_instant": {"url": "virtual_machines.api10json", "method": "POST"},
    "shutdown_cs": {"url": "virtual_machines/%s/shutdown.api10json", "method": "POST"},
    "reboot_cs": {"url": "virtual_machines/%s/reboot.api10json", "method": "POST"},
    "starup_cs": {"url": "virtual_machines/%s/power_on.api10json", "method": "POST"},
    "poweroff_cs": {"url": "virtual_machines/%s/power_off.api10json", "method": "POST"},
    "rebuild_cs": {"url": "virtual_machines/%s/rebuild.api10json", "method": "POST"},
    "rebuild_cs_net": {"url": "virtual_machines/%s/rebuild_network.api10json", "method": "POST"},
    "edit_cs": {"url": "virtual_machines/%s.api10json", "method": "PUT"},
    "rebuild_network": {"url": "https://api.vps.net/virtual_machines/%s/rebuild_network.api10json", "method": "POST"}
}


