import sys
from pathlib import Path
from runpy import run_path
import numpy as np
from PyQt6.QtWidgets import QApplication
from SysID_GUI import MainWindow, INTERFACE_SETUP
from machine_interfaces.Backend.State import State

setup_path = Path(__file__).resolve().parents[2] / "machine-interfaces/backends/atf2/machine_interfaces_atf2/interface_setup.py"
if setup_path.is_file():
    INTERFACE_SETUP["ATF2"] = run_path(str(setup_path))["INTERFACES"]

app = QApplication(sys.argv)

Interface = type(
    'InterfaceATF2_Ext',
    (),
    {"__module__": 'machine_interfaces_atf2.InterfaceATF2_Ext'},
)
interface = Interface()
interface.nsamples = 3
interface.energy_frequency_offset_khz = 4.0
interface.nominal_laser_intensity = 0.1
interface.test_laser_intensity = 0.125
interface.get_name = lambda: 'ATF2_Ext'
interface.corrs = ["H", "V"]
interface.bpms = ["BPM1", "BPM2"]
interface.get_bpms = lambda: {"names": interface.bpms}
interface.get_sequence = lambda: ["H", "V", "BPM1", "BPM2"]
interface.get_state = lambda: State(
    correctors=interface.get_correctors(),
    bpms={"names": interface.bpms, "x": np.zeros((1, 2)), "y": np.zeros((1, 2)), "tmit": np.ones((1, 2))},
    sequence=interface.get_sequence(),
    hcorrectors_names=["H"],
    vcorrectors_names=["V"],
)
interface.get_hcorrectors_names = lambda: ["H"]
interface.get_vcorrectors_names = lambda: ["V"]
interface.get_correctors = lambda: {
    "names": ["H", "V"],
    "bdes": np.array([1.0, 1.0]),
}

window = MainWindow(interface, "")
window.show()
sys.exit(app.exec())
