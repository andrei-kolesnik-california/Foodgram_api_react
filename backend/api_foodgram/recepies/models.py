from django.db import models


class Tag(models.Model):
    name = models.CharField(max_length=200)
    color = models.CharField(max_length=20)
    slug = models.SlugField(max_length=20, unique=True)

    class Meta:
        ordering = ["id"]
        verbose_name = "tag"
        verbose_name_plural = "tags"

    def __str__(self):
        return self.name
