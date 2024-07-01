import asyncio
import json
import os
from flask import Flask, jsonify, request, redirect, session, url_for, Response
import re
from urllib.parse import quote
import requests
from werkzeug.middleware.proxy_fix import ProxyFix
from packages.chatwootapi.service import WootHook
from packages.zalo.utils import generate_code_challenge, generate_code_verifier, verify_oa_secret_key
# For making HTTP requests to Zalo
from packages.zalo.zaloController import Zalo4rdAppClient
from dotenv import load_dotenv
from models.zalo import Attachment, AttachmentPayload, Message, Recipient, Sender, ZaloMessage, Recipient
from utils import EventMessageZaloOA, baseURLAPP, find_zaloid_value  # Import load_dotenv

app = Flask(__name__)
ZaloController = Zalo4rdAppClient()
load_dotenv()
# Set a secret key for session management
app.secret_key = os.getenv("FLASK_SECRET_KEY")
ChatWootController = WootHook()
appport = 5001
# Apply ProxyFix middleware
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)
# secertKey = ""

async def getcoversation( zalo_id):
    try:
        print("zalo_id", zalo_id)
    # response = await self.chatwoot.conversations.list(account_id=1, inbox_id=4)

        url = f"{os.getenv('CHATWOOT_URL')}/api/v1/accounts/1/conversations/filter"
        
        header = {
            'api_access_token': f'{os.getenv("ACCOUNT_ACCESS_TOKEN")}'
        }
        print("header", header)
        print("url", url)
        filter_value = {
            "payload": [
                {"attribute_key": "zaloid","filter_operator": "equal_to", "values": zalo_id},
                {"attribute_key": "zaloid","filter_operator": "equal_to", "values": zalo_id}
            ]
        }
        print("filter_value", filter_value)

        response = await asyncio.to_thread(requests.post, url, json=filter_value, headers=header)
        
        response.raise_for_status()
        print(response.json())
        result = find_zaloid_value(response.json().get('payload'), zalo_id)
        print(result.get("id", "91"))
        return result.get("id", "91")

    except Exception as err:
        return 91
@app.route('/')
async def index():
    #a = await ChatWootController.inforchatwoot()
    #print(a)
    coversation_ID = await getcoversation("8528810653932220332")
    print(coversation_ID)
    # conver_temp = await a.filter(account_id= 1, attribute_key= "status" , filter_operator= "Equal to" , query_operator=None , values = "12312312312")
    # print(conver_temp)

    # await ChatWootController.process_message("Hello World 4", "outgoing","91", None)

    return "hello world"


@app.route('/login')
def login():
    base_url = baseURLAPP(request, "zalokey")
    encoded_base_url = quote(base_url, safe='')
    code_verifier = generate_code_verifier()
    session['code_verifier'] = code_verifier
    code_challenge = generate_code_challenge(code_verifier)
    # print(code_challenge)

    session['state'] = session.get("state", None)
    if session['state'] is None:
        session['state'] = code_challenge

    # code_challenge = generate_code_challenge(code_verifier)

    session['code_challenge'] = code_challenge
    auth_url = ZaloController.getAuthUrl(
        encoded_base_url, code_challenge, session['state'])
    return redirect(auth_url)


@app.route('/zalokey')
def zalo_success():
    code_challenge = request.args.get('code_challenge', "")
    code = request.args.get('code', "")
    state = request.args.get('state', "")
    oa_id = request.args.get('oa_id')

    if not code_challenge or not code or not state or not oa_id:
        return "Authentication error (missing secret key or state)", 400

    if code_challenge != session['code_challenge'] or state != session['state']:

        return "Zalo Login Failed for code challenge or state mismatch"

    else:
        code_verifier = session.get("code_verifier")

        zalo_Key = ZaloController.get_access_token(code, code_verifier)
        accesskey = zalo_Key.get('access_token', "")
        refreshkey = zalo_Key.get('refresh_token', "")

        return accesskey + "||||||| " + refreshkey


