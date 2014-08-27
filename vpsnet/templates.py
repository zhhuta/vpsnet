__author__ = 'zhhuta'

#from .utils import request_handler
import vpsnet.utils

def get_list():
    """

    :return:
    """
    return vpsnet.utils.request_handler(name="template_list")