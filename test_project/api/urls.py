from django.contrib import admin
from django.urls import path
from .views import create_message, send_message, get_messages

urlpatterns = [
    path('message', create_message),
    path('send', send_message),
    path('messages/<email_value>', get_messages)
]
