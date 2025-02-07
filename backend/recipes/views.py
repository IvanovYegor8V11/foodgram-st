from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Recipe

class RecipeShortLinkView(APIView):
    """
    Представление для обработки короткой ссылки на рецепт.
    При GET-запросе перенаправляет пользователя на полную страницу рецепта.
    """
    def get(self, request, pk):
        # Получаем объект рецепта или возвращаем 404, если рецепт не найден
        recipe = get_object_or_404(Recipe, pk=pk)
        
        # Формируем полный URL для рецепта
        full_url = request.build_absolute_uri(f'/recipes/{recipe.pk}/')
        
        # Возвращаем ответ с полным URL
        return Response({'short_link': full_url}, status=status.HTTP_200_OK)