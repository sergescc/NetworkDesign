import CursorCntl
import IPTrafficData
import sys
import numpy as np
import statistics as stats
import matplotlib.pyplot as plt
import matplotlib.gridspec as gs
import math
from scipy.stats import poisson

DOMAIN_ADDR = [129, 63]
PORTS = 65536
SYSTEM_PORTS = 1023
RESERVED_PORTS = 49151
USER_PORTS = 65536
SYSTEM_PORT_STEPS = 10
RESERVED_PORT_STEPS = 100
USER_PORT_STEPS = 500

if __name__ == "__main__":

    if len(sys.argv) < 2:
        print(CursorCntl.CONST_ERROR + " Need to specify file to open")
        sys.exit(-1)

    # Read data from file

    data = IPTrafficData.read_data(sys.argv[1])

    pkt_port_width = []
    pkt_port_bins = [0]

    pkt_port_bins = range(0, SYSTEM_PORTS, SYSTEM_PORT_STEPS) \
                    + range(SYSTEM_PORTS + 1, RESERVED_PORTS, RESERVED_PORT_STEPS)\
                    + range(RESERVED_PORTS + 1, USER_PORTS, USER_PORT_STEPS)
    i_pkt_c = [0] * PORTS
    i_byte_c = [0] * PORTS
    i_pkt_c_pack = []
    i_byte_pack = []
    i_pkt_total = 0
    i_pkt_c_pack_norm = []
    i_byte_pack_norm = []
    i_pkt_total = 0
    i_byte_total = 0

    o_pkt_c = [0] * PORTS
    o_byte_c = [0] * PORTS
    o_pkt_c_pack = []
    o_pkt_c_pack_norm = []
    o_byte_pack_norm = []
    o_byte_pack = []
    o_pkt_total = 0
    o_byte_total = 0

    start_bin = 0

    i_pkt_bin_c = 0
    o_pkt_bin_c = 0

    i_byte_bin_c = 0
    o_byte_bin_c = 0

    for d in data:
        if d.dst_ip[:2] == DOMAIN_ADDR[:2]:
            i_pkt_c[d.iport] += 1
            i_byte_c[d.iport] += d.p_size
            i_pkt_total += 1
            i_byte_total += d.p_size
        if d.src_ip[:2] == DOMAIN_ADDR[:2]:
            o_pkt_c[d.oport] += 1
            o_byte_c[d.oport] += d.p_size
            o_pkt_total += 1
            o_byte_total += d.p_size

    for i in range(0, PORTS, 1):
        if i <= SYSTEM_PORTS:
            if i < (start_bin + SYSTEM_PORT_STEPS):
                i_pkt_bin_c += i_pkt_c[i]
                o_pkt_bin_c += o_pkt_c[i]
                i_byte_bin_c += i_byte_c[i]
                o_byte_bin_c += o_byte_c[i]
            else:
                pkt_port_width.append(SYSTEM_PORT_STEPS)
                i_pkt_c_pack.append(i_pkt_bin_c)
                o_pkt_c_pack.append(o_pkt_bin_c)
                i_byte_pack.append(i_byte_bin_c)
                o_byte_pack.append(o_byte_bin_c)
                i_pkt_c_pack_norm.append(i_pkt_bin_c/float(i_pkt_total))
                o_pkt_c_pack_norm.append(o_pkt_bin_c/float(o_pkt_total))
                i_byte_pack_norm.append(i_byte_bin_c/float(i_byte_total))
                o_byte_pack_norm.append(o_byte_bin_c/float(o_byte_total))
                i_pkt_bin_c = i_pkt_c[i]
                o_pkt_bin_c = o_pkt_c[i]
                i_byte_bin_c = i_byte_c[i]
                o_byte_bin_c = o_byte_c[i]
                start_bin += SYSTEM_PORT_STEPS
                if start_bin > SYSTEM_PORTS:
                    start_bin = SYSTEM_PORTS + 1
        elif i <= RESERVED_PORTS:
            if start_bin < SYSTEM_PORTS:
                pkt_port_width.append(SYSTEM_PORT_STEPS)
                i_pkt_c_pack.append(i_pkt_bin_c)
                o_pkt_c_pack.append(o_pkt_bin_c)
                i_byte_pack.append(i_byte_bin_c)
                o_byte_pack.append(o_byte_bin_c)
                i_pkt_c_pack_norm.append(i_pkt_bin_c/float(i_pkt_total))
                o_pkt_c_pack_norm.append(o_pkt_bin_c/float(o_pkt_total))
                i_byte_pack_norm.append(i_byte_bin_c/float(i_byte_total))
                o_byte_pack_norm.append(o_byte_bin_c/float(o_byte_total))
                i_pkt_bin_c = i_pkt_c[i]
                o_pkt_bin_c = o_pkt_c[i]
                i_byte_bin_c = i_byte_c[i]
                o_byte_bin_c = o_byte_c[i]
                start_bin = SYSTEM_PORTS + 1
            if i < (start_bin + RESERVED_PORT_STEPS):
                i_pkt_bin_c += i_pkt_c[i]
                o_pkt_bin_c += o_pkt_c[1]
                i_byte_bin_c += i_byte_c[i]
                o_byte_bin_c += o_byte_c[i]
            else:
                pkt_port_width.append(RESERVED_PORT_STEPS)
                i_pkt_c_pack.append(i_pkt_bin_c)
                o_pkt_c_pack.append(o_pkt_bin_c)
                i_byte_pack.append(i_byte_bin_c)
                o_byte_pack.append(o_byte_bin_c)
                i_pkt_c_pack_norm.append(i_pkt_bin_c/float(i_pkt_total))
                o_pkt_c_pack_norm.append(o_pkt_bin_c/float(o_pkt_total))
                i_byte_pack_norm.append(i_byte_bin_c/float(i_byte_total))
                o_byte_pack_norm.append(o_byte_bin_c/float(o_byte_total))
                i_pkt_bin_c = i_pkt_c[i]
                o_pkt_bin_c = o_pkt_c[i]
                i_byte_bin_c = i_byte_c[i]
                o_byte_bin_c = o_byte_c[i]
                start_bin += RESERVED_PORT_STEPS
                if start_bin > RESERVED_PORTS:
                    start_bin = RESERVED_PORTS + 1
        else:
            if start_bin < RESERVED_PORTS:
                pkt_port_width.append(RESERVED_PORT_STEPS)
                i_pkt_c_pack.append(i_pkt_bin_c)
                o_pkt_c_pack.append(o_pkt_bin_c)
                i_byte_pack.append(i_byte_bin_c)
                o_byte_pack.append(o_byte_bin_c)
                i_pkt_c_pack_norm.append(i_pkt_bin_c/float(i_pkt_total))
                o_pkt_c_pack_norm.append(o_pkt_bin_c/float(o_pkt_total))
                i_byte_pack_norm.append(i_byte_bin_c/float(i_byte_total))
                o_byte_pack_norm.append(o_byte_bin_c/float(o_byte_total))
                i_pkt_bin_c = i_pkt_c[i]
                o_pkt_bin_c = o_pkt_c[i]
                i_byte_bin_c = i_byte_c[i]
                o_byte_bin_c = o_byte_c[i]
                start_bin = RESERVED_PORTS + 1
            if i < (start_bin + USER_PORT_STEPS):
                i_pkt_bin_c += i_pkt_c[i]
                o_pkt_bin_c += o_pkt_c[i]
                i_byte_bin_c += i_byte_c[i]
                o_byte_bin_c += o_byte_c[i]
            else:
                pkt_port_width.append(USER_PORT_STEPS)
                i_pkt_c_pack.append(i_pkt_bin_c)
                o_pkt_c_pack.append(o_pkt_bin_c)
                i_byte_pack.append(i_byte_bin_c)
                o_byte_pack.append(o_byte_bin_c)
                i_pkt_c_pack_norm.append(i_pkt_bin_c/float(i_pkt_total))
                o_pkt_c_pack_norm.append(o_pkt_bin_c/float(o_pkt_total))
                i_byte_pack_norm.append(i_byte_bin_c/float(i_byte_total))
                o_byte_pack_norm.append(o_byte_bin_c/float(o_byte_total))
                i_pkt_bin_c = i_pkt_c[i]
                o_pkt_bin_c = o_pkt_c[i]
                i_byte_bin_c = i_byte_c[i]
                o_byte_bin_c = o_byte_c[i]
                start_bin += USER_PORT_STEPS

    pkt_port_width.append(USER_PORT_STEPS)
    i_pkt_c_pack.append(i_pkt_bin_c)
    o_pkt_c_pack.append(o_pkt_bin_c)
    i_byte_pack.append(i_byte_bin_c)
    o_byte_pack.append(o_byte_bin_c)
    i_pkt_c_pack_norm.append(i_pkt_bin_c/float(i_pkt_total))
    o_pkt_c_pack_norm.append(o_pkt_bin_c/float(o_pkt_total))
    i_byte_pack_norm.append(i_byte_bin_c/float(i_byte_total))
    o_byte_pack_norm.append(o_byte_bin_c/float(o_byte_total))

    grid = gs.GridSpec(2, 2)
    ip = plt.subplot(grid[0, 0])
    ic = plt.subplot(grid[0, 1])
    op = plt.subplot(grid[1, 0])
    oc = plt.subplot(grid[1, 1])

    ip.bar(pkt_port_bins,
           i_pkt_c_pack,
           color='purple',
           alpha=.5,
           label='Incoming Packets Counts',
           width=pkt_port_width)

    ip.set_xlim(-1000, USER_PORTS + 1000)
    ip.set_title("Incoming Packet Counts per Port")
    ip.set_xlabel("Ports")
    ip.set_ylabel("Counts")

    ic.bar(pkt_port_bins,
           i_pkt_c_pack_norm,
           color='purple',
           alpha=.5,
           label='Incoming Packets Counts',
           width=pkt_port_width)

    ic.set_xlim(-1000, USER_PORTS + 1000)
    ic.set_title("Probabilities of incoming Packet Counts per Port")
    ic.set_xlabel("Ports")
    ic.set_ylabel("Counts")

    op.bar(pkt_port_bins,
           o_pkt_c_pack,
           color='green',
           alpha=.5,
           label='Incoming Packets Counts',
           width=pkt_port_width)

    op.set_xlim(-1000, USER_PORTS + 1000)
    op.set_title("Outgoing Packet Counts per Port")
    op.set_xlabel("Ports")
    op.set_ylabel("Counts")

    oc.bar(pkt_port_bins,
           o_pkt_c_pack_norm,
           color='green',
           alpha=.5,
           label='Incoming Packets Counts',
           width=pkt_port_width)

    oc.set_xlim(-1000, USER_PORTS + 1000)
    oc.set_title("Probabilities of Outgoing Packet Counts per Port")
    oc.set_xlabel("Ports")
    oc.set_ylabel("Counts")

    plt.show()




    if len(sys.argv) > 2:
        plt.savefig(sys.argv[2])


