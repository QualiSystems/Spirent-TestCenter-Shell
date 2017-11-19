#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Tests for `IxiaShellDriver`
"""

import sys
import unittest

from cloudshell.api.cloudshell_api import ResourceAttributesUpdateRequest, AttributeNameValue
from shellfoundry.releasetools.test_helper import create_session_from_cloudshell_config

stc_chassis = {'direct-stc': {'address': '192.168.42.160',
                              'controller': '',
                              'port': '',
                              'install_path': 'C:/Program Files (x86)/Spirent Communications/Spirent TestCenter 4.71',
                              'modules': 1,
                              },
               'lab-server-stc': {'address': '192.168.42.160',
                                  'controller': '192.168.42.156',
                                  'port': '',
                                  'install_path': 'C:/Program Files (x86)/Spirent Communications/Spirent TestCenter 4.71',
                                  'modules': 1,
                                  },
               }


class TestIxiaChassisShell(unittest.TestCase):

    session = None

    def setUp(self):
        self.session = create_session_from_cloudshell_config()

    def tearDown(self):
        for resource in self.session.GetResourceList('Testing').Resources:
            self.session.DeleteResource(resource.Name)

    def testHelloWorld(self):
        pass

    def test_direct_stc(self):
        self._get_inventory('direct-stc', stc_chassis['direct-stc'])

    def test_lab_server_stc(self):
        pass

    def _get_inventory(self, name, properties):
        self.resource = self.session.CreateResource(resourceFamily='Traffic Generator Chassis',
                                                    resourceModel='TestCenter Chassis',
                                                    resourceName=name,
                                                    resourceAddress=properties['address'],
                                                    folderFullPath='Testing',
                                                    parentResourceFullPath='',
                                                    resourceDescription='should be removed after test')
        self.session.UpdateResourceDriver(self.resource.Name, 'TestCenterChassisDriver')
        attributes = [AttributeNameValue('Client Install Path', properties['install_path']),
                      AttributeNameValue('Controller Address', properties['controller']),
                      AttributeNameValue('Controller TCP Port', properties['port'])]
        self.session.SetAttributesValues(ResourceAttributesUpdateRequest(self.resource.Name, attributes))
        self.session.AutoLoad(self.resource.Name)
        resource_details = self.session.GetResourceDetails(self.resource.Name)
        assert(len(resource_details.ChildResources) == properties['modules'])
        self.session.DeleteResource(self.resource.Name)


if __name__ == '__main__':
    sys.exit(unittest.main())
