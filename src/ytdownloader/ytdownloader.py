from pytube import YouTube
from .ClipboardListener import ClipboardWatcher
from .converter import convert2mp3
from pathlib import Path
import time

# where to save
SAVE_PATH = Path(__file__).parent / "downloads"


def is_youtube_url(url:str):
    return any([pat in url for pat in ["youtube", "youtu.be"]]) and (url.lower().startswith("http://") or
                                                                     url.lower().startswith("https://") or
                                                                     url.lower().startswith("www."))


def ytdownloader(url):
    try:
        yt = YouTube(url)
    except Exception as e:
        print("Connection Error")  # to handle exception
        print(e)

    try:
        # for debugging:
        # for stream in yt.streams.filter(file_extension='mp4').order_by('abr').desc():
        #     print(stream)

        stream = yt.streams.filter(file_extension='mp4').order_by('abr').desc()[1]
        print(f'Downloading {stream}')
        file_path = stream.download(SAVE_PATH)

        print(f'Converting {file_path}')
        convert2mp3(file_path)
    except Exception as e:
        print(e)


def main():
    watcher = ClipboardWatcher(is_youtube_url,
                               ytdownloader,
                               1.)
    watcher.start()
    print("Waiting for clipboard link...")
    while True:
        try:
            time.sleep(10)
        except KeyboardInterrupt:
            watcher.stop()
            break


if __name__ == "__main__":
    main()