from __future__ import unicode_literals

from django.db import models
from django.utils import timezone


class Message(models.Model):
    group = models.ForeignKey(
        'group.Group',
        on_delete=models.CASCADE
    )
    user = models.ForeignKey(
        'account.User',
        on_delete=models.CASCADE
    )
    message = models.TextField()
    timestamp = models.DateTimeField(default=timezone.now, db_index=True)

    def __unicode__(self):
        return '[{timestamp}] {handle}: {message}'.format(**self.as_dict())

    @property
    def formatted_timestamp(self):
        return self.timestamp.strftime('%b %-d %-I:%M %p')
    
    def as_dict(self):
        return {'handle': self.handle, 'message': self.message, 'timestamp': self.formatted_timestamp}



