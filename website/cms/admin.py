from django.contrib import admin
from .models import Post,Tag,Comment,Reply,Category
from django_summernote.admin import SummernoteModelAdmin

# Register your models here.

class ReplyInline(admin.StackedInline):
    model = Reply
    extra = 5


class CommentAdmin(admin.ModelAdmin):
    inlines = [ReplyInline]


class PostAdmin(SummernoteModelAdmin):
    summernote_fields = '__all__'
    search_fields = ('title', 'text')
    list_display = ['title', 'is_public', 'updated_at', 'created_at', 'title_len']
    list_filter = ['is_public', 'tags']
    ordering = ('-updated_at',)

    def title_len(self, obj):
        return len(obj.title)

    title_len.short_description = 'タイトルの文字数'

admin.site.register(Category)
admin.site.register(Post, PostAdmin)
admin.site.register(Comment)
admin.site.register(Reply)
admin.site.register(Tag)


