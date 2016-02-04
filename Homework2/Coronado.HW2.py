#!/usr/bin/python
#///////////////////////////// CoronadoS.HW.2.py ///////////////////////////////////////////
#
#   By: Sergio Coroando
#
#   Purpose:
#   Pases in a file to be parsed from the command prompt and outputs traffic statistics from it
#
#   Dependency:
#   Depends of statistics and matplotlib librarrires
#   Also must include modules:
#       IPTrafficData
#       CursorCntl
#   Usage:
#   $ CoronadoS.HW1.py <data file> <graph Output file (optional)>
#
#////////////////////////////////////////////////////////////////////////////////////////////////

#/////////////////////////////////////// Imports ////////////////////////////////////////////////

import CursorCntl
import IPTrafficData
import sys
import statistics
import numpy as np
import matplotlib.pyplot as plt
import math
from scipy.stats import poisson


#////////////////////////////////////////// Main ////////////////////////////////////////////////

DOMAIN_ADDR = [129,63]
NUM_BINS = 100


def reject_outliers(dat):
    m = 2
    u = np.mean(dat)
    s = np.std(dat)
    filtered = [e for e in dat if (u - 2 * s < e < u + 2 * s)]
    return filtered




if __name__ == "__main__":

    if len(sys.argv) < 2:
        print(CursorCntl.CONST_ERROR + " Need to specify file to open")
        sys.exit(-1)

    # Read data from file

    data = IPTrafficData.read_data(sys.argv[1])

    incoming = []
    incoming_p_size = 0
    incoming_arrival_times = []

    outgoing = []
    outgoing_p_size =0
    outgoing_arrival_times =[]

    out_ref_time_set = False
    in_ref_time_set = False
    outgoing_ref_time = 0
    incoming_ref_time = 0
    o_n = 0
    i_n = 0

    for d in sorted(data):
        if d.src_ip[:2] == DOMAIN_ADDR[:2]:

            outgoing_p_size += d.p_size

            if out_ref_time_set:
                o_n += 1
                if len(outgoing_arrival_times) == 0:
                    outgoing_arrival_times.append(d.usec - outgoing_ref_time)
                else:
                    outgoing_arrival_times.append(d.usec - outgoing[-1].usec)
            else:
                outgoing_ref_time = d.usec
                out_ref_time_set = True
            outgoing.append(d)

        if d.dst_ip[:2] == DOMAIN_ADDR[:2]:
            incoming_p_size += d.p_size
            if in_ref_time_set:
                i_n += 1
                if len(incoming_arrival_times) == 0:

                    incoming_arrival_times.append(d.usec - incoming_ref_time)
                else:
                    incoming_arrival_times.append(d.usec - incoming[-1].usec)
            else:
                incoming_ref_time = d.usec
                in_ref_time_set = True
            incoming.append(d)

    fig, (ax1, ax2, ax3, ax4) = plt.subplots(4, 1, sharex=False, sharey=False)

    i_avg = statistics.mean(incoming_arrival_times)
    i_var = statistics.variance(incoming_arrival_times, i_avg)
    i_max = max(incoming_arrival_times)
    i_min = min(incoming_arrival_times)
    i_bin_max = int(math.ceil(i_max/100.0)*100)
    i_seg = i_bin_max/NUM_BINS

    o_avg = statistics.mean(outgoing_arrival_times)
    o_var = statistics.variance(outgoing_arrival_times, o_avg)
    o_max = max(outgoing_arrival_times)
    o_min = min(outgoing_arrival_times)
    o_bin_max = int(math.ceil(o_max/100.0)*100)
    o_seg = o_bin_max/NUM_BINS

    print ( "******** Raw data ********")
    print ("Incoming Max: " + str(i_max) + 'us')
    print ("Incoming Min: " + str(i_min) + 'us')
    print ("Incoming Avg: " + '{0:.2f}'.format(o_avg) + ' us')
    print ("Incoming Var: " + '{0:.2f}'.format(i_avg) + ' us^2')

    print ("Outgoing Max: " + str(o_max) + 'us')
    print ("Outgoing Min: " + str(o_min) + 'us')
    print ("Outgoing Avg: " + '{0:.2f}'.format(o_avg) + ' us')
    print ("Outgoing Var: " + '{0:.2f}'.format(o_var) + ' us^2')

    ax1.hist(incoming_arrival_times,
             bins=range(0, i_bin_max, i_seg),
             normed=False,
             facecolor='green',
             alpha=0.2,
             label='N(t) Incoming Packets',
             linewidth=2)
    ax2.hist(outgoing_arrival_times,
             bins=range(0, o_bin_max, o_seg),
             normed=False,
             facecolor='blue',
             alpha=0.2,
             label='N(t) Outgoing Packets',
             linewidth=2)

    ax1.set_ylabel("Count")
    ax1.set_xlabel("Time us")
    ax1.set_xticks(range(0, i_bin_max, i_seg * 10))

    ax2.set_ylabel("Count")
    ax2.set_xlabel("Time us")
    ax2.set_xticks(range(0, o_bin_max, o_seg * 10))

    incoming_arrival_times = reject_outliers(incoming_arrival_times)
    outgoing_arrival_times = reject_outliers(outgoing_arrival_times)
    o_avg = statistics.mean(outgoing_arrival_times)
    i_avg = statistics.mean(incoming_arrival_times)

    i_var = statistics.variance(incoming_arrival_times, i_avg)
    i_max = max(incoming_arrival_times)
    i_min = min(incoming_arrival_times)

    i_bin_max = int(math.ceil(i_max/100.0)*100)
    i_seg = (i_bin_max)/NUM_BINS

    o_var = statistics.variance(outgoing_arrival_times, o_avg)
    o_max = max(outgoing_arrival_times)
    o_min = min(outgoing_arrival_times)
    o_seg = (o_max - o_min)/NUM_BINS
    o_bin_max = int(math.ceil(o_max/100.0)*100)
    incoming_arrival_times = reject_outliers(incoming_arrival_times)
    outgoing_arrival_times = reject_outliers(outgoing_arrival_times)
    # Prepare plot

    i_counts, i_bins = np.histogram(incoming_arrival_times, range(0, i_bin_max + i_seg, i_seg), normed=True)
    o_counts, o_bins = np.histogram(outgoing_arrival_times, range(0, o_bin_max + o_seg, o_seg), normed=True)
    i_pdist = poisson(i_avg)
    o_pdist = poisson(o_avg)

    print ("******** Removed Outliers ********")

    print ("Incoming Max: " + str(i_max) + ' us')
    print ("Incoming Min: " + str(i_min) + ' us')
    print ("Incoming Avg: " + '{0:.2f}'.format(i_avg) + ' us')
    print ("Incoming Var: " + '{0:.2f}'.format(i_var) + ' us^2')

    print ("Outgoing Max: " + str(o_max) + ' us')
    print ("Outgoing Min: " + str(o_min) + ' us')
    print ("Outgoing Avg: " + '{0:.2f}'.format(o_avg) + ' us')
    print ("Outgoing Var: " + '{0:.2f}'.format(o_var) + ' us^2')

    ax3.plot(i_bins[:-1], i_counts,
             color='blue',
             alpha=.7,
             label='Incoming PMF',
             linewidth=3,
             drawstyle='steps',
             ls='-')
    ax3.plot(i_bins[:-1], i_pdist.pmf(i_bins[:-1]),
             color='cyan',
             alpha=.7,
             label='Poisson u=' + '{0:.2f}'.format(i_avg),
             linewidth=2,
             drawstyle='steps',
             ls=':')
    ax3.set_xlabel("Time us")
    ax3.set_ylabel("Probability p")
    ax3.set_xticks(range(0, i_bin_max, i_seg * 10))


    ax4.plot(o_bins[:-1], o_counts,
             color= 'purple',
             alpha=.7,
             label='Outgoing PMF',
             linewidth=3,
             drawstyle='steps-pre',
             ls='-')
    ax4.plot(o_bins[:-1], o_pdist.pmf(o_bins[:-1]),
             color='magenta',
             alpha=.7,
             label='Poisson u=' + '{0:.2f}'.format(o_avg),
             linewidth=2,
             drawstyle='steps-pre',
             ls=':')
    ax4.set_xlabel("Time us")
    ax4.set_ylabel("Probability p")
    ax4.set_xticks(range(0, o_bin_max, o_seg * 10))


    plt.disconnect(10)
    ax1.legend()
    ax2.legend()
    ax3.legend()
    ax4.legend()

    plt.grid(True, 'minor')

    if len(sys.argv) > 2:
        plt.savefig(sys.argv[2])

    plt.show()
