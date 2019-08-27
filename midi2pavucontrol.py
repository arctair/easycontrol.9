#!/usr/bin/python3
import mido
import pulsectl

bankToPulseObjectName = [
    'app:Loopback from Built-in Audio Analog Stereo',
    'app:Spotify',
    'app:playStream',
    'input:alsa_input.usb-Blue_Microphones_Yeti_Stereo_Microphone_REV8-00.analog-stereo',
    'input:alsa_input.pci-0000_00_1b.0.analog-stereo',
    'app:Playback',
    None,
    None,
    'output:alsa_output.pci-0000_00_1b.0.analog-stereo',
]

def pulseObjectByIndex(pulse, index):
    pulseObjectsByName = {
        **{'app:{}'.format(pulseObj.name): pulseObj for pulseObj in pulse.sink_input_list()},
        **{'input:{}'.format(pulseObj.name): pulseObj for pulseObj in pulse.source_list()},
        **{'output:{}'.format(pulseObj.name): pulseObj for pulseObj in pulse.sink_list()},
    }
    if index > len(bankToPulseObjectName):
        return
    name = bankToPulseObjectName[index]
    return pulseObjectsByName[name] if name in pulseObjectsByName else None

def handle_message(message):
    if message.type == 'control_change':
        handle_control_change(message)
    elif message.type == 'sysex':
        handle_sysex(message)
    elif message.type == 'program_change':
        handle_program_change(message)

def handle_control_change(message):
    if message.control >= 3 and message.control <= 11:
        with pulsectl.Pulse('easycontrol.9') as pulse:
            set_volume(pulse, pulseObjectByIndex(pulse, message.control - 3), message.value / 127)
    elif message.control >= 23 and message.control <= 31 and message.value == 127:
        with pulsectl.Pulse('easycontrol.9') as pulse:
            toggle_mute(pulse, pulseObjectByIndex(pulse, message.control - 23))

def set_volume(pulse, pulseObject, volume):
    if pulseObject:
        pulse.volume_set_all_chans(pulseObject, volume)

def toggle_mute(pulse, pulseObject):
    if pulseObject:
        pulse.mute(pulseObject, not pulseObject.mute)

def handle_sysex(message):
    pass

def handle_program_change(message):
    pass

with mido.open_input('WORLDE easy control:WORLDE easy control MIDI 1 28:0') as inport:
    for message in inport:
        handle_message(message)
