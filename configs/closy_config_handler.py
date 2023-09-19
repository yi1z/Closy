from configparser import ConfigParser
import json
import codecs


# default value any
dv = None

model = dv
voice = dv

wake_emotion = dv
max_emotion = dv
min_emotion = dv
emo_factor = dv

movement_lists = dv
wake_movement = dv
emo_to_mov = dv

wake_talk_rate = dv
emo_to_talk_rate = dv

user_speech_path = dv
hearing_threshold = dv

def load_config():
    global closy_model
    global closy_voice

    global closy_wake_emotion 
    global closy_max_emotion 
    global closy_min_emotion 
    global closy_emo_factor 

    global closy_movement_lists
    global closy_wake_movement 
    global closy_emo_to_mov

    global closy_wake_talk_rate 
    global closy_emo_to_talk_rate

    global closy_user_speech_path
    global closy_hearing_threshold

    config = ConfigParser()
    config.read('closy.conf', encoding='utf-8')

    closy_model = config.get('Closy', 'model')
    closy_voice = config.get('Closy', 'voice')

    closy_wake_emotion = config.get('Closy', 'wake_emotion')
    closy_max_emotion = config.get('Closy', 'max_emotion')
    closy_min_emotion = config.get('Closy', 'min_emotion')
    closy_emo_factor = config.get('Closy', 'emo_factor')

    closy_movement_lists = config.get('Closy', 'movement_lists')
    closy_wake_movement = config.get('Closy', 'wake_movement')
    closy_emo_to_mov = config.get('Closy', 'emo_to_mov')

    closy_wake_talk_rate = config.get('Closy', 'wake_talk_rate')
    closy_emo_to_talk_rate = config.get('Closy', 'emo_to_talk_rate')

    closy_user_speech_path = config.get('Closy', 'user_speech_path')
    closy_hearing_threshold = config.get('Closy', 'hearing_threshold')

    config_file = json.load(codecs.open('closy.json', 'r', 'utf-8-sig'))


def save_config(config_data):
    global config
    config = config_data
    config_file = codecs.open('closy.json', 'w', encoding='utf-8-sig')
    config_file.write(json.dumps(config, indent=4, ensure_ascii=False, sort_keys=True, separators=(',', ': ')))
    config_file.close()


