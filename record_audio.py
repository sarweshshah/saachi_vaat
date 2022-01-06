import sounddevice as sd
import soundfile as sf
import os

DATA_TYPE = "float32"
RECORDING_DURATION = 3.2  #seconds
SAMPLERATE = 44100

input_device_indices = []
output_device_indices = []


try:
    # Search for all existing sound devices
    sound_devices = sd.query_devices()
    print(sound_devices)

    # Search for USB devices with input channels
    for index, info in enumerate(sd.query_devices()):
        # if (info['max_input_channels'] > 0) and ("USB " in info["name"]):
        if (info['max_input_channels'] > 0):
            # print(index, info)
            input_device_indices.append(index)

        if (info['max_output_channels'] > 0):
            output_device_indices.append(index)
    print(input_device_indices)
    print(output_device_indices)

    sd.default.device = input_device_indices[0]
    indata = sd.rec(frames=int(RECORDING_DURATION * SAMPLERATE), samplerate=SAMPLERATE, blocking=True, channels=1, dtype=DATA_TYPE)

    rec_file_path = os.path.join(os.getcwd(), "rec" + str(input_device_indices[0]) + ".wav")
    sf.write(file=rec_file_path, data=indata, samplerate=SAMPLERATE, subtype='PCM_24')
    print(sf.info(rec_file_path))

except KeyboardInterrupt:
    print("Interrupted by user")
