"""
"""

from os import path
import sys
import unittest
import logging
from ConfigParser import SafeConfigParser

class TgTest(unittest.TestCase):

    config_file = path.join(path.dirname(__file__), 'TrafficGenerator.ini')

    config = None
    logger = logging.getLogger('log')

    @classmethod
    def setUpClass(cls):
        TgTest.config = SafeConfigParser(allow_no_value=True)
        TgTest.config.read(TgTest.config_file)

        TgTest.logger.setLevel(TgTest.config.get('Logging', 'level'))
        TgTest.logger.addHandler(logging.FileHandler(TgTest.config.get('Logging', 'file_name')))
        TgTest.logger.addHandler(logging.StreamHandler(sys.stdout))

    @classmethod
    def tearDownClass(cls):
        pass

    def testHelloWorld(self):
        print sys.version
        pass
