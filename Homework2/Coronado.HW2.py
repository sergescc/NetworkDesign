import CursorCntl
import IPTrafficData
import sys
import statistics as stats
import matplotlib.pyplot as plt
import matplotlib.gridspec as gs
import math
import numpy as np
from scipy.stats import poisson


TITLE_SIZE = 12
AXIS_LBL = 10
AXIS_MRK = 10
LBL_DIVIDER = 50
PMF_LEGEND_SIZE = 8
N_LEGEND_SIZE = 8
BORDER_PAD = 5
HEIGHT_PAD = .7
WIDTH_PAD = 5
FIGX_SIZE = 5
FIGY_SIZE = 5


DOMAIN_ADDR = [10, 253]
USEC_TO_SEC = 1000000.0
BIN_SIZE = 1000000
NUM_BINS = 100
PNUM_BINS = 50
ROUND_TO_PLACE = 50.0

def reject_outliers(data):
    m = 2
    u = np.mean(data)
    s = np.std(data)
    filtered = [e for e in data if (u - 2 * s < e < u + 2 * s)]
    return filtered

if __name__ == "__main__":

    if len(sys.argv) < 2:
        print(CursorCntl.CONST_ERROR + " Need to specify file to open")
        sys.exit(-1)

    # Read data from file

    data = IPTrafficData.read_data(sys.argv[1])

    cTime = 0

    i_n = 0
    i_p_size = 0
    i_elapsed = 0
    i_elapsed_t = []
    i_inter_arr_t = []
    i_ref_t_set = False
    i_ref_t = 0
    i_last_t = 0
    i_bin_n = 1
    i_bin_count = 0
    i_counts = []
    i_bytes = []

    o_n = 0
    o_p_size = 0
    o_elapsed = 0
    o_elapsed_t = []
    o_inter_arr_t = []
    o_ref_t_set = False
    o_ref_t = 0
    o_prev_t = 0
    o_bin_n = 1
    o_bin_count = 0
    o_counts = []
    o_bytes = []


    for d in sorted(data):
        assert (d.usec >= cTime)
        cTime = d.usec

        if d.dst_ip[:2] == DOMAIN_ADDR[:2]:
            i_bytes.append(d.p_size)
            i_p_size += d.p_size

            if i_ref_t_set:
                i_n += 1
                i_elapsed = d.usec - i_ref_t
                i_inter_arr_t.append(i_elapsed - i_elapsed_t[-1])
                i_elapsed_t.append(i_elapsed)

                if i_elapsed <= (i_bin_n * BIN_SIZE):
                    i_bin_count += 1
                else:
                    while i_elapsed > (i_bin_n * BIN_SIZE):
                        i_counts.append(i_bin_count)
                        i_bin_n += 1
                        i_bin_count = 0
                    i_bin_count = 1
            else:
                i_ref_t = d.usec
                i_ref_t_set = True
                i_elapsed_t.append(0)
            i_prev_t = d.usec

        if d.src_ip[:2] == DOMAIN_ADDR[:2]:
            o_bytes.append(d.p_size)
            o_p_size += d.p_size

            if o_ref_t_set:
                o_n += 1
                o_elapsed = d.usec - o_ref_t
                o_inter_arr_t.append(o_elapsed - o_elapsed_t[-1])
                o_elapsed_t.append(o_elapsed)

                if o_elapsed <= (o_bin_n * BIN_SIZE):
                    o_bin_count += 1
                else:
                    while o_elapsed > (o_bin_n * BIN_SIZE):
                        o_counts.append(o_bin_count)
                        o_bin_n += 1
                        o_bin_count = 0
                    o_bin_count = 1
            else:
                o_ref_t = d.usec
                o_ref_t_set = True
                o_elapsed_t.append(0)
            o_prev_t = d.usec

    grid = gs.GridSpec(3, 2)
    n  = plt.subplot(grid[0, :])
    ic = plt.subplot(grid[1, 0])
    ip = plt.subplot(grid[2, 0])
    oc = plt.subplot(grid[1, 1])
    op = plt.subplot(grid[2, 1])

    #fig, (n, ic, oc, ip, op) = plt.subplots(5, 1, sharex=False, sharey=False)

    n.plot(i_elapsed_t, range(0, len(i_elapsed_t), 1),
           color='blue',
           alpha=0.2,
           label='Incoming',
           linewidth=2,
           ls='-',
           drawstyle='step-pre')
    n.plot(o_elapsed_t, range(0, len(o_elapsed_t), 1),
           color='green',
           alpha=0.2,
           label='Outgoing',
           linewidth=2,
           ls='-',
           drawstyle='step-pre')

    for tick in n.xaxis.get_major_ticks():
        tick.label.set_fontsize(AXIS_MRK)
    for tick in n.yaxis.get_major_ticks():
        tick.label.set_fontsize(AXIS_MRK)
    n.set_ylabel("Total Count", fontdict={'fontsize': AXIS_LBL})
    n.set_xlabel("Time usec", fontdict={'fontsize': AXIS_LBL})
    n.set_title("Number of Packets Over Time", fontdict={'fontsize': TITLE_SIZE})
    n.legend(loc=4, prop={'size': N_LEGEND_SIZE})
    
    #i_inter_arr_t = reject_outliers(i_inter_arr_t)
    #o_inter_arr_t = reject_outliers(o_inter_arr_t)

    i_bin_size = int((math.ceil(max(i_inter_arr_t)/ROUND_TO_PLACE) * int(ROUND_TO_PLACE))/NUM_BINS)
    o_bin_size = int((math.ceil(max(o_inter_arr_t)/ROUND_TO_PLACE) * int(ROUND_TO_PLACE))/NUM_BINS)

    ic.hist(i_inter_arr_t,
            bins=range(0, max(i_inter_arr_t) + i_bin_size, i_bin_size),
            normed=True,
            facecolor='green',
            alpha=0.2,
            label='Incoming Packets Counts',
            linewidth=2)

    for tick in ic.xaxis.get_major_ticks():
        tick.label.set_fontsize(AXIS_MRK)
    for tick in ic.yaxis.get_major_ticks():
        tick.label.set_fontsize(AXIS_MRK)
    ic.set_ylabel("Probability", fontdict={'fontsize': AXIS_LBL})
    ic.set_xlabel("Time us", fontdict={'fontsize': AXIS_LBL})
    ic.set_title("Probability Distribution\nIncoming inter-packet times", fontdict={'fontsize': TITLE_SIZE})
    ic.set_xticks(range(0, max(i_inter_arr_t) + i_bin_size, i_bin_size * LBL_DIVIDER))
    ic.set_xlim(-100, max(i_inter_arr_t) + 100)
    ic.set_yscale('log')
    oc.hist(o_inter_arr_t,
            bins=range(0, max(o_inter_arr_t) + o_bin_size, o_bin_size),
            normed=True,
            facecolor='blue',
            alpha=0.2,
            label='Outgoing Packets Counts',
            linewidth=2)

    for tick in oc.xaxis.get_major_ticks():
        tick.label.set_fontsize(AXIS_MRK)
    for tick in oc.yaxis.get_major_ticks():
        tick.label.set_fontsize(AXIS_MRK)
    oc.set_ylabel("Probability", fontdict={'fontsize': AXIS_LBL})
    oc.set_xlabel("Time us", fontdict={'fontsize': AXIS_LBL})
    oc.set_title("Probability Distribution\n Outgoing inter-packet times", fontdict={'fontsize': TITLE_SIZE})
    oc.set_xticks(range(0, max(o_inter_arr_t) + o_bin_size, o_bin_size*LBL_DIVIDER))
    oc.set_yscale('log')
    ic_mean = stats.mean(i_counts)
    ic_limit = int(math.ceil(max(i_counts)/ROUND_TO_PLACE) * ROUND_TO_PLACE)
    ip_bin_size = int(ic_limit/ (PNUM_BINS * 1.0))

    oc_mean = stats.mean(o_counts)
    oc_limit = int(math.ceil(max(o_counts)/ROUND_TO_PLACE) * ROUND_TO_PLACE)
    op_bin_size = int(oc_limit/ (PNUM_BINS * 1.0))

    i_pdist = poisson(ic_mean)
    o_pdist = poisson(oc_mean)
    ip.bar(range(0, ic_limit, ip_bin_size),
           i_pdist.pmf(range(0, ic_limit, ip_bin_size)),
           color='purple',
           width=ip_bin_size,
           alpha=.2,
           label='Exact')

    ip.hist(i_counts,
            bins=range(0, ic_limit, ip_bin_size),
            normed=True,
            color='green',
            alpha=.2,
            label='Data')

    for tick in ip.xaxis.get_major_ticks():
        tick.label.set_fontsize(AXIS_MRK)
    for tick in ip.yaxis.get_major_ticks():
        tick.label.set_fontsize(AXIS_MRK)
    ip.set_xlim(0, ic_limit)
    ip.set_xlabel("Number of Arrivals", fontdict={'fontsize': 10})
    ip.set_ylabel("Probability p", fontdict={'fontsize': 10})
    ip.set_title("Incoming Arrival Count Probabilities\ndt ={0:.3f}s".format(BIN_SIZE / USEC_TO_SEC) +
                 " u= {0:.3f}s ".format(ic_mean), fontdict={'fontsize': 12})

    ip.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0, prop={'size': PMF_LEGEND_SIZE})

    op.hist(o_counts,
            bins=range(0, oc_limit, op_bin_size),
            normed=True,
            color='blue',
            alpha=.2,
            label='Data')
    op.bar(range(0, oc_limit, op_bin_size),
           o_pdist.pmf(range(0, oc_limit, op_bin_size)),
           color='purple',
           width=op_bin_size,
           alpha=.2,
           label='Exact')
    for tick in op.xaxis.get_major_ticks():
        tick.label.set_fontsize(AXIS_MRK)
    for tick in op.yaxis.get_major_ticks():
        tick.label.set_fontsize(AXIS_MRK)
    op.set_xlim(0, oc_limit)
    op.set_xlabel("Number of Arrivals", fontdict={'fontsize': AXIS_LBL})
    op.set_ylabel("Probability p", fontdict={'fontsize': AXIS_LBL})
    op.set_title("Outgoing Arrival Count Probabilities\ndt ={0:.3f}s".format(BIN_SIZE / USEC_TO_SEC) +
                 " u = {0:.3f}s".format(oc_mean), fontdict={'fontsize': 12})

    op.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0, prop={'size': PMF_LEGEND_SIZE})

    plt.tight_layout(pad=BORDER_PAD, h_pad=HEIGHT_PAD, w_pad=WIDTH_PAD)

    if len(sys.argv) > 2:
        plt.savefig(sys.argv[2])

    # #################### INCOMING PACKETS STATS ########################################
    print("\n\n////////////////////// INCOMING PACKET STATISTICS ////////////////////////////")
    print("N: " + str(i_n))
    print("Connection Time: " + str((i_elapsed_t[-1] - i_elapsed_t[0])/USEC_TO_SEC))
    print("Total Bytes: " + str(i_p_size))
    print("Mean Bytes: " + str(stats.mean(i_bytes)))
    print("Byte Variance: " + str(stats.variance(i_bytes)))
    print("Inter-Arrival Mean: " + '{0:0.5f}'.format(stats.mean(i_inter_arr_t)/USEC_TO_SEC))
    print("Inter-Arrival Variance: " + '{0:0.5f}'.format(stats.variance(i_inter_arr_t)/(USEC_TO_SEC * USEC_TO_SEC)))

    # #################### OUTGOING PACKETS STATS ########################################
    print("\n\n////////////////////// OUTGOING PACKET STATISTICS ////////////////////////////")
    print("N: " + str(o_n))
    print("Connection Time: " + str((o_elapsed_t[-1] - o_elapsed_t[0])/USEC_TO_SEC))
    print("Total Bytes: " + str(o_p_size))
    print("Mean Bytes: " + str(stats.mean(o_bytes)))
    print("Byte Variance: " + str(stats.variance(o_bytes)))
    print("Inter-Arrival Mean: " + '{0:.5f}'.format(stats.mean(o_inter_arr_t)/USEC_TO_SEC))
    print("Inter-Arrival Variance: " + '{0:.5f}'.format(stats.variance(o_inter_arr_t)/(USEC_TO_SEC * USEC_TO_SEC)))

    plt.show()
