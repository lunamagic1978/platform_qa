from django.forms import modelformset_factory
from guide.models import GuideProject
from guide.form import CreateGuideGuideForm, CreateGuideProjectForm


class GuideFormsetsFactory():

    def guide_project_formsets(self, request_POST=None):
        _formsets = modelformset_factory(GuideProject, form=CreateGuideProjectForm, fields=("project_name", "project_description"), extra=0, can_delete=True)
        if request_POST:
            return _formsets(request_POST)
        else:
            return _formsets