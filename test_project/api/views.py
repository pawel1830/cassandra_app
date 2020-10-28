from django.core.exceptions import ValidationError
from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework import status
from django.core.validators import validate_email
import logging
from django.core.mail import send_mail
from rest_framework.views import APIView
from django.conf import settings

from .models import Message
from .serializer import MessageSerializer

logger = logging.getLogger(__name__)


class MessageSendView(APIView):

    def validate_magic_number(self, magic_number):
        if not magic_number:
            return 0, 'Magic number not exists'
        try:
            int(magic_number)
        except ValueError:
            return 0, 'Magic number must be int'
        return 1, ''

    def post(self, request, *args, **kwargs):
        email_user = settings.EMAIL_HOST_USER
        request_data = JSONParser().parse(request)
        magic_number = request_data.get('magic_number')
        ok, error = self.validate_magic_number(magic_number)
        if not ok:
            return Response(
                data={"errors": error},
                status=status.HTTP_400_BAD_REQUEST
            )
        messages = Message.objects.filter(magic_number=int(magic_number))
        for message in messages:
            try:
                send_mail(message.title, message.content, email_user, [message.email],
                          fail_silently=False)
                message.delete()
            except Exception as e:
                logger.error(e)
                return Response({'errors': 'Internal Error'},
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response({"message": "Messages send"})


class MessageListView(ListAPIView):
    serializer_class = MessageSerializer

    def get_queryset(self):
        email_value = self.kwargs['email_value']
        return Message.objects.filter(email=email_value)

    def get(self, request, *args, **kwargs):
        try:
            email_value = self.kwargs['email_value']
            validate_email(email_value)
        except ValidationError:
            return Response({"errors": 'Email invalid'}, status=status.HTTP_400_BAD_REQUEST)
        return super(MessageListView, self).get(request, *args, **kwargs)


class MessageCreateView(CreateAPIView):
    serializer_class = MessageSerializer
