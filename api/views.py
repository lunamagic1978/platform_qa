from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .form import CreateApiProjectForm, EditApiProjectForm, CreateApiApiForm, EditApiApiForm, UpdataJson
from .form import PostJsonTestCaseForm
from django.http import HttpResponseRedirect, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .api_lab import api_valid_factory
from .models import ApiProject, ApiApi, ApiTestCase, ApiBody
from datetime import datetime
from django.forms import formset_factory
# Create your views here.

@login_required
def api(request):
    username = request.session.get('username', '')
    create_api_project_form_init = CreateApiProjectForm()
    edit_api_project_form_init = EditApiProjectForm()
    create_api_api_form_init = CreateApiApiForm()
    edit_api_api_form_init = EditApiApiForm()

    if request.method == "POST":
        if "submit_createApiProject" in request.POST:
            create_api_project_POST = CreateApiProjectForm(request.POST)
            if create_api_project_POST.is_valid():
                create_api_project_factory = api_valid_factory.ApiProjectValidFactory(
                    request=request, temp=create_api_project_POST.cleaned_data, username=username,
                )
                create_api_project_factory.create_api_project()

        return HttpResponseRedirect('/api/')
    else:
        ctx = {"create_api_project_form": create_api_project_form_init,
               "edit_api_project_form": edit_api_project_form_init,
               "create_api_api_form": create_api_api_form_init,
               "edit_api_api_form": edit_api_api_form_init,
               "username": username,}
        return render(request, 'api.html', ctx)


@login_required
def api_testcase_list(request, projectId, apiId):
    username = request.session.get('username', '')
    project_obj = ApiProject.objects.get(pk=projectId)
    api_obj = ApiApi.objects.get(pk=apiId)
    api_post_json_sample_form = UpdataJson()
    api_test_objs = ApiTestCase.objects.filter(api_api_name_id=apiId).values()

    api_bodys = ApiBody.objects.filter(api_api_name_id=apiId)
    api_bodys_len = len(api_bodys)

    # 根据api_test_objs对testcase的展示进行初始化
    if api_test_objs:
        pass
    else:
        test_case_formsets_init = formset_factory(form=PostJsonTestCaseForm, can_order=True, can_delete=True)
        test_case_formsets = test_case_formsets_init(form_kwargs={"initial": {"apiId": apiId}})

    if request.method == "POST":
        if "update_json_sample" in request.POST:
            updata_json_sample_POST = UpdataJson(request.POST)
            if updata_json_sample_POST.is_valid():
                updata_json_sample_factory = api_valid_factory.ApiApiValidFactory(
                    request=request, temp=updata_json_sample_POST.cleaned_data, username=username
                )
                updata_json_sample_factory.updata_json_smaple(apiId)
        return HttpResponseRedirect('/api/testcaselist/project%s/api%s/' % (projectId, apiId))
    else:
        if api_obj.api_method == "POST" and api_obj.api_post_method == "json" and not api_obj.api_post_json_sample:
            json_flag = False
        else:
            json_flag = True

        ctx = {"project_obj": project_obj,
               "api_obj": api_obj,
               "json_flag": json_flag,
               "api_post_json_sample_form": api_post_json_sample_form,
               "test_case_formsets": test_case_formsets,
               "api_bodys": api_bodys,
               "api_bodys_len": api_bodys_len,
               }
        return render(request, 'apiCaseList.html', ctx)


@csrf_exempt
def api_tree(request):

    api_tree = []
    api_project_objs = ApiProject.objects.all()
    for api_obj in api_project_objs:
        add_dict = {}
        if api_obj.api_project_port == "80":
            host_content = api_obj.api_project_host
        else:
            host_content = "%s:%s" % (api_obj.api_project_host, api_obj.api_project_port)
        if api_obj.api_project_description:
            add_dict["text"] = "%s : %s  【 Host :%s】" % (api_obj.api_project_name, api_obj.api_project_description, host_content)
        else:
            add_dict["text"] = "%s 【 Host :%s】" % (api_obj.api_project_name, host_content)
        add_dict["api_project_id"] = api_obj.pk
        add_dict["api_project_name"] = api_obj.api_project_name
        add_dict["api_project_description"] = api_obj.api_project_description
        add_dict["api_project_host"] = api_obj.api_project_host
        add_dict["api_project_port"] = api_obj.api_project_port

        nodes_list = []
        api_objs = ApiApi.objects.filter(api_project_name=api_obj.pk)
        for api in api_objs:
            api_dict = {}
            api_dict['href'] = "http://127.0.0.1:8000/api/testcaselist/project%s/api%s/" % (api_obj.pk, api.pk)
            api_dict['text'] = '%s: %s' %(api.api_api_name, api.api_path)
            api_dict['api_api_id'] = api.pk
            api_dict['api_api_name'] = api.api_api_name
            api_dict['api_path'] = api.api_path
            api_dict['api_method'] = api.api_method
            api_dict['api_protocol'] = api.api_protocol
            api_dict['api_post_method'] = api.api_post_method
            api_dict["api_project_name"] = api_obj.api_project_name

            nodes_list.append(api_dict)

        add_dict['nodes'] = nodes_list
        api_tree.append(add_dict)
    return JsonResponse({"data": api_tree})


