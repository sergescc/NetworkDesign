import CursorCntl
import IPTrafficData
import sys
import matplotlib.pyplot as plt
import matplotlib.gridspec as gs


DOMAIN_ADDR = [129, 63]
PORTS = 65536
SYSTEM_PORTS = 1023
RESERVED_PORTS = 49151
USER_PORTS = 65536
SYSTEM_PORT_STEPS = 1
RESERVED_PORT_STEPS = 10
USER_PORT_STEPS = 50

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
    imax_pkt_count = 0
    imax_byte_count =0
    imax_byte_port = 0
    imax_pkt_c_port= 0

    omax_pkt_count = 0
    omax_byte_count = 0
    omax_byte_port = 0
    omax_pkt_c_port = 0


    for d in data:

        if d.dst_ip[:2] == DOMAIN_ADDR[:2]:
            i_pkt_c[d.iport] += 1
            i_byte_c[d.iport] += d.p_size
            i_pkt_total += 1
            i_byte_total += d.p_size
            if i_pkt_c[d.iport] > imax_pkt_count:
                imax_pkt_c_port = d.iport
                imax_pkt_count = i_pkt_c[d.iport]
            if i_byte_c[d.iport] > imax_byte_count:
                imax_byte_count = i_byte_c[d.iport]
                imax_byte_port = d.iport

        if d.src_ip[:2] == DOMAIN_ADDR[:2]:
            o_pkt_c[d.oport] += 1
            o_byte_c[d.oport] += d.p_size
            o_pkt_total += 1
            o_byte_total += d.p_size
            if o_pkt_c[d.oport] > omax_pkt_count:
                omax_pkt_c_port = d.oport
                omax_pkt_count = o_pkt_c[d.oport]
            if o_byte_c[d.oport] > omax_byte_count:
                omax_byte_count = o_byte_c[d.oport]
                omax_byte_port = d.oport

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
    ib = plt.subplot(grid[0, 1])
    op = plt.subplot(grid[1, 0])
    ob = plt.subplot(grid[1, 1])

    ip.bar(pkt_port_bins,
           i_pkt_c_pack_norm,
           color='purple',
           alpha=.5,
           label='PMF Incoming Packets Counts',
           width=pkt_port_width)

    ip.set_xlim(-1000, USER_PORTS + 1000)
    ip.set_title("PMF Incoming Packet Counts per Port")
    ip.set_xlabel("Ports")
    ip.set_ylabel("Probabilities")

    ib.bar(pkt_port_bins,
           i_byte_pack_norm,
           color='purple',
           alpha=.5,
           label='PMF Incoming Byte Counts per Port',
           width=pkt_port_width)
    ib.set_xlim(-1000, USER_PORTS + 1000)
    ib.set_title("PMF Incoming Byte Counts per Port")
    ib.set_xlabel("Ports")
    ib.set_ylabel("Probabilities")

    op.bar(pkt_port_bins,
           o_pkt_c_pack_norm,
           color='green',
           alpha=.5,
           label='Incoming Packets Counts',
           width=pkt_port_width)

    op.set_xlim(-1000, USER_PORTS + 1000)
    op.set_title("PMF Outgoing Packet Counts per Port")
    op.set_xlabel("Ports")
    op.set_ylabel("Probabilities")

    ob.bar(pkt_port_bins,
           o_byte_pack_norm,
           color='green',
           alpha=.5,
           label='Incoming Packets Counts',
           width=pkt_port_width)

    ob.set_xlim(-1000, USER_PORTS + 1000)
    ob.set_title("PMF Outgoing Byte Counts per Port")
    ob.set_xlabel("Ports")
    ob.set_ylabel("Probabilities")

    print( "\n\n " + "/" * 15 + " Incoming Stats " + "/" * 15)
    print("Total Bytes: " + str(i_byte_total))
    print("Max Bytes per Port:" + str(imax_byte_count))
    print("Port with most byte traffic: " + str(imax_byte_port))
    print("Total Packets: " + str(i_pkt_total))
    print("Max Packets per Port: " +str(imax_pkt_count))
    print("Port with most packet traffic: " + str(imax_pkt_c_port))

    print( "\n\n " +"/" * 15 + " Outgoing Stats " + "/" * 15)
    print("Total Bytes: " + str(o_byte_total))
    print("Max Bytes per Port:" + str(omax_byte_count))
    print("Port with most byte traffic: " + str(omax_byte_port))
    print("Total Packets: " + str(o_pkt_total))
    print("Max Packets per Port: " +str(omax_pkt_count))
    print("Port with most packet traffic: " + str(omax_pkt_c_port))

    plt.show()

    if len(sys.argv) > 2:
        plt.savefig(sys.argv[2])


