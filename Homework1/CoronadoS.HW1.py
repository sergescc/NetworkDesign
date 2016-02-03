#!/usr/bin/python
#///////////////////////////// CoronadoS.HW.1.py ///////////////////////////////////////////
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
import matplotlib.pyplot as plt


#////////////////////////////////////////// Main ////////////////////////////////////////////////

if __name__ == "__main__":

    if len(sys.argv) < 2:
        print(CursorCntl.CONST_ERROR + " Need to specify file to open")
        sys.exit(-1)

    # Read data from file

    data = IPTrafficData.read_data(sys.argv[1])


    num_entries = 0
    packets = []
    src_traffic = {}
    dst_traffic = {}
    src_subnet_traffic = {}
    dst_subnet_traffic = {}

#   Collect Subnet Information and number of entries

    for d in data:
        num_entries += 1
        packets.append(d.p_size)
        string_ip_src = '.'.join(map(str, d.src_ip))
        string_ip_dst = '.'.join(map(str, d.dst_ip))
        string_ip_src_subnet = '.'.join(map(str, d.src_ip[0:2]))
        string_ip_dst_subnet = '.'.join(map(str, d.dst_ip[0:2]))
        if string_ip_src in src_traffic:
            src_traffic[string_ip_src] += d.p_size
        else:
            src_traffic[string_ip_src] = d.p_size
        if string_ip_dst in dst_traffic:
            dst_traffic[string_ip_dst] += d.p_size
        else:
            dst_traffic[string_ip_dst] = d.p_size
        if string_ip_src_subnet in src_subnet_traffic:
            src_subnet_traffic[string_ip_src_subnet] += d.p_size
        else:
            src_subnet_traffic[string_ip_src_subnet] = d.p_size
        if string_ip_dst_subnet in dst_subnet_traffic:
            dst_subnet_traffic[string_ip_dst_subnet] += d.p_size
        else:
            dst_subnet_traffic[string_ip_dst_subnet] = d.p_size

    # Calculate Subnet and Ip specific statistics

    min_src_traffic = min(src_traffic.values())
    max_src_traffic = max(src_traffic.values())
    min_subnet_src_traffic = min(src_subnet_traffic.values())
    max_subnet_src_traffic = max(src_subnet_traffic.values())

    min_dst_traffic = min(dst_traffic.values())
    max_dst_traffic = max(dst_traffic.values())
    min_subnet_dst_traffic = min(dst_subnet_traffic.values())
    max_subnet_dst_traffic = max(dst_subnet_traffic.values())


    # Ouput general connection stats

    print("\n\n**** Stats per Connection ****\n\n")
    print("Number of Entries: " + str(num_entries))
    print("Max: " + str(max(packets)))
    print("Min: " + str(min(packets)))
    print("Mean: " + str(statistics.mean(packets)))
    print("Median: " + str(statistics.median(packets)))
    print("Mode: " + str(statistics.mode(packets)))
    print("Var: " + str(statistics.variance(packets)))

    print("\n\n**** Stats per Specific IP ****\n\n")
    print("Outgoing Min:  " + str(min_src_traffic))
    print("Outgoing Max: " + str(max_src_traffic))
    for ip, size in src_traffic.items():
        if size == max_src_traffic:
            print("\tIP: " + ip)

    print("Incoming Min: " + str(min_dst_traffic))
    print("Incoming Max: " + str(max_dst_traffic))
    for ip, size in dst_traffic.items():
        if size == max_dst_traffic:
            print("\tIP: " + ip)

    print("Mean Outgoing: " + str(statistics.mean(src_traffic.values())))
    print("Median Outgoing: " + str(statistics.median(src_traffic.values())))
    print("Variance Outgoing: " + str(statistics.variance(src_traffic.values())))
    print("Mean Incoming: " + str(statistics.mean(dst_traffic.values())))
    print("Median Incoming: " + str(statistics.median(dst_traffic.values())))
    print("Variance Incoming: " + str(statistics.variance(dst_traffic.values())))


    # Output Ip specifi stats

    print("\n\n**** Stats per Specific Subnet ****\n\n")
    print("Outgoing Min:  " + str(min_subnet_src_traffic))
    print("Outgoing Max: " + str(max_subnet_src_traffic))
    for ip, size in src_subnet_traffic.items():
        if size == max_subnet_src_traffic:
            print("\tSubnet: " + ip)

    print("Incoming Min: " + str(min_subnet_dst_traffic))
    print("Incoming Max: " + str(max_subnet_dst_traffic))
    for ip, size in dst_subnet_traffic.items():
        if size == max_subnet_dst_traffic:
            print("\tSubnet: " + ip)

    print("Mean Outgoing: " + str(statistics.mean(src_subnet_traffic.values())))
    print("Median Outgoing: " + str(statistics.median(src_subnet_traffic.values())))
    print("Variance Outgoing: " + str(statistics.variance(src_subnet_traffic.values())))
    print("Mean Incoming: " + str(statistics.mean(dst_subnet_traffic.values())))
    print("Median Incoming: " + str(statistics.median(dst_subnet_traffic.values())))
    print("Variance Incoming: " + str(statistics.variance(dst_subnet_traffic.values())))


    # Prepare plot

    fig, ax = plt.subplots(1,1)

    n, bins, patches = ax.hist(packets, bins=range(-200, 1600, 50),
                               normed=False, facecolor='green', alpha=0.5)
    plt.xlabel('Packet Size')
    plt.ylabel('Count')
    plt.title('Packet Size')
    plt.disconnect(10)

    ax.set_xticks(range(-200, 1600, 200))
    ax.set_yticks(range(0, 12000, 500))
    ax.grid(True)


    if len(sys.argv) > 2:
        plt.savefig(sys.argv[2])
    bin_counts = {}
    counter = 0
    for pckt in packets:
        start = 1
        counter += 1
        #print(str(counter) + ": " + str(pckt))
        while pckt > (start * 50):
            start += 1
        if ((start - 1) * 50) in bin_counts.keys():
            bin_counts[(start - 1) * 50] += 1
        else:
            bin_counts[((start - 1) * 50)] = 1

# Uncomment to see bin distribution

#    for bin in sorted(bin_counts.keys()):
#        print(str(bin) + " - " + str(bin + 50) + ": " + str(bin_counts[bin]))
    plt.show()
