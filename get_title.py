import subprocess
import json

def get_youtube_title_id(channel_id):
    try:
        result = subprocess.run(["streamlink", "--json", f"https://www.youtube.com/channel/{channel_id}/live"], 
                                stdout=subprocess.PIPE, 
                                stderr=subprocess.PIPE, 
                                text=True)
        data = json.loads(result.stdout)
        title = data['metadata']['title']
        id = data['metadata']['id']
        url = f"https://www.youtube.com/watch?v={id}"
    except Exception as e:
        print("Error:", e)
        return None, None
    return title, id, url
