from django.db import models

# Create your models here.

class BaseResource(modesl.Model):
    Name = models.CharField(max_length=100, blank=False)
    class Meta:
        abstract = True

class Director(BaseResource):
    DirPort = models.IntegerField(default=9101)
    Address = models.IPAddressField(blank=False)
    Password = models.CharField(blank=False)
    Monitor = models.BoolenField(default=False)

class Console(BaseResource):
    Password = models.CharField(blank=False)
    Director = models.ForeignKey(Director, blank=False)
    HeartBeatInterval = models.IntegerField(default=0)

