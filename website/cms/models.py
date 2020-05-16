from django.conf import settings
from django.db import models
from django.utils import timezone
from django.forms import ModelForm, TextInput, Textarea

# Create your models here.
class Tag(models.Model):    
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Post(models.Model):
    """記事"""
    category = models.ForeignKey(Category,on_delete=models.PROTECT)
    title = models.CharField('タイトル',max_length=32)
    text = models.TextField('本文')
    tags = models.ManyToManyField(Tag,verbose_name ='タグ',blank=True)
    relation_posts = models.ManyToManyField('self',verbose_name ='関連記事',blank=True)
    is_public = models.BooleanField('公開可能か?', default=True)
    description = models.TextField('記事の説明', max_length=130)
    keywords = models.CharField('記事のキーワード', max_length=255, default='記事のキーワード')
    created_at = models.DateTimeField('作成日', default=timezone.now)
    updated_at = models.DateTimeField('更新日', default=timezone.now)
    published_at = models.DateTimeField(blank=True, null=True)
    image = models.ImageField(upload_to='post_images/', null=True, blank=True)

    def __str__(self):
        return self.title

class Comment(models.Model):
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name='comments')
    author = models.CharField(max_length=50)
    text = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(default=False)

    class Meta:
        ordering = ['-timestamp']

    def approve(self):
        self.approved = True
        self.save()

    def __str__(self):
        return self.text


class Reply(models.Model):
    
    comment = models.ForeignKey(
        Comment, on_delete=models.CASCADE, related_name='replies')
    author = models.CharField(max_length=50)
    text = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(default=False)

    def approve(self):
        self.approved = True
        self.save()

    def __str__(self):
        return self.text



class Meta:
    ordering = ['-created_at']
   
    def save(self, *args, **kwargs):
        if self.is_public and not self.published_at:
            self.published_at = timezone.now()
        super().save(*args, **kwargs)

    def __str__(self):

        return self.title