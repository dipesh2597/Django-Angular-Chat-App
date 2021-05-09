import json
from channels import Channel,Group
from channels.sessions import channel_session
from urllib.parse import parse_qs
from .models import ChatMessage,ChatSession
from channels.auth import channel_session_user
import json
from urllib import parse

from channels import Group
from channels.sessions import channel_session

def msg_consumer(message):
    # Save to model
    print("message consumer",message.content)
    session_uuid = message.content['session_uuid']
    # Broadcast to listening sockets
    message.channel_name = session_uuid
    print("message sending to group")
    Group("%s" % session_uuid).send({
        "text": message.content['message'],
    })
    print("message sent")

# Connected to websocket.connect
@channel_session_user
def ws_connect(message):
    # Work out room name from path (ignore slashes)
    print("user >> ",message.user)
    session_uuid = message.content['path'].strip("/")
    print("websocket >> ",session_uuid)
    # Save session_uuid in session and add us to the group
    message.channel_session['session_uuid'] = session_uuid
    query = parse.parse_qs(message['query_string'])
    Group("%s" % session_uuid).add(message.reply_channel)
    # Accept the connection request
    message.reply_channel.send({"accept": True})
    print("reply sent")

# Connected to websocket.receive
@channel_session
def ws_message(message):
    # Stick the message onto the processing queue
    Channel("chat-messages").send({
        "session_uuid": message.channel_session['session_uuid'],
        "message": message['text'],
    })

# Connected to websocket.disconnect
@channel_session
def ws_disconnect(message):
    Group("%s" % message.channel_session['session_uuid']).discard(message.reply_channel)