from django.contrib import admin
from .models import Advertise, Article, Category, Comment, View, Subscriber
# Register your models here.


def reject_selected(modeladmin, request, queryset):
    queryset.update(status='rejected', active=False)
    reject_selected.short_description = "Reject selected"


def pend_selected(modeladmin, request, queryset):
    queryset.update(status='pending', active=False)
    pend_selected.short_description = "Pend selected"


def publish_selected(modeladmin, request, queryset):
    queryset.update(status='published', active=True)
    publish_selected.short_description = "Publish selected"


def editor(modeladmin, request, queryset):
    queryset.update(editors_pick=True)
    editor.short_description = "Make selected editors pick"


def remove_editor(modeladmin, request, queryset):
    queryset.update(editors_pick=False)
    remove_editor.short_description = "Remove editors pick"


def trend(modeladmin, request, queryset):
    queryset.update(trend_for='unlimited')
    trend.short_description = "Make selected trend for unlimited time"


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title',  'author', 'publish', 'status')
    list_filter = ('status', 'created', 'publish',
                   'active', 'trend_for', 'revise', 'editors_pick')
    search_fields = ('title', 'body', 'author__username')
    prepopulated_fields = {'slug': ('title',)}
    raw_id_fields = ('author',)
    date_hierarchy = 'publish'
    ordering = ('status', 'publish')
    actions = [reject_selected, pend_selected,
               publish_selected, remove_editor, editor, trend]


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    search_fields = ('category',)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    search_fields = ('body', 'user', 'article',)
    list_display = ('user', 'article', 'created', 'active')
    list_filter = ('created', 'active')


@admin.register(View)
class ViewAdmin(admin.ModelAdmin):
    search_fields = ('article',)
    list_display = ('article', 'click')


@admin.register(Subscriber)
class SusAdmin(admin.ModelAdmin):
    search_fields = ('email',)

@admin.register(Advertise)
class AdsAdmin(admin.ModelAdmin):
    search_fields = ('link','desc')