import sys
from pathlib import Path
from runpy import run_path
import numpy as np
from PyQt6.QtWidgets import QApplication
from SysID_GUI import MainWindow, INTERFACE_SETUP
from machine_interfaces.Backend.State import State

setup_path = Path(__file__).resolve().parents[2] / "machine-interfaces/backends/clear/machine_interfaces_clear/interface_setup.py"
if setup_path.is_file():
    INTERFACE_SETUP["CLEAR"] = run_path(str(setup_path))["INTERFACES"]

app = QApplication(sys.argv)

Interface = type(
    "CLEAR_real_machine",
    (),
    {"__module__": "machine_interfaces_clear.InterfaceCLEAR"},
)
interface = Interface()
interface.nsamples = 3
interface.rf_phase_nominal = 128.0
interface.rf_phase_test = 108.0
interface.uvatt2_test_steps = 1000.0
interface.quadrupole_scaling_factor = 0.5
interface.get_name = lambda: "CLEAR"
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
