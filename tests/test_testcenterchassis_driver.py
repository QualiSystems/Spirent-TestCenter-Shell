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

client_install_path = 'C:/Program Files (x86)/Spirent Communications/Spirent TestCenter 4.52'
address = '192.168.42.159'
address = '10.26.4.151'
controller = '192.168.42.156'
controller = ''


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
        self.inventory = self.driver.get_inventory(self.context)
        for r in self.inventory.resources:
            print r.relative_address, r.model, r.name
        for a in self.inventory.attributes:
            print a.relative_address, a.attribute_name, a.attribute_value


if __name__ == '__main__':
    sys.exit(unittest.main())
