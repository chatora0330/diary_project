from datetime import datetime
from io import BytesIO
from pathlib import Path
from zoneinfo import ZoneInfo

from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse
from PIL import Image

from .models import Page


class PageAccessTest(TestCase):
    def setUp(self):
        self.user_a = User.objects.create_user(
            username="user_a",
            password="testpassword123",
        )

        self.user_b = User.objects.create_user(
            username="user_b",
            password="testpassword123",
        )

        self.page = Page.objects.create(
            user=self.user_a,
            title="Aさんの日記",
            body="これはAさんの日記です。",
            page_date=datetime(2026, 9, 12, 12, 0, tzinfo=ZoneInfo("Asia/Tokyo")),
        )

    def test_user_a_can_view_own_page(self):
        self.client.login(
            username="user_a",
            password="testpassword123",
        )

        response = self.client.get(reverse("diary:page_detail", kwargs={"id": self.page.id}))

        self.assertEqual(response.status_code, 200)

    def test_user_b_cannot_view_user_a_page(self):
        self.client.login(
            username="user_b",
            password="testpassword123",
        )

        response = self.client.get(reverse("diary:page_detail", kwargs={"id": self.page.id}))

        self.assertEqual(response.status_code, 404)

    def test_user_can_see_only_own_pages(self):
        Page.objects.create(
            user=self.user_b,
            title="Bさんの日記",
            body="これはBさんの日記です。",
            page_date=datetime(
                2026,
                9,
                13,
                12,
                0,
                tzinfo=ZoneInfo("Asia/Tokyo"),
            ),
        )

        self.client.login(
            username="user_a",
            password="testpassword123",
        )

        response = self.client.get(reverse("diary:page_list"))

        self.assertContains(response, "Aさんの日記")
        self.assertNotContains(response, "Bさんの日記")

    def test_user_b_cannot_update_user_a_page(self):
        self.client.login(
            username="user_b",
            password="testpassword123",
        )

        response = self.client.get(reverse("diary:page_update", kwargs={"id": self.page.id}))

        self.assertEqual(response.status_code, 404)

    def test_user_b_cannot_delete_user_a_page(self):
        self.client.login(
            username="user_b",
            password="testpassword123",
        )

        response = self.client.post(reverse("diary:page_delete", kwargs={"id": self.page.id}))

        self.assertEqual(response.status_code, 404)

        self.assertTrue(Page.objects.filter(id=self.page.id).exists())

    def test_replace_picture_deletes_old_picture(self):
        self.client.login(
            username="user_a",
            password="testpassword123",
        )

        old_image = BytesIO()
        Image.new("RGB", (100, 100)).save(old_image, format="JPEG")
        old_image.seek(0)

        self.page.picture = SimpleUploadedFile(
            "old.jpg",
            old_image.read(),
            content_type="image/jpeg",
        )
        self.page.save()

        old_picture_path = self.page.picture.path

        new_image = BytesIO()
        Image.new("RGB", (100, 100)).save(new_image, format="JPEG")
        new_image.seek(0)

        self.page.picture = SimpleUploadedFile(
            "new.jpg",
            new_image.read(),
            content_type="image/jpeg",
        )
        self.page.save()

        self.assertFalse(Path(old_picture_path).exists())
        self.assertTrue(Path(self.page.picture.path).exists())

    def test_page_list_pagination(self):
        self.client.login(
            username="user_a",
            password="testpassword123",
        )

        for number in range(2, 12):
            Page.objects.create(
                user=self.user_a,
                title=f"日記{number}",
                body=f"日記{number}の本文です。",
                page_date=datetime(
                    2026,
                    9,
                    number,
                    12,
                    0,
                    tzinfo=ZoneInfo("Asia/Tokyo"),
                ),
            )

        response = self.client.get(reverse("diary:page_list"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["page_obj"]), 10)
        self.assertTrue(response.context["page_obj"].has_next())

        response = self.client.get(
            reverse("diary:page_list"),
            {"page": 2},
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["page_obj"]), 1)
        self.assertFalse(response.context["page_obj"].has_next())
        self.assertTrue(response.context["page_obj"].has_previous())
