import odrive
from odrive.enums import *
import time
from odrive.utils import *
import time
import chart


odrv0= odrive.find_any()

odrv0.axis0.controller.config.control_mode = CONTROL_MODE_VELOCITY_CONTROL

odrv0.axis0.controller.config.input_mode = INPUT_MODE_VEL_RAMP
odrv0.axis0.controller.config.vel_ramp_rate = 0.2
odrv0.axis0.requested_state = AXIS_STATE_CLOSED_LOOP_CONTROL
odrv0.axis0.controller.input_vel = 1

variables = []
t = time.time()
while(1):
    variables.append([
        odrv0.axis0.encoder.vel_estimate,
        odrv0.axis0.encoder.shadow_count,
        odrv0.axis0.controller.vel_setpoint,
        odrv0.axis0.motor.current_control.Iq_setpoint,
        odrv0.axis0.motor.current_control.Iq_measured,
        ]
    )
    time.sleep(.01)
    if time.time() - t > 6:
        break

chart.chart(variables)


