from django.shortcuts import redirect
from django.urls import reverse
from rest_framework.views import APIView

from .models import Recipe


class GetRecipeByShortLink(APIView):
    """View для обработки коротких ссылок на рецепты"""

    def get(self, request, pk):
        """Метод для перенаправления на API-эндпоинт рецепта"""
        recipe = Recipe.objects.get(pk=pk)
        return redirect(reverse('recipes-detail', args=[pk])) 