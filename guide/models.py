from django.db import models
from datetime import datetime

# Create your models here.


class GuideProject(models.Model):
    project_name = models.CharField(max_length=1000)
    project_description = models.CharField(max_length=1000, null=True, blank=True)
    creater = models.CharField(max_length=1000, null=True)
    create_date = models.DateTimeField("createTime", default=datetime.now)
    update_date = models.DateTimeField("updateTime", default=datetime.now)
    updater = models.CharField(max_length=1000, null=True)

    def __str__(self):
        return "Guide %s" % self.project_name

    class Meta:
        app_label = "guide"