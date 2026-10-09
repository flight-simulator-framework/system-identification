# System Identification

Machine excitation and data acquisition for corrector and quadrupole-mover system identification.

For correctors, the application applies positive and negative kicks relative to their initial settings, records the beam response, and restores the initial settings after each pair of measurements. The acquired data can be used to calculate a response matrix.

## Usage

Select the machine or simulation interface, the correctors to excite and the BPMs to include in the measurements.

In the GUI, configure:

- Initial horizontal and vertical kick amplitudes.
- Optional beam energy and intensity changes.
- Maximum corrector strengths.
- Target horizontal and vertical orbit excursions.
- Number of iterations and output directory.

During successive SysID cycles, the application adjusts the kick amplitudes to approach the target orbit excursion while respecting the configured corrector limits. The amplitudes can increase or decrease depending on the measured response.

Monitor the response plots during acquisition. Paired positive/negative measurements are saved as `DATA*.pkl` snapshots for offline reconstruction in Response Matrix.

## GUI variants

- `SysID_GUI.py`: excitation using corrector magnets.
- `SysID_QM_GUI.py`: excitation using horizontal and vertical quadrupole-mover displacements, with configurable displacement ranges and target orbit excursions.

The separate `random_excitation/SysID_rnd.py` script provides an experimental random-excitation version of the application.

## Installation and startup

On a control-room computer, install the applications with the deployment script of your machine: [CLEAR](https://gitlab.cern.ch/flight-simulator/machine-interfaces/-/blob/master/backends/clear/clear_deploy.md), [ATF2](https://gitlab.cern.ch/flight-simulator/machine-interfaces/-/blob/master/backends/atf2/atf2_deploy.md), [ESRF](https://gitlab.cern.ch/flight-simulator/machine-interfaces/-/blob/master/backends/esrf/esrf_deploy.md) or [FACET2](https://gitlab.cern.ch/flight-simulator/machine-interfaces/-/blob/master/backends/facet2/facet2_deploy.md). It creates a shared virtual environment and one launcher per GUI, e.g. `./SysID_GUI.sh`.

For a local installation, use Python 3.11 or newer and keep the repositories in one directory:

```bash
git clone https://gitlab.cern.ch/flight-simulator/machine-interfaces.git
git clone https://gitlab.cern.ch/flight-simulator/system-identification.git
python3 -m venv venv
source venv/bin/activate
pip install -e machine-interfaces -e machine-interfaces/backends/esrf -e system-identification
cd system-identification
python SysID_GUI.py
```

Replace `esrf` with `atf2` or `facet2` for another machine. The CLEAR control-system packages are available only from the CERN Acc-Py index; elsewhere, install only the CLEAR simulation:

```bash
pip install rf-track cpymad
pip install --no-deps -e machine-interfaces/backends/clear
```

Editable installs pick up `git pull` changes without reinstalling.

For quadrupole-mover measurements, run `python SysID_QM_GUI.py`. For the real ESRF machine, set `TANGO_HOST` before starting the GUI.
