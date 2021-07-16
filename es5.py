from pyo import *
import collections

global gTriggerBuffer
gTriggerBuffer = collections.deque(maxlen=100)

global ges5bitmask
ges5bitmask = 0

ES5UNIT = 2.0/256

global gES
gES = Sig(0)

def onoff(args):
    """Pin 1-8, value 1=on, 0 = off, trigger 1 = trigger, 0 = latch"""
    global gTriggerBuffer
    global ges5bitmask
    pin, value, gate_or_trigger = args[0], args[1], args[2]

    # error check input values
    if pin < 1 or pin > 8:
        print("Error, pin must be a number between 1 and 8")
    bittarget = 2 ** (pin - 1) # allows 2^^0, trust me
    # print("bittarget = "+str(bittarget))
    if value == 1:
        # Set bit
        if bittarget & ges5bitmask:
            print("Error: bit is already set!")
            pass
        else:
            # set bit in ges5bitmask
            ges5bitmask = ges5bitmask | bittarget
            # print("bitmask = "+str(ges5bitmask))
            doSetVoltages(ges5bitmask) # it all happens here
            if gate_or_trigger == 1:
                # invoke CallAfter to turn off pin later
                gTriggerBuffer.append(CallAfter(onoff, time=0.01, arg=(pin, 0, 0)))
    # reset pin
    else:
        if not bittarget & ges5bitmask:
            # print("Error: bit is already reset!")
            pass
        else:
            # clear bit in ges5bitmask
            ges5bitmask = (ges5bitmask & ~bittarget) & 0b11111111
            # print("bitmask = "+str(ges5bitmask))
            doSetVoltages(ges5bitmask) # it all happens here

def doSetVoltages(bitmask):
    global gES
    output = 0
    if bitmask & 0b10000000: # MSB is set
        output = -1 + (bitmask-128)*ES5UNIT
    else: # MSB is not set
        output = bitmask*ES5UNIT + ES5UNIT
    gES.setValue(output)
    gES.out(6)




