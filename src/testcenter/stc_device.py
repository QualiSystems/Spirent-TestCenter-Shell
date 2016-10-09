"""
This module implements classes and utility functions to manage STC emulated device.
"""

from stc_object import StcObject


class StcDevice(StcObject):
    """ Represent STC emulated device. """

    # Create device under port (in STC objects tree emulateddevice is under project).
    def __init__(self, **data):
        """
        :param parent: when creating - port, when reading - project.
        """

        # Make sure parent is project.
        parent = data.pop('parent', None)
        data['parent'] = self.project

        # Create StcDevice object.
        data['objType'] = 'emulateddevice'
        super(StcDevice, self).__init__(**data)

        # If we create new device we should place it under the requested parent.
        if 'objRef' not in data:
            self.set_attributes(AffiliatedPort=parent.obj_ref())
            port = parent
        else:
            port = parent.get_object_by_ref(self.get_attribute('AffiliatedPort'))

        # Replace parent from project to parent.
        self._data['parent'] = port
        port.objects[self.obj_ref()] = self
        self.project.objects.pop(self.obj_ref())

    def command(self, command, wait_after=2, **arguments):
        self.project.command_devices(command, wait_after, self, **arguments)

    def send_arp_ns(self):
        StcObject.send_arp_ns(self)

    def ping(self, ip):
        self.command('PingVerifyConnectivity', PingAddress=ip)
        self.inter.test_rc('PassFailState')

    def start(self, wait_after=4):
        self.command('DeviceStart', wait_after)
        self.inter.test_rc('Status')

    def stop(self, wait_after=4):
        self.command('DeviceStop', wait_after)
        self.inter.test_rc('Status')

    def command_emulations(self, command, wait_after=4, **arguments):
        self.project.command_device_emulations(command, wait_after, self, **arguments)


class StcEmulation(StcObject):
    """ Base class for all STC emulations. """

    def command(self, command, wait_after=4, **arguments):
        """ Perform """
        self.project.command_emulations(command, wait_after, self, **arguments)


class StcRouter(StcEmulation):

    objects_list = 'RouterList'


class StcClient(StcEmulation):

    objects_list = 'BlockList'


class StcServer(StcEmulation):

    objects_list = 'ServerList'
