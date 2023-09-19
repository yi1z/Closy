import pyaudio
import wave
from tqdm import tqdm
import time
import math, struct
from threading import Thread
from configs import closy_config_handler as cch

SHORT_NORMALIZE = (1.0/32768.0)
swidth = 2


# a recorder that records user's voice when speech is detected
class Recorder:

    # reference: https://stackoverflow.com/questions/18406570/python-record-audio-on-detected-sound
    @staticmethod
    def rms(frame):
        count = len(frame) / swidth
        format = "%dh" % (count)
        shorts = struct.unpack(format, frame)

        sum_squares = 0.0
        for sample in shorts:
            n = sample * SHORT_NORMALIZE
            sum_squares += n * n
        rms = math.pow(sum_squares / count, 0.5)

        return rms * 1000
    
    def __init__(self, closy):
        # whether the recorder is running
        self.is_running = True
        # whether the recorder is recording
        self.is_recording = False
        # whether the recorder is processing the recorded speech
        self.is_processing = False
        
        # get the metadata from the config
        self.output_path = cch.closy_user_speech_path
        self.threshold = cch.closy_hearing_threshold

        self.closy = closy

        self.chunk = 1024
        self.format = pyaudio.paInt16
        self.channels = 1
        self.rate = 16000
        # the time the recorder will wait before considering a speech is finished
        self.timeout = 5

        # open up the stream
        self.stream = self.p.open(format=self.format,
                                  channels=self.channels,
                                  rate=self.rate,
                                  input=True, output=True,
                                  frames_per_buffer=self.chunk)

    def listen(self):
        print("监测语音中...")
        while self.is_running:
            # if closy is not speaking, check for audio input
            if not self.closy.is_speaking:
                try:
                    audio_input = self.stream.read(self.chunk)
                except:
                    print("设备似乎有问题，请检查后重新启动。")
                    self.is_running = False
                
                # if no audio has been picked up
                if audio_input is None:
                    continue

                rms_val = self.rms(audio_input)
                # check if the rms value breaks the threshold
                if rms_val > self.threshold:
                    # if so, record the speech
                    self.record()
                    print("监测语音中...")

    def record(self):
        print("检测到语音，开始录音。")
        self.is_recording = True

        rec = []
        # current time
        curr = time.time()
        # the end time of the recorded speech
        end = time.time() + self.timeout

        while curr <= end:
            audio_input = self.stream.read(self.chunk)
            # check if the audio input breaks the threshold
            rms_val = self.rms(audio_input)
            if rms_val > self.threshold:
                # if so, refresh the end time of the recorded speech
                end = time.time() + self.timeout

            # change the current time
            curr = time.time()
            rec.append(audio_input)
        
        self.write(b''.join(rec))

    def write(self, audio):
        print("录音结束，开始处理。")
        self.is_recording = False
        self.is_processing = True

        # write the audio to a wav file
        wf = wave.open(self.output_path, 'wb')
        wf.setnchannels(self.channels)
        wf.setsampwidth(self.p.get_sample_size(self.format))
        wf.setframerate(self.rate)
        wf.writeframes(audio)
        wf.close()

        # finish processing
        self.is_processing = False
        print("处理结束。")

    def close(self):
        self.stream.close()
        self.p.terminate()
        self.is_running = False
        print("录音进程已关闭。")


if __name__ == "__main__":
    # short test

    # metadata for the recorder
    metadata = {
        "output_path": "output.wav",
        "threshold": 1000
    }

    # create a recorder
    recorder = Recorder(metadata)
    # start the recorder
    recorder.listen()
    # close the recorder
    recorder.close()
