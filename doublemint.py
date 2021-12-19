import time
from odrive.enums import *

tables = [odrv0.axis0,odrv0.axis1]
for table in tables:
    table.requested_state = AXIS_STATE_FULL_CALIBRATION_SEQUENCE
time.sleep(1)
for table in tables:
    if table.current_state != 1:
      pass
for table in tables:
    table.controller.config.control_mode = CONTROL_MODE_POSITION_CONTROL
    table.requested_state = AXIS_STATE_CLOSED_LOOP_CONTROL
