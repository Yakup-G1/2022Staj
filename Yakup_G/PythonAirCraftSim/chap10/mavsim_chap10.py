"""
mavsim_python
    - Chapter 10 assignment for Beard & McLain, PUP, 2012
    - Last Update:
        3/11/2019 - RWB
"""
import sys
sys.path.append(r'C:\Users\PC_1589\Desktop\PythonAirCraftSim')
import numpy as np
import parameters.simulation_parameters as SIM
RadtoDeg = 57.29577951308232
from chap3.data_viewer import data_viewer
from chap4.wind_simulation import wind_simulation
from chap6LQR.autopilot import autopilot
from chap7.mav_dynamics import mav_dynamics

from chap8.observer import observer
from chap10.path_follower import path_follower
from chap10.path_viewer import path_viewer
from chap11.Mod_anlama_algoritmasi import Mod_Anlayici


from PyQt5.QtWidgets import QApplication
from chap11.Qtim import Window
App = QApplication(sys.argv)
window = Window()

# initialize the visualization
path_view = path_viewer()  # initialize the viewer
data_view = data_viewer()  # initialize view of data plots
VIDEO = False  # True==write video, False==don't write video
if VIDEO == True:
    from chap2.video_writer import video_writer
    video = video_writer(video_name="chap10_video.avi",
                         bounding_box=(0, 0, 1000, 1000),
                         output_rate=SIM.ts_video)

# initialize elements of the architecture
wind = wind_simulation(SIM.ts_simulation)
mav = mav_dynamics(SIM.ts_simulation)
ctrl = autopilot(SIM.ts_simulation)
obsv = observer(SIM.ts_simulation)
path_follow = path_follower()
Mod_Anlama  = Mod_Anlayici()
# path definition
from message_types.msg_path import msg_path
path = msg_path()
# path.flag = 'line'
path.flag = 'orbit'
if path.flag == 'line':
    path.line_origin = np.array([[0.0, 0.0, -100.0]]).T
    path.line_direction = np.array([[1.0, 1.0, 0.0]]).T
    path.line_direction = path.line_direction / np.linalg.norm(path.line_direction)
else:  # path.flag == 'orbit'
    path.orbit_center = np.array([[0.0, 0.0, -150.0]]).T  # center of the orbit
    path.orbit_radius = 300.0  # radius of the orbit
    path.orbit_direction = -1  # orbit direction: 1==clockwise, -1==counter clockwise

# initialize the simulation time
sim_time = SIM.start_time

# main simulation loop
print("Press Command-Q to exit...")
while sim_time < SIM.end_time:

    #-------observer-------------
    measurements = mav.sensors  # get sensor measurements
    estimated_state = obsv.update(measurements)  # estimate states from measurements

    #-------path follower-------------
    autopilot_commands = path_follow.update(path, mav.msg_true_state)  # for debugging
    # autopilot_commands = path_follow.update(path, estimated_state)

    #-------controller-------------
    delta, commanded_state = ctrl.update(autopilot_commands, mav.msg_true_state) # for debugging
    # delta, commanded_state = ctrl.update(autopilot_commands, estimated_state)

    #-------physical system-------------
    current_wind = wind.update()  # get the new wind vector
    # mav.update_state(delta, np.array([[0., 0., 0., 0., 0., 0.]]).T) # for debugging
    mav.update_state(delta, current_wind)  # propagate the MAV dynamics
    mav.update_sensors()
    
    my_heading = mav.msg_true_state.psi*RadtoDeg
    Roll       = mav.msg_true_state.phi*RadtoDeg
    Pitch      = mav.msg_true_state.theta*RadtoDeg
    
   # Mod_Anlama.Update_Mod(my_heading,mav.msg_true_state.Vg,mav.msg_true_state.h,Roll,Pitch,my_heading) #mav.msg_true_state.Vg=groundspeed
    
    window.update(mav.msg_true_state)
    
    #print(mav._t_gps,"--",mav._gps_eta_n)
    #-------update viewer-------------
    path_view.update(path, mav.msg_true_state)  # plot path and MAV
    data_view.update(mav.msg_true_state, # true states
                     estimated_state, # estimated states
                     commanded_state, # commanded states
                     SIM.ts_simulation)
    if VIDEO == True: video.update(sim_time)
    
    #-------increment time-------------
    sim_time += SIM.ts_simulation

if VIDEO == True: video.close()




