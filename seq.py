import os
import thinkdsp
import pydub
import numpy as np
import math
from pydub.playback import play

class sequencer:
    def time_shift(wave,t_shift):
        wav = wave.copy()
        wav.shift(t_shift)
        return(wav)
    def time_np(t,samp):
        return(np.linspace(0,t, int(t*samp)))