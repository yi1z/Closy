from __future__ import annotations

from recorder import Recorder
import emotion
from configs import closy_config_handler as cch


# The virtual assistant
class Closy:
    
    def __init__(self):
        # load the config
        cch.load_config()

        self.is_running = False
        self.is_listening = True
        self.is_speaking = False

        self.recorder = Recorder()
        
        # the current model state of the virtual assistant
        self.curr_emotion = cch.closy_wake_emotion
        self.curr_movement = cch.closy_wake_movement

        # the history of the model state of the virtual assistant
        # this will be used as referenced supplied to GPT
        self.emotion_history = {}
        self.movement_history = {}
        self.responses = {}

        self.model = cch.closy_model
        self.voice = cch.closy_voice
        self.wake_emotion = cch.closy_wake_emotion
        self.max_emotion = cch.closy_max_emotion
        self.min_emotion = cch.closy_min_emotion
        # how drastic it is for Closy to change her emotion due to an influence
        self.emo_factor = cch.closy_emo_factor
        # all movements Closy can take
        self.movement_lists = cch.closy_movement_lists
        # initial movement
        self.wake_movement = cch.closy_wake_movement
        # map from emotion to movement
        self.emo_to_mov = cch.closy_emo_to_mov
        # how often Closy would talk when she wakes up
        self.wake_talk_rate = cch.closy_wake_talk_rate
        # how often Closy would talk when she is in a certain emotion
        self.emo_to_talk_rate = cch.closy_emo_to_talk_rate

    def wake(self):
        self.is_running = True

    def rest(self):
        self.is_running = False

    def listen(self):
        pass

    def make_response(self):
        pass

    def change_emotion(self, text):
        # analysis the emotion of the text
        emo_score = emotion.get_emo(text)
        # if the request returns -1, do nothing
        if emo_score == -1:
            return
        # if the request returns a valid score, update Closy's emotion
        self.curr_emotion += emo_score * self.emo_factor
        # if the emotion is out of bound, set it to the bound
        if self.curr_emotion > self.max_emotion:
            self.curr_emotion = self.max_emotion
        elif self.curr_emotion < self.min_emotion:
            self.curr_emotion = self.min_emotion


    def make_movement(self):
        pass

    def speak(self):
        pass