@app.route('/zalo/access_OAInformation')
def zalo_access_OAInformation():
    access_token = request.args.get('access_token')
    if not access_token:
        return "Missing access token", 400

    oa_info = ZaloController.getInforOA(access_token)
    return oa_info


@app.route('/zalo/access_UserInformation')
def zalo_access_UserInformation():
    uid = request.args.get('uid')
    user_info = ZaloController.getInformationUser(uid)
    return user_info


@app.route('/zalo/receive', methods=['GET', 'POST'])
async def zalo_receive():
    if request.method == 'GET':
        return Response("Event received", status=200)

    elif request.method == 'POST':
        data = request.get_json(force=True, silent=True)
        type_message = EventMessageZaloOA(data.get('event_name', ''))
        print(type_message)
        if type_message == "outgoing":
            return Response("Event received", status=200)
        if data is None:
            return Response("Invalid JSON payload", status=400)
        zalo_id = data.get("sender", {}).get("id", "")

        if verify_oa_secret_key(data, request.headers, request.data):
            return Response("Invalid signature or specific Zalo ID", status=400)
        if zalo_id == "3202842660808701267":
            zalo_id = data.get("recipient", {}).get("id", "")

        # Check and create contact
        contact_exists = await ChatWootController.searchcontact(zalo_id)

        if contact_exists == []:
            await createContant(zalo_id)

        # Process message and attachments
        app_id = data.get("app_id", "")
        if not app_id:
            return Response("Event received", status=200)

        message_text = data["message"].get("text", "")
        attachments = []
        for attachment in data["message"].get("attachments", []):
            if "payload" in attachment and "url" in attachment["payload"]:
                attachment_type = attachment["type"]
                url = attachment["payload"]["url"]
                if attachment_type in ("image", "audio", "video", "gif"):
                    attachments.append(url)
                elif attachment_type == "file":
                    message_text += url
                elif attachment_type in ("link", "location", "sticker"):
                    message_text += url

                    if attachment_type == "location":
                        location = attachment["payload"].get("coordinates")
                        if location:
                            message_text += f"Vị trí latitude {location['latitude']} : vị trí longitude {location['longitude']}"

        coversation_ID = await ChatWootController.getcoversation(zalo_id)
        if coversation_ID == 91:
            print("coversation_ID", coversation_ID)

            # re_contact_exists = await ChatWootController.searchcontact(zalo_id)
            # await createContant(zalo_id)
            message_text = f"{message_text} (Zalo ID: {zalo_id})"
        # print("coversation_ID", coversation_ID)
        # print("attachments", attachments)
        # print("message_text", message_text)
        # print("EventMessageZaloOA", EventMessageZaloOA(data.get('event_name', '')))

        await ChatWootController.process_message(
            message_text,
            type_message=type_message,
            conversation_id=coversation_ID,
            attachments=attachments if attachments else None  # Pass attachments conditionally
        )

        return Response("Event received", status=200)

    else:
        return Response("Invalid request method", status=405)


async def createContant(zalo_id):
    user_info = ZaloController.getInformationUser(zalo_id)
    # if user_info.get("data", {}) :
    #     ZaloController.get_access_token_with_refresh_token(zalo_refestoken)
    user_data = user_info.get("data", {})  # Handle potential missing data

    # Use a more concise way to build the name (f-string interpolation)
    name = f"{user_data.get('display_name', '')} "
    # ({user_data.get('user_alias', '')})".strip()
    avatar = user_data.get("avatar", "")

    # Safely access nested dictionaries (shared_info, tags_and_notes_info)
    shared_info = user_data.get("shared_info", {})
    tags_notes_info = user_data.get("tags_and_notes_info", {})

    # Format phone
    phone = f"+{shared_info.get('phone', '')}" if shared_info.get('phone') else ""
    mail = shared_info.get("email", "")
    note = tags_notes_info.get("note", "")
    # Await contact creation and return a more informative message
    API_RESUFLT = await ChatWootController.createContacts(phone, mail, name, avatar, note, zalo_id)
    await ChatWootController.createcoversation(API_RESUFLT, zalo_id)


