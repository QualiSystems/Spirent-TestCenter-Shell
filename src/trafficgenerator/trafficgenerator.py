"""
This module implements classes and utility functions to manage TGN chassis.
"""


class TrafficGenerator(object):
    """ Base class for all TGN classes. """

    logger = None
    inter = None

    def __init__(self, logger):
        self.logger = logger

    def disconnect(self):
        self.inter.tcl_interp.destroy()
