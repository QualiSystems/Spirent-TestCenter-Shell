"""
Base class for all STC package tests.

Implemented in separate module so it can be replaced easily in different environments.
"""

from os import path

from trafficgenerator.test.tg_test import TgTest

from testcenter.stc_tcl import StcTcl
from testcenter.stc_app import StcApp


class StcTestBase(TgTest):

    stc = None

    TgTest.config_file = path.join(path.dirname(__file__), 'TestCenter.ini')

    def setUp(self):
        super(StcTestBase, self).setUp()
        tcl_inter = StcTcl(self.logger, self.config.get('STC', 'install_dir'))
        self.stc = StcApp(self.logger, self.config.get('STC', 'install_dir'), tcl_inter=tcl_inter)
        log_level = self.config.get('STC', 'log_level')
        self.stc.system.get_child('automationoptions').set_attributes(LogLevel=log_level)
        self.stc.connect()

    def tearDown(self):
        super(StcTestBase, self).tearDown()
        self.stc.reset_config()

    def testHelloWorld(self):
        pass
