"""
This module implements classes and utility functions to manage STC application.
"""

from os import path
import sys
import time
import logging

from trafficgenerator.trafficgenerator import TrafficGenerator

from stc_object import StcObject
from python.stc_python import StcPythonEnhanced
from stc_device import StcDevice, StcServer, StcClient, StcRouter
from stc_port import StcPort, StcGenerator, StcAnalyzer
from stc_project import StcProject
from stc_stream import StcStream, StcGroupCollection, StcTrafficGroup


class StcApp(TrafficGenerator):
    """ TestCenter driver. Equivalent to TestCenter Application. """

    TYPE_2_OBJECT = {'analyzer': StcAnalyzer,
                     'bgprouterconfig': StcRouter,
                     'dhcpv4serverconfig': StcServer,
                     'dhcpv4blockconfig': StcClient,
                     'emulateddevice': StcDevice,
                     'generator': StcGenerator,
                     'groupcollection': StcGroupCollection,
                     'port': StcPort,
                     'streamblock': StcStream,
                     'trafficgroup': StcTrafficGroup,
                     }

    lab_server = None

    system = None
    project = None

    def __init__(self, logger, stc_install_dir, tcl_inter=None):
        super(self.__class__, self).__init__(logger)
        self.inter = tcl_inter if tcl_inter else StcPythonEnhanced(logger, stc_install_dir)
        StcObject.logger = self.logger
        StcObject.inter = self.inter
        StcObject.str_2_class = self.TYPE_2_OBJECT
        self.system = StcObject(objType='system', objRef='system1')

    def load_tcl_stats(self, tcllib_dir, tgnlib_dir):
        """ Load Tcl scripts required for STC statistics functionality.

        :param tcllib_dir: full path tcllib directory.
        :param stats_scripts_file: full path to file containing Tcl statistics script.
        """

        self.inter.load_tcl_stats(tcllib_dir, tgnlib_dir)
        self.inter.eval("::TestCenter::SetStatsViews " + self.project.obj_ref())

    def connect(self, lab_server=None, chassis=None):
        """ Create project object and optionally connect to lab server and/or chassis.

        :param lab_server: optional lab server address.
        :param chassis: optional chassis address.
        """

        self.project = StcProject(parent=self.system)
        StcObject.project = self.project
        self.lab_server = lab_server
        if self.lab_server:
            self.inter.perform('CSTestSessionConnect', Host=self.lab_server, CreateNewTestSession=True)
        if chassis:
            self.inter.perform('ChassisConnect', Hostname=chassis)

    def disconnect(self):
        """ Disconnect from chassis and lab server (if used). """

        if self.lab_server:
            self.inter.perform('CSTestSessionDisconnect', Terminate=True)
        else:
            self.inter.perform('ChassisDisconnectAll')
        self.reset_config()
        super(self.__class__, self).disconnect()

    def load_config(self, config_file_name):
        """ Load configuration file from tcc or xml.

        Configuration file type is extracted from the file suffix - xml or tcc.

        :param config_file_name: full path to the configuration file.
        """

        ext = path.splitext(config_file_name)[-1].lower()
        if ext == '.tcc':
            self.inter.perform('LoadFromDatabase',
                               DatabaseConnectionString=path.normpath(config_file_name))
        elif ext == '.xml':
            self.inter.perform('LoadFromXml', FileName=path.normpath(config_file_name))
        else:
            raise ValueError('Configuration file type {} not supported.'.format(ext))

    def reset_config(self):
        self.inter.perform('ResetConfig', config='system1')

    def save_config(self, config_file_name):
        """ Save configuration file as tcc or xml.

        Configuration file type is extracted from the file suffix - xml or tcc.
        :param config_file_name: full path to the configuration file.
        """

        ext = path.splitext(config_file_name)[-1].lower()
        if ext == '.tcc':
            self.inter.perform('SaveToTcc', FileName=path.normpath(config_file_name))
        elif ext == '.xml':
            self.inter.perform('SaveAsXml', FileName=path.normpath(config_file_name))
        else:
            raise ValueError('Configuration file type {0} not supported.'.format(ext))

    def apply(self):
        self.inter.apply()

    def clear_results(self):
        self.project.clear_results()

    #
    # Online commands.
    # All commands assume that all ports are reserved and port objects exist under project.
    #

    def send_arp_ns(self):
        StcObject.send_arp_ns(*self.project.get_objects_by_type('port'))

    #
    # Devices commands.
    #

    def start_devices(self):
        self._command_devices('DeviceStart')

    def stop_devices(self):
        self._command_devices('DeviceStop')

    def _command_devices(self, command):
        self.project.command_devices(command, 4)
        self.inter.test_rc('Status')
        time.sleep(4)

    #
    # Traffic commands.
    #

    def start_traffic(self, blocking=False):
        self.project.start_ports(blocking)

    def stop_traffic(self):
        self.project.stop_ports()

    def wait_traffic(self):
        self.project.wait_traffic()


def testcenter(args):
    """ Stand alone STC application.

    Serves as code snippet and environment testing.
    """

    # TODO: replace with ini file.
    install_dir = 'C:/Program Files (x86)/Spirent Communications/Spirent TestCenter 4.60'
    log_level = 'INFO'
    log_file_name = 'test/logs/testcenter.txt'

    logger = logging.getLogger('log')
    logger.setLevel(log_level)
    logger.addHandler(logging.FileHandler(log_file_name))
    logger.addHandler(logging.StreamHandler(sys.stdout))

    stc = StcApp(logger, install_dir)
    stc.system.get_child('automationoptions').set_attributes(LogLevel=log_level)
    stc.connect()

if __name__ == "__main__":
    sys.exit(testcenter((sys.argv[1:])))
