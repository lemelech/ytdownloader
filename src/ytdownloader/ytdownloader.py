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

def download_best_audio_as_mp3(video_url, save_path=SAVE_PATH): # got from https://dev.to/_ken0x/downloading-and-converting-youtube-videos-to-mp3-using-yt-dlp-in-python-20c5
    ydl_opts = {
        'outtmpl': str(save_path) + '/%(title)s.%(ext)s',  # Save path and file name
        'postprocessors': [{  # Post-process to convert to MP3
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',  # Convert to mp3
            'preferredquality': '0',  # '0' means best quality, auto-determined by source
        }],
    }
    with YoutubeDL(ydl_opts) as ydl:
        ydl.download([video_url])


def ytdownloader(url, single=True):
    try:
        download_url = url
        if single:
            download_url = get_clean_youtube_url(url)

        print(f'Downloading {download_url}')
        # with YoutubeDL(ydl_opts) as ydl:
        #     ydl.download(url)
        download_best_audio_as_mp3(download_url,  SAVE_PATH)   

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


from urllib.parse import urlparse, parse_qs, urlencode, urlunparse

def get_clean_youtube_url(url):
    parsed = urlparse(url)
    
    # Keep only the video id parameter
    query_params = parse_qs(parsed.query)
    clean_query = {'v': query_params.get('v', [None])[0]} if 'v' in query_params else {}
    
    # Rebuild URL with only v= parameter
    new_query = urlencode(clean_query, doseq=True)
    clean_url = urlunparse((
        parsed.scheme,
        parsed.netloc,
        parsed.path,
        parsed.params,
        new_query,
        ''  # remove fragment
    ))
    
    return clean_url


if __name__ == "__main__":
    main()