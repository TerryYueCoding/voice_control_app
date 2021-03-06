"""
Configuration definition
"""

# Audio
_AUDIO_FRAME_RATE = 8000
_AUDIO_DATA_WIDTH = 2
_AUDIO_CHANNELS = 1

# Threshold
_AUDIO_VALID_THRESHOLD = 5000
_AUDIIO_CUT_THRESHOLD = 500

# 
_EXTEND_NUM = 800
_BLOCKLEN = 1024
_LOW_PASS_CUTOFF = 2000
_FILTER_ORDER = 4
_USE_FILTER = False


# Audio spectrogram 
_IMAGE_HEIGHT = 256
_IMAGE_WIDTH = 256
_IMAGE_CHANNELS = 3
_MODEL_N_CLASSES = 12

# SVM
_SVM_IMAGE_HEIGHT = 64
_SVM_IMAGE_WIDTH = 64