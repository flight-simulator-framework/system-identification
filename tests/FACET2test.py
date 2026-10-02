import sys
from pathlib import Path
from runpy import run_path
import numpy as np
from PyQt6.QtWidgets import QApplication
from SysID_GUI import MainWindow, INTERFACE_SETUP
from machine_interfaces.Backend.State import State

setup_path = Path(__file__).resolve().parents[2] / "machine-interfaces/backends/facet2/machine_interfaces_facet2/interface_setup.py"
if setup_path.is_file():
    INTERFACE_SETUP["FACET2"] = run_path(str(setup_path))["INTERFACES"]

app = QApplication(sys.argv)

Interface = type(
    'InterfaceFACET2_Linac',
    (),
    {"__module__": 'machine_interfaces_facet2.InterfaceFACET2_Linac'},
)
interface = Interface()
interface.nsamples = 10
interface.bba_bc11_energy_offset_mev = -3.0
interface.bba_downstream_energy_offset_mev = -40.0
interface.bba_uvwp_offset_deg = -2.5
interface.get_name = lambda: 'FACET2_Linac'
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
