from django.db import models
from django.core import validators
from django.contrib.auth import get_user_model

User = get_user_model()


class Tag(models.Model):
    BLUE = '#0000FF'
    ORANGE = '#FFA500'
    GREEN = '#008000'
    PURPLE = '#800080'
    YELLOW = '#FFFF00'

    COLOR_CHOICES = [
        (BLUE, 'BLUE'),
        (ORANGE, 'ORANGE'),
        (GREEN, 'GREEN'),
        (PURPLE, 'PURPLE'),
        (YELLOW, 'YELLOW'),
    ]
    name = models.CharField(max_length=50)
    color = models.CharField(max_length=10, unique=True,
                             choices=COLOR_CHOICES, verbose_name="checkbox color")
    slug = models.SlugField(max_length=20, unique=True,
                            verbose_name="unique slug")

    class Meta:
        ordering = ["id"]

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField(max_length=200)
    measurement_unit = models.CharField(max_length=10)

    class Meta:
        ordering = ["id"]
        constraints = [
            models.UniqueConstraint(fields=['name', 'measurement_unit'],
                                    name='name_unit_unique')
        ]

    def __str__(self):
        return f'{self.name}, {self.measurement_unit}'


class Recipe(models.Model):
    tags = models.ManyToManyField(
        Tag,
        related_name="recipes",
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes',
        help_text='author',
        db_index=True,
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        through="IngredientInRecipe"
    )
    name = models.CharField(
        max_length=250,
        db_index=True)
    image = models.ImageField(
        upload_to=''
    )
    text = models.TextField(verbose_name="description")
    cooking_time = models.IntegerField(
        verbose_name="cooking time in minutes",
    )
    pub_date = models.DateTimeField(auto_now_add=True, db_index=True,
                                    verbose_name='Publish date')

    class Meta:
        ordering = ('-pub_date',)

    def __str__(self):
        return self.name


class IngredientInRecipe(models.Model):
    ingredient = models.ForeignKey(Ingredient,
                                   on_delete=models.CASCADE,
                                   related_name='ingredient_name',
                                   )
    recipe = models.ForeignKey(Recipe,
                               on_delete=models.CASCADE,
                               related_name='ingredient_amount',
                               )
    amount = models.PositiveIntegerField(
        validators=[validators.MinValueValidator(
            1, message='Not less than 1')],
        verbose_name='ingredient amount'
    )

    class Meta:
        verbose_name = 'ingredient in recipe'
        verbose_name_plural = 'ingredients in recipes'
        constraints = [
            models.UniqueConstraint(
                fields=['ingredient', 'recipe'],
                name='recipe_ingredient_unique'
            )
        ]

    def __str__(self):
        return f'Ingredient "{self.ingredient}" of "{self.recipe}" recipe.'


class Favorite(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='favorite_subscriber',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='favorite_recipe',
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'], name='favorite_user_recept_unique'
            )
        ]

    def __str__(self):
        return f'Рецепт "{self.recipe}" в избранном у {self.user}'


class Purchase(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='purchase',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='purchase',
    )
    date_added = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        ordering = ('-date_added',)
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'], name='purchase_user_recipe_unique'
            )
        ]

    def __str__(self):
        return f'Recipe "{self.recipe}" in the {self.user} purchasing list'
