import os
import thinkdsp
import pydub
import numpy as np
import math
from pydub.playback import play

class synthesizer:
    #creates a simple sin wave
    def sin_create(f,time):
        return(np.sin(2*np.pi*f*time))
    #creates envelope according to adsr
    def envelope (A,D,D_A,S,R,samp):
          # y= 1/A*x
        attack_ = np.linspace(0,1,int(samp*A))
        decay_ = np.linspace(1,1-D_A,int(samp*D))
        sustain_ = np.empty(int(samp*S))
        sustain_.fill(1-D_A)
        release_ = np.linspace(1-D_A,0,int(R*samp))
        env_ = np.concatenate((attack_,decay_,sustain_,release_))
        return(env_)
    # creates kick from transient envelopes and initial frequency
    def kick(f,trans,trans_pitch,time,intercept):
        return(trans*np.sin(2*np.pi*((f*(1+100000**(-trans_pitch+intercept)))*time)))
    #shifts the frequency according to major chords
    def single_shift(f,key_shift):
        if key_shift == 0:
#             f_list.append(f*4/3)
            new_wav = f  
        elif key_shift == -1:
            new_wav = 8/9*f
        elif key_shift == -2:
            new_wav = 4/5*f
        elif key_shift == -3:
            new_wav = 3/4*f
        elif key_shift == -4:
            new_wav = 2/3*f
        elif key_shift == -5:
            new_wav = 3/5*f
        elif key_shift == -6:
            new_wav = 3/5*f
        elif key_shift == 1:
#             f_list.append(f*4/3)
            new_wav = 9/8*f  
        elif key_shift == 2:
#             f_list.append(f*4/3)
            new_wav = 5/4*f    
        elif key_shift == 3:
#             f_list.append(f*3/2)
            new_wav = 4/3*f
        elif key_shift == 4:
#             f_list.append(f*3/2)
            new_wav = 3/2*f
        elif key_shift == 5:
            new_wav = 5/3*f
        elif key_shift == 6:
            new_wav = 5/3*f
        else:
            new_wav = 0 
        return(new_wav)
    #creates unison effect
    def uni_(f,voices, detune_lim,time):
        detune = np.linspace(-1*detune_lim,1*detune_lim, voices)
        chorus_ = np.sin(2*np.pi*f*time)
        for i in range(0,voices):
            chorus_ = chorus_ + np.sin(2*np.pi*(f+detune[i])*time)
        return(chorus_)
    #creates frequency modulation of fundamentla frequency based on fm matrix.
    def fm_(ff,fm, A ,time):
#         for i in range(0,len(fm)):
#             for j in range(0,len(fm[i]):
#                 jj = len(fm[i])-j
#                 f[i,j] =np.sin(2*np.pi*(fc+ A[i][jj]*fm[i][jj])*time)
#                 fc = fm[i][j]
#             fc = ff
        tpi_ = 2*np.pi*time
        #equation for FM modulation for 6 modulators in series
        return(np.sin((ff+A[0]*np.sin((fm[0]+A[1]*np.sin((fm[1]+A[2]*np.sin((fm[2]+A[3]*np.sin((fm[3]+A[4]*np.sin((fm[4]+A[5]*np.sin((fm[5])*tpi_))*tpi_))*tpi_))*tpi_))*tpi_))*tpi_))*tpi_))
    # turns np to wave
    def wave_map(wave, samp):
        return(thinkdsp.Wave(wave, framerate = 44100))