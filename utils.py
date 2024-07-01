


import mimetypes
import os

from PIL import Image
from io import BytesIO
import requests
import aiohttp


def baseURLAPP(request, custom_url=None):
    if custom_url is None:
        baseurl = request.host_url
    else:
        baseurl = request.host_url + custom_url
    # base_url = baseurl.replace(request.host, f"{request.host}:{appport}")
    return baseurl


def find_zaloid_value(data, target_zaloid):
    """
    Searches the provided JSON data for a conversation with the given 'zaloid'.

    Args:
        data (dict): The JSON data to search.
        target_zaloid (str): The zaloid value to look for.

    Returns:
        dict or None: The conversation dictionary containing the matching zaloid, or None if not found.
    """
    try:
        conversations = data
        for conversation in conversations:
            sender = conversation["meta"]["sender"]
            if sender["custom_attributes"].get("zaloid") == target_zaloid:
                return conversation
    except (KeyError, TypeError) as e:
        print(f"Error searching JSON: {e}")
    return None


async def download_file(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                return await response.read()
            else:
                print(f"Failed to download file from {url}")
                return None

def get_file_type(file_name):
    mime_type, _ = mimetypes.guess_type(file_name)
    if mime_type and mime_type.startswith('image/'):
        return 'image'
    return 'application/octet-stream'  # Default to binary file type
ALLOWED_EXTENSIONS = {'.pdf', '.doc', '.docx' , '.png' , '.jpeg' , '.jpg'}
MAX_FILE_SIZE = 5 * 1024 * 1024 
# async def prepare_file_for_chatwoot(attachments):
#     files = []
#     for url in attachments:
#         if not url.startswith("https://"):
#             print("url_to_image")
#             continue
#         # if url == 'url_to_image' or url == 'link' :
#         #     print("url_to_image")
#         #     return
#         file_content = await download_file(url)
#         if file_content:
#             file_name = url.split("/")[-1]
#             file_type = get_file_type(file_name)
#             files.append((file_name, file_content, file_type))
#     return files


ALLOWED_EXTENSIONS = {'.pdf', '.doc', '.docx', '.png', '.jpeg', '.jpg', '.gif', '.tiff', '.tif', '.bmp', '.webp', '.svg', '.ico'}
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5 MB in bytes

async def prepare_file_for_chatwoot(attachments):
    files = []
    print(f"Attachments: {attachments}")
    for url in attachments:
        if not url.startswith("https://"):
            print(f"Skipping non-HTTPS URL: {url}")
            continue

        try:
            file_content = await download_file(url)
            if not file_content:
                print(f"Failed to download file from URL: {url}")
                continue

            file_name = url.split("/")[-1]

            # --- Validation ---
            file_extension = os.path.splitext(file_name)[1].lower()
            print(f"File extension: {file_extension}")
            if file_extension not in ALLOWED_EXTENSIONS:
                raise ValueError("Unsupported file type.")

            file_size = len(file_content)
            if file_size > MAX_FILE_SIZE:
                raise ValueError("File size exceeds the 5MB limit.")

            # Determine file type (MIME type)
            file_type = get_file_type(file_name)

            files.append((file_name, file_content, file_type))

        except (ValueError, Exception) as e:
            print(f"Error processing file from URL {url}: {e}")
            continue

    return files

List_Action_User = ['user_send_location', 'user_send_image' ,'user_send_link' , 'user_send_text', 
                    'user_send_sticker', 'user_send_gif' ,'user_send_audio' ,
                    'user_send_video'  , 'user_send_file' , 'user_reacted_message',
                    "user_send_business_card"]
List_Action_anonymous = ['anonymous_send_location', 'anonymous_send_image' ,'anonymous_send_link' 
                         , 'anonymous_send_text', 'anonymous_send_sticker', 
                         'anonymous_send_gif' ,'anonymous_send_audio' , 'anonymous_send_video'  ,
                         'anonymous_send_file' , 'anonymous_reacted_message']
def EventMessageZaloOA(event_message):
    if event_message in List_Action_User or event_message in List_Action_anonymous:
        return "incoming"
    else:
        return "outgoing"
    


    
# async def download_file(url):
#     async with aiohttp.ClientSession() as session:
#         async with session.get(url) as response:
#             if response.status == 200:
#                 return await response.read()
#             else:
#                 print(f"Failed to download file from {url}")
#                 return None

# async def prepare_file_for_chatwoot(attachments):
#     files = []
#     for url in attachments:
#         file_content = await download_file(url)
#         if file_content:
#             file_name = url.split("/")[-1]
#             files.append(('attachments[]', (file_name, BytesIO(file_content), 'application/octet-stream')))
#     return files

# async def download_file(url):
#     async with aiohttp.ClientSession() as session:
#         async with session.get(url) as response:
#             if response.status == 200:
#                 return await response.read()
#             else:
#                 print(f"Failed to download file from {url}")
#                 return None
# def get_file_type(file_name):
#     mime_type, _ = mimetypes.guess_type(file_name)
#     if mime_type and mime_type.startswith('image/'):
#         return 'image'
#     return 'file' #'application/octet-stream''

# async def prepare_file_for_chatwoot(attachments):
#     files = []
#     for url in attachments:
#         file_content = await download_file(url)
#         if file_content:
#             file_name = url.split("/")[-1]
#             file_type = get_file_type(file_name)
#             files.append(('attachments[]', (file_name, file_content, file_type)))
#     return files


# async def prepare_file_for_chatwoot(attachments):
#     files = []
#     for url in attachments:
#         file_content = await download_file(url)
#         if file_content:
#             file_name = url.split("/")[-1]
#             files.append(('attachments[]', (file_name, file_content, 'application/octet-stream')))
#     return files
# async def prepare_file_for_chatwoot(attachments):
#     files = []
#     for url in attachments:
#         file_content = await download_file(url)
#         if file_content:
#             file_name = url.split("/")[-1]
#             file_type = get_file_type(file_name)
#             files.append({
#                 'file_name': file_name,
#                 'file_content': file_content,
#                 'file_type': file_type
#             })
#     return files