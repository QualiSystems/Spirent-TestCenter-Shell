"""
This module implements classes and utility functions to manage STC streamblocks.
"""

from stc_object import StcObject
from trafficgenerator.tgn_tcl import tcl_list_2_py_list


class StcStream(StcObject):
    """ Represent STC stream block. """

    def __init__(self, **data):
        """ Create new streamblock on STC.

        Remove automatically created Ethernet and IPv4 configurations under StreamBlock.

        :param parent: port object.
        :return: streamblock object.
        """
        data['objType'] = 'StreamBlock'
        super(StcStream, self).__init__(**data)

    def _create(self):
        sb_ref = super(StcStream, self)._create()
        # Remove automatically created Ethernet and IPv4 configurations under StreamBlock.
        self.inter.config(sb_ref, FrameConfig='')
        return sb_ref

    def send_arp_ns(self):
        StcObject.send_arp_ns(self)


class StcGroupCollection(StcObject):
    """ Represent STC group collection. """

    def __init__(self, **data):
        """ Create new group collection on STC.

        Set GroupName = name.

        :param name: group name.
        :return: group collection object.
        """
        data['objType'] = 'GroupCollection'
        data['parent'] = self.project
        super(StcGroupCollection, self).__init__(**data)

    def _create(self):
        gc_ref = super(StcGroupCollection, self)._create()
        self.inter.config(gc_ref, GroupName=self.obj_name())
        return gc_ref


class StcTrafficGroup(StcObject):
    """ Represent STC traffic group. """

    def __init__(self, **data):
        """ Create new traffic group object.

        Set GroupName = name.

        :param name: group name.
        :param parent: group collection object.
        :return: traffic group object.
        """

        data['objType'] = 'TrafficGroup'
        super(StcTrafficGroup, self).__init__(**data)

    def _create(self):
        tg_ref = super(StcTrafficGroup, self)._create()
        self.inter.config(tg_ref, GroupName=self.obj_name())
        return tg_ref

    def set_attributes(self, apply_=False, **attributes):
        for sb in self.get_stream_blocks():
            sb.set_attributes(apply_, **attributes)

    def get_stream_blocks(self):
        streamBlocks = tcl_list_2_py_list(self.get_attribute('AffiliationTrafficGroup-Targets'))
        stc_sbs = [self.project.get_object_by_ref(r) for r in streamBlocks]
        if None in stc_sbs:
            self.project.get_stream_blocks()
            stc_sbs = [self.project.get_object_by_ref(r) for r in streamBlocks]
        return stc_sbs
