from email import utils
import re
import time
import requests
from dotenv import load_dotenv, set_key
import os

from utils import *
import asyncio


class Zalo4rdAppClient:
    def __init__(self):
        self.authCodeUrl = 'https://oauth.zaloapp.com/v4/oa/access_token'
        self.OAAPIUrl = 'https://openapi.zalo.me/v2.0/oa/getoa'
        self.LoginUrl = 'https://oauth.zaloapp.com/v4/oa/permission'
        load_dotenv()
        self.access_token = os.getenv('ACCESS_TOKEN')
        self.refresh_token = os.getenv('REFRESH_TOKEN')
        self.token_expires_at = float(os.getenv('TOKEN_EXPIRES_AT', 0))

    def update_env_file(self, key, value):
        dotenv_path = '.env'
        set_key(dotenv_path, key, value)

    def getAuthUrl(self, url, code_verifier, state):
        login_endpoint = f"{self.LoginUrl}?app_id={os.getenv('ZALO_APP_ID')}&redirect_uri={
            url}&code_challenge={code_verifier}&state={state}"
        return login_endpoint

    def get_access_token(self, code, code_verifier):
        params = {
            'app_id': os.getenv('ZALO_APP_ID'),
            'code': code,
            'grant_type': 'authorization_code',
            'code_verifier': code_verifier,
        }
        response = requests.post(
            url=self.authCodeUrl,
            data=params,
            headers={
                "secret_key": os.getenv('ZALO_APP_SECRET'),
                'Content-Type': 'application/x-www-form-urlencoded'
            }
        )
        accessKey = response.json()
        if accessKey.get('access_token'):
            self.access_token = accessKey['access_token']
            self.refresh_token = accessKey.get('refresh_token')
            self.token_expires_at = time.time() + int(accessKey['expires_in'])
            self.update_env_file('ACCESS_TOKEN', self.access_token)
            self.update_env_file('REFRESH_TOKEN', self.refresh_token)
            self.update_env_file('TOKEN_EXPIRES_AT',
                                 str(self.token_expires_at))
        return accessKey

    def get_access_token_with_refresh_token(self):
        params = {
            'app_id': os.getenv('ZALO_APP_ID'),
            'grant_type': 'refresh_token',
            'refresh_token': self.refresh_token,
        }
        response = requests.post(
            url=self.authCodeUrl,
            data=params,
            headers={
                "secret_key": os.getenv('ZALO_APP_SECRET'),
                'Content-Type': 'application/x-www-form-urlencoded'
            }
        )
        accessKey = response.json()
        if accessKey.get('access_token'):
            self.access_token = accessKey['access_token']
            self.refresh_token = accessKey.get('refresh_token')
            self.token_expires_at = time.time() + int(accessKey['expires_in'])
            self.update_env_file('ACCESS_TOKEN', self.access_token)
            self.update_env_file('REFRESH_TOKEN', self.refresh_token)
            self.update_env_file('TOKEN_EXPIRES_AT',
                                 str(self.token_expires_at))
        return accessKey

    def is_token_expired(self):
        if self.token_expires_at and time.time() > self.token_expires_at:
            return True
        return False

    def get_valid_access_token(self):
        if self.is_token_expired():
            self.get_access_token_with_refresh_token()
        return self.access_token

    def getInforOA(self):
        access_token = self.get_valid_access_token()
        response = requests.get(
            url=self.OAAPIUrl,
            headers={
                "access_token": access_token,
                'Content-Type': 'application/x-www-form-urlencoded'
            }
        )
        return response.json()

    def getInformationUser(self, uid):
        access_token = self.get_valid_access_token()
        params = {"data": f'{{"user_id":"{uid}"}}'}
        response = requests.get(
            url="https://openapi.zalo.me/v3.0/oa/user/detail",
            params=params,
            headers={
                "access_token": access_token,
                'Content-Type': 'application/x-www-form-urlencoded'
            }
        )
        return response.json()

    # def send_message(self, msg, uid, attachment=None):
    #     access_token = self.get_valid_access_token()
    #     print(attachment)
    #     Json_format = {
    #         "recipient": {
    #             "user_id": uid
    #         },
    #         "message": {
    #             "text": msg,
    #             # "attachment": {
    #             #     "type": "template",
    #             #     "payload": {
    #             #             "template_type": "media",
    #             #             "elements": [{
    #             #                 "media_type": "image",
    #             #                 "url": "https://stc-developers.zdn.vn/images/bg_1.jpg"
    #             #             }]
    #             #     }
    #             # }
    #         }
    #     }
    #     # response = requests.post(
    #     #     url="https://openapi.zalo.me/v3.0/oa/message/cs",
    #     #     json=Json_format,
    #     #     headers={
    #     #         "access_token": access_token,
    #     #         'Content-Type': 'application/json'
    #     #     }
    #     # )
    #     # print(response.json())
    #     # return response.json()
    def determine_media_type(self, url):
        # Simple method to determine media type from the file extension
        if url.endswith(('.jpg', '.jpeg', '.png', '.gif')):
            return "image"
        elif url.endswith(('.mp4', '.mov', '.wmv', '.flv')):
            return "video"
        elif url.endswith(('.mp3', '.wav', '.aac')):
            return "audio"
        else:
            return "file"

    async def upload_file(self, file_path_urls):
        access_token = self.get_valid_access_token()

        files_data = await prepare_file_for_chatwoot(file_path_urls)
        files = []
        for file_name, file_content, file_type in files_data:
            files.append(('file', (file_name, file_content, file_type)))
        response = requests.post(
            url="https://openapi.zalo.me/v2.0/oa/upload/file",
            files=files,
            headers={
                "access_token": access_token
            }
        )
        return response.json()

    async def send_message(self, msg, uid, attachments=None):
        access_token = self.get_valid_access_token()
        msg = msg or ''  # Đảm bảo msg không null

        if attachments:
            for url in attachments:
                media_type = self.determine_media_type(url)

                if media_type == "file":
                    response = await self.upload_file([url])
                    response_data = response.get('data', {})
                    if response_data:
                        attachment_type = "file"
                        payload = {"token": response_data.get('token', '')}
                    else:
                        continue
                else:
                    attachment_type = "template"
                    payload = {
                        "template_type": "media",
                        "elements": [{"media_type": media_type, "url": url}]
                    }

                # Gửi tin nhắn vớiảnh kèm theo (chỉ gửi msg với ảnh cuối cùng)
                send_msg = msg if url == attachments[-1] else "" 

                json_format = {
                    "recipient": {"user_id": uid},
                    "message": {
                        "text": send_msg, 
                        "attachment": {
                            "type": attachment_type,
                            "payload": payload
                        }
                    }
                }

                response = requests.post(
                    url="https://openapi.zalo.me/v3.0/oa/message/cs",
                    json=json_format,
                    headers={
                        "access_token": access_token,
                        'Content-Type': 'application/json'
                    }
                )

                try:
                    response.raise_for_status() 
                except requests.exceptions.RequestException as e:
                    print(f"Error sending message: {e}")
        else:
            Json_format = {
                "recipient": {
                    "user_id": uid
                },
                "message": {
                    "text": msg,
                }
            }
            requests.post(
                url="https://openapi.zalo.me/v3.0/oa/message/cs",
                json=Json_format,
                headers={
                    "access_token": access_token,
                    'Content-Type': 'application/json'
                }
            )
