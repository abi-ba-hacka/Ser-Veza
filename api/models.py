from __future__ import unicode_literals

import uuid
import json
import random
from django.db import models
from authemail.models import EmailUserManager, EmailAbstractUser


class Owner(EmailAbstractUser):
    # Required
    objects = EmailUserManager()


class Shelter(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    name = models.CharField(max_length=64)
    address = models.CharField(max_length=64, blank=True)
    city = models.CharField(max_length=64, blank=True)
    state = models.CharField(max_length=64, blank=True)
    country = models.CharField(max_length=64, blank=True)

    class Meta:
        verbose_name = 'Shelter'
        verbose_name_plural = 'Shelters'
        ordering = ('created',)

    def __unicode__(self):
        return ', '.join([self.name, self.city])


class Growler(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    origin = models.ForeignKey(Shelter)
    owner = models.ForeignKey(Owner, related_name='growlers')
    code = models.CharField(max_length=64, unique=True)

    class Meta:
        verbose_name = 'Growler'
        verbose_name_plural = 'Growlers'
        ordering = ('created',)

    def __init__(self, *args, **kwargs):
        super(Growler, self).__init__(*args, **kwargs)

    def save(self, *args, **kwargs):
        self.code = self.code or str(uuid.uuid4()).replace('-', '')[:8]
        super(Growler, self).save(*args, **kwargs)

    def __unicode__(self):
        return '%s from %s' % (self.code, self.owner.email)


class Prize(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    name = models.CharField(max_length=64)

    class Meta:
        verbose_name = 'Prize'
        verbose_name_plural = 'Prizes'
        ordering = ('created',)

    def __unicode__(self):
        return self.name


class Beer(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    name = models.CharField(max_length=64)

    class Meta:
        verbose_name = 'Beer'
        verbose_name_plural = 'Beers'
        ordering = ('created',)

    def __unicode__(self):
        return self.name


class Refill(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    location = models.ForeignKey(Shelter)
    beer = models.ForeignKey(Beer)
    prize = models.ForeignKey(Prize)
    growler = models.ForeignKey(Growler, related_name='refills')

    class Meta:
        verbose_name = 'Refill'
        verbose_name_plural = 'Refills'
        ordering = ('created',)

    def __unicode__(self):
        return self.beer.name
