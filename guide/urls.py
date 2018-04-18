from django.urls import path
from .views import guide, guide_tree, guide_delete_node, project_edit_node, guide_edit_node

urlpatterns = [
    path('', guide, name='guide'),
    path('guidetree/', guide_tree, name='guide_tree'),
    path('deletenode/', guide_delete_node, name='guide_delete_node'),
    path('editprojectnode/', project_edit_node, name='guide_edit_project_node'),
    path('editguidenode/', guide_edit_node, name='guide_edit_guide_node'),
]