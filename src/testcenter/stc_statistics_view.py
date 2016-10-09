"""
This module implements classes and utility functions to manage STC statistics views.
"""

from trafficgenerator.tgn_tcl import py_list_to_tcl_list

from stc_object import StcObject


class StcStats(object):
    """ Represents statistics view.

    The statistics dictionary represents a table:
    Statistics Name | Object 1 Value | Object 2 Value | ...
    object          |                |                |
    parents         |                |                |
    topLevelName    |                |                |
    Stat 1          |                |                |
    ...

    For example, generatorportresults statistics for two ports might look like the following:
    Statistics Name     | Object 1 Value           | Object 2 Value
    object              | analyzerportresults1     | analyzerportresults2
    parents             | project1/port1/analyzer1 | project1/port2/analyzer2
    topLevelName        | Port 1                   | Port 2
    GeneratorFrameCount | 1000                     | 2000
    ...
    """

    inter = None
    statistics = {}

    def __init__(self, view):
        super(StcStats, self).__init__()
        self.view = view
        self.inter = StcObject.inter
        self.subscribe()
        self.statistics = {}

    def subscribe(self):
        """ Subscribe to statistics view. """
        self._command('Subscribe')

    def unsubscribe(self):
        """ UnSubscribe from statistics view. """
        self._command('Unsubscribe')

    def read_stats(self, *stats):
        """ Reads the statistics view from STC and saves it in statistics dictionary.

        :param stats: list of statistics names to read, empty list will read all statistics.
        """

        stat_out = self._command('GetStatistics', py_list_to_tcl_list(stats))
        for line in stat_out.split('ListDelimiter')[1].strip().split('\n'):
            name = line.strip().split('\t')[0]
            self.statistics[name] = line.strip().split('\t')[1:]

    def get_row(self, row='topLevelName'):
        """
        :param row: requested row (== statistic name)
        :returns: all statistics values for the requested row.
        """
        return self.statistics[row]

    def get_stats(self, obj_id, obj_id_stat='topLevelName'):
        """
        :param obj_id: requested object ID.
        :param obj_id_stat: which statistics name to use as object ID, sometimes topLevelName is
            not meaningful and it is better to use other unique identifier like stream ID.
        :returns: all statistics values for the requested object ID.
        """
        obj_statistics = {}
        for counter in self.statistics.keys():
            if self.statistics[counter]:
                obj_statistics[counter] = self.get_stat(obj_id, counter, obj_id_stat)
        return obj_statistics

    def get_stat(self, obj_id, counter, obj_id_stat='topLevelName'):
        """
        :param obj_id: requested object id.
        :param counter: requested statistics (note that some statistics are not counters).
        :param obj_id_stat: which statistics name to use as object ID, sometimes topLevelName is
            not meaningful and it is better to use other unique identifier like stream ID.
        :returns: the value of the requested counter for the requested object ID.
        """
        obj_index = self.statistics[obj_id_stat].index(obj_id)
        return self.statistics[counter][obj_index]

    def get_counter(self, obj_id, counter, obj_id_stat='topLevelName'):
        """
        :param obj_id: requested object ID.
        :param counter: requested statistics (note that some statistics are not counters).
        :param obj_id_stat: which statistics name to use as object ID, sometimes topLevelName is
            not meaningful and it is better to use other unique identifier like stream ID.
        :returns: the float value of the requested counter for the requested object ID.
        """
        return float(self.get_stat(obj_id, counter, obj_id_stat))

    #
    # Private methods.
    #

    def _command(self, command, *arguments):
        return self.inter.eval('::TestCenter::' + command + ' ' + self.view +
                               ' ' + ' '.join(arguments))
