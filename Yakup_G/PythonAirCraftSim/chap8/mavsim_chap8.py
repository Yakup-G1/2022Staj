"""
mavsim_python
    - Chapter 8 assignment for Beard & McLain, PUP, 2012
    - Last Update:
        2/21/2019 - RWB
"""
import sys
sys.path.append(r'C:\Users\PC_1589\Desktop\pyton_deneme')
import numpy as np
import parameters.simulation_parameters as SIM
RadtoDeg = 57.29577951308232
from chap2.mav_viewer import mav_viewer
from chap3.data_viewer import data_viewer
from chap4.wind_simulation import wind_simulation
from chap6LQR.autopilot import autopilot
from chap7.mav_dynamics import mav_dynamics
from chap8.observer import observer
from tools.signals import signals
from chap11.Mod_anlama_algoritmasi import Mod_Anlayici

# initialize the visualization
mav_view = mav_viewer()  # initialize the mav viewer
data_view = data_viewer()  # initialize view of data plots
VIDEO = False  # True==write video, False==don't write video
if VIDEO == True:
    from chap2.video_writer import video_writer
    video = video_writer(video_name="chap8_video.avi",
                         bounding_box=(0, 0, 1000, 1000),
                         output_rate=SIM.ts_video)

# initialize elements of the architecture
wind = wind_simulation(SIM.ts_simulation)
mav = mav_dynamics(SIM.ts_simulation)
ctrl = autopilot(SIM.ts_simulation)
obsv = observer(SIM.ts_simulation)
Mod_Anlama  = Mod_Anlayici()
# autopilot commands
from message_types.msg_autopilot import msg_autopilot
commands = msg_autopilot()
Va_command = signals(dc_offset=25.0, amplitude=0.10, start_time=2.0, frequency = 0.01)
h_command = signals(dc_offset=100.0, amplitude=0.10, start_time=0.0, frequency = 0.02)
chi_command = signals(dc_offset=np.radians(0), amplitude=np.radians(45), start_time=5.0, frequency = 0.015)

# initialize the simulation time
sim_time = SIM.start_time

# main simulation loop
print("Press Command-Q to exit...")

from message_types.msg_state import msg_state
temp = msg_state()

while sim_time < SIM.end_time:

    #-------autopilot commands-------------
    commands.airspeed_command = Va_command.square(sim_time)
    commands.course_command = chi_command.square(sim_time)
    commands.altitude_command = h_command.square(sim_time)

    #-------controller-------------
    measurements = mav.sensors  # get sensor measurements
    estimated_state = obsv.update(measurements)  # estimate states from measurements

    temp = mav.msg_true_state
    temp.p = estimated_state.p
    temp.q = estimated_state.q
    temp.r = estimated_state.r
    temp.h = estimated_state.h
    temp.Va = estimated_state.Va
    temp.phi = estimated_state.phi
    temp.theta = estimated_state.theta
    temp.pn = estimated_state.pn
    temp.pe = estimated_state.pe
    temp.Vg = estimated_state.Vg
    temp.chi = estimated_state.chi
    temp.wn = estimated_state.wn
    temp.we = estimated_state.we
    temp.psi = estimated_state.psi

    # if sim_time < 10:
    # delta, commanded_state = ctrl.update(commands, mav.msg_true_state)
    # # delta, commanded_state = ctrl.update(commands, estimated_state)
    # else:
    delta, commanded_state = ctrl.update(commands, temp)

    #-------physical system-------------
    current_wind = wind.update()  # get the new wind vector
    mav.update_state(delta, current_wind)  # propagate the MAV dynamics
    mav.update_sensors()

    #-------update viewer-------------
    mav_view.update(mav.msg_true_state)  # plot body of MAV
    data_view.update(mav.msg_true_state, # true states
                     estimated_state, # estimated states
                     commanded_state, # commanded states
                     SIM.ts_simulation)
    if VIDEO == True: video.update(sim_time)
    
    my_heading = mav.msg_true_state.psi*RadtoDeg
    Roll       = mav.msg_true_state.phi*RadtoDeg
    Pitch      = mav.msg_true_state.theta*RadtoDeg
    #print("GpsN:",round(mav.msg_true_state.pn,2),"GpsE:",round(mav.msg_true_state.pe,2),"Altitude:",round(mav.msg_true_state.h,2),"Roll:",round(mav.msg_true_state.phi*57.29577951,2),"Pitch:",round(mav.msg_true_state.theta*57.29577951,2),"Yaw:",round(mav.msg_true_state.psi*57.29577951,2))
    
    #print("Accel_x:",round(mav.sensors.accel_x,2),"Accel_y:",round(mav.sensors.accel_y,2),"Accel_z:",round(mav.sensors.accel_z,2),"diff_pressure:",round(mav.sensors.diff_pressure,2),"Static_pressure:",round(mav.sensors.static_pressure,2),"Sensor_h:",round(mav.sensors.gps_h,2))
    Mod_Anlama.Update_Mod(my_heading,mav.msg_true_state.Vg,mav.msg_true_state.h,Roll,Pitch,my_heading) #mav.msg_true_state.Vg=groundspeed
    print("")
    
   # print(mav._gps_eta_e,"--",mav._gps_eta_n)
    #-------increment time-------------
    sim_time += SIM.ts_simulation

if VIDEO == True: video.close()




