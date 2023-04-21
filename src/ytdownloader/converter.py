import subprocess
from pathlib import Path


def convert2mp3(file_path, quality=5):
    file_path = str(file_path)
    print('starting to convert: {file_path}...', end='')
    process = subprocess.Popen(['ffmpeg', '-i', file_path, '-q:a', str(quality), '-map', 'a', file_path + '.mp3'],
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    print('Done.')
    print(stdout, stderr)


def convert_all_to_mp3(dir_path, pat='*.mp4'):
    dir_path = Path(dir_path)
    for file_path in dir_path.glob(pat):
        convert2mp3(str(file_path))


if __name__ == "__main__":
    convert_all_to_mp3('.')
