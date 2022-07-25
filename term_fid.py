import matplotlib.pyplot as plt
import numpy as np

# Time Vector
times = np.linspace(0.0, 10.0, 2001)

datapath = "img/fidelity_array/"

trials = 10000

term_fid = [0 for i in range(2001)]
min_fid = [100000 for i in range(2001)]

for tr in range(trials):
    tmp = np.loadtxt(datapath + str(tr) + ".txt")
    print(tr)
    for i in range(2001):
        term_fid[i] = term_fid[i] + tmp[i]
        min_fid[i] = min_fid[i] if min_fid[i] < tmp[i] else tmp[i]
        # if tr == 0:
        #     print(tr, i, tmp[i], term_fid[i], min_fid[i])

term_fid_np = np.array([t / trials for t in term_fid])
min_fid_np = np.array(min_fid)

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

plt.savefig("fidelity_result.png")
plt.cla()

plt.hist(term_fid, bins=12)
plt.gca().set(title='Frequency Histogram', ylabel='Frequency')

plt.savefig("dist_term.png")
