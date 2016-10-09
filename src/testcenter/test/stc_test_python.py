"""
Base class for all STC package tests.

Implemented in separate module so it can be replaced easily in different environments.
"""

import os

from trafficgenerator.test.tg_test import TgTest

from testcenter.stc_app import StcApp


class StcTestPython(TgTest):

    TgTest.config_file = os.path.join(os.path.dirname(__file__), 'TestCenter.ini')

    def setUp(self):
        self.stc = StcApp(self.logger, self.config.get('STC', 'install_dir'))

    def tearDown(self):
        pass

    def testHelloWorld(self):
        pass

    def testLoadChassis(self):
        resources = []
        self.stc.connect(chassis='10.224.18.200')
        chassis_manager = self.stc.system.get_child('PhysicalChassisManager')
        chassis = chassis_manager.get_child('PhysicalChassis')
        resources.append(chassis)
        for test_module in chassis.get_children('PhysicalTestModule'):
            description = test_module.get_attribute('Description')
            if description:
                resources.append(test_module)
                for port_group in test_module.get_children('PhysicalPortGroup'):
                    resources.append(port_group)
                    for port in port_group.get_children('PhysicalPort'):
                        resources.append(port)
        print ', '.join(r.obj_ref() for r in resources)
