"""
Script to initialize ES=8 and import es5 controls.

"""
from pyo import *
import collections

class globalContext():
    def __init__(self, bpm = 120):
        self.bpm = bpm
        self.collection = collections.deque(maxlen=100)

    def get_bpm(self):
        return self.bpm

    def add_collection(thing):
        self.collection.append(thing)

app = globalContext()



def get_audio_device(dev_name):
    txt = pa_get_devices_infos()
    audio_device = None
    for key in txt[0].keys():
        if txt[0].get(key).get('name')  == dev_name:
            return key
    return None

if isinstance((audio_device := get_audio_device('ES-8')), int):
    s = Server(duplex=1)
    s.setOutputDevice(audio_device)
    s.setInputDevice(audio_device)
    s.setNchnls(10)
    s.setIchnls(4)
    s.boot().start()
else:
    s = Server(duplex=1) 

from es5 import *
#q = Pattern(onoff,.25,(1,1,1))
# q.play()
