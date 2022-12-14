"""
mavsim_python
    - Chapter 11 assignment for Beard & McLain, PUP, 2012
    - Last Update:
        3/26/2019 - RWB
"""

import sys
sys.path.append(r'C:\Users\PC_1589\Desktop\PythonAirCraftSim')


import numpy as np
import parameters.simulation_parameters as SIM
import parameters.planner_parameters as PLAN

from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QGridLayout

RadtoDeg = 57.29577951308232

from message_types.msg_sensors import msg_sensors
from message_types.msg_state import msg_state

from chap3.data_viewer import data_viewer
from chap4.wind_simulation import wind_simulation
from chap6LQR.autopilot import autopilot
from chap7.mav_dynamics import mav_dynamics
from chap8.observer import observer
from chap10.path_follower import path_follower
from chap11.path_manager import path_manager
from chap11.waypoint_viewer import waypoint_viewer
from chap11.Mod_anlama_algoritmasi import Mod_Anlayici

# initialize the visualization
waypoint_view = waypoint_viewer()  # initialize the viewer

App = QApplication(sys.argv)

from chap11.Qtim import Window

window = Window()

#data_view = data_viewer()  # initialize view of data plots
VIDEO = False  # True==write video, False==don't write video
if VIDEO == True:
    from chap2.video_writer import video_writer
    video = video_writer(video_name="chap11_video.avi",
                         bounding_box=(0, 0, 1000, 1000),
                         output_rate=SIM.ts_video)

# initialize elements of the architecture
wind = wind_simulation(SIM.ts_simulation)
mav = mav_dynamics(SIM.ts_simulation)
ctrl = autopilot(SIM.ts_simulation)
obsv = observer(SIM.ts_simulation)
path_follow = path_follower()
path_manage = path_manager()

Mod_Anlama  = Mod_Anlayici()
# waypoint definition
from message_types.msg_waypoints import msg_waypoints
waypoints = msg_waypoints()
# waypoints.type = 'straight_line'
# waypoints.type = 'fillet'
waypoints.type = 'dubins'
waypoints.num_waypoints = 8
Va = PLAN.Va0
waypoints.ned[:, 0:waypoints.num_waypoints] \
    = np.array([[0, 0, -100],
                [1000, 0, -100],
                [0, 1000, -100],
                [1000, 1000, -100],
                [0, 0, -100],
                [1000, 0, -100],
                [0, 1000, -100],
                [1000, 1000, -100]]).T
waypoints.airspeed[:, 0:waypoints.num_waypoints] \
    = np.array([[Va, Va, Va, Va, Va, Va, Va, Va]])
waypoints.course[:, 0:waypoints.num_waypoints] \
    = np.array([[np.radians(0),
                 np.radians(45),
                 np.radians(45),
                 np.radians(-135),
                 np.radians(0),
                 np.radians(45),
                 np.radians(45),
                 np.radians(-135)
                 ]])

# initialize the simulation time
sim_time = SIM.start_time
old_heading=0
# main simulation loop
print("Press Command-Q to exit...")
while sim_time < SIM.end_time:
    #-------observer-------------
    measurements = mav.sensors  # get sensor measurements
    estimated_state = obsv.update(measurements)  # estimate states from measurements

    my_heading = mav.msg_true_state.psi*RadtoDeg
    Roll       = mav.msg_true_state.phi*RadtoDeg
    Pitch      = mav.msg_true_state.theta*RadtoDeg
    
    #Mod_Anlama.Update_Mod(my_heading,mav.msg_true_state.Vg,mav.msg_true_state.h,Roll,Pitch,my_heading) #mav.msg_true_state.Vg=groundspeed
    window.update(mav.msg_true_state)

    #-------path manager-------------
    path = path_manage.update(waypoints, PLAN.R_min, estimated_state)

    #-------path follower-------------
    autopilot_commands = path_follow.update(path, estimated_state)

    #-------controller-------------
    delta, commanded_state = ctrl.update(autopilot_commands, estimated_state)

    #-------physical system-------------
    current_wind = wind.update()  # get the new wind vector
    mav.update_state(delta, current_wind)  # propagate the MAV dynamics
    mav.update_sensors()
    
    #-------update viewer-------------
    waypoint_view.update(waypoints, path, mav.msg_true_state)  # plot path and MAV
   #data_view.update(mav.msg_true_state, # true states
                    # estimated_state, # estimated states
                   #  commanded_state, # commanded states
                    # SIM.ts_simulation)
    if VIDEO == True: video.update(sim_time)

    
    #-------increment time-------------
    sim_time += SIM.ts_simulation

if VIDEO == True: video.close()





