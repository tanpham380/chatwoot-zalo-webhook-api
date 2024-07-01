
# # @app.route('/zalo/receive', methods=['GET', 'POST'])
# # async def zalo_receive():
# #     if request.method == 'GET':
# #         return Response("Event received", status=200)

# #     elif request.method == 'POST':
# #         data = request.get_json()
# #         headers = request.headers
# #         print("data : ", data)
# #         zalo_id = data.get("sender", {"id": ""}).get("id")
# #         if data and "X-ZEvent-Signature" in headers:
# #             if verify_oa_secret_key(data, headers, request.data):
# #                 return Response("Invalid signature", status=400)
# #         if zalo_id == "":
# #             return Response("Invalid Zalo ID", status=400)
# #         try:
# #             if zalo_id == "3202842660808701267":
# #                 return Response("Event received", status=200)

# #             contact_exists = await ChatWootController.searchcontact(zalo_id)
# #             if not contact_exists:
# #                 await createContant(zalo_id)
                
                
# #             app_id=data.get("app_id" , ""),
# #             if app_id =="":
# #                 return Response("Event received", status=200)
            
# #             if data["message"].get("text", "") is None:
# #                 data["message"]["text"] = ""
# #             message_text = data["message"].get("text", "")
# #             attachments = []
# #             if data["message"].get("attachments"):
# #                 attachment_data = data["message"]["attachments"]
# #                 if attachment_data is None:
# #                     return Response("Event received", status=200)
# #                 for payload_data in attachment_data :
        
# #                     if "payload" in payload_data and payload_data["type"] == "image" :
# #                         if "url" in payload_data["payload"]:
# #                             url = payload_data["payload"]["url"]
# #                             attachments.append(url)
# #                     elif "payload" in payload_data and payload_data["type"] == "audio" :
# #                         if "url" in payload_data["payload"]:
# #                             url = payload_data["payload"]["url"]
# #                             attachments.append(url)
# #                     elif "payload" in payload_data and payload_data["type"] == "video" :
# #                         if "url" in payload_data["payload"]:
# #                             url = payload_data["payload"]["url"]
# #                             attachments.append(url)
# #                     elif "payload" in payload_data and payload_data["type"] == "sticker" :
# #                         if "url" in payload_data["payload"]:
# #                             url = payload_data["payload"]["url"]
# #                             attachments.append(url)
# #                     elif "payload" in payload_data and payload_data["type"] == "file" :
# #                         if "url" in payload_data["payload"]:
# #                             url = payload_data["payload"]["url"]
# #                             message_text =+ url
# #                     elif "payload" in payload_data and payload_data["type"] == "link" :
# #                         url = payload_data["payload"]["url"]
# #                         message_text =+ url
# #                     elif "payload" in payload_data and payload_data["type"] == "location" :
# #                         location = payload_data["payload"]["coordinates"]
# #                         message_text =+ location['latitude'] + " " + location['longitude']
# #                     else :
# #                         url = payload_data["payload"]["url"]
# #                         attachments.append(payload_data)
# #             coversation_ID = await ChatWootController.getcoversation(zalo_id)
            
# #             print("coversation_ID", coversation_ID)
# #             print("attachments", attachments)
# #             print("message_text", message_text)
# #             print("EventMessageZaloOA", EventMessageZaloOA(data.get('event_name', '')))
# #             # if coversation_ID != None :
# #             #     if attachments != None:
# #             #         await ChatWootController.process_message(message_text, type_message=EventMessageZaloOA(data.get('event_name', '')), coversation_id=coversation_ID, attachment=attachments)
# #             #     else :
# #             #         await ChatWootController.process_message(message_text, type_message=EventMessageZaloOA(data.get('event_name', '')), coversation_id=coversation_ID, attachment=None)
# #             # await ChatWootController.process_message("Hello World2", type_message="incoming" , coversation_id="71" , attachment=None)

# #             return Response("Event received", status=200)

# #         except json.JSONDecodeError:
# #             return Response("Invalid JSON payload", status=400)

# #     else:
# #         return Response("Invalid request method", status=405)
    
    
    
    
    
# #     @app.route('/zalo/receive', methods=['GET', 'POST'])
# # async def zalo_receive():
# #     if request.method == 'GET':
# #         return Response("Event received", status=200)

# #     elif request.method == 'POST':
# #         data = request.get_json()
# #         zalo_id = data.get("sender", {}).get("id", "")  # Safer extraction
# #         print("data : ", data)
# #         # Early exit for invalid signature or specific Zalo ID
# #         if verify_oa_secret_key(data, request.headers, request.data):
# #             return Response("Invalid signature or specific Zalo ID", status=400)
# #         # if zalo_id == "3202842660808701267":
# #         #     return Response("Invalid signature or specific Zalo ID", status=200)
# #         try:
# #             # Check contact existence and create if needed
# #             contact_exists = await ChatWootController.searchcontact(zalo_id)
# #             if not contact_exists:
# #                 await createContant(zalo_id)

# #             # Extract and process message details
# #             app_id = data.get("app_id", "")
# #             if not app_id:
# #                 return Response("Event received", status=200) 
            
# #             message_text = data["message"].get("text", "")
# #             attachments = []

