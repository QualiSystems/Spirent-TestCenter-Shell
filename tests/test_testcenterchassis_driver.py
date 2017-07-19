#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Tests for `TestCenterChassisDriver`
"""

import sys
import logging
import unittest

from cloudshell.shell.core.driver_context import (ConnectivityContext, ResourceContextDetails, InitCommandContext)
from src.driver import TestCenterChassisDriver

address = '192.168.42.159'
client_install_path = 'C:/Program Files (x86)/Spirent Communications/Spirent TestCenter 4.71'
controller = ''
controller = '192.168.42.156'


class TestTestCenterChassisDriver(unittest.TestCase):

    def setUp(self):
        connectivity = ConnectivityContext(None, None, None, None)
        resource = ResourceContextDetails('testing', None, None, None, None, None, None, None, None, None)
        resource.address = address
        resource.attributes = {'Client Install Path': client_install_path,
                               'Controller Address': controller}
        self.context = InitCommandContext(connectivity, resource)
        self.driver = TestCenterChassisDriver()
        self.driver.initialize(self.context)
        print self.driver.logger.handlers[0].baseFilename
        self.driver.logger.addHandler(logging.StreamHandler(sys.stdout))

    def tearDown(self):
        pass

    def testAutoload(self):
        inventory = self.driver.get_inventory(self.context)
        for r in inventory.resources:
            print r.relative_address, r.model, r.name
        for a in inventory.attributes:
            print a.relative_address, a.attribute_name, a.attribute_value


if __name__ == '__main__':
    sys.exit(unittest.main())