# Error creating contact: ("operation=not_found_error, response=Response(url='https://crm.cloudday.vn/api/v1/accounts/1/conversations', method='POST', body={'error': 'Resource could not be found'}, headers=Headers({'server': 'nginx/1.18.0 (Ubuntu)', 'date': 'Fri, 28 Jun 2024 02:24:26 GMT', 'content-type': 'application/json; charset=utf-8', 'transfer-encoding': 'chunked', 'connection': 'keep-alive', 'x-frame-options': 'SAMEORIGIN', 'x-xss-protection': '0', 'x-content-type-options': 'nosniff', 'x-download-options': 'noopen', 'x-permitted-cross-domain-policies': 'none', 'referrer-policy': 'strict-origin-when-cross-origin', 'cache-control': 'no-cache', 'x-request-id': 'ef8ad8d1-2628-405f-b001-e446635ad776', 'x-runtime': '0.010377', 'strict-transport-security': 'max-age=31536000; includeSubDomains'}), status_code=404, client_response=<Response [404 Not Found]>)", Response(url='https://crm.cloudday.vn/api/v1/accounts/1/conversations', method='POST', body={'error': 'Resource could not be found'}, headers=Headers({'server': 'nginx/1.18.0 (Ubuntu)', 'date': 'Fri, 28 Jun 2024 02:24:26 GMT', 'content-type': 'application/json; charset=utf-8', 'transfer-encoding': 'chunked', 'connection': 'keep-alive', 'x-frame-options': 'SAMEORIGIN', 'x-xss-protection': '0', 'x-content-type-options': 'nosniff', 'x-download-options': 'noopen', 'x-permitted-cross-domain-policies': 'none', 'referrer-policy': 'strict-origin-when-cross-origin', 'cache-control': 'no-cache', 'x-request-id': 'ef8ad8d1-2628-405f-b001-e446635ad776', 'x-runtime': '0.010377', 'strict-transport-security': 'max-age=31536000; includeSubDomains'}), status_code=404, client_response=<Response [404 Not Found]>))

@app.route('/chatwoot/receive', methods=['POST'])
async def receive_mess_from_chatwoot():
    """Handles incoming messages from Chatwoot."""
    try:
        auth_key = request.args.get('authenticationKey')
        if auth_key != os.getenv("WEBHOOK_CHATWOOT_ACCESSKEY"):
            return Response("Unauthorized", status=401)

        if request.method == 'POST':

            data = request.get_json()

            if data.get('message_type') == 'incoming':
                return Response("Event received", status=200)

            zalo_id = data.get('conversation', {}).get('meta', {}).get(
                'sender', {}).get('custom_attributes', {}).get('zaloid')
            # identifier = data.get('conversation', {}).get(
            #     'meta', {}).get('sender', {}).get('identifier')
            content = data.get('content')
            type_message = data.get('message_type')
            attachments = [a.get('data_url') for a in data.get(
                'attachments', []) if a.get('data_url')]
            # if zalo_id == "8528810653932220332":
            if type_message == "outgoing":
                # Default to True if 'private' key is missing
                private_value = data.get('private', True)

                if private_value:  # Check directly if private_value is True
                    return Response("Event received", status=200)
                else:
                    await ZaloController.send_message(
                        content, zalo_id, attachments)
                    return Response("Event received", status=200)

            return Response("Event received", status=200)
    except Exception as e:
        return Response("Invalid JSON", status=400)


# @app.route('/zalo/send', methods=['POST'])
# def zalo_send():
#     data = request.get_json(force=True, silent=True)
#     if data is None:
#         return Response("Invalid JSON payload", status=400)
#     zalo_id = data.get("recipient_id", "")
#     message = data.get("message", "")
#     if not zalo_id or not message:
#         return Response("Missing recipient ID or message", status=400)
#     # Send message
#     response = ZaloController.send_message(zalo_access_token, zalo_id, message)
#     return jsonify(response)
if __name__ == '__main__':
    app.run(debug=False, port=appport, host='0.0.0.0')
