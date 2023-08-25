import pyaudio
import wave
from tqdm import tqdm
import time

from core import closy


# A recorder that records user's audio
class Recorder:
    def __init__(self, chunk=1024, channels=1, rate=16000):
        self.CHUNK = chunk
        self.FORMAT = pyaudio.paInt16
        self.CHANNELS = channels
        self.RATE = rate
        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(format=self.FORMAT,
                                  channels=self.CHANNELS,
                                  rate=self.RATE,
                                  input=True,
                                  frames_per_buffer=self.CHUNK)

    def record(self, seconds):
        frames = []
        for i in range(0, int(self.RATE / self.CHUNK * seconds)):
            data = self.stream.read(self.CHUNK)
            frames.append(data)
        return frames
    
    def close(self):
        self.stream.stop_stream()
        self.stream.close()
        self.p.terminate()


def main():
    closy = closy.Closy()

