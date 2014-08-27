__author__ = 'zhhuta'

import vpsnet.utils
#from .utils import request_handler
#from imp import reload




def get():
    #reload(vpsnet.utils)
    """

    :return:
    """
    return vpsnet.utils.request_handler(name="vpsnet_profile")