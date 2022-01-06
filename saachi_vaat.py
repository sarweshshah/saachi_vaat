#!/usr/bin/env python3
import sounddevice as sd
import soundChamber as sc

numChambers = 7

soundChambers = []
input_device_indices = []
output_device_indices = []

try:
    device_dict = sd.query_devices()
    print(device_dict)

    # Search for USB devices with input channels
    for index, device in enumerate(device_dict):
        # if (device['max_input_channels'] > 0) and ("USB " in info["name"]):
        if device['max_input_channels'] > 0:
            input_device_indices.append(index)

        if device['max_output_channels'] > 0:
            output_device_indices.append(index)

    print(input_device_indices)
    print(output_device_indices)

    # sc.SoundChamber().play_an_audiofile(device_index=output_device_indices[0])

    for i in range(0, numChambers - 1):
        soundChambers.append(sc.SoundChamber())

    soundChambers[0].recognise_audio()

except KeyboardInterrupt:
    print('Interrupted by user')
