#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Tests for `TestCenterChassisDriver`
"""

import unittest

from cloudshell.shell.core.driver_context import (ConnectivityContext, ResourceContextDetails, InitCommandContext)

from src.stc_handler import StcHandler


class TestTestCenterChassisDriver(unittest.TestCase):

    def setUp(self):
        self.connectivity = ConnectivityContext(None, None, None, None)
        self.resource = ResourceContextDetails(None, None, None, None, None, None, None, None, None, None)
        self.resource.address = '10.254.7.84'
        self.resource.attributes = {'Client Install Path':
                                    'C:\Program Files (x86)\Spirent Communications\Spirent TestCenter 4.52'}
        context = InitCommandContext(self.connectivity, self.resource)
        self.handler = StcHandler()
        self.handler.initialize(context)

    def tearDown(self):
        pass

    def test_get_inventory_something(self):
        context = InitCommandContext(self.connectivity, self.resource)
        inventory = self.handler.get_inventory(context)
        for r in inventory.resources:
            print r.relative_address, r.model, r.name
        for a in inventory.attributes:
            print a.relative_address, a.attribute_name, a.attribute_value


if __name__ == '__main__':
    import sys
    sys.exit(unittest.main())
