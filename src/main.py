import os
import wave
import multiprocessing
import numpy as np
import pandas as pd

def main():
    base_dir = 'data'
    dir = 'audio_16k'
    audio_dir = os.path.join(base_dir, dir)
    audios = os.listdir(audio_dir)
    num_processes = multiprocessing.cpu_count()
    audio_paths = [os.path.join(audio_dir, file) for file in audios]
    results = run_pool(task=read_wav_file, data=audio_paths, pool_size=num_processes)
    print(results[0])
    return

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
        results = pool.map(task, data)
    return results 

if __name__ == '__main__':
    main()
