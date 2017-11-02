import django.dispatch

create_message = django.dispatch.Signal(providing_args=["room", "user", "content", "msg_type"])