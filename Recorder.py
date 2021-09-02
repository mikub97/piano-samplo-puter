import wave
import numpy
import time
# # # # #
# CONSTANTS

# sound length (seconds, a float)
SOUNDLEN = 3.0
# sound frequency (in Herz: the number of vibrations per second)
SOUNDFREQ = 1000

# maximal amplitude
MAXAMP = 32767 / 2
# sampling frequency (in Herz: the number of samples per second)
SAMPLINGFREQ = 48000
# the number of channels (1=mono, 2=stereo)
NCHANNELS = 1

class Recorder(object):
    def __init__(self,filename):
        self.is_rec=False
        self.name = filename
        self.sound_history = []

    def record(self):
        self.is_rec = not self.is_rec
        if self.is_rec:
            self.file = wave.open(f'{self.name}.wav', 'w')
            # set the parameters
            self.file.setframerate(SAMPLINGFREQ)
            self.file.setnchannels(NCHANNELS)
            self.file.setsampwidth(2)
            self.time0 = time.time()
            print('Recording')
        else:
            self.file.close()
            print('finito')


    def play(self,sound,time):
        print(time)
        a= sound.get_raw()
        self.file.writeframesraw(sound.get_raw())

