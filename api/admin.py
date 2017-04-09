from django.contrib import admin
from .models import *
# Register your models here.


@admin.register(Growler)
class GrowlerAdmin(admin.ModelAdmin):
    list_display = ['owner', 'created', 'code']
    readonly_fields = ['code']


@admin.register(Refill)
class RefillAdmin(admin.ModelAdmin):
    list_display = ['user', 'created', 'beer']

    def user(self, obj):
        owner = obj.growler.owner
        return "%s %s" % (owner.first_name, owner.last_name)
