#!/usr/bin/python
#///////////////////////////// CoronadoS.HW.2.py ///////////////////////////////////////////
#
#   By: Sergio Coroando
#
#   Purpose:
#   Pases in a file to be parsed from the command prompt and outputs traffic statistics from it
#
#   Dependency:
#   Depends of statistics and matplotlib, numpy and scipy libraries
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

# ////////////////////////////////////////// Main ////////////////////////////////////////////////

DOMAIN_ADDR = [129, 63]
NUM_BINS = 100
BIN_uSEC = 50000

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
    incoming_counting = []
    incoming_p_size = 0
    incoming_arrival_times = []

    outgoing = []
    outgoing_counting = []
    outgoing_p_size = 0
    outgoing_arrival_times = []

    out_ref_time_set = False
    in_ref_time_set = False
    outgoing_ref_time = 0
    incoming_ref_time = 0
    o_n = 0
    i_n = 0

    i_bin_start = BIN_uSEC
    o_bin_start = BIN_uSEC
    i_bin_count = 0
    o_bin_count = 0
    bin_offset = 1
    i_counts = []
    o_counts = []

    previousTime = 0;

    for d in sorted(data):

        assert (d.usec >= previousTime)
        previousTime = d.usec

        if d.src_ip[:2] == DOMAIN_ADDR[:2]:

            outgoing_p_size += d.p_size

            if out_ref_time_set:
                if len(outgoing_arrival_times) == 0:
                    outgoing_arrival_times.append(d.usec - outgoing_ref_time)
                else:
                    outgoing_arrival_times.append(d.usec - outgoing[-1].usec)
                outgoing_counting.append(d.usec - outgoing_ref_time)
                outgoing.append(d)
                o_n += 1
            else:
                outgoing_ref_time = d.usec
                out_ref_time_set = True

        if d.dst_ip[:2] == DOMAIN_ADDR[:2]:
            incoming_p_size += d.p_size
            if in_ref_time_set:
                if len(incoming_arrival_times) == 0:
                    incoming_arrival_times.append(d.usec - incoming_ref_time)
                else:
                    incoming_arrival_times.append(d.usec - incoming[-1].usec)
                incoming_counting.append(d.usec - incoming_ref_time)
                incoming.append(d)
                i_n += 1
            else:
                incoming_ref_time = d.usec
                in_ref_time_set = True

    fig, (n, ax1, ax2, ax3, ax4) = plt.subplots(5, 1, sharex=False, sharey=False)

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

    print ("******** Raw data ********")
    print ("Incoming Max: " + str(i_max) + ' us')
    print ("Incoming Min: " + str(i_min) + ' us')
    print ("Incoming Avg: " + '{0:.2f}'.format(i_avg) + ' us')
    print ("Incoming Var: " + '{0:.2f}'.format(i_avg) + ' us^2')
    print ("Incoming N: " + str(i_n))

    print ("Outgoing Max: " + str(o_max) + ' us')
    print ("Outgoing Min: " + str(o_min) + ' us')
    print ("Outgoing Avg: " + '{0:.2f}'.format(o_avg) + ' us')
    print ("Outgoing Var: " + '{0:.2f}'.format(o_var) + ' us^2')
    print ("Outgoing N: " + str(o_n))

    n.plot(incoming_counting, range(0, len(incoming_counting), 1),
           color='blue',
           alpha=0.2,
           label='N(t) Incoming Packets',
           linewidth=2,
           ls='-',
           drawstyle='step-pre')
    n.plot(outgoing_counting, range(0, len(outgoing_counting), 1),
           color='green',
           alpha=0.2,
           label='N(t) Outgoing Packets',
           linewidth=2,
           ls='-',
           drawstyle='step-pre')
    n.legend()

    ax1.hist(incoming_arrival_times,
             bins=range(0, i_bin_max + i_seg, i_seg),
             normed=False,
             facecolor='green',
             alpha=0.2,
             label='Incoming Packets Counts',
             linewidth=2)
    ax2.hist(outgoing_arrival_times,
             bins=range(0, o_bin_max + o_seg, o_seg),
             normed=False,
             facecolor='blue',
             alpha=0.2,
             label='Outgoing Packets Counts',
             linewidth=2)

    ax1.set_ylabel("Count")
    ax1.set_xlabel("Time us")
    ax1.set_xticks(range(0, i_bin_max + i_seg, i_seg * 20))

    ax2.set_ylabel("Count")
    ax2.set_xlabel("Time us")
    ax2.set_xticks(range(0, o_bin_max + o_seg, o_seg * 20))

    incoming_arrival_times = reject_outliers(incoming_arrival_times)
    outgoing_arrival_times = reject_outliers(outgoing_arrival_times)

    for d in sorted(incoming_counting):
        if d < i_bin_start:
            i_bin_count += 1
        else:
            i_bin_start += BIN_uSEC
            i_counts.append(i_bin_count)
            while d > i_bin_start:
                i_bin_start += BIN_uSEC
                i_counts.append(0)
            i_bin_count = 1
    i_counts.append(i_bin_count)

    for d in sorted(outgoing_counting):
        if d < o_bin_start:
            o_bin_count += 1
        else:
            o_bin_start += BIN_uSEC
            o_counts.append(o_bin_count)
            while d > o_bin_start:
                o_bin_start += BIN_uSEC
                o_counts.append(0)
            o_bin_count = 1
    o_counts.append(o_bin_count)

    assert (o_n == sum(o_counts))
    assert (i_n == sum(i_counts))

    o_avg = statistics.mean(outgoing_arrival_times)
    i_avg = statistics.mean(incoming_arrival_times)

    i_var = statistics.variance(incoming_arrival_times, i_avg)
    i_max = max(incoming_arrival_times)
    i_min = min(incoming_arrival_times)

    #i_bin_max = int(math.ceil(i_max/100.0)*100)
    #i_seg = i_bin_max/NUM_BINS

    o_var = statistics.variance(outgoing_arrival_times, o_avg)
    o_max = max(outgoing_arrival_times)
    o_min = min(outgoing_arrival_times)
    #o_bin_max = int(math.ceil(o_max/100.0)*100)
    #o_seg = o_bin_max/NUM_BINS


    #incoming_arrival_times = reject_outliers(incoming_arrival_times)
    #outgoing_arrival_times = reject_outliers(outgoing_arrival_times)
    # Prepare plot

    #i_counts, i_bins = np.histogram(incoming_arrival_times, range(0, i_bin_max, i_seg), normed=True)
    #o_counts, o_bins = np.histogram(outgoing_arrival_times, range(0, o_bin_max, o_seg), normed=True)

    i_mean = statistics.mean(incoming_counting)
    o_mean = statistics.mean(outgoing_counting)

    i_pdist = poisson(i_mean)
    o_pdist = poisson(o_mean)
    pi_counts = [float(x / (i_n * 1.0)) for x in i_counts]
    po_counts = [float(x / (o_n * 1.0)) for x in o_counts]

    total_pi = sum(pi_counts)
    total_po = sum(po_counts)

    assert (int(total_pi) == 1), "PMF does not add up to One"
    assert (int(total_po) == 1), "PMF does not add up to One"

    print ("******** Removed Outliers ********")

    print ("Incoming Max: " + str(i_max) + ' us')
    print ("Incoming Min: " + str(i_min) + ' us')
    print ("Incoming Avg: " + '{0:.2f}'.format(i_avg) + ' us')
    print ("Incoming Var: " + '{0:.2f}'.format(i_var) + ' us^2')
    print ("Incoming N: " + str(len(incoming_arrival_times)))

    print ("Outgoing Max: " + str(o_max) + ' us')
    print ("Outgoing Min: " + str(o_min) + ' us')
    print ("Outgoing Avg: " + '{0:.2f}'.format(o_avg) + ' us')
    print ("Outgoing Var: " + '{0:.2f}'.format(o_var) + ' us^2')
    print ("Outgoing N: " + str(len(outgoing_arrival_times)))

    i_bins = range(0, max(incoming_counting), BIN_uSEC)
    o_bins = range(0, max(outgoing_counting), BIN_uSEC)

    i_theoretical = i_pdist.pmf(i_bins)
    o_theoretical = o_pdist.pmf(o_bins)


    #ax3.plot(i_bins, pi_counts,
    #         color='blue',
    #         alpha=.7,
    #         label='Incoming PMF',
    #         linewidth=3,
    #         drawstyle='steps-post',
    #         ls='-')
    ax3.plot(i_bins, i_theoretical,
             color='black',
             alpha=1,
             label='Poisson u=' + '{0:.2f}'.format(i_avg),
             linewidth=2,
             drawstyle='steps',
             ls=':')
    ax3.set_xlabel("Time us")
    ax3.set_ylabel("Probability p")
    ax3.set_xticks(range(-BIN_uSEC, max(incoming_counting) + BIN_uSEC, BIN_uSEC * 3))


    ax4.plot(o_bins, po_counts,
             color= 'purple',
             alpha=.7,
             label='Outgoing PMF',
             linewidth=3,
             drawstyle='steps-post',
             ls='-')
    ax4.plot(o_bins, o_theoretical,
             color='magenta',
             alpha=1,
             label='Poisson u=' + '{0:.2f}'.format(o_avg),
             linewidth=2,
             drawstyle='steps',
             ls=':')
    ax4.set_xlabel("Time us")
    ax4.set_ylabel("Probability p")
    ax4.set_xticks(range(-BIN_uSEC, max(outgoing_counting) + BIN_uSEC, BIN_uSEC * 3))
    ax1.legend()
    ax2.legend()
    ax3.legend()
    ax4.legend()

    ax4.grid(True, 'both')

    if len(sys.argv) > 2:
        plt.savefig(sys.argv[2])

    plt.show()
