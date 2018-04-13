from django.urls import path
from .views import guide, guide_tree

urlpatterns = [
    path('', guide, name='guide'),
    path('guidetree/', guide_tree, name='guide_tree')
]