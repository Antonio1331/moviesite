from django.contrib import admin
from django.utils.safestring import mark_safe
from django.contrib.auth.models import Group
from .models import Genre, Movie, Comment, UserProfile


class CommentInline(admin.StackedInline):
    model = Comment
    extra = 0


class GenreAdmin(admin.ModelAdmin):
    list_display = ('id', 'type')
    list_display_links = ('id', 'type')
    search_fields = ('type',)
    ordering = ('type',)
    fields = ('type',)


class MovieAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'title', 'director', 'genre',
        'author', 'release', 'published', 'get_image'
    )
    list_display_links = ('id', 'title', 'get_image')
    search_fields = ('title', 'description')
    list_filter = ('genre', 'release')
    list_editable = ('director', 'genre', 'published', 'author')
    inlines = [CommentInline]

    def get_image(self, obj: Movie):
        if obj.cover:
            return mark_safe(f"<img src='{obj.cover.url}' width='60px' />")
        return "No Image"
    get_image.short_description = "Cover"

    fieldsets = (
        ("Ma'lumotlar", {
            'fields': ('title', 'director', 'description', 'genre', 'author'),
        }),
        ("Media fayllar", {
            'fields': ('cover', 'video')
        }),
        ("Qo‘shimcha", {
            'fields': ('release', 'published')
        }),
    )


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'bio', 'get_avatar')
    search_fields = ('user__username', 'bio')

    def get_avatar(self, obj):
        if obj.avatar:
            return mark_safe(f"<img src='{obj.avatar.url}' width='40px' />")
        return "No Avatar"
    get_avatar.short_description = "Avatar"



admin.site.register(Genre, GenreAdmin)
admin.site.register(Movie, MovieAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
admin.site.unregister(Group)

@admin.register(Group)
class CustomGroupAdmin(admin.ModelAdmin):
    list_display = ("name",)
