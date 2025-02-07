from django.urls import path
from . import views

urlpatterns = [
    path('s/<int:pk>/', views.RecipeShortLinkView.as_view(), name='recipe-short-link'),
]