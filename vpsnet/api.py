__author__ = 'zhhuta'
DEFAULT_HANDLER = None
METHODS = {
    "get_all_cs": {"url": "virtual_machines.api10json", "method": "GET"},
    "get_cs_property": {"url": "virtual_machines/%s.api10json", "method": "GET"},
    "search": {"url": "virtual_machines.api10json?search=%s", "method": "GET"},
    "create_cs": {"url": "virtual_machines.api10json", "method": "POST"},
    "create_instant": {"url": "virtual_machines.api10json", "method": "POST"},
    "shutdown_cs": {"url": "virtual_machines/%s/shutdown.api10json", "method": "POST"},
    "reboot_cs": {"url": "virtual_machines/%s/reboot.api10json", "method": "POST"},
    "startup_cs": {"url": "virtual_machines/%s/power_on.api10json", "method": "POST"},
    "power_off_cs": {"url": "virtual_machines/%s/power_off.api10json", "method": "POST"},
    "rebuild_cs": {"url": "virtual_machines/%s/rebuild.api10json", "method": "POST"},
    "rebuild_cs_net": {"url": "virtual_machines/%s/rebuild_network.api10json", "method": "POST"},
    "edit_cs": {"url": "virtual_machines/%s.api10json", "method": "PUT"},
    "delete_cs": {"url": "virtual_machines/%s.api10json", "method": "DELETE"},
    "cs_reset_rpass": {"url": "virtual_machines/%s/reset_password.api10json", "method": "POST"},
    "rebuild_network": {"url": "https://api.vps.net/virtual_machines/%s/rebuild_network.api10json", "method": "POST"},
    "backup_lists": {"url": "virtual_machines/%s/backups.api10json", "method": "GET"},
    "rsync_backup_info": {"url": "virtual_machines/%s/backups/rsync_backup.api10json", "method": "GET"},
    "create_template": {"url": "virtual_machines/%s/backups.api10json", "method": "POST"},
    "convert_backup2template": {"url": "virtual_machines/%s/backups/%s/convert.api10json", "method": "POST"},
    "backup_delete": {"url": "virtual_machines/%s/backups/%s.api10json", "method": "DELETE"},
    "restore_from_backup": {"url": "virtual_machines/%s/backups/%s/restore.api10json", "method": "POST"}
}
from . import HEADERS


class Handler(object):
    headers = HEADERS

    def __init__(self, base_url=None, username=None, password=None, verify=True):
        self.base_url = base_url
        self.username = username
        self.password = password
        self.verify = verify
        self.method = METHODS


def set_default_handler(request_handler):
    """Set the default request handler."""
    if not isinstance(request_handler, Handler):
        raise TypeError(
            "Attempted to set an invalid request handler as default.")
    print "setting DEFAULT_HANDLER"
    global DEFAULT_HANDLER
    DEFAULT_HANDLER = request_handler