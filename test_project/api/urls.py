from django.urls import path
from .views import MessageListView, MessageCreateView, MessageSendView

urlpatterns = [
    path('message', MessageCreateView.as_view(), name='create-message'),
    path('send', MessageSendView.as_view(), name='send-message'),
    path('messages/<email_value>', MessageListView.as_view(), name='get-messages')
]
