import os
from tqdm import tqdm
import subprocess
from get_title import get_youtube_title_id
from upload import upload_file
from send_mail import send_email
import re
import logging
from setup_ffmpeg import setup_ffmpeg
logging.basicConfig(level=logging.DEBUG)

def sanitize_filename(filename):
    return re.sub(r'[<>:"/\\|?*\x00-\x1F]', '_', filename)

def encode_filename(filename):
    print(f"Encoding file: {filename}")
    sanitized_filename = sanitize_filename(filename)
    outfile = sanitized_filename.replace('.mp4', '_encoded.mp4')
    command = f'ffmpeg -i "{sanitized_filename}" -y -c copy -avoid_negative_ts make_zero "{outfile}"'
    subprocess.run(command, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
    print(f"Encoded file saved as: {outfile}")
    return outfile

def run_command(command):
    cmd = command
    result = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    return result.stdout

def download_stream(url, title, filename, channel_id):
    filename = sanitize_filename(filename)
    try:
        command = f"./ytarchive --save --verbose --live-from '0h00m00s' -o '{title}' https://www.youtube.com/channel/{channel_id}/live  best"
        print(f"Running command: {command}")
        print(f"Downloading Stream: {title}")
        run_command(command)
        stream = f'{title}.mp4'
        if not stream:
            print("No streams found!")
            return None
    except KeyboardInterrupt:
        print("\nDownload interrupted! Encoding the partially downloaded file...")
        out = encode_filename(filename)
        if os.path.exists(filename):
            os.remove(filename)
        out.replace('_encoded.mp4', '.mp4')
        return out
    except Exception as e:
        print(f"An error occurred: {e}")
        if os.path.exists(filename):
            out = encode_filename(filename)
            os.remove(filename)
        out.replace('_encoded.mp4', '.mp4')
        return out
    out = encode_filename(filename)
    if os.path.exists(filename):
        os.remove(filename)
    out.replace('_encoded.mp4', '.mp4')
    return out

def main_process(channel_id, emails, nyberman: bool = False):
    print(f"Checking for live streams on {channel_id}...")
    try:
        title, _, url = get_youtube_title_id(channel_id)
    except Exception as e:
        print("No Live Streams Currently.")
        return None
    print(f"Found live stream: {title}")
    sanitized_title = sanitize_filename(title)
    print(f"Downloading stream: {title}")
    file = download_stream(url, sanitized_title, f'{sanitized_title}.mp4', channel_id)
    if file is None:
        print("No Live Streams Currently.")
        return None
    else:
        print(f"Downloaded and encoded file saved as: {file}")
        print("Uploading file...")
        if os.path.exists(file):
            if nyberman:
                id = upload_file(file, os.getenv("BUZZ_API"), os.getenv("BUZZ_FOLDER_NYBERMAN"))
            else:
                id = upload_file(file, os.getenv("BUZZ_API"), os.getenv("BUZZ_FOLDER_GENERAL"))
            if id:
                file_url = f"https://buzzheavier.com/f/{id}"
                print(f"File uploaded successfully! URL: {file_url}")
                send_email(emails, title, file_url, youtube_url=url)
                os.remove(file)
                return file_url
            else:
                print("Failed to upload file.")
                os.remove(file)
                return None
        else:
            print(f"Encoded file not found: {file}")
            os.remove(file)
            return None


def main(yt_id, emails: list, nyberman=False):
    setup_ffmpeg()
    main_process(yt_id, emails, nyberman)

main('UChXsCcj64gdYp8FVCFTzwiw', ['raannakasturi@gmail.com', 'kothariprarthi@gmail.com'], nyberman=False)
