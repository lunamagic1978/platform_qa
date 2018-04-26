# -*- coding: utf-8 -*-
from django import forms
from django.forms import ModelForm
from .models import ApiProject, ApiApi, ApiBody

METHOD_CHOICE = (('GET', 'GET'),
                 ('POST', 'POST'),
                 )

PROTOCOL_CHOICE = (('HTTP', 'HTTP'),
                   ('HTTPS', 'HTTPS'),
                   )

POST_CHOICE = (
               ('form-data', 'form-data'),
               ('x-form', 'x-form'),
               ('json', 'json'),
               )


class CreateApiProjectForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super(CreateApiProjectForm, self).__init__(*args, **kwargs)
        self.fields['api_project_name'].widget.attrs["class"] = "form-control"
        self.fields['api_project_description'].widget.attrs["class"] = "form-control"
        self.fields['api_project_host'].widget.attrs["class"] = "form-control"
        self.fields['api_project_port'].widget.attrs["class"] = "form-control"


    class Meta:
        model = ApiProject
        fields = ('api_project_name', 'api_project_description', 'api_project_host', 'api_project_port')


class EditApiProjectForm(forms.Form):

    edit_api_project_name = forms.CharField()
    edit_api_project_description = forms.CharField()
    edit_api_project_host = forms.CharField()
    edit_api_project_port = forms.CharField()

    def __init__(self, *args, **kwargs):
        super(EditApiProjectForm, self).__init__(*args, **kwargs)
        self.fields['edit_api_project_name'].widget.attrs["class"] = "form-control"
        self.fields['edit_api_project_description'].widget.attrs["class"] = "form-control"
        self.fields['edit_api_project_host'].widget.attrs["class"] = "form-control"
        self.fields['edit_api_project_port'].widget.attrs["class"] = "form-control"


class CreateApiApiForm(ModelForm):

    api_method = forms.ChoiceField(choices=METHOD_CHOICE)
    api_protocol = forms.ChoiceField(choices=PROTOCOL_CHOICE)
    api_post_method = forms.ChoiceField(choices=POST_CHOICE)

    def __init__(self, *args, **kwargs):
        super(CreateApiApiForm, self).__init__(*args, **kwargs)
        self.fields['api_api_name'].widget.attrs["class"] = "form-control"
        self.fields['api_path'].widget.attrs["class"] = "form-control"
        self.fields['api_method'].widget.attrs["class"] = "form-control"
        self.fields['api_protocol'].widget.attrs["class"] = "form-control"
        self.fields['api_post_method'].widget.attrs["class"] = "form-control"

    class Meta:
        model = ApiApi
        fields = ('api_project_name', 'api_api_name', 'api_path', "api_method", 'api_protocol', 'api_post_method')


class EditApiApiForm(forms.Form):

    edit_api_api_name = forms.CharField()
    edit_api_path = forms.CharField()
    edit_api_method = forms.ChoiceField(choices=METHOD_CHOICE)
    edit_api_protocol = forms.ChoiceField(choices=PROTOCOL_CHOICE)
    edit_api_post_method = forms.ChoiceField(choices=POST_CHOICE)

    def __init__(self, *args, **kwargs):
        super(EditApiApiForm, self).__init__(*args, **kwargs)
        self.fields['edit_api_api_name'].widget.attrs["class"] = "form-control"
        self.fields['edit_api_path'].widget.attrs["class"] = "form-control"
        self.fields['edit_api_method'].widget.attrs["class"] = "form-control"
        self.fields['edit_api_protocol'].widget.attrs["class"] = "form-control"
        self.fields['edit_api_post_method'].widget.attrs["class"] = "form-control"


class UpdataJson(forms.Form):

    api_post_json_sample = forms.CharField(widget=forms.Textarea)

    def __init__(self, *args, **kwargs):
        super(UpdataJson, self).__init__(*args, **kwargs)
        self.fields['api_post_json_sample'].widget.attrs['style'] = "width:600px; height: 500px"


class BaseTestCaseForm(forms.Form):

    def __init__(self, *args, **kwargs):
        super(BaseTestCaseForm, self).__init__(*args, **kwargs)
        self.apiId = kwargs['initial']['apiId']
        print(self.apiId)


class PostJsonTestCaseForm(BaseTestCaseForm):

    def __init__(self, *args, **kwargs):
        super(PostJsonTestCaseForm, self).__init__(*args, **kwargs)
        api_key_objs = ApiBody.objects.filter(api_api_name_id=self.apiId)
        for obj in api_key_objs:
            print(obj.api_body_key)
            print(obj.api_body_key_type)
