from django.db import models


class Tag(models.Model):
    name = models.CharField(max_length=200)
    color = models.CharField(max_length=20)
    slug = models.SlugField(max_length=20, unique=True)

    class Meta:
        ordering = ["id"]

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField(max_length=200)
    measurement_unit = models.CharField(max_length=10)

    class Meta:
        ordering = ["id"]
        # verbose_name = "ingredient"
        # verbose_name_plural = "ingredients"

    def __str__(self):
        return self.name
