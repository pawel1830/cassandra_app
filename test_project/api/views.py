from smtplib import SMTPException

from django.conf import settings
from django.core import mail
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework import status
from rest_framework.pagination import PageNumberPagination


from .models import Message
from .serializer import MessageSerializer


@api_view(['POST'])
def create_message(request):
    message_data = JSONParser().parse(request)
    message_serializer = MessageSerializer(data=message_data)
    if not message_serializer.is_valid():
        return Response({"errors": message_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    message_serializer.save()
    return JsonResponse(message_serializer.data, status=status.HTTP_201_CREATED)


@api_view(['POST'])
def send_message(request):
    request_data = JSONParser().parse(request)
    magic_number = request_data.get('magic_number')
    if not magic_number:
        return Response({"errors": "Bad magic_number"}, status=status.HTTP_400_BAD_REQUEST)
    messages = Message.objects.filter(magic_number=magic_number)
    try:
        with mail.get_connection() as connection:
            for message in messages:
                mail.EmailMessage(
                    subject=message.title,
                    body=message.content,
                    to=[message.email],
                    connection=connection,
                ).send()
                message.delete()
    except SMTPException:
        return Response({'errors': 'SMTP Error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    except Exception as e:
        return Response({'errors': 'Internal Error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return Response({"message": "Messages send"})


@api_view(['GET'])
def get_messages(request, email_value):
    paginator = PageNumberPagination()
    rest_framework_settings = getattr(settings, 'REST_FRAMEWORK')
    paginator.page_size = rest_framework_settings.get('PAGE_SIZE', 10)
    messages = Message.objects.filter(email=email_value)
    messages_page = paginator.paginate_queryset(messages, request)
    message_serializer = MessageSerializer(messages_page, many=True)
    return paginator.get_paginated_response(message_serializer.data)