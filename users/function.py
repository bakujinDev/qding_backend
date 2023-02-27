import urllib
from rest_framework import status
from rest_framework.response import Response
from rest_framework.exceptions import ParseError, NotFound
from django.conf import settings
from users.models import Notification


def subscribe_notification(model, request_user, create_or_delete=False):
    subscribeExist = model.notification_user.filter(pk=request_user.pk).exists()

    if subscribeExist:
        if create_or_delete:
            model.notification_user.remove(request_user)

            return "remove"
    else:
        model.notification_user.add(request_user)

        return "create"


def add_notification(
    user,
    content,
    push_url,
):
    Notification.objects.create(
        user=user,
        content=content,
        push_url=urllib.parse.urljoin(settings.BASE_URL, push_url),
    )


def add_notifications_to_user_list(
    model,
    request_user,
    content,
    push_url,
):
    for user in model.notification_user.all():
        if user == request_user:
            continue

        Notification.objects.create(
            user=user,
            content=content,
            push_url=urllib.parse.urljoin(settings.BASE_URL, push_url),
        )

        subscribe_notification(model=model, request_user=request_user)
