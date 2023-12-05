from django.contrib import admin

from .models import Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'author',
        'text',
    )
    list_filter = ('author', 'name')
    search_fields = ('name',)
