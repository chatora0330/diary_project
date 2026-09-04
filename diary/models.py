import uuid

from django.db import models


class Page(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, verbose_name="ID")
    title = models.CharField(max_length=100, verbose_name="タイトル")
    body = models.TextField(max_length=2000, verbose_name="本文")
    page_date = models.DateTimeField(verbose_name="日付")
    picture = models.ImageField(
        upload_to="diary/picture/", blank=True, null=True, verbose_name="写真")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="作成日時")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新日時")

    def __str__(self):
        return self.title
