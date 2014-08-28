__author__ = 'zhhuta'

#from .utils import vpsnet.utils.request_handler
import vpsnet


def get_cloudservers():
    """
    Get an list of all cloudservers assigned to account
    :return: array of json objects with cloudservers details
    """
    return vpsnet.utils.request_handler(name="get_all_cs")


def get_cs_property(cs_id):
    """
    Get details of cloudserver with specific id
    :param cs_id: ID of cloudserver assigned at control.vps.net
    :return: json object with cloudserver details
    """
    return vpsnet.utils.request_handler(cs_id=cs_id, name="get_cs_property")


def search(statment):
    """
    Search for CloudServer base on lable, IP, domain name or tag
    :param statment:
    :return: list of cloudserver jsons
    """
    return vpsnet.utils.request_handler(cs_id=statment, name="search")


def create(data):
    """
    Create CloudServer with params specified at data dict
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
    return vpsnet.utils.request_handler(data=data, name="create_cs")


def create_instant(data):
    """
    Create instant cloudserver
    :param data: dict with params
    example:
    data = {"instant":true, "country":1 }
    :return: json object with cloudserver details
    """
    return vpsnet.utils.request_handler(data=data, name="create_instant")


def reboot(cs_id):
    """
    Reboot cloudserver with id
    :param cs_id:
    :return: json object with cloudserver details
    """
    return vpsnet.utils.request_handler(cs_id=cs_id, name="reboot_cs")


def reboot_recovery(cs_id):
    """
    Reboot cloudserver into recovery-mode with id
    :param cs_id:
    :return: json object with cloudserver details
    """
    data = {'mode': 'recovery'}
    return vpsnet.utils.request_handler(cs_id=cs_id, name="reboot_cs", data=data)


def start_up(cs_id):
    """
    StartUP cloudserver with id
    :param cs_id:
    :return: cloudserver with id
    """
    return vpsnet.utils.request_handler(cs_id=cs_id, name="startup_cs")


def power_off(cs_id):
    """
    PowerOff cloudserver with id
    :param cs_id:
    :return: cloudserver with id
    """
    return vpsnet.utils.request_handler(cs_id=cs_id, name="power_off_cs")


def rebuild(cs_id, data):
    """ Reinstall/Rebuild cloudserver with id
    :param cs_id:
    example
    data = { "virtual_machine" : {"system_template_id": 4302 } }
    :return: cloudserver with id
    """
    return vpsnet.utils.request_handler(cs_id=cs_id, name="rebuild_cs", data=data)


def rebuild_network(cs_id):
    """
    Rebuild network for cloudserver
    :param cs_id:
    :return:
    """
    return vpsnet.utils.request_handler(cs_id=cs_id, name="rebuild_network")


def edit(cs_id, data):
    """
    Edit CloudServer
    :param cs_id:
    :param data:
    :return:
    """
    return vpsnet.utils.request_handler(cs_id=cs_id, name="edit_cs", data=data)


def delete(cs_id):
    """
    Delete CloudServer
    :param cs_id: CloudServer Id
    :return:
    """
    return vpsnet.utils.request_handler(cs_id=cs_id, name="delete_cs")


def reset_root_pass(cs_id):
    """
    Reset root password for CloudServer
    :param cs_id: CloudServer Id
    :return: json with new password
    """
    return vpsnet.utils.request_handler(cs_id=cs_id, name="cs_reset_rpass")