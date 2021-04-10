from django.contrib import admin
from .models import Profile, CreatorProfile


def approve_selected(modeladmin, request, queryset):
    queryset.update(is_approved=True)
    approve_selected.short_description = "Approve Selected"


def remove_approval(modeladmin, request, queryset):
    queryset.update(is_approved=False)
    remove_approval.short_description = "Remove approval of Selected"


def ban_selected(modeladmin, request, queryset):
    queryset.update(banned=True)
    ban_selected.short_description = "Ban selected user"


def lift_ban(modeladmin, request, queryset):
    queryset.update(banned=False)
    lift_ban.short_description = "Lift ban"


def make_creator(modeladmin, request, queryset):
    queryset.update(is_creator=True)
    make_creator.short_description = "Make creator"


def remove_creator(modeladmin, request, queryset):
    queryset.update(is_creator=False)
    remove_creator.short_description = "Remove creator"


class ProfileAdmin(admin.ModelAdmin):
    search_fields = ('id', 'user__username',
                     'user__first_name', 'user__last_name')
    list_display = ('user', 'is_creator', 'is_anonymous')
    list_filter = ('is_creator', 'is_anonymous')
    actions = [make_creator, remove_creator]


class CreatorProfileAdmin(admin.ModelAdmin):
    search_fields = ('id', 'user__username', 'user__first_name',
                     'user__last_name', 'phonenumber', 'channel_name')
    list_display = ('user', 'channel_name', 'is_approved', 'banned')
    list_filter = ('is_approved', 'banned')
    actions = [approve_selected, remove_approval, ban_selected, lift_ban]


admin.site.register(Profile, ProfileAdmin)
admin.site.register(CreatorProfile, CreatorProfileAdmin)
