# //////////////////////////// CoronadoS.HW.1.py ///////////////////////////////////////////
#
#   By: Sergio Coroando
#
#   Purpose:
#   Structure containing Data Files and parsing function
#
#
#   Dependency:
#
#        CursorCntl.py
#
# ////////////////////////////////////////////////////////////////////////////////////////

import os
import CursorCntl
import re


class IPDataEntry:

    src_ip = []
    dst_ip = []
    p_size = 0
    oport = 0
    iport = 0
    usec = 0

    class CnxnTime:
        hour = 0
        min = 0
        sec = 0

    def __cmp__(self, other):
        if hasattr(other, 'usec'):
            return int(self.usec.__cmp__(other.usec))


def read_data(file):
    data_set = []
    if os.path.isfile(file):
        opened_file = open(file, "r", 1)
    else:
        print(CursorCntl.CONST_ERROR + "Could Not Open Specified File\n")
        return -1

    for line in opened_file:
        if line != "\n":
            split_line = re.split('IP|>|tcp', line)
            sip_split = re.split('[.:]', split_line[1])
            dip_split = re.split('[.:]', split_line[2])
            entry=IPDataEntry()
            entry.src_ip = [int(sip_split[0]), int(sip_split[1]), int(sip_split[2]), int(sip_split[3])]
            entry.dst_ip = [int(dip_split[0]), int(dip_split[1]), int(dip_split[2]), int(dip_split[3])]
            entry.oport = int(sip_split[4])
            entry.iport = int(dip_split[4])
            entry.p_size = int(split_line[3])
            time_split = split_line[0].split(":")
            entry.CnxnTime.hour = int(time_split[0])
            entry.CnxnTime.min = int(time_split[1])
            entry.CnxnTime.sec = float(time_split[2])
            entry.usec = int(entry.CnxnTime.sec * 1000000 + entry.CnxnTime.min * 60000000 + entry.CnxnTime.hour * 3600000000)
            data_set.append(entry)

    return data_set


