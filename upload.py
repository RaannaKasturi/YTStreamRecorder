import requests

def upload_file(file, api_key, folder_id):
    url = f"https://w.buzzheavier.com/{file}?folderId={folder_id}"
    headers = {
        "Authorization": f"Bearer {api_key}"
    }
    with open(file, 'rb') as file_data:
        response = requests.put(url, headers=headers, data=file_data)
        if response.status_code in [200, 201]:
            print("File uploaded successfully.")
            return response.json().get('id', None)
        else:
            print(f"Failed to upload. Status code: {response.status_code}, Response: {response.text}")
            return None
