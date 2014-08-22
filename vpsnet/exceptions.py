__author__ = 'zhhuta'


class VpsNetError(Exception):
    """
    Class for printing errors.
    """

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)
