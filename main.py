import os
import streamlink
from tqdm import tqdm
import subprocess
from get_title import get_youtube_title_id
from upload import upload_file
from send_mail import send_email
import re

def sanitize_filename(filename):
    return re.sub(r'[<>:"/\\|?*\x00-\x1F]', '_', filename)

def encode_filename(filename):
    sanitized_filename = sanitize_filename(filename)
    outfile = sanitized_filename.replace('.mp4', '_encoded.mp4')
    command = f'ffmpeg -i "{sanitized_filename}" -y -c copy -avoid_negative_ts make_zero "{outfile}"'
    subprocess.run(command, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
    return outfile

def download_stream(url, title, filename):
    filename = sanitize_filename(filename)
    urls = streamlink.streams(url)
    stream = urls.get("best")
    if not stream:
        print("No streams found!")
        return None
    print(f"Downloading Stream: {title}")
    try:
        with open(filename, 'wb') as out_file:
            with stream.open() as fd:
                with tqdm(unit='B', unit_scale=True, desc=filename) as pbar:
                    while True:
                        data = fd.read(1024)
                        if not data:
                            break
                        out_file.write(data)
                        pbar.update(len(data))
    except KeyboardInterrupt:
        print("\nDownload interrupted! Encoding the partially downloaded file...")
        out = encode_filename(filename)
        if os.path.exists(filename):
            os.remove(filename)
        return out
    except Exception as e:
        print(f"An error occurred: {e}")
        if os.path.exists(filename):
            out = encode_filename(filename)
            os.remove(filename)
        return out
    out = encode_filename(filename)
    if os.path.exists(filename):
        os.remove(filename)
    return out

def main(channel_id, emails, nyberman: bool = False):
    try:
        title, _, url = get_youtube_title_id(channel_id)
    except Exception as e:
        print("No Live Streams Currently.")
        return None
    sanitized_title = sanitize_filename(title)
    file = download_stream(url, sanitized_title, f'{sanitized_title}.mp4')
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
                send_email(emails, title, file_url)
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
