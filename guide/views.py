# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .form import CreateGuideProjectForm, CreateGuideGuideForm
from guide.guide_lab import guide_valid_factory
from django.http import HttpResponseRedirect, JsonResponse
from .models import GuideGuide, GuideProject
from guide.guide_lab.guide_formsets_factory import GuideFormsetsFactory

# Create your views here.


@login_required
def guide(request):
    username = request.session.get('username', '')
    create_guide_project_form_init = CreateGuideProjectForm()
    create_guide_guide_form_init = CreateGuideGuideForm()
    edit_guide_project_formsets_init = GuideFormsetsFactory().guide_project_formsets()
    if request.method == "POST":
        if "submit_createProject" in request.POST:
            create_guide_project_form_POST = CreateGuideProjectForm(request.POST)
            if create_guide_project_form_POST.is_valid():
                create_guide_project_factory = guide_valid_factory.GuideProjectValidFactory(
                    request=request, temp=create_guide_project_form_POST.cleaned_data, username=username)
                create_guide_project_factory.create_guide_project()
        elif "submit_createGuide" in request.POST:
            create_guide_guide_form_POST = CreateGuideGuideForm(request.POST)
            if create_guide_guide_form_POST.is_valid():
                create_guide_guide_factory = guide_valid_factory.GuideGuideValidFactory(
                    request=request, temp=create_guide_guide_form_POST.cleaned_data, username=username
                )
                create_guide_guide_factory.create_guide_guide()
        elif "editguideprojectsave" in request.POST:
            edit_guide_project_formsets_POST = GuideFormsetsFactory().guide_project_formsets(request_POST=request.POST)
            if edit_guide_project_formsets_POST.is_valid():
                edit_guide_project_factory = guide_valid_factory.GuideProjectValidFactory(
                    request=request, formsets_POST=edit_guide_project_formsets_POST)
                edit_guide_project_factory.edit_guide_project_save()

        return HttpResponseRedirect('/guide/')
    else:
        ctx = {"create_guide_project_form": create_guide_project_form_init,
               "create_guide_guide_form": create_guide_guide_form_init,
               "edit_guide_project_formsets": edit_guide_project_formsets_init}
        return render(request, 'guide.html', ctx)


def guide_tree(request):

    guide_tree = []
    button = ""
    # button = '<input type="submit" class="form-control btn btn-primary" value="确定" style="display: inline;" name="submit_createGuide">'
    # button = "<button class='tree-button' style='float: right; margin-right: 10px'>删除</button><button style='float: right; margin-right: 10px'>修改</button><button style='float: right; margin-right: 10px'>新增</button>"
    project_objs = GuideProject.objects.all()
    for project_obj in project_objs:
        add_dict ={}
        if project_obj.project_description:
            add_dict["text"] = "%s : %s" % (project_obj.project_name, project_obj.project_description) + button
        else:
            add_dict["text"] = project_obj.project_name + button
        nodes_list = []
        guide_objs = GuideGuide.objects.filter(project_name=project_obj.pk)
        for guide_obj in guide_objs:
            guide_dict = {}
            if guide_obj.guide_description:
                guide_dict['text'] = "%s : %s" % (guide_obj.guide_name, guide_obj.guide_description) + button
            else:
                guide_dict['text'] = guide_obj.guide_name + button
            guide_dict["href"] = guide_obj.guide_url
            nodes_list.append(guide_dict)
        add_dict["nodes"] = nodes_list
        guide_tree.append(add_dict)
    return JsonResponse({"data": guide_tree})