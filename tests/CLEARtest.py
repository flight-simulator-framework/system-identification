import ast
import os
import sys
from datetime import datetime
from pathlib import Path
from runpy import run_path
import numpy as np
from PyQt6.QtWidgets import QApplication

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

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
interface_path = Path(__file__).resolve().parents[2] / "machine-interfaces/backends/clear/machine_interfaces_clear/InterfaceCLEAR.py"
name_lists = {}
for node in ast.walk(ast.parse(interface_path.read_text())):
    if isinstance(node, ast.Assign) and isinstance(node.value, ast.List) and isinstance(node.targets[0], ast.Name) and node.targets[0].id in ("sequence", "monitors", "correctors"):
        name_lists[node.targets[0].id] = ast.literal_eval(node.value)
sequence = [name for name in name_lists["sequence"] if name in name_lists["monitors"] or name in name_lists["correctors"]]
corrs = [name for name in sequence if name in name_lists["correctors"]]
bpms = [name for name in sequence if name in name_lists["monitors"]]
hcorrs = [name for name in corrs if ("DHG" in name) or ("DHJ" in name)]
vcorrs = [name for name in corrs if ("DVG" in name) or ("DVJ" in name) or ("SDV" in name)]

interface.get_name = lambda: "CLEAR"
interface.corrs = corrs
interface.bpms = bpms
interface.get_bpms = lambda: {"names": interface.bpms}
interface.get_sequence = lambda: sequence
interface.get_state = lambda: State(
    correctors=interface.get_correctors(),
    bpms={"names": interface.bpms, "x": np.zeros((1, len(bpms))), "y": np.zeros((1, len(bpms))), "tmit": np.ones((1, len(bpms)))},
    sequence=interface.get_sequence(),
    hcorrectors_names=hcorrs,
    vcorrectors_names=vcorrs,
)
interface.get_hcorrectors_names = lambda: hcorrs
interface.get_vcorrectors_names = lambda: vcorrs
interface.get_correctors = lambda: {
    "names": corrs,
    "bdes": np.array([4.0 if name in hcorrs else 4.06567 for name in corrs]),
}

dir_name = os.path.expanduser(f"~/CERN-Flight_Simulator-Data/CLEAR_{datetime.now().strftime('%Y%m%d_%H%M%S')}")
window = MainWindow(interface, dir_name)
window.show()
sys.exit(app.exec())