# #             for attachment_data in data["message"].get("attachments", []):
# #                 if "payload" in attachment_data:
# #                     payload = attachment_data["payload"]
# #                     attachment_type = attachment_data["type"]
# #                     url = payload.get("url")

# #                     if attachment_type in ("image", "audio", "video", "sticker"):
# #                         if url:
# #                             attachments.append(url)
# #                     elif attachment_type == "file":
# #                         if url:
# #                             message_text += url
# #                     elif attachment_type in ("link", "location"):
# #                         if url:
# #                             message_text += url
# #                         if attachment_type == "location":
# #                             location = payload.get("coordinates")
# #                             if location:
# #                                 message_text += f"Vị trí latitude {location['latitude']} : vị trí longitude {location['longitude']}"

# #             coversation_ID = await ChatWootController.getcoversation(zalo_id)
# #             print("coversation_ID", coversation_ID)
# #             print("attachments", attachments)
# #             print("message_text", message_text)
# #             print("EventMessageZaloOA", EventMessageZaloOA(data.get('event_name', '')))
# #             # Send message to ChatWoot (conditionally)
# #             if attachments == [] :
# #                 await ChatWootController.process_message(
# #                     content = message_text, 
# #                     type_message=EventMessageZaloOA(data.get('event_name', '')), 
# #                     conversation_id=coversation_ID,
# #                     attachments = None
# #                 )
# #             else :
# #                 await ChatWootController.process_message(
# #                     message_text, 
# #                     type_message=EventMessageZaloOA(data.get('event_name', '')), 
# #                     conversation_id=coversation_ID,
# #                     attachments = attachments
# #                 )
# #             # if coversation_ID is not None:
# #             #     await ChatWootController.process_message(
# #             #         message_text, 
# #             #         type_message=EventMessageZaloOA(data.get('event_name', '')), 
# #             #         coversation_id=coversation_ID, 
# #             #         attachment=attachments if attachments else None  # Pass attachments conditionally
# #             #     )

# #             return Response("Event received", status=200)

# #         except json.JSONDecodeError:
            
# #             return Response("Invalid JSON payload", status=400)

# #     else:
# #         return Response("Invalid request method", status=405) 



# @app.route('/zalo/receive', methods=['GET', 'POST'])
# async def zalo_receive():
#     if request.method == 'GET':
#         return Response("Event received", status=200)

#     elif request.method == 'POST':
#         data = request.get_json()
#         zalo_id = data.get("sender", {}).get("id", "")  # Safer extraction
#         print("data : ", data)
#         # Early exit for invalid signature or specific Zalo ID
#         if verify_oa_secret_key(data, request.headers, request.data):
#             return Response("Invalid signature or specific Zalo ID", status=400)
#         if zalo_id == "3202842660808701267":
#             zalo_id = data.get("recipient", {}).get("id", "")
        
#         try:
#             # Check contact existence and create if needed
#             contact_exists = await ChatWootController.searchcontact(zalo_id)
#             if not contact_exists:
#                 await createContant(zalo_id)

#             # Extract and process message details
#             app_id = data.get("app_id", "")
#             if not app_id:
#                 return Response("Event received", status=200) 
            
#             message_text = data["message"].get("text", "")
#             attachments = []

#             for attachment_data in data["message"].get("attachments", []):
#                 if "payload" in attachment_data:
#                     payload = attachment_data["payload"]
#                     attachment_type = attachment_data["type"]
#                     url = payload.get("url")

#                     if attachment_type in ("image", "audio", "video", "sticker" , "gif"):
#                         if url:
#                             attachments.append(url)
#                     elif attachment_type == "file":
#                         if url:
#                             message_text += url
#                     elif attachment_type in ("link", "location"):
#                         if url:
#                             message_text += url
#                         if attachment_type == "location":
#                             location = payload.get("coordinates")
#                             if location:
#                                 message_text += f"Vị trí latitude {location['latitude']} : vị trí longitude {location['longitude']}"

#             coversation_ID = await ChatWootController.getcoversation(zalo_id)
#             if coversation_ID == 91:
#                 message_text = f"{message_text} (Zalo ID: {zalo_id})"
#             print("coversation_ID", coversation_ID)
#             print("attachments", attachments)
#             print("message_text", message_text)
#             print("EventMessageZaloOA", EventMessageZaloOA(data.get('event_name', '')))
#             # Send message to ChatWoot (conditionally)
#             if attachments == [] :
#                 await ChatWootController.process_message(
#                     content = message_text, 
#                     type_message=EventMessageZaloOA(data.get('event_name', '')), 
#                     conversation_id=coversation_ID,
#                     attachments = None
#                 )
#             else :
#                 await ChatWootController.process_message(
#                     message_text, 
#                     type_message=EventMessageZaloOA(data.get('event_name', '')), 
#                     conversation_id=coversation_ID,
#                     attachments = attachments
#                 )
#             # if coversation_ID is not None:
#             #     await ChatWootController.process_message(
#             #         message_text, 
#             #         type_message=EventMessageZaloOA(data.get('event_name', '')), 
#             #         coversation_id=coversation_ID, 
#             #         attachment=attachments if attachments else None  # Pass attachments conditionally
#             #     )

#             return Response("Event received", status=200)

#         except json.JSONDecodeError:
            
#             return Response("Invalid JSON payload", status=400)

#     else:
#         return Response("Invalid request method", status=405) 

