from init import *
import odrive
import time
from odrive.enums import *

odrv0 = odrive.find_any()

tables = [odrv0.axis0,odrv0.axis1]
for table in tables:
    table.requested_state = AXIS_STATE_FULL_CALIBRATION_SEQUENCE

time.sleep(12)
for table in tables:
    table.encoder.set_linear_count(0)

for index, table in enumerate(tables):
    print("putting table {} into position mode".format(index))
    table.controller.config.control_mode = CONTROL_MODE_POSITION_CONTROL
    time.sleep(.5)
    print("putting table {} into closed loop state".format(index))
    table.requested_state = AXIS_STATE_CLOSED_LOOP_CONTROL
    time.sleep(.5)

# TODO replace these with app. values
global gBPM
global gBeatDuration

gBPM = app.get_bpm()

gBeatDuration = gBPM/60.0
duration = gBeatDuration/16.0

f = Adsr(attack=.01, decay=duration*.3, sustain=duration*.1, release=duration*.1, dur=duration, mul=1)
g = Sig(1, mul=f).out(1)

h = Adsr(attack=.01, decay=duration*.3, sustain=duration*.1, release=duration*.1, dur=duration, mul=1)
i = Sig(1, mul=h).out(2)


def babyscratch(args):
    subdiv,direction,motor,adsr,sig = args[0],args[1],args[2],args[3],args[4]
    if direction == 1:
        if random.random() > .2: 
            adsr.play()
        motor.controller.input_pos = 0
        gTriggerBuffer.append(CallAfter(function = babyscratch, time=(gBeatDuration/subdiv), arg=(16,0,motor,adsr,sig)))
    elif direction == 0:
        if random.random() > .1: 
            adsr.play()
        motor.controller.input_pos = .2 * random.random()


#scratches
for table in tables:
    print(table.encoder.shadow_count)

for table in tables:
    table.encoder.set_linear_count(0)


odrv0.axis0.encoder.set_linear_count(0)
print("After reset:")
for table in tables:
    print(table.encoder.shadow_count)

time.sleep(3)
print("launching scratch 1")
scratch1 = Pattern(babyscratch, gBeatDuration/16.0,(16,1,odrv0.axis0,f,g))

time.sleep(3)
print("now scratch 2..")
scratch2 = Pattern(babyscratch, gBeatDuration/16.0,(16,1,odrv0.axis1,h,i))

time.sleep(3)

#bass drum
q = Pattern(onoff,gBeatDuration/4.0,(2,1,1))


q.play(); 
print("telling 1 to play")
scratch1.play()
print("telling 2 to play")
scratch2.play()



# q.stop(); r.stop()