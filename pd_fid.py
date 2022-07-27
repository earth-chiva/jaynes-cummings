import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np

import scipy
from scipy import stats

# Time Vector
times = np.linspace(0.0, 10.0, 2001)

# ---------- Data Loader Part

# datapath = "img/fidelity_array/"

# trials = 10000

# data_arr = []

# for tr in range(trials):
#     tmp = np.loadtxt(datapath + str(tr) + ".txt")
#     data_arr.append(tmp)
#     if tr % 1000 == 0:
#         print(tr)

# np.savetxt("fid_at_time.txt")

# ---------- Load data and prepare figure

fid_at_time = np.loadtxt("fid_at_time.txt")

fig, ax = plt.subplots(figsize=(20, 20))


def pm_hist(idx):
    weights = np.ones_like(fid_at_time[idx]) / 10000
    ax.hist(fid_at_time[idx], weights=weights,
            bins=np.arange(0, 1.0 + 0.005, 0.005))
    plt.gca().set(
        title=f'Frequency Histogram at time t={times[idx]}', ylabel='Frequency')
    ax.set_ylim([0, 0.4])


def graphFitter(idx):
    fid_flip = np.ones_like(fid_at_time[idx]) - fid_at_time[idx]
    weights = np.ones_like(fid_flip) / 10000
    _, bins, _ = plt.hist(fid_flip, bins=np.arange(
        0, 1.0 + 0.005, 0.005), weights=weights, alpha=0.5)
    ax.cla()
    loc, scale = scipy.stats.expon.fit(fid_flip)

    return loc, scale


def pdf(loc, scale, resize=False):

    bins = np.arange(0, 1.0 + 0.005, 0.005)

    def pd_curve(x):
        if resize:
            return 0.005 * (1 / scale) * np.exp((x + loc - 1) / scale)
        else:
            return (1 / scale) * np.exp((x + loc - 1) / scale)

    plt.plot(bins, pd_curve(bins))

    plt.suptitle(
        f"Probability Distrubition Function: $y = \\frac{{1}}{{{scale:.3f}}} e^{{ \\frac{{x - {(1-loc):.3f}}}{{{scale:.3f}}} }}$")

    if resize:
        ax.set_ylim([0, 0.4])
    else:
        ax.set_ylim([0, 80])

# --- Setting of the graph / animation


with_hist = False
resize = False


# ---------- Fidelity Distribution


def fidelity_distribution(frame_no):

    print(f"Frame number: {frame_no}")

    loc, scale = graphFitter(frame_no)
    if with_hist:
        pm_hist(frame_no)

    pdf(loc, scale, resize=resize)

    if not resize:
        plt.gca().set(
            title=f'Probability density curve at time t={times[frame_no]}')
    else:
        plt.gca().set(
            title=f'Probability density curve (scaled to fit histogram) at time t={times[frame_no]}')


# ---------- Histogram Animation


# anim = FuncAnimation(fig, pm_hist, frames=2000,
#                      interval=25, repeat=False)
# anim.save("fid_pdf.gif", savefig_kwargs={'facecolor': 'white'})


# ---------- PDF with Histogram Animation


anim = FuncAnimation(fig, fidelity_distribution, frames=range(4, 2000, 4),
                     interval=25, repeat=False)
anim.save("fid_pdf.gif", savefig_kwargs={'facecolor': 'white'})


# ---------- Plot and Save/Show


# t = 7.5         # Time 0 <= t <= 10
# fidelity_distribution(int(t * 200))

# plt.savefig(f"fid_dist_t={t}.png")

# plt.show()
