__author__ = 'zhhuta'

from .utils import request_handler


def get_list():
    """
    get a list of clouds from vps.net
    :return:
    """
    return request_handler(name="cloud_list")