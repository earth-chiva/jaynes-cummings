---
marp: true
math: true
class: invert
header: 'Bachelor Thesis Presentation'
style: |
    section {
        justify-content: flex-start;
    }
---

<style>
    img[alt~="center"] {
        display: block;
        margin: 0 auto;
        background-color: white;
    }
    h2 {
        color: #f93;
    }
</style>

<style scoped>
    section {
        justify-content: center;
    }
</style>

# Numerical Analysis on Jaynes-Cummings Model of a qubit coupled with 1-mode photon subjected to two-state random telegraph noise

### Advisor: Prof. Hirokawa Masao, Dr. Hidaka Takeru

### Parakorn Leknamongkol

##### Department of Electrical Engineering and Computer Science, Kysuhu University

---

# Outline

- Background
    - Jaynes-Cummings Model
    - Random Telegraph Noise
    - Lindblad Master Equation
- Method
    - Operator
    - Measurement and Fidelity
    - QuTiP
- Result

---

<style scoped>
    section {
        justify-content: center;
        align-items: center;
    }
</style>

# Background

---

# Jaynes-Cummings Model

-   Theoretical model describing interaction between field (resonator) and atom (qubit)

## Define state space

-   The eigenstate of the system: $\ket{q,n} = \ket{q} \otimes \ket{n}$.

    -   The **qubit** has fermionic state $\ket{q}$ in complex Euclidean space $\mathbb{C}^2$.
    -   The **resonator** has bosonic Fock state $\ket{n}$ in sequence spaces $l^2(\mathbb{N})$,
        where $n$ is the number of photons in the field

        and $l^2(\mathbb{N}) = \{(c_k)_{n=1}^\infty \in \mathbb{C}^\mathbb{N} | \sum_{k=1}^\infty |c_k|^2 < \infty\}$.

---

## Hamiltonian

Let $\omega_q, \omega_r$ be the frequency of the qubit and resonator.

-   The qubit Hamiltonian is given by

$$H_q = \frac{1}{2}\hbar \omega_q\sigma_z$$

where $\sigma_z$ is the Pauli Z matrix.

-   The resonator Hamiltonian is given by

$$H_r = \hbar \omega_r a^{\dagger} a$$

where $a, a^{\dagger}$ are the annihilation and creation operator of the resonator.

---

## Interaction Hamiltonian

-   In the rotating-wave approximation model, the **interaction Hamiltonian** is defined by,

$$H_I = g\sigma_+ a + g^* \sigma_- a^{\dagger}$$

where $g$ is coupling strength between atom and field.

-   The full Hamiltonian acting on the whole state space is

$$ H = \frac{1}{2} \hbar\omega_q (\sigma_z \otimes \mathbb{1}_r) + \hbar\omega_r (\mathbb{1}_q \otimes a^\dagger a) + (g(t)\sigma_+ \otimes a + g^* (t) \sigma_- \otimes a^\dagger)$$

where $1_q, 1_r$ is the identity operators for qubit and resonator space.

---

# Random Telegraph Noise

-  Frequently known as burst noise
-  Occur when MOSFET drain current makes a discrete jump as a function of time.
-  Random-phase telegraph in coupling strength term is defined by

$$g(t) = g_0 e^{-\phi(t)}$$

where $g_0$ is the amplitude of the coupling strength and phase $\phi(t)$ is a fluctuation by jump defined by $\phi(t) = \pi \phi_0 \mathrm{RTN}(t)$. The value of $\phi_0$ is called phase fluctuation, and $\mathrm{RTN}(t)$ is the telegraph noise generated at time $t$.

---

## Mathematical description of $\mathrm{RTN}(t)$

Let $\tau_0, \tau_1$ be the mean lifetimes of the state $0$ and $1$ respectively.

- The probability of the state being $0$ is $\frac{\tau_0}{\tau_0 + \tau_1}.$ 
- The probability of the state being $1$ is $\frac{\tau_1}{\tau_0 + \tau_1}.$

The probability of staying at $1$ after being in state $0$ for time $dt$ is $P_{11}$ defined by

$$ P_{11} (dt) = \frac{1}{\tau_0+\tau_1}\left(\tau_1 e^{-\left(\frac{1}{\tau_0} + \frac{1}{\tau_1}\right) dt}  + \tau_0 \right).$$
The probability of staying at $0$ after being in state $1$ for time $dt$ is $P_{00}$ defined by
$$P_{00} (dt) = \frac{1}{\tau_0+\tau_1}\left(\tau_0 e^{-\left(\frac{1}{\tau_0} + \frac{1}{\tau_1}\right) dt}  + \tau_1 \right).$$

---

# Lindblad master equation

The time evolution of the density operator $\rho$ is described using __Lindblad master equation__ given by

$$\dot{\rho}(t) = -\frac{i}{\hbar} [H(t), \rho(t)] + \sum_n \left[C_n\rho(t)C_n^{\dagger} - \rho(t) C_n^{\dagger}C_n - C_n^{\dagger} C_n\rho(t) \right]$$

where $C_n$ are collapse operators.

- Here, the collapse operators are neglected. Therefore, the evolution is the __Heisenberg equation__.

$$\dot{\rho}(t) = -\frac{i}{\hbar} [H(t), \rho(t)]$$

---

<style scoped>
    section {
        justify-content: center;
        align-items: center;
    }
</style>

# Method

---

# Opearator

## Hamiltonian and the time evolution

