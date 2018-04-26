# -*- coding: utf-8 -*-
from django.db import models
from datetime import datetime

# Create your models here.


class ApiProject(models.Model):

    api_project_name = models.CharField(max_length=1000)
    api_project_description = models.CharField(max_length=1000, null=True, blank=True)
    api_project_host = models.CharField(max_length=100, default="")
    api_project_port = models.CharField(max_length=10, default="80")
    api_project_creater = models.CharField(max_length=1000, null=True)
    api_project_create_date = models.DateTimeField("createTime", default=datetime.now)
    api_project_update_date = models.DateTimeField("updateTime", default=datetime.now)
    api_project_updater = models.CharField(max_length=1000, null=True)

    def __str__(self):
        return "%s" % self.api_project_name

    class Meta:
        app_label = "api"


class ApiApi(models.Model):

    api_project_name = models.ForeignKey(ApiProject, on_delete=models.CASCADE)
    api_api_name = models.CharField(max_length=1000)
    api_path = models.CharField(max_length=1000)
    api_method = models.CharField(max_length=100)
    api_protocol = models.CharField(max_length=100)
    api_post_method = models.CharField(max_length=100, null=True, blank=True)
    api_post_json_sample = models.CharField(max_length=5000, null=True, blank=True)
    api_api_creater = models.CharField(max_length=1000)
    api_api_updater = models.CharField(max_length=1000)
    api_api_creater_date = models.DateTimeField("createTime", default=datetime.now)
    api_api_update_date = models.DateTimeField("updateTime", default=datetime.now)

    def __str__(self):
        return self.api_api_name

    class Meta:
        app_label = "api"


class ApiBody(models.Model):
    api_api_name = models.ForeignKey(ApiApi, on_delete=models.CASCADE)
    api_body_key = models.CharField(max_length=1000, blank=True, null=True)
    api_body_key_type = models.CharField(max_length=1000, blank=True, null=True)

    def __str__(self):
        return self.api_body_key

    class Meta:
        app_label = "api"


class ApiTestCase(models.Model):

    api_api_name = models.ForeignKey(ApiApi, on_delete=models.CASCADE)
    api_case_description = models.CharField(max_length=1000, blank=True, null=True)
    api_test_head = models.CharField(max_length=1000, blank=True, null=True)
    api_test_params = models.CharField(max_length=1000, blank=True, null=True)
    api_test_bodys = models.CharField(max_length=1000, blank=True, null=True)
    api_response_code = models.CharField(max_length=1000, blank=True, null=True)
    api_response_time = models.CharField(max_length=1000, blank=True, null=True)
    api_response_content = models.CharField(max_length=1000, blank=True, null=True)
    api_except_code = models.CharField(max_length=1000, blank=True, null=True)
    api_except_time = models.CharField(max_length=1000, blank=True, null=True)
    api_except_content = models.CharField(max_length=1000, blank=True, null=True)

    def __str__(self):
        return self.api_case_description

    class Meta:
        app_label = "api"