"""
"""

import os
import posixpath
import imp


class StcPythonEnhanced(object):

    def __init__(self, logger, stc_install_dir):
        """ Init STC Python package.

        Add logger to log STC python package commands only.
        This creates a clean python script that can be used later for debug.
        """

        super(self.__class__, self).__init__()
        stc_private_install_dir = posixpath.sep.join([stc_install_dir, 'Spirent TestCenter Application'])
        os.environ['STC_PRIVATE_INSTALL_DIR'] = stc_private_install_dir
        stc_python_module = posixpath.sep.join([stc_private_install_dir, 'API/Python/StcPython.py'])
        self.stc = imp.load_source('StcPython', stc_python_module).StcPython()

    def create(self, obj_type, parent, **attributes):
        """ Creates one or more Spirent TestCenter Automation objects.

        :param obj_type: object type.
        :param parent: object parent - object will be created under this parent.
        :param attributes: additional attributes.
        :return: STC object reference.
        """

        return self.stc.create(obj_type, under=parent.obj_ref(), **attributes)

    def perform(self, command, **arguments):
        """ Execute a command.

        :param command: requested command.
        :param arguments: additional arguments.
        """

        return self.stc.perform(command, **arguments)

    def get(self, obj_ref, attribute=None):
        """ Returns the value(s) of one or more object attributes or a set of object handles.

        :param obj_ref: requested object reference.
        :param attribute: requested attribute. If empty - return values of all object attributes.
        :return: requested value(s) as returned by get command.
        """

        return self.stc.get(obj_ref, attribute)