@csrf_exempt
def api_edit_project_node(request):
    if request.method == "POST":
        data = request.POST
        api_project_name = data["api_project_name"]
        api_project_description = data["api_project_description"]
        api_project_id = data["api_project_id"]
        api_project_host = data["api_project_host"]
        api_project_port = data["api_project_port"]
        updater = data["updater"]
        try:
            obj = ApiProject.objects.get(pk=api_project_id)
        except Exception:
            return JsonResponse({"status_code": "400",
                                 "data": "你修改的项目不存在"})
        obj.api_project_name = api_project_name
        obj.api_project_description = api_project_description
        obj.api_project_updater = updater
        obj.api_project_update_date = datetime.now()
        obj.api_project_host = api_project_host
        obj.api_project_port = api_project_port
        try:
            obj.save()
        except Exception:
            return JsonResponse({"status_code": "401",
                                 "data": "保存修改的项目报错"})
        return JsonResponse({"statue_code": "200",
                             "data": "保存成功",
                             })
    return JsonResponse({"statue_code": "402",
                             "data": "请求的方式不正确",
                             })

@csrf_exempt
def api_create_api_node(request):
    if request.method == "POST":
        data = request.POST
        api_project_id = data['api_project_id']
        api_api_name = data['api_api_name']
        api_path =data['api_path']
        creater = data['creater']
        api_protocol = data['api_protocol']
        api_method = data['api_method']
        api_post_method = data['api_post_method']
        obj = ApiApi.objects.create(api_api_name=api_api_name, api_path=api_path, api_method=api_method,
                                    api_protocol=api_protocol, api_post_method=api_post_method,
                                    api_project_name_id=api_project_id, api_api_creater=creater,
                                    api_api_updater=creater, api_api_creater_date=datetime.now(),
                                    api_api_update_date=datetime.now(), )
        try:
            obj.save()
        except Exception:
            return JsonResponse({"status_code": "401",
                                 "data": "创建接口报错"})
        return JsonResponse({"statue_code": "200",
                             "data": "创建接口成功",
                             })

    return JsonResponse({"statue_code": "402",
                             "data": "请求的方式不正确",
                             })


@csrf_exempt
def api_edit_api_node(request):
    if request.method == "POST":
        data = request.POST
        edit_api_api_id = data['edit_api_api_id']
        edit_api_api_name = data['edit_api_api_name']
        edit_api_path =data['edit_api_path']
        updater = data['edit_updater']
        edit_api_protocol = data['edit_api_protocol']
        edit_api_method = data['edit_api_method']
        edit_api_post_method = data['edit_api_post_method']
        try:
            obj = ApiApi.objects.get(pk=edit_api_api_id)
        except:
            return JsonResponse({"status_code": "403",
                                 "data": "需要修改的接口ID不存在"})
        obj.api_api_name = edit_api_api_name
        obj.api_path = edit_api_path
        obj.api_method = edit_api_method
        obj.api_protocol = edit_api_protocol
        obj.api_post_method = edit_api_post_method
        obj.api_api_updater = updater
        obj.api_api_update_date = datetime.now()
        try:
            obj.save()
        except Exception:
            return JsonResponse({"status_code": "401",
                                 "data": "修改接口报错"})
        return JsonResponse({"statue_code": "200",
                             "data": "修改接口成功",
                             })

    return JsonResponse({"statue_code": "402",
                             "data": "请求的方式不正确",
                             })