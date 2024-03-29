from utils import *
import os
import multiprocessing
import zipfile
from time import perf_counter
import concurrent.futures

def main():
    base_dir = "data"
    dir = "audio_16k"
    zip_file_path = "vs_release_16k.zip"
    folders_to_extract = ["audio_16k", "meta"]

    # if not os.path.exists(base_dir):
    #     with zipfile.ZipFile(zip_file_path, 'r') as zf:
    #         targets = []
    #         for file in zf.namelist():
    #             if any(file.startswith(folder) for folder in folders_to_extract):
    #                 targets.append((file, base_dir))
    #         num_processes = multiprocessing.cpu_count()
    #         run_pool(task=zf.extract, data=targets, pool_size=num_processes)
    audio_dir = os.path.join(base_dir, dir)
    audios = os.listdir(audio_dir)
    num_processes = multiprocessing.cpu_count()
    audio_paths = [os.path.join(audio_dir, file) for file in audios]
    results = run_pool(task=read_wav_file, data=audio_paths, pool_size=num_processes)
    print(results[0])
    return

def extract_file(zip_file, file_name, output_dir):
    zip_file.extract(file_name, output_dir)

if __name__ == '__main__':
    start = perf_counter()
    main()
    stop = perf_counter()
    print(f"Elapsed: {stop-start:.2f}s")
