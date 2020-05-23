from scipy.io import wavfile as sciwv
import numpy as np
import playsound as ps
import wave as wv

wr = wv.open('you-are-acting-so-weird.wav', 'r')
ww = wv.open('new_test.wav', 'w')

par = list(wr.getparams())
#par[3] = 0
#par = tuple(par)
ww.setparams(par)
sz = wr.getframerate()//20
c = int(wr.getnframes()/sz)
shift = 750//20

for num in range(c):
    da = np.fromstring(wr.readframes(sz), dtype=np.int16)
    left = da[0::2]
    right = da[1::2]
    #Take DFT
    lf = np.fft.rfft(left)
    rf = np.fft.rfft(right)
    #Scale It Up or Down
    lf = np.roll(lf, shift)
    rf = np.roll(rf, shift)
    lf[0:shift] = 0
    rf[0:shift] = 0
    #Take inverse DFT
    nl = np.fft.irfft(lf)
    nr = np.fft.irfft(rf)
    #Put it altogether
    ns = np.column_stack((nl,nr)).ravel().astype(np.int16)
    ww.writeframes(ns.tostring())

wr.close()
ww.close()

ps.playsound('you-are-acting-so-weird.wav')
ps.playsound('new_test.wav')


