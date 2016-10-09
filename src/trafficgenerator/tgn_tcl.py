"""
This module implements classes and utility functions to manage TGN Python <-> Tcl connectivity.
"""

from os import path
import logging

from Tkinter import Tk


def tcl_str(string=''):
    """
    :param string: Python string.
    :returns: Tcl string surrounded by {}.
    """
    return ' {' + string + '} '


def tcl_file_name(name):
    """
    :param names: file name.
    :returns: normalized file name with forward slashes.
    """
    return tcl_str(path.normpath(name).replace('\\', '/'))


def get_args_pairs(arguments):
    """
    :param arguments: Python dictionary of TGN API command arguments <key, value>.
    :returns: Tcl list of argument pairs <-key, value> to be used in TGN API commands.
    """
    return ' '.join(' '.join(['-' + k, tcl_str(str(v))]) for k, v in arguments.items())


def build_obj_ref_list(objects):
    """
    :param objects: Python list of requested objects.
    :returns: Tcl list of all requested objects references.
    """
    return ' '.join([o.obj_ref() for o in objects])


def is_true(str_value):
    """
    :param str_value: String to evaluate.
    :returns: True if Tcl string represents True value else return False.
    """
    return str_value.lower() in ('true', '1')


def is_false(str_value):
    """
    :param str_value: String to evaluate.
    :returns: True if Tcl string represents False value else return True.
    """
    return str_value.lower() in ('false', '0', 'null', 'none')


tcl_interp_g = None
""" Global Tcl interpreter for Tcl based utilities. Does not log its operations. """


def tcl_list_2_py_list(tcl_list):
    """ Convert Tcl list to Python list using Tcl interpreter.

    :param tcl_list: string representing the Tcl string.
    :return: Python list equivalent to the Tcl list.
    """
    return tcl_interp_g.eval('join' + tcl_str(tcl_list) + '\\t').split('\t') if tcl_list else []


def py_list_to_tcl_list(py_list):
    """ Convert Python list to Tcl list using Tcl interpreter.

    :param py_list: Python list.
    :return: string representing the Tcl string equivalent to the Python list.
    """
    py_list_str = [str(s) for s in py_list]
    return tcl_str(tcl_interp_g.eval('split' + tcl_str('\t'.join(py_list_str)) + '\\t'))


class TgnTk(Tk):
    """ Raw Tk interpreter wrapper for TGN projects. """

    def __init__(self):
        Tk.__init__(self)

    def eval(self, command):
        return self.tk.eval(command)


class TgnTcl(object):
    """ Tcl connectivity for TGN projects. """

    tcl_interp = None

    tcl_script = None
    logger = None
    rc = None

    def __init__(self, logger, tcl_interp=None):
        """ Init Python Tk package.

        Add logger to log Tcl commands only.
        This creates a clean Tcl script that can be used later for debug.
        We assume that there might have both IXN and STC sessions simultaneously so we add suffix
        to create two distinguished Tcl scripts.
        """

        self.logger = logger
        logger_file_name = path.splitext(logger.handlers[0].baseFilename)[0]
        tcl_logger_file_name = logger_file_name + '-' + self.__class__.__name__ + '.tcl'
        self.tcl_script = logging.getLogger('tcl' + self.__class__.__name__)
        self.tcl_script.addHandler(logging.FileHandler(tcl_logger_file_name))
        self.tcl_script.setLevel(logger.getEffectiveLevel())

        if not tcl_interp:
            self.tcl_interp = TgnTk()
        else:
            self.tcl_interp = tcl_interp
        global tcl_interp_g
        tcl_interp_g = self.tcl_interp

    def eval(self, command):
        """ Execute Tcl command.

        Write the command to tcl script (.tcl) log file.
        Execute the command.
        Write the command and the output to general (.txt) log file.

        :param command: Command to execute.
        :returns: command raw output.
        """
        self.logger.debug(command)
        self.tcl_script.info(command)
        self.rc = self.tcl_interp.eval(command)
        self.logger.debug('\t' + self.rc)
        return self.rc

    def source(self, script_file):
        self.eval('source ' + tcl_file_name(script_file))
