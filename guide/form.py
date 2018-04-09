# -*- coding: utf-8 -*-

from django import forms
from django.forms import ModelForm
from .models import GuideProject


class CreateGuideProjectForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super(CreateGuideProjectForm, self).__init__(*args, **kwargs)

    class Meta:
        model = GuideProject
        fields = ('project_name', 'project_description')