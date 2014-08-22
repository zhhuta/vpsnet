__author__ = 'zhhuta'

from .utils import request_handler


def get():
    """

    :return:
    """
    return request_handler(name="vpsnet_profile")