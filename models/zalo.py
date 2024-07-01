from dataclasses import dataclass, field
from typing import List, Optional




@dataclass
class coordinates:
    latitude : str = None
    longitude: str = None
    
@dataclass
class AttachmentPayload:
    thumbnail: Optional[str] = None
    coordinate: Optional[coordinates] = None
    url: Optional[str] = None
    id: Optional[str] = None

@dataclass
class Attachment:
    id : str = None
    type: Optional[str] = None
    payload: Optional[AttachmentPayload] = None


@dataclass
class Message:
    msg_id: str = None
    text: str = None
    attachments: Optional[List[Attachment]] = None

@dataclass
class Recipient:
    id: str

@dataclass
class Sender:
    id: str

@dataclass
class ZaloMessage:
    app_id: Optional[str] = None
    event_name: Optional[str] = None
    user_id_by_app: Optional[str] = None
    timestamp: Optional[str] = None
    sender: Sender = field(default_factory=Sender)
    recipient: Recipient = field(default_factory=Recipient)
    message: Optional[Message] = None
    recipient: Recipient = field(default_factory=Recipient)
    
    
#             zalo_message = ZaloMessage(
#     event_name=data.get("event_name"),
#     app_id=data.get("app_id"),
#     user_id_by_app = data.get("user_id_by_app"),
#     timestamp=data.get("timestamp"),
#     sender=Sender(id=data["sender"]["id"]),
#     recipient=Recipient(id=data["recipient"]["id"]),
#     message=Message(msg_id=data["message"]["msg_id"], text=data["message"]["text"])
# )    
    
    
