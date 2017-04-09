from django.contrib import admin
from .models import *
# Register your models here.


@admin.register(Shelter)
class ShelterAdmin(admin.ModelAdmin):
    list_display = ['name', 'address', 'city', 'state', 'country']
    search_fields = ['name', 'city', 'state']


@admin.register(Beer)
class BeerAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']


@admin.register(Prize)
class PrizeAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']


@admin.register(Growler)
class GrowlerAdmin(admin.ModelAdmin):
    list_display = ['owner', 'created', 'code']
    readonly_fields = ['code']
    search_fields = ['code']


@admin.register(Refill)
class RefillAdmin(admin.ModelAdmin):
    list_display = ['user', 'created', 'beer', 'prize']

    def beer(self, obj):
        return obj.get_beer_display()

    def prize(self, obj):
        return obj.get_prize_display()

    def user(self, obj):
        owner = obj.growler.owner
        return "%s %s" % (owner.first_name, owner.last_name)
