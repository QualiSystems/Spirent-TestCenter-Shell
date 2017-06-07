
import sys
import logging

from cloudshell.shell.core.driver_context import AutoLoadDetails, AutoLoadResource, AutoLoadAttribute
from cloudshell.shell.core.session.cloudshell_session import CloudShellSessionContext

from testcenter.stc_app import StcApp
from testcenter.api.stc_tcl import StcTclWrapper


class StcHandler(object):

    def __init__(self):

        self.logger = logging.getLogger('log')
        self.logger.addHandler(logging.FileHandler('c:/temp/stc_chassis_shell.log'))
        self.logger.addHandler(logging.StreamHandler(sys.stdout))
        self.logger.setLevel(logging.DEBUG)

    def initialize(self, context):
        """
        :type context: cloudshell.shell.core.driver_context.InitCommandContext
        """

        client_install_path = context.resource.attributes['Client Install Path']
        controller = context.resource.attributes['Controller Address']
        lab_server = controller if controller else None
        self.stc = StcApp(self.logger, StcTclWrapper(self.logger, client_install_path))
        self.stc.connect(lab_server)

    def get_inventory(self, context):
        """ Return device structure with all standard attributes

        :type context: cloudshell.shell.core.driver_context.AutoLoadCommandContext
        :rtype: cloudshell.shell.core.driver_context.AutoLoadDetails
        """

        self.resources = []
        self.attributes = []
        address = context.resource.address
        chassis = self.stc.hw.get_chassis(address)
        chassis.get_inventory()
        self._get_chassis(chassis)
        details = AutoLoadDetails(self.resources, self.attributes)
        return details

    def _get_chassis(self, chassis):
        """ Get chassis resource and attributes. """

        self._get_attributes('',
                             {'Model': chassis.attributes['Model'],
                              'Serial Number': chassis.attributes['SerialNum'],
                              'Server Description': '',
                              'Vendor': 'Spirent',
                              'Version': chassis.attributes['FirmwareVersion']})

        for module in chassis.modules.values():
            if module.attributes['Model']:
                self._get_module(module)

        for power_supply in chassis.pss.values():
            self._get_power_supply(power_supply)

    def _get_module(self, module):
        """ Get module resource and attributes. """

        relative_address = 'M' + module.attributes['Index']
        resource = AutoLoadResource(model='Generic Traffic Generator Module',
                                    name='Module' + module.attributes['Index'],
                                    relative_address=relative_address)
        self.resources.append(resource)
        self._get_attributes(relative_address,
                             {'Model': module.attributes['Model'],
                              'Serial Number': module.attributes['SerialNum'],
                              'Version': module.attributes['FirmwareVersion']})
        for port_group in module.pgs.values():
            self._get_port_group(relative_address, port_group)

    def _get_port_group(self, module_address, port_group):
        """ Get port group resource and attributes. """

        relative_address = module_address + '/PG' + port_group.attributes['Index']
        resource = AutoLoadResource(model='Generic Port Group', name='PG' + port_group.attributes['Index'],
                                    relative_address=relative_address)
        self.resources.append(resource)
        for port in port_group.ports.values():
            self._get_port(relative_address, port)

    def _get_port(self, port_group_address, port):
        """ Get port resource and attributes. """

        relative_address = port_group_address + '/P' + port.attributes['Index']
        resource = AutoLoadResource(model='Generic Traffic Generator Port', name='Port' + port.attributes['Index'],
                                    relative_address=relative_address)
        self.resources.append(resource)
        max_speed = self._get_max_speed(port.obj_parent().obj_parent().attributes['SupportedSpeeds'])
        self.attributes.append(AutoLoadAttribute(relative_address=relative_address,
                                                 attribute_name='Max Speed',
                                                 attribute_value=max_speed))

    def _get_power_supply(self, power_supply):
        """ get power supplies resource and attributes. """

        relative_address = 'PP' + power_supply.attributes['Index']
        resource = AutoLoadResource(model='Generic Power Port', name='PP' + power_supply.attributes['Index'],
                                    relative_address=relative_address)
        self.resources.append(resource)

    def _get_attributes(self, relative_address, attributes):
        """ Get attributes. """

        for attribute_name, attribute_value in attributes.items():
            self.attributes.append(AutoLoadAttribute(relative_address=relative_address,
                                                     attribute_name=attribute_name,
                                                     attribute_value=attribute_value))

    def set_port_attribute(self, context, port_name):
        """

        :param context:
        :param port_name: String example :'TestCenter Chassis 222/Module9/Port Group3/Port3':'TCP'
        :return:
        """
        splited_name = port_name.split(":")
        port_full_name = splited_name[0]
        port_logic_name = splited_name[1]

        my_api = CloudShellSessionContext(context).get_api()
        return my_api.SetAttributeValue(resourceFullPath=port_full_name, attributeName="Logical Name",
                                        attributeValue=port_logic_name)

    def _get_max_speed(self, supported_speeds):
        num_speeds = list(float(s[:-1])*1000 if s[-1] == 'M' else float(s[:-1])*1000*1000 for s in supported_speeds)
        max_speed = max(zip(num_speeds, supported_speeds))
        return max_speed[1]
