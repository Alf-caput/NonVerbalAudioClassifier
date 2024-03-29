import os
import wave
import multiprocessing
import numpy as np
import pandas as pd


def read_wav_file(wav_file):
    with wave.open(wav_file, 'rb') as wf:
        num_frames = wf.getnframes()
        frames = wf.readframes(num_frames)
        wave_array = np.frombuffer(frames, dtype=np.int16)
        wave_name = os.path.splitext(wav_file)[0]
    return wave_name, wave_array

def run_pool(task, data, pool_size=1):
    print(f"Number of processes: {pool_size}")
    with multiprocessing.Pool(processes=pool_size) as pool:
        if isinstance(data[0], tuple):  # Si el primer elemento es una tupla, usa starmap
            results = pool.starmap(task, data)
        else:
            results = pool.map(task, data)
    return results 
