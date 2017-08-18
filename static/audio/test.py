from scipy.io import wavfile
import numpy as np
from matplotlib import pyplot as plt
for n in range(5):
    path = "phrase0{}.wav".format(n + 1)
    fs, x = wavfile.read(path)
    print(path, fs)
    wavfile.write(path, rate=fs, data=x.astype(np.int16))
    print(np.max(x))
