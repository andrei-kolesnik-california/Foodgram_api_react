from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class Tag(models.Model):
    name = models.CharField(max_length=50)
    color = models.CharField(verbose_name="checkbox color", max_length=20)
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


class Recipe(models.Model):
    tags = models.ManyToManyField(Tag, related_name="recipes")
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='author',
        help_text='Please input author',
        db_index=True,
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        through="RecipeIngredient"
    )
    is_favorited = models.BooleanField(default=False)
    is_in_shopping_cart = models.BooleanField(default=False)
    name = models.CharField(
        verbose_name="name",
        max_length=250,
        db_index=True)
    image = models.ImageField(
        verbose_name="image",
        upload_to="upload"
    )
    text = models.TextField(verbose_name="description")
    cooking_time = models.IntegerField(
        verbose_name="Cooking time in minutes",
    )

    def get_ingredients(self):
        return "\n".join([p.ingredients for p in self.ingredients.all()])

    def get_tags(self):
        return "\n".join([p.tags for p in self.tags.all()])

    class Meta:
        verbose_name = "recipe"
        verbose_name_plural = "recipes"
        # ordering = ["-created"]

    def __str__(self):
        return self.name


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        verbose_name="recipe",
        on_delete=models.CASCADE,
        related_name="recipe_ingredients",
    )
    ingredient = models.ForeignKey(
        Ingredient,
        verbose_name="ingredient",
        on_delete=models.CASCADE
    )
    amount = models.PositiveSmallIntegerField(
        verbose_name="amount",
        null=False,
        default=10,
    )

    # class Meta:
    #     constraints = [
    #         models.UniqueConstraint(
    #             fields=["recipe", "ingredient"],
    #             name="recipe_ingredients"
    #         )
    #     ]
