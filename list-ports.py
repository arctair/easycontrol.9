import mido
for port in mido.get_input_names():
    print(port)
