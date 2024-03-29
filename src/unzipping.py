# SuperFastPython.com
# unzip a large number of files concurrently with threads
from zipfile import ZipFile
from concurrent.futures import ThreadPoolExecutor
 
# unzip a file from an archive
def unzip_file(handle, filename, path):
    # unzip the file
    handle.extract(filename, path)
    # report progress
    print(f'.unzipped {filename}')
 
# unzip a large number of files
def main(path='tmp'):
    # open the zip file
    
    zip_file_name = "vs_release_16k.zip"
    folders_to_extract = ["audio_16k", "meta"]
    with ZipFile(zip_file_name, 'r') as handle:
        # start the thread pool
        with ThreadPoolExecutor(100) as exe:
            # unzip each file from the archive
            _ = []
            for file in handle.namelist():
                if any(file.startswith(folder) for folder in folders_to_extract):
                    _.append(exe.submit(unzip_file, handle, file, path))
# entry point
if __name__ == '__main__':
    main()