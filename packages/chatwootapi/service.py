
import os

import requests
from woot import AsyncChatwoot
from utils import find_zaloid_value, prepare_file_for_chatwoot

import asyncio

class WootHook:
    def __init__(self):
        self.chatwoot = AsyncChatwoot(
            chatwoot_url=os.getenv('CHATWOOT_URL'),
            access_key=os.getenv('ACCOUNT_ACCESS_TOKEN'),

        )
        self.account_id = 1

    async def inforchatwoot(self):
        # return self.chatwoot.messages
        return self.chatwoot.messages

    def get_source_id_for_inbox(self, contact_data, number_check):
        """Trích xuất source_id khi inbox.id bằng  number_check từ dữ liệu contact_inboxes.

        Args:
            contact_data (list): Danh sách các từ điển liên hệ.

        Returns:
            list: Danh sách các giá trị source_id khi inbox.id bằng number_check, hoặc một danh sách trống nếu không tìm thấy.
        """
        source_ids = []

        for contact in contact_data:
            # Kiểm tra xem khóa 'contact_inboxes' có tồn tại trong từ điển `contact` không
            if "contact_inboxes" in contact:
                for inbox_info in contact["contact_inboxes"]:
                    # Kiểm tra xem các khóa 'inbox' và 'id' có tồn tại trong từ điển `inbox_info` không
                    if "inbox" in inbox_info and "id" in inbox_info["inbox"] and inbox_info["inbox"]["id"] == number_check:
                        source_ids.append(inbox_info["source_id"])

        return source_ids

    async def createContacts(self, phone, mail, name, avatar, note, zalo_id):

        for keyword in [zalo_id, phone, mail]:
            contact_info = await self.getsearchcontact(keyword)
            check_contact = contact_info.get("payload", [])
            if check_contact == []:
                continue
            else:
                payload_contact = contact_info['payload']
                source_id = self.get_source_id_for_inbox(payload_contact, 4)
                return source_id[0]

        contact_info = await self.chatwoot.contacts.create(
            identifier=zalo_id,
            account_id=self.account_id,
            avatar_url=avatar,
            inbox_id=4,
            email=mail,
            phone_number=phone,
            name=name,
            custom_attributes={"zaloid": zalo_id, "note": note},
        )

        if contact_info.status_code == 200:
            for inbox in contact_info.body['payload']["contact"]["contact_inboxes"]:
                if inbox["inbox"]["id"] == 4:
                    return inbox["source_id"]

    # async def createContacts(self, phone, mail, name, avatar, note, zalo_id):

    #     for keyword in [zalo_id, phone, mail]:
    #         contact_info = await self.getsearchcontact(keyword)
    #         if contact_info and contact_info.status_code == 200 and contact_info.body.get('payload'):
    #             for inbox in contact_info.body['payload'][0]["contact"]["contact_inboxes"]:
    #                 if inbox["inbox"]["id"] == 4:
    #                     return inbox["source_id"]

    #     contact_info = await self.chatwoot.contacts.create(
    #         identifier=zalo_id,
    #         account_id=self.account_id,
    #         avatar_url=avatar,
    #         inbox_id=4,
    #         email=mail,
    #         phone_number=phone,
    #         name=name,
    #         custom_attributes={"zaloid": zalo_id, "note": note},
    #     )

    #     if contact_info.status_code == 200:
    #         for inbox in contact_info.body['payload']["contact"]["contact_inboxes"]:
    #             if inbox["inbox"]["id"] == 4:
    #                 return inbox["source_id"]

    #     print("Error creating contact or contact not found.")
    #     return False

    async def searchcontact(self, keyword):
        # Combine status code check and payload check into a single condition
        response = await self.chatwoot.contacts.search(account_id=self.account_id, q=keyword)
        # print("search contact", response.body.get('payload'))
        return response.body.get('payload')

    async def getsearchcontact(self, keyword):
        # Combine status code check and payload check into a single condition
        response = await self.chatwoot.contacts.search(account_id=self.account_id, q=keyword)
        return response.body or ""  # Return body if it exists, else an empty string

    async def createcoversation(self, source_id, zalo_id):
        list_agents = await self.chatwoot.inbox.list_agents(account_id=self.account_id, inbox_id=4)
        ids = [item['id'] for item in list_agents.body['payload']]

        await self.chatwoot.conversations.create(
            account_id=self.account_id,
            source_id=source_id,
            assignee_id=ids,
            custom_attributes={"zaloid": zalo_id, },
            status='open'


        )
        # print("Coverstation ID?????",conversations_ID.body)

    # async def getcoversation(self, conversation_id):

    #     response = await self.chatwoot.conversations.list(account_id = 1, inbox_id = 4  )
    #     print(response.body)
    #     if response != None :
    #         return find_zaloid_value(response.body, conversation_id)["id"]

    async def getcoversation(self, zalo_id):
        try:
            print("zalo_id", zalo_id)
        # response = await self.chatwoot.conversations.list(account_id=1, inbox_id=4)

            url = f"{os.getenv('CHATWOOT_URL')}/api/v1/accounts/{self.account_id}/conversations/filter"
            header = {
                'api_access_token': f'{os.getenv("ACCOUNT_ACCESS_TOKEN")}'
            }
            filter_value = {
                "payload": [
                    {"attribute_key": "zaloid","filter_operator": "equal_to", "values": zalo_id},
                    {"attribute_key": "zaloid","filter_operator": "equal_to", "values": zalo_id}
                ]
            }

            response = await asyncio.to_thread(requests.post, url, json=filter_value, headers=header)

            response.raise_for_status()
            print(response.json())
            result = find_zaloid_value(response.json().get('payload'), zalo_id)
            print(result.get("id", "91"))
            return result.get("id", "91")

        except Exception as err:
            return 91

    async def process_message(self, content, type_message, conversation_id, attachments):
        try:
            if attachments:
                file_data = await prepare_file_for_chatwoot(attachments)

                if file_data == [] or file_data is None:
                    await self.chatwoot.messages.create(
                        account_id=1,
                        conversation_id=conversation_id,
                        content=content,
                        message_type=type_message,
                        private=True,
                    )
                else:
                    files_payload = [('attachments[]', (name, content, type))
                                     for name, content, type in file_data]
                    url_api = f"{os.getenv('CHATWOOT_URL')}/api/v1/accounts/1/conversations/{conversation_id}/messages"
                    data = {
                        "content": content,
                        "message_type": type_message,
                        "private": True,
                    }
                    headers = {
                        'api_access_token': f'{os.getenv("ACCOUNT_ACCESS_TOKEN")}'
                    }

                    response = requests.post(url_api, data=data, files=files_payload, headers=headers)
                    response.raise_for_status()  # This will raise an error for bad responses

            else:
                response = await self.chatwoot.messages.create(
                    account_id=1,
                    conversation_id=conversation_id,
                    content=content,
                    message_type=type_message,
                    private=True,

                )
        except Exception as err:
            print(f"Error: {err}")
