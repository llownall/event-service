from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.db import models
from django.utils.translation import gettext_lazy as _


class EventType(models.IntegerChoices):
    MEETING = 0, _('Встреча')
    CALL = 1, _('Звонок')


class Event(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None, null=True)
    title = models.CharField(max_length=100)
    body = models.TextField()
    date = models.DateTimeField()
    type = models.IntegerField(
        verbose_name='Тип события',
        choices=EventType.choices,
        default=EventType.MEETING
    )
    was_notified = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    def notify(self):
        send_mail(
            'Скоро событие',
            f'Через день запланировано событие "{self.title}"',
            'event.notify.service@mail.ru',
            [self.user.email],
            fail_silently=False,
        )
        self.was_notified = True
        self.save()
