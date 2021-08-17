# Photoinduced Charge Transfer using DFTB+ and Libra
We simulate charge transfer from 2H2PC to C60. The electronic structure calculations have been done using DFTB+ package and the dynamics (FSSH and Markov) have been implemented using Libra.

The steps involved are as follows :

1. Calculation of  Orbital Overlaps : We caclulate the orbital overlaps between the constituent molecules and the system to determine the MOs of interest. We use the eigenvector data which was obtained
using DFTB+.

2. Calculation of time-dependent eigenspectrum : We determine the possible transitions that can take place over the course of the MD trajectory. This information is used for choosing the initial state of the system.

3. Trajectory Sampling : Multiple trajectories are sampled from the initial MD trajectory. All MD calculation have been done using DFTB+.

4. Calculation of Hvib files : The vibronic hamiltonian matrices are generated for each time step using Libra libraries. 

5. NAMD : The non-adiabatic molecular dynamics are executed using Libra. 
