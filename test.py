import pyaudio
import tensorflow as tf
import numpy as np
import struct
import time
import joblib
import cv2 as cv

from cnn_model import get_model
from util import cut_audio, get_arr_from_audio, save_wave_file

from config import _AUDIO_CHANNELS, _AUDIO_DATA_WIDTH, _AUDIO_VALID_THRESHOLD, _AUDIO_FRAME_RATE, _BLOCKLEN, _SVM_IMAGE_HEIGHT, _SVM_IMAGE_WIDTH

import os

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

SAVE_AUDIO = False
SAVE_IMAGE = True
audio_saved_count = 0
image_saved_count = 0

MODEL_TPYE = 'SVM'

cnn_weight_save_path = 'models/model2_checkpoint'
svm_model_path = 'models/svm_model'
test_data = 'test_data/'

if MODEL_TPYE == 'CNN':
    my_model = get_model(n_class=10)
    my_model.load_weights(cnn_weight_save_path)

if MODEL_TPYE == 'SVM':
    my_model = joblib.load(svm_model_path)
block_buffer = []


recording = True
detected = False

def callback(in_data, frame_count, time_info, flag):
    global block_buffer, detected, recording
    signal_block = np.frombuffer(in_data, dtype=np.int16)


    audio_valid = np.max(signal_block) - np.min(signal_block) > _AUDIO_VALID_THRESHOLD

    
    if not detected and audio_valid:
        detected = True
    if detected and not audio_valid:
        detected = False
        recording = False
    if detected:
        block_buffer.append(signal_block)

    return(signal_block, pyaudio.paContinue)

p = pyaudio.PyAudio()
PA_FORMAT = p.get_format_from_width(_AUDIO_DATA_WIDTH)
stream = p.open(
    format = PA_FORMAT,
    channels = _AUDIO_CHANNELS,
    rate = _AUDIO_FRAME_RATE,
    input = True,
    output = False,
    stream_callback=callback,
    frames_per_buffer=_BLOCKLEN)

print('**start**')

stream.start_stream()

while True:
    time.sleep(0.1)

    if not recording:
        stream.stop_stream()

        print('Voice detected')
        
        audio_sequence = np.hstack(block_buffer)
        audio_sequence = cut_audio(audio_sequence)
    
        img_arr = get_arr_from_audio(audio_sequence,showImg=True, Transfer=False)

        if MODEL_TPYE == 'CNN':
            res_arr = my_model.predict(img_arr)
            res = np.where(res_arr == np.max(res_arr))[1][0]

        if MODEL_TPYE == 'SVM':
            img_arr = (img_arr - np.mean(img_arr)) / np.std(img_arr)
            res = my_model.predict(img_arr.reshape(1,-1))[0]
        print(res)        

        if SAVE_AUDIO:
            wave_file_name = f'testdata/audio_save_{audio_saved_count}_{res}.wav'
            save_wave_file(test_data + audio_sequence, wave_file_name)
            audio_saved_count = audio_saved_count + 1
        
        if SAVE_IMAGE:
            image_file_name = f'testdata/image_save_{image_saved_count}_{res}.png'
            img_arr = img_arr.reshape(_SVM_IMAGE_HEIGHT, _SVM_IMAGE_WIDTH, 3) * 255
            cv.imwrite(test_data + image_file_name, img_arr.astype(np.int16))
            image_saved_count = image_saved_count + 1

        block_buffer = []
        recording = True
        stream.start_stream()

        
    

stream.stop_stream()
stream.close()
p.terminate()