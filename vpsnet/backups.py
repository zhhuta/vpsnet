__author__ = 'zhhuta'

from .utils import request_handler


def list_all(cs_id):
    """

    :param cs_id:
    :return:
    """
    return request_handler(cs_id=cs_id, name="backup_lists")


def rsync_info(cs_id):
    """

    :param cs_id:
    :return:
    """
    return request_handler(cs_id=cs_id, name="rsync_backup_info")


def create_template(cs_id):
    """

    :param cs_id:
    :return:
    """
    return request_handler(cs_id=cs_id, name="create_template")


def convert2template(cs_id, backup_id):
    """

    :param cs_id:
    :param backup_id:
    :return:
    """
    return request_handler(cs_id=(cs_id, backup_id), name="cs_id,backup_id")


def delete(cs_id, backup_id):
    """

    :param cs_id:
    :param backup_id:
    :return:
    """
    return request_handler(cs_id=(cs_id, backup_id), name="backup_delete")