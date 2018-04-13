# -*- coding: utf-8 -*-
from django import forms
from django.forms import ModelForm
from .models import GuideProject, GuideGuide


class CreateGuideProjectForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super(CreateGuideProjectForm, self).__init__(*args, **kwargs)
        self.fields['project_name'].widget.attrs["class"] = "form-control"
        self.fields['project_description'].widget.attrs["class"] = "form-control"


    class Meta:
        model = GuideProject
        fields = ('project_name', 'project_description')


class CreateGuideGuideForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super(CreateGuideGuideForm, self).__init__(*args, **kwargs)
        self.fields['project_name'].widget.attrs["class"] = "form-control"

    class Meta:
        model = GuideGuide
        fields = ('project_name', 'guide_name', 'guide_description', 'guide_url')