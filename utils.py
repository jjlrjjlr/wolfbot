import requests
import hikari
from os import path, makedirs
from hashlib import sha1

def save_file(path: str, filename: str, url: str, id='') -> str:
    '''Downloads a file (url) and saves it to path/filename.
    Returns: The path to the saved file.'''
    makedirs(path, exist_ok=True)
    request = requests.get(url)
    with open(''.join([path, id, filename]), 'wb') as file:
        for chunk in request.iter_content(chunk_size=1024):
            if chunk:
                file.write(chunk)
        file.flush()
        file.close()
    return ''.join([path, filename])