from __future__ import unicode_literals

import uuid
import json
import random
from django.db import models
from authemail.models import EmailUserManager, EmailAbstractUser


class Owner(EmailAbstractUser):
    # Required
    objects = EmailUserManager()


class Growler(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    owner = models.ForeignKey(Owner, related_name='growlers')
    code = models.CharField(max_length=64, unique=True)

    class Meta:
        verbose_name = 'Growler'
        verbose_name_plural = 'Growlers'
        ordering = ('created',)

    def __init__(self, *args, **kwargs):
        super(Growler, self).__init__(*args, **kwargs)
        self.code = str(uuid.uuid4()).replace('-', '')[:8]

    def __unicode__(self):
        return '%s from %s' % (self.code, self.owner.email)


class Refill(models.Model):
    BEER_BLONDE = 0
    BEER_PORTER = 1
    BEER_CHOICES = (
        (BEER_BLONDE, 'blonde'),
        (BEER_PORTER, 'porter'),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    beer = models.IntegerField(choices=BEER_CHOICES, default=BEER_BLONDE)
    growler = models.ForeignKey(Growler, related_name='refills')

    class Meta:
        verbose_name = 'Refill'
        verbose_name_plural = 'Refills'
        ordering = ('created',)

    def __unicode__(self):
        return self.get_beer_display()
