from multiprocessing.dummy import freeze_support
from qutip import *
import numpy as np
from multiprocessing import Pool, cpu_count

from mfplot import mfplot

# Numbers of Fock states
resonator_fock_num = 15
# Frequency
omega_q = 1.0 * 2 * np.pi   # Qubit
omega_r = 1.0 * 2 * np.pi   # Resonator
# Qubit-Resonator Coupling strength
g_res = 0.5 * 2 * np.pi     # Coupling Strength
# Random Telegraph Noise
phase_fluc = 0.55           # The strength of 'random-phase' telegraph
# Prob of RTN being 0,1
tau_0 = 0.9
tau_1 = 0.1
isInterval = True
# Setting initial time
init_time = 0
fin_time = 10
# The initial state
rho0 = tensor([basis(2, 0), basis(resonator_fock_num, 1)])
# Number of Trial
trial = 1000

results_dir = "img/phase" + str(phase_fluc).replace('.', '-') + "/"


def main():

    for i in range(trial):
        parameter = [(results_dir, resonator_fock_num, omega_q, omega_r, g_res, phase_fluc,
                     tau_0, tau_1, isInterval, init_time, fin_time, rho0, i)]
        with Pool(processes=cpu_count()) as pool:
            pool.starmap(mfplot, parameter)

        print(i)


if __name__ == '__main__':
    freeze_support()
    main()
