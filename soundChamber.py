import sounddevice as sd
import soundfile as sf
import os
import speech_recognition as sr
import gpio


class SoundChamber:
    def __init__(self, order_num: int = 0):
        self.orderNumber = order_num
        self.chamberFileLabel = str(order_num) + '.wav'

        self.recording_duration = 3.2  # seconds
        self.recording_timeout = 3.2  # seconds

        self.data_type = "float32"
        self.default_samplerate = 44100
        self.default_channels = 1

        self.recognizer = sr.Recognizer()
        self.mic = sr.Microphone()

    @staticmethod
    def show_available_devices():
        sound_devices = dict(enumerate(sd.query_devices()))
        print(sound_devices)

    def record_audio(self, device_index: int = 0):
        sd.default.device = device_index

        indata = sd.rec(frames=int(self.recording_duration * SAMPLERATE), samplerate=self.default_samplerate, blocking=True, channels=self.default_channels, dtype=self.data_type)

        sf.write(data=indata, file=os.path.join(os.getcwd(), self.chamberFileLabel), samplerate=self.default_samplerate, subtype='PCM_24')

    @staticmethod
    def play_an_audiofile(filepath: str = "samples/1.wav", device_index: int = 0):

        # Locating a file in the project directory and play  it
        rec_file_path = os.path.join(os.getcwd(), filepath)
        audiodata, fs = sf.read(file=rec_file_path)

        sd.play(audiodata, device=device_index, samplerate=fs, blocking=True, loop=False)

    def recognise_audio(self, savefile: bool = False):
        with self.mic as source:
            # listen for 1 second to calibrate the energy threshold for ambient noise levels
            # recognizer.adjust_for_ambient_noise(source)
            print("Say something...")
            audio_data = self.recognizer.listen(source, timeout=5, phrase_time_limit=7.2)

            if savefile is True:
                with open("rec1.wav", "wb") as rec_file:
                    rec_file.write(audio_data.get_wav_data())

        # recognize speech using Google Speech Recognition
        try:
            # for testing purposes, we're just using the default API key
            # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
            # instead of `r.recognize_google(audio)`
            print("GSR thinks you said: " + self.recognizer.recognize_google(audio_data))
        except sr.UnknownValueError:
            print("GSR could not understand audio")
        except sr.RequestError as e:
            print("Could not request results from GSR service; {0}".format(e))

    def transcribe_audio_file(self, filepath):
        pass
