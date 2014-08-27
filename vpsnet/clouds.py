__author__ = 'zhhuta'

#from .utils import request_handler
import vpsnet.utils

def get_list():
    """
    get a list of clouds from vps.net
    :return:
    """
    return vpsnet.utils.request_handler(name="cloud_list")