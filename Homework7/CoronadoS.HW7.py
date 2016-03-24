#!/usr/bin/python2.7

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gs
import matplotlib.ticker as tk

"""
if len(sys.argv) < 4:
    print ("USAGE: Coronado.HWT <Arrival Rate> <Service Rate> <Set Size>\n\n")
    sys.exit(0)

arrival_rate = float(sys.argv[1])
service_rate = float(sys.argv[2])
n = int(sys.argv[3])

if arrival_rate/service_rate > 1:
    print ("ERROR: Arrival rate must be smaller than departure rate \n\n")
"""


def generate_queue_data(arrival_rate, service_rate, n):
    np.random.seed()

    end_time = 0
    elapsed_time = 0
    counter = 0
    service_queue = []
    q_size = 0
    s_size = 0
    n_sys = {}
    last_change = 0
    system_empty = True

    while counter < n:
        counter += 1
        int_arrival_time = np.random.exponential(1/arrival_rate)
        service_time = np.random.exponential(1/service_rate)
        elapsed_time += int_arrival_time

        if elapsed_time < end_time:
            service_queue.append(service_time)
            if s_size in n_sys:
                n_sys[s_size] += elapsed_time - last_change
            else:
                n_sys[s_size] = elapsed_time - last_change
            s_size += 1
            q_size += 1
            last_change = elapsed_time
        elif elapsed_time > end_time:
            while elapsed_time > end_time:
                if q_size > 0:
                    if s_size in n_sys:
                        n_sys[s_size] += end_time - last_change
                    else:
                        n_sys[s_size] = end_time - last_change
                    last_change = end_time
                    s_size -= 1
                    q_size -= 1
                    end_time += service_queue.pop(0)
                else:
                    if system_empty:
                        if s_size in n_sys:
                            n_sys[s_size] += elapsed_time - last_change
                        else:
                            n_sys[s_size] = elapsed_time - last_change
                        s_size += 1
                        system_empty = False
                        last_change = elapsed_time
                    else:
                        if s_size in n_sys:
                            n_sys[s_size] += end_time - last_change
                        else:
                            n_sys[s_size] = end_time - last_change
                        last_change = end_time
                        s_size -= 1
                        system_empty = True
                    end_time = elapsed_time + service_time
        else:
            if q_size > 0:
                service_queue.append(service_time)
                end_time += service_queue.pop(0)
            else:
                end_time += service_time

    if end_time > elapsed_time:
        if s_size in n_sys:
            n_sys[s_size] += end_time - last_change
        else:
            n_sys[s_size] = end_time - last_change
        total_time = end_time
    else:
        if s_size in n_sys:
            n_sys[s_size] += elapsed_time - last_change
        else:
            n_sys[s_size] = elapsed_time - last_change
        total_time = elapsed_time

    mean = 0
    variance = 0

    for d in n_sys.keys():
        n_sys[d] /= total_time
        mean += n_sys[d] * d

    for d in n_sys.keys():
        variance += ((d - mean) ** 2)*n_sys[d]
    return mean, variance

if __name__ == '__main__':
    means = []
    variances = []
    arrival_rates = np.linspace(5, 9.9, 1000)
    utilization = np.linspace(.5, .99, 1000)
    utilization_ticks = np.linspace(.5, .99, 10)
    for d in arrival_rates:
        tmp_mean, tmp_variance = generate_queue_data(d, 10.0, 100000)
        means.append(tmp_mean)
        variances.append(tmp_variance)

    grid = gs.GridSpec(2, 1)
    u = plt.subplot(grid[0, :])
    var = plt.subplot(grid[1, :])

    u.plot(utilization, means, color='green', alpha=.3, linewidth=3)
    u.set_xlabel('Utilization')
    u.set_ylabel('Mean Packets in System')
    u.set_xticks(utilization_ticks)
    u.get_xaxis().set_minor_locator(tk.AutoMinorLocator())
    u.get_yaxis().set_minor_locator(tk.AutoMinorLocator())
    u.grid(True, which='major', linewidth=.5)
    u.grid(True, which='minor', linewidth=.1)

    var.plot(utilization, variances, color='purple', alpha=.5, linewidth=3)
    var.set_xlabel('Utilization')
    var.set_ylabel('Variance of Packets in System')
    var.set_xticks(utilization_ticks)
    var.get_xaxis().set_minor_locator(tk.AutoMinorLocator())
    var.get_yaxis().set_minor_locator(tk.AutoMinorLocator())
    var.grid(True, which='major', linewidth=.5)
    var.grid(True, which='minor', linewidth=.1)
    plt.show()
