from datetime import timedelta

from background_task import background
from django.contrib.auth.models import User
from django.utils import timezone

from events.models import Event


@background
def notify_user(user_id):
    user = User.objects.get(id=user_id)
    for event in Event.objects.filter(user=user).filter(was_notified=False) \
            .filter(date__gt=timezone.now() - timedelta(days=1)) \
            .filter(date__lt=timezone.now() + timedelta(days=1)):
        event.notify()
