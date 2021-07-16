"""
Script to initialize ES=8 and import es5 controls.



"""
from pyo import *
def get_audio_device(dev_name):
    txt = pa_get_devices_infos()
    audio_device = None
    for key in txt[0].keys():
        if txt[0].get(key).get('name')  == dev_name:
            return key
    return None

if isinstance((audio_device := get_audio_device('ES-8')), int):
    s = Server()
    s.setOutputDevice(audio_device)
    s.setInputDevice(audio_device)
    s.setNchnls(10)
    s.setIchnls(4)
    s.boot().start()

from es5 import *
q = Pattern(onoff,.25,(1,1,1))
q.play()
