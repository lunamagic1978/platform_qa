from django.urls import path
from .views import api, api_tree, api_edit_project_node, api_create_api_node, api_edit_api_node,api_testcase_list

urlpatterns = [
    path('', api, name='api'),
    path('apitree/', api_tree, name='api_tree'),
    path('editprojectnode/', api_edit_project_node, name='api_edit_project_node'),
    path('createapinode/', api_create_api_node, name='api_create_api_node'),
    path('editapinode/', api_edit_api_node, name='api_edit_api_node'),
    path('testcaselist/project<int:projectId>/api<int:apiId>/', api_testcase_list, name='api_testcase_list')
]