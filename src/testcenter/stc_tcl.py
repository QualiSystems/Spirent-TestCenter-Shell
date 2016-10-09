"""
"""

from os import path

from trafficgenerator.tgn_utils import TgnError
from trafficgenerator.tgn_tcl import TgnTcl, get_args_pairs, tcl_file_name, tcl_list_2_py_list


class StcTcl(TgnTcl):
    """ Tcl interpreter for TestCenter. """

    def __init__(self, logger, stc_install_dir, tcl_interp=None):
        super(StcTcl, self).__init__(logger, tcl_interp)
        tcl_lib_dir = path.join(stc_install_dir, 'Tcl/lib')
        if path.exists(tcl_lib_dir):
            # If STC Tcl is installed add it's directory to auto_path
            self.eval('lappend auto_path ' + tcl_file_name(tcl_lib_dir))
        else:
            # Set Tcl variable dir and source pkgIndex.
            # It is the user responsibility to edit pkgIndex.
            self.eval('set dir ' + tcl_file_name(path.join(stc_install_dir,
                                                           'Spirent TestCenter Application')))
            self.source(path.join(stc_install_dir, 'Spirent TestCenter Application/pkgIndex.tcl'))
        self.ver = self.eval('package require SpirentTestCenter')

    def load_tcl_stats(self, tcllib_dir, tgnlib_dir):
        self.eval('set dir ' + tcl_file_name(tcllib_dir))
        self.source(path.join(tcllib_dir, 'pkgIndex.tcl'))
        self.source(path.join(tgnlib_dir, 'trafficgenerator.tcl'))
        self.source(path.join(tgnlib_dir, 'stc_stats.tcl'))

    def stc_command(self, command, *attributes):
        self.stc_rc = self.eval('stc::' + command + ' ' + ' '.join(attributes))
        return self.stc_rc

    def parse_rc(self, attribute):
        attributes_dict = dict(zip(*[iter(tcl_list_2_py_list(self.stc_rc))] * 2))
        return attributes_dict.get('-' + attribute, None)

    def test_rc(self, attribute):
        status = self.parse_rc(attribute).lower()
        if status and 'passed' not in status and 'successful' not in status:
            raise TgnError('{} = {}'.format(attribute, status))

    #
    # SpirentTestCenter Tcl package commands.
    #

    def apply(self):
        """ Sends a test configuration to the Spirent TestCenter chassis. """
        self.stc_command('apply')

    def config(self, obj_ref, **attributes):
        """ Set or modifies one or more object attributes, or a relation.

        :param obj_ref: requested object reference.
        :param attributes: dictionary of {attributes: values} to configure.
        """

        self.stc_command('config', obj_ref, get_args_pairs(attributes))

    def create(self, obj_type, parent, **attributes):
        """ Creates one or more Spirent TestCenter Automation objects.

        :param obj_type: object type.
        :param parent: object parent - object will be created under this parent.
        :param attributes: additional attributes.
        :return: STC object reference.
        """

        return self.stc_command('create ' + obj_type + ' -under ' + parent.obj_ref(),
                                get_args_pairs(attributes))

    def delete(self, obj_ref):
        """ Delete the specified object.

        :param obj_ref: object reference of the object to delete.
        """

        return self.stc_command('delete', obj_ref)

    def get(self, obj_ref, attribute=None):
        """ Returns the value(s) of one or more object attributes or a set of object handles.

        :param obj_ref: requested object reference.
        :param attribute: requested attribute. If empty - return values of all object attributes.
        :return: requested value(s) as returned by get command.
        """

        attribute = '-' + attribute if attribute is not None else ''
        return self.stc_command('get', obj_ref, attribute)

    def perform(self, command, **arguments):
        """ Execute a command.

        :param command: requested command.
        :param arguments: additional arguments.
        """

        self.stc_command('perform', command, get_args_pairs(arguments))
