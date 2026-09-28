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


```bash
git clone https://gitlab.cern.ch/flight-simulator/machine-interfaces.git
git clone https://gitlab.cern.ch/flight-simulator/system-identification.git
cd system-identification
poetry update rf-track --lock
poetry install --extras clear
poetry run python SysID_GUI.py
```

Keep these repositories in the same parent directory; Poetry uses their local editable packages. The selected extra installs only that machine adapter and its dependencies. Available machine extras: `clear`, `atf2`, `facet2`, `esrf`; combine them with `--extras "clear atf2"` when needed.

For quadrupole-mover measurements:

```bash
poetry run python SysID_QM_GUI.py
```
