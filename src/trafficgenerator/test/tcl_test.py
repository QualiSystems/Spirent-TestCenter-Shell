"""
"""

from os import path

from trafficgenerator.tgn_tcl import TgnTcl, tcl_list_2_py_list, py_list_to_tcl_list

from tg_test import TgTest


class TclTest(TgTest):

    TgTest.config_file = path.join(path.dirname(__file__), 'TrafficGenerator.ini')

    def testList(self):
        tcl = TgnTcl(self.logger)

        py_list = ['a', 'b b']
        tcl_list_length = tcl.eval('llength ' + py_list_to_tcl_list(py_list))
        assert(int(tcl_list_length) == 2)

        tcl_list = '{a} {b b}'
        py_list_length = len(tcl_list_2_py_list(tcl_list))
        assert(py_list_length == 2)

        pass
