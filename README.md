# System Identification

Machine excitation and data acquisition for corrector and quadrupole-mover system identification.

For correctors, the application applies positive and negative kicks relative to their initial settings, records the beam response, and restores the initial settings after each pair of measurements. The acquired data can be used to calculate a response matrix.

## Usage

Select the correctors to excite and the BPMs to include in the measurements.

In the GUI, configure:
- Initial horizontal and vertical kick amplitudes.
- Optional beam energy and intensity changes.
- Maximum corrector strengths.
- Target horizontal and vertical orbit excursions.

During successive SysID cycles, the application adjusts the kick amplitudes to approach the target orbit excursion while respecting the configured corrector limits.

## Installation

From the repository directory, install the dependencies:

```bash
poetry install
```