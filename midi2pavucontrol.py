import mido
import pulsectl

def handle_message(message):
    if message.type == 'control_change':
        handle_control_change(message)
    elif message.type == 'sysex':
        handle_sysex(message)
    elif message.type == 'program_change':
        handle_program_change(message)

def handle_control_change(message):
    if message.control >= 3 and message.control <= 11:
        set_volume(message.control - 3, message.value / 127)
    elif message.control >= 23 and message.control <= 31 and message.value == 127:
        toggle_mute(message.control - 23)

def set_volume(index, volume):
    with pulsectl.Pulse('volume-increaser') as pulse:
        audioObjects = pulse.source_list() + pulse.sink_list() + pulse.sink_input_list()
        if index < len(audioObjects):
            pulse.volume_set_all_chans(audioObjects[index], volume)

def toggle_mute(index):
    with pulsectl.Pulse('volume-increaser') as pulse:
        audioObjects = pulse.source_list() + pulse.sink_list() + pulse.sink_input_list()
        if index < len(audioObjects):
            pulse.mute(audioObjects[index], not audioObjects[index].mute)

def handle_sysex(message):
    pass

def handle_program_change(message):
    pass

with mido.open_input('WORLDE easy control:WORLDE easy control MIDI 1 20:0') as inport:
    for message in inport:
        handle_message(message)
