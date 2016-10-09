
import logging

from cloudshell.shell.core.driver_context import AutoLoadDetails, AutoLoadResource, AutoLoadAttribute

from testcenter.stc_app import StcApp


class StcHandler(object):

    def initialize(self, context):
        """
        :type context: cloudshell.shell.core.driver_context.InitCommandContext
        """

        client_install_path = context.resource.attributes['Client Install Path']

        self.logger = logging.getLogger('log')
        self.logger.setLevel('DEBUG')
        self.stc = StcApp(self.logger, client_install_path)
        self.stc.connect(lab_server=None, chassis=context.resource.address)

    def get_inventory(self, context):
        """ Return device structure with all standard attributes

        :type context: cloudshell.shell.core.driver_context.AutoLoadCommandContext
        :rtype: cloudshell.shell.core.driver_context.AutoLoadDetails
        """

        self.resources = []
        self.attributes = []
        chassis_manager = self.stc.system.get_child('PhysicalChassisManager')
        chassis = chassis_manager.get_child('PhysicalChassis')
        self._get_chassis(chassis)
        details = AutoLoadDetails(self.resources, self.attributes)
        return details

    def load_config(self, context, config_file_name):
        """
        :type context: cloudshell.shell.core.driver_context.ResourceCommandContext
        """
        pass

    def start_traffic(self, context):
        """
        :type context: cloudshell.shell.core.driver_context.ResourceRemoteCommandContext
        """
        pass

    def stop_traffic(self, context):
        """
        :type context: cloudshell.shell.core.driver_context.ResourceRemoteCommandContext
        """
        pass

    def _get_chassis(self, chassis):
        """ Get chassis resource and attributes. """

        self.attributes.append(AutoLoadAttribute(relative_address='',
                                                 attribute_name='Vendor',
                                                 attribute_value='Spirent'))
        self._get_attributes('', chassis,
                             {'Model': 'Model',
                              'Server Description': 'Hostname',
                              'Version': 'FirmwareVersion'})
        for test_module in chassis.get_children('PhysicalTestModule'):
            description = test_module.get_attribute('Description')
            if description:
                self._get_module(test_module)

    def _get_module(self, module):
        """ Get module resource and attributes. """

        index = module.get_attribute('Index')
        relative_address = index
        resource = AutoLoadResource(model='Generic Traffic Module', name='Slot ' + index,
                                    relative_address=relative_address)
        self.resources.append(resource)
        self._get_attributes(relative_address, module,
                             {'Model': 'Model'})
        for port_group in module.get_children('PhysicalPortGroup'):
            self._get_port_group(relative_address, port_group)

    def _get_port_group(self, module_address, port_group):
        """ Get port group resource and attributes. """

        index = port_group.get_attribute('Index')
        relative_address = module_address + '/' + index
        resource = AutoLoadResource(model='Generic Port Group', name='Port Group ' + index,
                                    relative_address=relative_address)
        self.resources.append(resource)
        for port in port_group.get_children('PhysicalPort'):
            self._get_port(relative_address, port)

    def _get_port(self, port_group_address, port):
        """ Get port resource and attributes. """

        index = port.get_attribute('Index')
        relative_address = port_group_address + '/' + index
        resource = AutoLoadResource(model='Generic Traffic Port', name='Port ' + index,
                                    relative_address=relative_address)
        self.resources.append(resource)

    def _get_attributes(self, relative_address, stc_obj, attributes):
        """ Get attributes. """

        for attribute_name, attribute in attributes.items():
            self.attributes.append(AutoLoadAttribute(relative_address=relative_address,
                                                     attribute_name=attribute_name,
                                                     attribute_value=stc_obj.get_attribute(attribute)))
