import uuid
from pathlib import Path

from django.contrib.auth.models import User
from django.db import models


class Page(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="pages", 
        verbose_name="ユーザー",
    )
    
    id = models.UUIDField(
        primary_key=True, 
        default=uuid.uuid4, 
        editable=False, 
        verbose_name="ID",
    )
    
    title = models.CharField(max_length=100, verbose_name="タイトル")
    
    body = models.TextField(max_length=2000, verbose_name="本文")
    
    page_date = models.DateTimeField(verbose_name="日付")
    
    picture = models.ImageField(
        upload_to="diary/picture/", 
        blank=True, 
        null=True, 
        verbose_name="写真",
    )
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="作成日時")
    
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新日時")

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        old_page = None

        if self.pk:
            old_page = Page.objects.filter(pk=self.pk).first()

        if old_page and old_page.picture and old_page.picture != self.picture:
            Path(old_page.picture.path).unlink(missing_ok=True)

        super().save(*args, **kwargs)    

    def delete(self, *args, **kwargs):
        picture = self.picture
        super().delete(*args, **kwargs)
        if picture:
            Path(picture.path).unlink(missing_ok=True)
