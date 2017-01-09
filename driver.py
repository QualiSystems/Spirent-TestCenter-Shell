
from cloudshell.shell.core.resource_driver_interface import ResourceDriverInterface

from stc_handler import StcHandler


class TestCenterChassisDriver(ResourceDriverInterface):

    def __init__(self):
        self.handler = StcHandler()

    def initialize(self, context):
        """
        :type context: cloudshell.shell.core.driver_context.InitCommandContext
        """
        self.handler.initialize(context)
        return 'Finished initializing'

    # Destroy the driver session, this function is called every time a driver instance is destroyed
    # This is a good place to close any open sessions, finish writing to log files
    def cleanup(self):
        pass

    def get_inventory(self, context):
        """ Return device structure with all standard attributes

        :type context: cloudshell.shell.core.driver_context.AutoLoadCommandContext
        :rtype: cloudshell.shell.core.driver_context.AutoLoadDetails
        """
        return self.handler.get_inventory(context)

    def set_port_logic_name(self,context,logic_names):
        return self.handler.set_port_attribute(context,logic_names)
