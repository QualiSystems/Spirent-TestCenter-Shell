#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Tests for `TestCenterChassisDriver`
"""

import sys
import logging
import unittest

from shellfoundry.releasetools.test_helper import create_session_from_cloudshell_config, create_autoload_context

from src.driver import TestCenterChassisDriver

client_install_path = 'C:/Program Files (x86)/Spirent Communications/Spirent TestCenter 4.71'
controller = '192.168.42.182'
controller = ''
address = '192.168.42.218'


class TestStcChassisDriver(unittest.TestCase):

    def setUp(self):
        self.session = create_session_from_cloudshell_config()
        self.context = create_autoload_context(address, client_install_path, controller, '')
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
