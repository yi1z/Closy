from __future__ import annotations

from recorder import Recorder


# The virtual assistant
class Closy:
    
    def __init__(self):
        self.is_running = False
        self.is_listening = True
        self.is_speaking = False

        self.recorder = Recorder()
        
        # the current model state of the virtual assistant
        self.curr_emotion = None
        self.curr_movement = None
        # the history of the model state of the virtual assistant
        # this will be used as referenced supplied to GPT
        self.emotion_history = {}
        self.movement_history = {}
        self.responses = {}

    def wake(self):
        self.is_running = True

    def rest(self):
        self.is_running = False

    def listen(self):
        pass

    def make_response(self):
        pass

    def change_emotion(self):
        pass

    def make_movement(self):
        pass

    def speak(self):
        pass
