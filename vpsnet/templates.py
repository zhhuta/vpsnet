__author__ = 'zhhuta'

from .utils import request_handler


def get_list():
    """

    :return:
    """
    return request_handler(name="template_list")