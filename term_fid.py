import matplotlib.pyplot as plt
import numpy as np

# Time Vector
times = np.linspace(0.0, 10.0, 2001)

# Phase Fluctuation
phase = 0.55

datapath = "img/phase" + str(phase).replace('.', '-') + "/fidelity_array/"

# Number of trial
trials = 1000

term_fid = [0 for i in range(2001)]
min_fid = [100000 for i in range(2001)]

# Load the data of all trials and find average fidelity and minimum fidelity

for tr in range(trials):
    tmp = np.loadtxt(datapath + str(tr) + ".txt")
    print(tr)
    for i in range(2001):
        term_fid[i] = term_fid[i] + tmp[i]
        min_fid[i] = min_fid[i] if min_fid[i] < tmp[i] else tmp[i]

term_fid_np = np.array([t / trials for t in term_fid])
min_fid_np = np.array(min_fid)

# Plot the graph

fig, (term_fid_axes, min_fid_axes) = plt.subplots(2, 1, figsize=(10, 10))

term_fid_axes.plot(
    times, term_fid_np, label="Average Terminal fidelity at time $t$")
term_fid_axes.legend(loc=0)
term_fid_axes.set_xlabel('Time')
term_fid_axes.set_ylabel('Fidelity')

min_fid_axes.plot(times, min_fid_np, label="Minimum fidelity at time $t$")
min_fid_axes.legend(loc=0)
min_fid_axes.set_xlabel('Time')
min_fid_axes.set_ylabel('Fidelity')

plt.savefig("fidelity_result" + str(phase).replace('.', '-') + ".png")
plt.cla()
