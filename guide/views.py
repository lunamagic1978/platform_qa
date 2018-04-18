# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .form import CreateGuideProjectForm, CreateGuideGuideForm
from guide.guide_lab import guide_valid_factory
from django.http import HttpResponseRedirect, JsonResponse
from .models import GuideGuide, GuideProject
from guide.guide_lab.guide_formsets_factory import GuideFormsetsFactory
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime

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
               "edit_guide_project_formsets": edit_guide_project_formsets_init,
               "username": username}
        return render(request, 'guide.html', ctx)


@csrf_exempt
def guide_tree(request):

    guide_tree = []
    project_objs = GuideProject.objects.all()
    for project_obj in project_objs:
        add_dict ={}
        if project_obj.project_description:
            add_dict["text"] = "%s : %s" % (project_obj.project_name, project_obj.project_description)
        else:
            add_dict["text"] = project_obj.project_name
        add_dict["guide_project_id"] = project_obj.pk
        add_dict["project_name"] = project_obj.project_name
        add_dict["project_description"] = project_obj.project_description
        nodes_list = []
        guide_objs = GuideGuide.objects.filter(project_name=project_obj.pk)
        for guide_obj in guide_objs:
            guide_dict = {}
            if guide_obj.guide_description:
                guide_dict['text'] = "%s : %s" % (guide_obj.guide_name, guide_obj.guide_description)
            else:
                guide_dict['text'] = guide_obj.guide_name
            guide_dict["href"] = guide_obj.guide_url
            guide_dict["guide_guide_id"] = guide_obj.pk
            guide_dict["guide_name"] = guide_obj.guide_name
            guide_dict["guide_description"] = guide_obj.guide_description
            nodes_list.append(guide_dict)
        add_dict["nodes"] = nodes_list
        guide_tree.append(add_dict)
    return JsonResponse({"data": guide_tree})


@csrf_exempt
def guide_delete_node(request):
    if request.method == "POST":
        guide_project_id = request.POST['guide_project_id']
        guide_guide_id = request.POST['guide_guide_id']
        if guide_guide_id and guide_project_id:
            print("both all")
            data = "both all"
        elif guide_project_id and not guide_guide_id:
            GuideProject.objects.get(pk=guide_project_id).delete()
            data = "project is delete"
        elif not guide_project_id and guide_guide_id:
            GuideGuide.objects.get(pk=guide_guide_id).delete()
            data = "guide is delete"
        else:
            print("both empty")
            data = "both empty"

        print(request.POST)
        print("method is post")
        method = "POST"
    else:
        print("method is get")
        method = "GET"
        data = "get"
    return JsonResponse({"method": method,
                         "body": request.POST,
                         "data": data,
                         })

@csrf_exempt
def project_edit_node(request):
    statue_code = "200"
    if request.method == "POST":
        data = request.POST
        guide_project_id = data['guide_project_id']
        project_name = data['project_name']
        project_description = data['project_description']
        updater = data['updater']
        obj = GuideProject.objects.get(pk=guide_project_id)
        obj.project_name = project_name
        obj.project_description = project_description
        obj.updater = updater
        obj.update_date = datetime.now()
        obj.save()
        data = "save success"

    return JsonResponse({"statue_code": statue_code,
                         "data": data,
                         })