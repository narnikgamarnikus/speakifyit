from django.apps import AppConfig


class ChatsConfig(AppConfig):
    name = 'speakifyit.chats'
    verbose_name = "Chats"

    def ready(self):
    	pass
