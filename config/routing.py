from channels.routing import route, include
from speakifyit.chats.consumers import chat_connect, chat_message, chat_disconnect, chat_join, chat_leave, chat_send, chat_contact

websocket_chat_routing = [
    route("websocket.connect", chat_connect, ),
    route("websocket.receive", chat_message, ),
    route("websocket.disconnect", chat_disconnect, ),
]

chat_routing = [
    # Handling different chat commands (websocket.receive is decoded and put
    # onto this channel) - routed on the "command" attribute of the decoded
    # message.
    route("chat.receive", chat_join, command="^join$"),
    route("chat.receive", chat_leave, command="^leave$"),
    route("chat.receive", chat_send, command="^send$"),
    route("chat.receive", chat_contact, command="^contact$"),
]

channel_routing = [
    include(websocket_chat_routing),
    include(chat_routing),
]
