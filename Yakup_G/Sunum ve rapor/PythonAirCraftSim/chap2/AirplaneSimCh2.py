"""
mavSimPy 
    - Chapter 2 assignment for Beard & McLain, PUP, 2012
    - Update history:  
        1/10/2019 - RWB
"""

import sys
sys.path.append(r'C:\Users\PC_1589\Desktop\PythonAirCraftSim')
import numpy as np
import parameters.simulation_parameters as SIM
import pyqtgraph as pg

from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QGridLayout

# load message types
from message_types.msg_state import msg_state
state = msg_state()  # instantiate state message

#from chap2.mav_viewer import mav_viewer
from chap2.mav_viewer import mav_viewer

from chap11.Qtim import Window


# initialize the mav viewer
#mav_view = mav_viewer()
#mav_view = mav_viewer()

App = QApplication(sys.argv)

# create the instance of our Window
window = Window()

# start the app

phim=0.0
thetam=0.0
psim=0.0
# initialize the simulation time
sim_time = SIM.start_time

# main simulation loop
while sim_time < SIM.end_time:
    #-------vary states to check viewer-------------
    T = 5
    if sim_time < T:
        state.h += 10*SIM.ts_simulation
    elif sim_time < 5*T:
        state.phi -= 0.1*SIM.ts_simulation
        phim = state.phi * 57.29577951;
    elif sim_time < 10*T:
        state.theta += 0.1*SIM.ts_simulation
    else:
        state.psi += 0.1*SIM.ts_simulation
    print("PHİ:",round(state.phi,2),"phimm:",round(phim,2),"YAW:",round(state.psi,2))
    
    
    #-------update viewer-------------
    #mav_view.update(state)
   # window.UiComponents(state)
    window.update(state)
    
    
    #-------increment time-------------
    sim_time += SIM.ts_simulation
    

print("Press Ctrl-Q to exit...")
pg.QtGui.QApplication.instance().exec_()




