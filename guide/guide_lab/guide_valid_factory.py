# -*- coding: utf-8 -*-
from lab import notify
from guide.models import GuideProject, GuideGuide
from datetime import datetime

class ValidFactory():

    def __init__(self, temp=None, request=None, formsets_POST=None, username=None,):
        self.temp = temp
        self.request = request
        self.formsets_POST = formsets_POST
        self.username = username


class GuideProjectValidFactory(ValidFactory):

    def create_guide_project(self):
        project_name = self.temp['project_name']
        project_description = self.temp['project_description']
        username = self.username

        obj = GuideProject.objects.create(project_name=project_name, project_description=project_description,
                    creater=username, updater=username, create_date=datetime.now(), update_date=datetime.now())
        try:
            obj.save()
            notify.flash(self.request, 'info', '项目保存成功')
        except Exception as e:
            notify.flash(self.request, 'info', '项目保存异常')

    def edit_guide_project_save(self):
        try:
            self.formsets_POST.save()
            notify.flash(self.request, 'info', '项目编辑成功')
        except Exception:
            notify.flash(self.request, 'info', '项目编辑异常')


class GuideGuideValidFactory(ValidFactory):

    def create_guide_guide(self):
        project_name = self.temp['project_name']
        guide_name = self.temp['guide_name']
        guide_description = self.temp['guide_description']
        guide_url = self.temp['guide_url']
        username = self.username

        obj = GuideGuide.objects.create(project_name=project_name, guide_name=guide_name,
                    guide_description=guide_description, guide_url=guide_url, guide_creater=username,
                    guide_updater=username, guide_create_date=datetime.now(), guide_update_date=datetime.now())

        try:
            obj.save()
            notify.flash(self.request, 'info', '引导保存成功')
        except Exception as e:
            notify.flash(self.request, 'info', '引导保存异常')