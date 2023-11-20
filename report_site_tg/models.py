import uuid
from django.db import models


class Report(models.Model):
    phone_number = models.CharField(max_length=20)
    user_agent = models.TextField()
    mail = models.TextField()
    report_text = models.TextField()


class Order(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4)
    count_reports = models.IntegerField()
    url_report = models.CharField(max_length=150)
    count_threads = models.IntegerField()
    reports = models.ManyToManyField(Report)
    proxy = models.CharField(max_length=200, null=True)

    def get_absolute_url(self):
        return f'/site_reports/order/{self.uuid}/'


class Text(models.Model):
    content = models.TextField()

    def __str__(self):
        return self.content
