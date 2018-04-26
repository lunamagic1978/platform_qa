from lab import notify, valid_factory
from .api_handle import post_json_level1_key_to_dict_handle
from api.models import ApiProject, ApiApi, ApiBody
from datetime import datetime
import json


class ApiProjectValidFactory(valid_factory.ValidFactory):

    def create_api_project(self):

        api_project_name = self.temp['api_project_name']
        api_project_description = self.temp['api_project_description']
        api_project_host = self.temp['api_project_host']
        api_project_port = self.temp['api_project_port']

        username = self.username
        obj = ApiProject.objects.create(api_project_name=api_project_name, api_project_description=api_project_description,
                                        api_project_creater=username, api_project_updater=username,
                                        api_project_create_date=datetime.now(), api_project_update_date=datetime.now(),
                                        api_project_host=api_project_host, api_project_port=api_project_port)
        try:
            obj.save()
            notify.flash(self.request, 'info', '项目保存成功')
        except Exception as e:
            notify.flash(self.request, 'info', '项目保存异常')


class ApiApiValidFactory(valid_factory.ValidFactory):

    def updata_json_smaple(self, apiId):
        api_post_json_sample = self.temp['api_post_json_sample']

        try:
            post_json_sample = json.loads(api_post_json_sample)
        except Exception:
            print("error")
        try:
            obj = ApiApi.objects.get(pk=apiId)
        except Exception:
            notify.flash(self.request, 'info', '数据库没有获取到对应的接口id')
            return ""

        if isinstance(post_json_sample, dict):
            post_json_sample_key_dict = post_json_level1_key_to_dict_handle(post_json_sample)
            for key in post_json_sample_key_dict:
                ApiBody.objects.create(api_api_name_id=apiId, api_body_key=key, api_body_key_type=post_json_sample_key_dict[key])
            obj.api_post_json_sample = post_json_sample
            obj.save()
            notify.flash(self.request, 'info', 'json sample保存成功')
        else:
            notify.flash(self.request, 'info', 'json sample的格式不正确')



