from django.conf import settings
from users.models import Notification
import urllib


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

        model.notification_user.add(request_user)
