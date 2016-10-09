"""
"""

import time
import re
from collections import OrderedDict

from trafficgenerator.tgn_tcl import build_obj_ref_list, tcl_list_2_py_list
from trafficgenerator.tgn_object import TgnObject


def extract_stc_obj_type_from_obj_ref(obj_ref):
    # Extract object type from object reference. Note that there are rare cases where
    # object reference has no sequential number suffix like 'automationoptions'.
    m = re.search('(.*\D+)\d+', obj_ref)
    return m.group(1) if m else obj_ref


class StcObject(TgnObject):

    # Class level variables
    logger = None
    inter = None
    project = None

    str_2_class = {}

    def __init__(self, **data):
        if 'objType' not in data and 'objRef' in data:
            data['objType'] = extract_stc_obj_type_from_obj_ref(data['objRef'])
        super(StcObject, self).__init__(**data)

    def get_obj_class(self, str_obj):
        return StcObject.str_2_class.get(str_obj.lower(), StcObject)

    def _create(self):
        """ Create new object on STC.

        @return: STC object reference.
        """

        # At this time objRef is not set yet so we must use direct calls to inter.
        if 'name' in self._data:
            return self.inter.create(self.obj_type(), self.obj_parent(), name=self.obj_name())
        else:
            stc_obj = self.inter.create(self.obj_type(), self.obj_parent())
            self._data['name'] = self.inter.get(stc_obj, 'name')
            return stc_obj

    def command(self, command, wait_after=0, **arguments):
        self.inter.perform(command, **arguments)
        time.sleep(wait_after)

    def get_attribute(self, attribute):
        return self.inter.get(self.obj_ref(), attribute)

    def get_attributes(self):
        attributes_list = self.inter.get(self.obj_ref())
        attributes_dict = dict(zip(*[iter(tcl_list_2_py_list(attributes_list))] * 2))
        return dict(zip([s[1:] for s in attributes_dict.keys()], attributes_dict.values()))

    def get_children(self, *types):
        children_objs = OrderedDict()
        if not types:
            types = self.get_all_child_types()
        for child_type in types:
            output = self.get_attribute('children' + '-' + child_type)
            children_objs.update(self._build_children_objs(child_type, output.split(' ')))
        return children_objs.values()

    def get_all_child_types(self):
            children = self.get_attribute('children').split()
            return list(set([m.group(1) for c in children for m in [re.search('(.*\D+)\d+', c)]]))

    def set_attributes(self, apply_=False, **attributes):
        self.inter.config(self.obj_ref(), **attributes)
        if apply_:
            self.inter.apply()

    def get_name(self):
        return self.get_attribute('name')

    @classmethod
    def send_arp_ns(cls, *handle_list):
        """ Send ARP and NS for ports, devices or stream blocks. """
        StcObject.inter.perform('ArpNdStart', HandleList=build_obj_ref_list(handle_list))
