from django.urls import path
from .views import GetRecipeByShortLink

app_name = 'recipes'

urlpatterns = [
    path('api/recipes/<int:pk>/', GetRecipeByShortLink.as_view(), name='recipe-short-link'),
] 