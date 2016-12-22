import zipfile
import os
import os.path as P
import requests
import tempfile
import urllib
import json
import sys


class AudioLoader(object):
    def __init__(self, owner_id, count):
        access_token = 'defdd41f07aba99b71e9f1435ef8f9fdf95e2a334bdab2ab8b07d7' \
                       '02505b070a991a5c526bafa717ef019'
        url_base = 'https://api.vk.com/method/audio.get'

        self.params = {
            "owner_id": owner_id,  # 126788602,
            "count": count,  # 2,
            "access_token": access_token,
            "v": "5.57"
        }

        params_compiled = urllib.parse.urlencode(self.params)
        self.url = "%s?%s" % (url_base, params_compiled)

    def get_audio(self):
        response = requests.get(self.url)
        directory_name = tempfile.mkdtemp()

        response_data = response.json()
        response = response_data.get('response')

        print(response)

        if not response or len(response) == 0:
            sys.exit()

        zip_f = zipfile.ZipFile('%s.zip' % (self.params["owner_id"]), 'w')
        for audio in response_data['response']['items']:
            print("{artist} - {title}".format(**audio))

            audio_file = tempfile.NamedTemporaryFile(dir=directory_name)

            audio_response = requests.get(audio['url'])
            audio_file.write(audio_response.content)

            zip_f.write(P.join(directory_name, audio_file.name),
                        arcname="{artist} - {title}.mp3".format(**audio))

        return zip_f

            # url = 'https://api.vk.com/method/audio.get?'\
            #     'owner_id=%s&count=%s&access_token=%s&v=5.57' % (owner_id, count, access_token)