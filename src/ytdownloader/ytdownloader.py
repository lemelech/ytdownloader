from .ClipboardListener import ClipboardWatcher
from .converter import convert2mp3
from pathlib import Path
import time
from yt_dlp import YoutubeDL


# where to save
SAVE_PATH = Path(__file__).parent / "downloads"
LOG_PATH = Path(__file__).parent / "downloads.log"


ydl_opts = {
            'format': 'm4a/bestaudio/best',
            # ℹ️ See help(yt_dlp.postprocessor) for a list of available Postprocessors and their arguments
            'postprocessors': [{  # Extract audio using ffmpeg
                                'key': 'FFmpegExtractAudio',
                                'preferredcodec': 'mp3',}#'m4a',}
                               ],
            'nocheckcertificate': True
            }
def is_youtube_url(url:str):
    return any([pat in url for pat in ["youtube", "youtu.be"]]) and (url.lower().startswith("http://") or
                                                                     url.lower().startswith("https://") or
                                                                     url.lower().startswith("www."))


def ytdownloader(url):
    try:
        print(f'Downloading {url}')
        with YoutubeDL(ydl_opts) as ydl:
            ydl.download(url)

        with open(LOG_PATH, 'a') as f:
            f.write(f'{url} \n')
        # print(f'Converting {file_path}')
        # convert2mp3(file_path)
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