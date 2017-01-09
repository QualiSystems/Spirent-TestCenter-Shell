
import logging

from cloudshell.shell.core.driver_context import AutoLoadDetails, AutoLoadResource, AutoLoadAttribute
from cloudshell.shell.core.session.cloudshell_session import CloudShellSessionContext
from testcenter.stc_app import StcApp
from testcenter.api.stc_tcl import StcTclWrapper


class StcHandler(object):

    def initialize(self, context):
        """
        :type context: cloudshell.shell.core.driver_context.InitCommandContext
        """

        client_install_path = context.resource.attributes['Client Install Path']
        self.logger = logging.getLogger('log')
        self.logger.setLevel('DEBUG')
        self.stc = StcApp(self.logger, StcTclWrapper(self.logger, client_install_path))
        self.stc.connect()

    def get_inventory(self, context):
        """ Return device structure with all standard attributes

        :type context: cloudshell.shell.core.driver_context.AutoLoadCommandContext
        :rtype: cloudshell.shell.core.driver_context.AutoLoadDetails
        """

        self.resources = []
        self.attributes = []
        address = context.resource.address
        chassis = self.stc.hw.get_chassis(address)
        self._get_chassis(chassis)
        details = AutoLoadDetails(self.resources, self.attributes)
        return details

    def _get_chassis(self, chassis):
        """ Get chassis resource and attributes. """

        self.attributes.append(AutoLoadAttribute(relative_address='',
                                                 attribute_name='Vendor',
                                                 attribute_value='Spirent'))
        self._get_attributes('', chassis,
                             {'Model': chassis.attributes['Model'],
                              'Serial Number': chassis.attributes['SerialNum'],
                              'Server Description': '',
                              'Version': chassis.attributes['FirmwareVersion']})
#        self._get_power_suppies(chassis.get_child('PhysicalChassisPowerSupplyStatus'))
        for test_module in chassis.get_thin_inventory():
            if test_module.get_attribute('Description'):
                self._get_module(test_module)

    def _get_power_suppies(self, power_supplies):
        """ get power supplies resource and attributes. """
        power_supply_list = power_supplies.get_list_attribute('PowerSupplyList')
        power_supply_status_list = power_supplies.get_list_attribute('PowerSupplyStatusList')
        for name, status in power_supply_list, power_supply_status_list:
            if name.startswith('chs') and status != 'POWER_STATUS_NOT_PRESENT':
                index = name.split('-')[1]
                relative_address = index
                AutoLoadResource(model='Generic Power Port', name='PP' + index,
                                 relative_address=relative_address)

    def _get_module(self, module):
        """ Get module resource and attributes. """

        index = module.get_attribute('Index')
        relative_address = index
        resource = AutoLoadResource(model='Generic Traffic Generator Module', name='Module' + index,
                                    relative_address=relative_address)
        self.resources.append(resource)
        self._get_attributes(relative_address, module,
                             {'Model': 'Model',
                              'Serial Number': 'SerialNum'})
        for port_group in module.get_children('PhysicalPortGroup'):
            self._get_port_group(relative_address, port_group)

    def _get_port_group(self, module_address, port_group):
        """ Get port group resource and attributes. """

        index = port_group.get_attribute('Index')
        relative_address = module_address + '/' + index
        resource = AutoLoadResource(model='Generic Port Group', name='Port Group' + index,
                                    relative_address=relative_address)
        self.resources.append(resource)
        for port in port_group.get_children('PhysicalPort'):
            self._get_port(relative_address, port)

    def _get_port(self, port_group_address, port):
        """ Get port resource and attributes. """

        index = port.get_attribute('Index')
        relative_address = port_group_address + '/' + index
        resource = AutoLoadResource(model='Generic Traffic Generator Port', name='Port' + index,
                                    relative_address=relative_address)
        self.resources.append(resource)

    def _get_attributes(self, relative_address, stc_obj, attributes):
        """ Get attributes. """

        for attribute_name, attribute in attributes.items():
            self.attributes.append(AutoLoadAttribute(relative_address=relative_address,
                                                     attribute_name=attribute_name,
                                                     attribute_value=stc_obj.get_attribute(attribute)))

    def get_api(self,context):
        """

        :param context:
        :return:
        """

        return CloudShellSessionContext(context).get_api()

    def set_port_attribute(self,context,port_name):
        """

        :param context:
        :param port_name: String example :'TestCenter Chassis 222/Module9/Port Group3/Port3':'TCP'
        :return:
        """
        splited_name = port_name.split(":")
        port_full_name = splited_name[0]
        port_logic_name = splited_name[1]

        my_api = self.get_api(context)
        return my_api.SetAttributeValue(resourceFullPath=port_full_name, attributeName="Logical Name", attributeValue=port_logic_name)


