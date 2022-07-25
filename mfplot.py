from qutip import *
import numpy as np
import matplotlib.pyplot as plt
import os

# Time Vector
times = np.linspace(0.0, 10.0, 2001)


def mfplot(results_dir, resonator_fock_num, omega_q, omega_r, g_res, phase_fluc, tau_0, tau_1, isInterval, init_time, fin_time, rho0, idx):

    # Directory checker

    if not os.path.isdir(results_dir):
        os.makedirs(results_dir + "fidelity_plot")
        os.makedirs(results_dir + "measure_plot")
        os.makedirs(results_dir + "fidelity_array")

    # Operators
    # Pauli

    pauli_x = tensor([sigmax(), qeye(resonator_fock_num)])
    pauli_y = tensor([sigmay(), qeye(resonator_fock_num)])
    pauli_z = tensor([sigmaz(), qeye(resonator_fock_num)])

    # Annihilation Operator for Qubit and Resonator

    sm_q = tensor([destroy(2), qeye(resonator_fock_num)])
    a = tensor([qeye(2), destroy(resonator_fock_num)])

    # Number Operators for Qubit and Resonator

    num_q = sm_q.dag() * sm_q
    num_r = a.dag() * a

    def prob_11(t): return (
        tau_0 * np.exp(- (1/tau_0 + 1/tau_1) * t) + tau_1) / (tau_0 + tau_1)

    def prob_00(t): return (
        tau_1 * np.exp(- (1/tau_0 + 1/tau_1) * t) + tau_0) / (tau_0 + tau_1)

    latest_jump = 0
    current_state = 1
    rtn = []

    for i in times:
        prob_no_jump = prob_11 if current_state == 1 else prob_00
        coin_toss = np.random.random()
        if (coin_toss < prob_no_jump(i-latest_jump)):
            rtn.append(current_state)
        else:
            current_state = 0 if current_state == 1 else 1      # Flip the state
            rtn.append(current_state)
            latest_jump = i

    if isInterval:
        new_rtn = []
        for k, i in enumerate(rtn):
            if times[k] < init_time or times[k] > fin_time:
                new_rtn.append(0)
            else:
                new_rtn.append(rtn[k])
        rtn = new_rtn

    def func(t): return (
        g_res * np.exp(phase_fluc * (np.array(rtn)) * 1j * np.pi))

    def noisy_func(t): return func(t)

    noisy_data = noisy_func(times)
    noisy_data_conj = np.conj(noisy_data)

    g = Cubic_Spline(times[0], times[-1], noisy_data)
    g_conj = Cubic_Spline(times[0], times[-1], noisy_data_conj)

    # Hamiltonian

    H_0 = 0.5 * omega_q * pauli_z + omega_r * a.dag() * a
    H_1 = [[sm_q.dag() * a, g], [sm_q * a.dag(), g_conj]]

    H = [H_0] + H_1

    H_const_noise = H_0 + g_res * (sm_q.dag() * a + sm_q * a.dag())
    H_no_noise = H_0

    # MeSolve

    measurement_basis = [num_q, pauli_z, num_r]

    output = mesolve(H, rho0, times, [], measurement_basis)
    output_const_coupling = mesolve(
        H_const_noise, rho0, times, [], measurement_basis)
    output_no_noise = mesolve(H_no_noise, rho0, times, [], measurement_basis)

    densityM_output = mesolve(H, rho0, times, [])
    densityM_const_coupling = mesolve(
        H_const_noise, rho0, times, [])
    densityM_no_noise = mesolve(H_no_noise, rho0, times, [])

    # Fidelity

    fid = []

    min_fid = 100000

    for i, dm in enumerate(densityM_const_coupling.states):
        fid_val = fidelity(
            densityM_const_coupling.states[i], densityM_output.states[i])
        fid.append(fid_val)
        if fid_val < min_fid:
            min_fid = fid_val

    # Expected value of number operators

    fig, ((qubit_measure, pauliZ_measure, resonator_measure), (axes_prob_no_coupling,
                                                               axes_prob_const_coupling, axes_prob_noisy)) = plt.subplots(2, 3, figsize=(25, 10))

    # No Noise

    expected_qubit_no_noise = output_no_noise.expect[0]
    expected_pauliZ_no_noise = output_no_noise.expect[1]
    expected_res_no_noise = output_no_noise.expect[2]

    # Constant Coupling strength

    expected_qubit_const_coupling = output_const_coupling.expect[0]
    expected_pauliZ_const_coupling = output_const_coupling.expect[1]
    expected_res_const_coupling = output_const_coupling.expect[2]

    # Noisy

    expected_qubit = output.expect[0]
    expected_pauliZ = output.expect[1]
    expected_res = output.expect[2]

    # Qubit Measurement

    qubit_measure.set_title("Qubit")
    qubit_measure.plot(times, expected_qubit_no_noise, label="No coupling")
    qubit_measure.plot(times, expected_qubit_const_coupling,
                       label="Constant coupling strength")
    qubit_measure.plot(times, expected_qubit, label="Noisy coupling strength")
    qubit_measure.legend(loc=0)
    qubit_measure.set_xlabel('Time')
    qubit_measure.set_ylabel('Expected Value')

    # Qubit Measurement on sigma_z basis

    pauliZ_measure.set_title("Qubit measured on $\sigma_z$ basis")
    pauliZ_measure.plot(times, expected_pauliZ_no_noise,
                        label="No coupling")
    pauliZ_measure.plot(times, expected_pauliZ_const_coupling,
                        label="Constant coupling strength")
    pauliZ_measure.plot(times, expected_pauliZ,
                        label="Noisy coupling strength")
    pauliZ_measure.legend(loc=0)
    pauliZ_measure.set_xlabel('Time')
    pauliZ_measure.set_ylabel('Expected Value')

    # Resonator Measurement

    resonator_measure.set_title("Resonator")
    resonator_measure.plot(times, expected_res_no_noise, label="No coupling")
    resonator_measure.plot(times, expected_res_const_coupling,
                           label="Constant coupling strength")
    resonator_measure.plot(times, expected_res,
                           label="Noisy coupling strength")
    resonator_measure.legend(loc=0)
    resonator_measure.set_xlabel('Time')
    resonator_measure.set_ylabel('Expected Value')

    # No coupling

    axes_prob_no_coupling.set_title("No coupling Hamiltonian")
    axes_prob_no_coupling.plot(times, expected_res_no_noise, label="Resonator")
    axes_prob_no_coupling.plot(times, expected_pauliZ_no_noise,
                               label="Qubit measured on $\sigma_z$ basis")
    axes_prob_no_coupling.plot(times, expected_qubit_no_noise, label="Qubit")
    axes_prob_no_coupling.legend(loc=0)
    axes_prob_no_coupling.set_xlabel('Time')
    axes_prob_no_coupling.set_ylabel('Expected Value')

    # Constant coupling strength

    axes_prob_const_coupling.set_title(
        "Constant coupling strength Hamiltonian")
    axes_prob_const_coupling.plot(
        times, expected_res_const_coupling, label="Resonator")
    axes_prob_const_coupling.plot(times, expected_pauliZ_const_coupling,
                                  label="Qubit measured on $\sigma_z$ basis")
    axes_prob_const_coupling.plot(
        times, expected_qubit_const_coupling, label="Qubit")
    axes_prob_const_coupling.legend(loc=0)
    axes_prob_const_coupling.set_xlabel('Time')
    axes_prob_const_coupling.set_ylabel('Expected Value')

    # Noisy coupling strength

    axes_prob_noisy.set_title("Noisy coupling strength Hamiltonian")
    axes_prob_noisy.plot(times, expected_res, label="Resonator")
    axes_prob_noisy.plot(times, expected_pauliZ,
                         label="Qubit measured on $\sigma_z$ basis")
    axes_prob_noisy.plot(times, expected_qubit, label="Qubit")
    axes_prob_noisy.legend(loc=0)
    axes_prob_noisy.set_xlabel('Time')
    axes_prob_noisy.set_ylabel('Expected Value')

    plt.tight_layout()
    plt.savefig(results_dir + "measure_plot/" + str(idx) + ".png")
    plt.close()

    # Telegraph Noise

    fig, (axes_noise, axes_fid) = plt.subplots(2, 1, figsize=(10, 10))

    axes_noise.plot(times, np.angle(noisy_data), label="Phase of Noise")
    axes_noise.legend(loc=0)
    axes_noise.set_xlabel('Time')
    axes_noise.set_ylabel('Phase')

    axes_fid.plot(times, fid, label="Fidelity")
    axes_fid.legend(loc=0)
    axes_fid.set_xlabel('Time')
    axes_fid.set_ylabel('Fidelity')

    plt.savefig(results_dir + "fidelity_plot/" + str(idx) + ".png")
    plt.cla()
    plt.close()

    np.savetxt(results_dir + "fidelity_array/" + str(idx) + ".txt", fid)

    return min_fid, fid[-1]
