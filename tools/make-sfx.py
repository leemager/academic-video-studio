"""Create a quiet original transition sound, not music. Never replaces a take."""
from pathlib import Path
import numpy as np
import soundfile as sf
from scipy.signal import butter, sosfilt
root=Path(__file__).resolve().parents[1]
rate=48000; t=np.arange(int(.88*rate))/rate
noise=np.random.default_rng(910).normal(0,1,len(t))
noise=sosfilt(butter(2,[400,4500],btype='bandpass',fs=rate,output='sos'),noise)
envelope=np.sin(np.pi*t/.88)**2.7
signal=noise*envelope*(.65+.35*np.sin(2*np.pi*(120*t+500*t*t)))
signal=signal/(np.max(np.abs(signal))+1e-9)*.36
pan=np.linspace(-.5,.5,len(t))
stereo=np.column_stack((signal*np.sqrt((1-pan)/2),signal*np.sqrt((1+pan)/2)))
target=root/'public/sfx/soft-swoosh.wav';target.parent.mkdir(parents=True,exist_ok=True)
with target.open('xb') as stream:sf.write(stream,stereo,rate,format='WAV',subtype='PCM_16')
print(target)
