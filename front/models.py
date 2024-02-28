from django.db import models
from datetime import date


NEWS_CATEGORY = (
    ("Health", "Health"),
    ("Research", "Research"),
    ("Information", "Information"),
    ("Anouncement", "Anouncement"),
)
GALLERY_CATEGORY = (
    ("Seminar", "Seminar"),
    ("Training", "Training"),
    ("Report", "Report"),
)


class NewsCategory(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        ordering = ("-id",)

    def __str__(self):
        return self.name


class GalleryCategory(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        ordering = ("-id",)

    def __str__(self):
        return self.name