- Comparing three Hamiltonians  on the effect of the telegraph noise on the evolution:
    - Free Hamiltonian
    $$ H_0 = \frac{1}{2} \Omega_q \sigma_z + \Omega_r a^{\dagger} a$$
    - Hamiltonian with constant coupling strength
    $$H_{const} = H_0 + g(\sigma_+ a + \sigma_- a^{\dagger})$$
    - Hamiltonian with telegraph noise
    $$H = H_0 + (g(t)\sigma_+ a + g^* (t) \sigma_- a^\dagger)$$

---

## Obtaining the Liouvillian superoperators

- The time evolution of the density matrix is given by

$$\dot{\rho}(t) = -\frac{i}{\hbar}[H(t), \rho(t)].$$

- By vectorizing the density operator $\mathrm{vec}(\rho) = ||\rho\rangle$ , we obtain the Liouvillian superoperator $\tilde{\mathcal{L}}$ from

$$ \frac{d}{dt} ||\rho \rangle = \tilde{\mathcal{L}}||\rho\rangle.$$

- It is important to note that Liouville operator only __depends on phase fluctuation $\phi_0$__.

---

## Transformation to other channel representation

- Choi matrix is the bipartite column reshuffling of the Liouvillian operators.

- The spectral decomposition of Choi matrix creates the Kruas operator. (The Kraus operator is not unique.)


![width:600px center](representation_diagram.gif)

---

# Measurement and fidelity

- The initial state $\rho_0$ is set to $|g,1\rangle$. The density operator evolves using master equation.

- Three measurement basis are qubit number operator $\sigma_+ \sigma_-$, Pauli Z $\sigma_z$, and resonator number operator $a^{\dagger}a$ is plotted w.r.t. time.

- The fidelity of the density operator is compared between constant coupling strength and telegraph noise w.r.t. time at each phase fluctuation.

---

# QuTiP

![center](qutip.png)

- The open-source software for simulating the dynamics of open quantum systems in python
- Equipped with basic operators, representation transformation, master equation solver, and fidelity function
- To simulate infinite bosonic Fock space, we use 15 number of Fock states.

---


## Numerical analysis

- To obtain the operators, the Hamiltonians of each case are transformed using QuTiP.
- To obtain the measurement, the function `mesolve()` is used.
- By generating 1000 trials of random noise for each phase fluctuation $\phi_0 = 0.05, 0.10, 0.15, ..., 0.55$, we can find the average fidelity and the minimum fidelity at time $t$.
- By generating 10000 trials of random noise for phase fluctuation $\phi_0 = 0.25$, we can find the distribution of the fidelity when the system subjected to $t$ seconds of noise.

---

<style scoped>
    section {
        justify-content: center;
        align-items: center;
    }
</style>


# Result

---

# Hamiltonian

- The free Hamiltonian is given by

$$H_0 = \left[\begin{array}{cc}
    \Omega_r a^{\dagger} a + \frac{1}{2} \Omega_q& 0 \\
    0 & \Omega_r a^\dagger a - \frac{1}{2} \Omega_q
\end{array}\right].$$

- The constant coupling strength Hamiltonian is

$$H_{const} = \left[\begin{array}{cc}
    \Omega_r a^{\dagger} a + \frac{1}{2} \Omega_q& g_0a^\dagger \\
    g_0a & \Omega_r a^\dagger a - \frac{1}{2} \Omega_q
\end{array}\right].$$

- For the coupling strength with telegraph noise, the Hamiltonian at state $1$ is given by

$$H_{1} = \left[\begin{array}{cc}
    \Omega_r a^{\dagger} a + \frac{1}{2} \Omega_q& g_0e^{i\pi\phi_0}a^\dagger \\
    g_0e^{-i\pi\phi_0} a & \Omega_r a^\dagger a - \frac{1}{2} \Omega_q
\end{array}\right].$$

---

# Liouvillian Operator

## Free Hamiltonian

![width:900px center](liouville_no_coupling.png)

---

## Constant coupling Hamiltonian

![width:900px center](liouville_const_coupling.png)

---

## Liouvillian operator at each phase fluctuation $\phi_0$

![center](phase_fluc_liouvillian.gif)

---

# Kraus Operator

- Since the Choi rank is $2$, there are $2$ Kraus operators in each case.

---

## No coupling strength

![width:500px center](no_coupling_kraus1.png)

![width:500px center](no_coupling_kraus2.png)

---

## Constant coupling strength

![width:500px center](const_coupling_kraus1.png)

![width:500px center](const_coupling_kraus2.png)

---

## Coupling strength with phase fluctuation

![width:500px center](comp_coupling_kraus1.png)

![width:500px center](comp_coupling_kraus2.png)

---

# The Effect of noise on the measurement

![width:1200px center](measure_plot.png)

---

# The Effect of noise on the fidelity

![width:500px center](fidelity_plot.png)

---

# Observing the coupling strength with phase fluctuation

- Deploying rectangular pulse wave phase fluctuation with a period of 1 second.

![width:700px center](interval_noise.png)

---

## The measurement on rectangular pulse wave phase fluctuation

![width:1200px center](measure_interval_noise.png)

---

## The fidelity on rectangular pulse wave phase fluctuation

![width:900px center](interval_noise_fid.png)

---

# Average fidelity and minimum fidelity at time $t$

- Phase Fluctuation $\phi_0 = 0.25$

![center width:450px](fidelity_result0-25.png)

---

- Phase Fluctuation $\phi_0 = 0.50$

![center width:450px](fidelity_result0-5.png)

---

# The probabilty density function of the fidelity

- The PDF is given by $f(x) = \left\{
\begin{array}{ll}
    \frac{1}{\alpha}e^{\frac{x-1}{\alpha}} & 0\leq x \leq 1 \\
    0 & \mathrm{otherwise}
\end{array}\right. .$

![width:430px center](fid_Hist_pdf.gif)