import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np

# Time Vector
times = np.linspace(0.0, 10.0, 2001)

datapath = "img/phase0-/fidelity_array/"

trials = 10000

data_arr = []

for tr in range(trials):
    tmp = np.loadtxt(datapath + str(tr) + ".txt")
    data_arr.append(tmp)
    if tr % 1000 == 0:
        print(tr)

fid_at_time = np.transpose(np.array(data_arr))

fig, ax = fig, ax = plt.subplots(figsize=(20, 20))


def pd_t(idx):
    ax.cla()
    weights = np.ones_like(fid_at_time[idx]) / 10000
    ax.hist(fid_at_time[idx*4], weights=weights,
            bins=np.arange(0.2, 1.0 + 0.005, 0.005))
    plt.gca().set(title='Frequency Histogram at time t=' +
                  str(times[idx*4]), ylabel='Frequency')
    ax.set_ylim([0, 0.3])
    ax.set_xlim([0.2, 1.0])
    print(idx*4)


anim = FuncAnimation(fig, pd_t, frames=500,
                     interval=100, repeat=False)

anim.save("pd_hist.gif", savefig_kwargs={'facecolor': 'white'})
