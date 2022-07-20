from rest_framework.viewsets import ReadOnlyModelViewSet, ModelViewSet
from rest_framework import permissions
from .models import Favorite, IngredientInRecipe, Purchase, Tag, Ingredient, Recipe
from .serializers import TagSerializer, IngredientSerializer, FavoriteRecipesSerializer, PurchaseSerializer, RecipeSerializer
from django.shortcuts import get_object_or_404
from rest_framework.decorators import action
from rest_framework import status
from django.http import HttpResponse
from rest_framework.response import Response
from django.db.models import Sum
from users.permissions import IsAuthorOrReadOnly
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from .filters import IngredientSearchFilter, RecipeFilter
from django_filters.rest_framework.backends import DjangoFilterBackend


class TagViewSet(ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (permissions.AllowAny,)
    pagination_class = None


class IngredientViewSet(ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = (permissions.AllowAny,)
    filter_backends = (IngredientSearchFilter,)
    pagination_class = None


class RecipeViewSet(ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    filter_backends = (DjangoFilterBackend,)
    filter_class = RecipeFilter
    filterset_fields = ('tags', )

    def get_permissions(self):
        if self.action in [
            'list',
            'retrieve',
        ]:
            permission_classes = [permissions.AllowAny]
        elif self.action in [
            'update',
            'partial_update',
            'destroy'
        ]:
            permission_classes = [IsAuthorOrReadOnly]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]

    @staticmethod
    def post_or_delete(request, model, serializer, pk):
        if request.method != 'POST':
            model.objects.filter(
                user=request.user, recipe=Recipe.objects.get(id=pk)).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        serializer = serializer(
            data={'user': request.user.id, 'recipe': pk},
            context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(
        detail=True,
        methods=['POST', 'DELETE'],
    )
    def favorite(self, request, pk):
        return self.post_or_delete(
            request,
            Favorite,
            FavoriteRecipesSerializer,
            pk
        )

    @action(
        detail=True,
        methods=['POST', 'DELETE'],
    )
    def shopping_cart(self, request, pk):
        return self.post_or_delete(
            request,
            Purchase,
            PurchaseSerializer,
            pk
        )

    @action(detail=False,
            methods=['get'],
            )
    def download_shopping_cart(self, request, pk=None):
        ingredients = IngredientInRecipe.objects.filter(
            recipe__purchase__user=request.user
        ).values(
            'ingredient__name',
            'ingredient__measurement_unit'
        ).annotate(amount=Sum('amount'))
        pdfmetrics.registerFont(
            TTFont('mon-amour', 'mon-amour-one-medium.ttf', 'UTF-8'))
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = ('attachment; '
                                           'filename="shopping_list.pdf"')
        page = canvas.Canvas(response)
        page.setFont('mon-amour', size=24)
        page.drawString(200, 800, 'Список ингредиентов')
        height = 750
        counter = 1
        for item in ingredients:
            name = item['ingredient__name']
            amount = item['amount']
            unit = item['ingredient__measurement_unit']
            page.drawString(
                75, height, (f'{counter} {name} - {amount}, {unit}'))
            height -= 25
            counter += 1
        page.showPage()
        page.save()
        return response
