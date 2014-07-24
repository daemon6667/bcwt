from django.db import models

# Create your models here.

class BaseResource(models.Model):
    Name = models.CharField(max_length=100, blank=False)
    def __unicode__(self):
        return self.Name
    class Meta:
        abstract = True

class Director(BaseResource):
    DirPort = models.IntegerField(default=9101)
    Address = models.IPAddressField(blank=False)
    Password = models.CharField(blank=False, max_length=100)
    Monitor = models.BooleanField(default=False)

class Console(BaseResource):
    Password = models.CharField(blank=False, max_length=100)
    Director = models.ForeignKey(Director, blank=False)
    HeartBeatInterval = models.IntegerField(default=0)

class Device(BaseResource):
    FILE = "File"
    TAPE = "Tape"
    FIFO = "Fifo"
    DEVICE_TYPES = (
        (FILE, "File"),
        (TAPE, "Tape"),
        (FIFO, "Fifo"),
    )
    ArchiveDevice = models.CharField(max_length=100)
    DeviceType = models.CharField(max_length=4, choices=DEVICE_TYPES, default=FILE)
    MediaType = models.CharField(max_length=100)
    AutoChanger = models.BooleanField(default=False)
    MaximumConcurrentJobs = models.IntegerField(default=5)
    def __unicode__(self):
        return "%s - %s" % (self.Name, self.DeviceType)

class Storage(BaseResource):
    WorkingDirectory = models.CharField(max_length=250, default="/var/db/bacula", blank=False)
    PidDirectory = models.CharField(max_length=250, default="/var/run", blank=False)
    MaximumConcurrentJobs = models.IntegerField(default=10)
    SDAddress = models.IPAddressField(blank=False) 
    SDPort = models.IntegerField(default=9103)
    def __unicode__(self):
        return "%s %s:%d" % (self.Name, self.SDAddress, self.SDPort)

class Pool(BaseResource):
    BACKUP = 'Backup'
    RESTORE = 'Restore'
    POOL_TYPES = (
        (BACKUP, "Backup"),
        (RESTORE, "Restore"),
    )
    PoolType = models.CharField(max_length=7, choices=POOL_TYPES, default=BACKUP, blank=False)
    LabelFormat = models.CharField(max_length=20, default="Vol_", blank=False)
    MaximumVolumeJobs = models.IntegerField(default=5, blank=False)
    MaximumVolumeBytes = models.IntegerField(default=1024*1024*1024, blank=False)
    MaximumVolumes = models.IntegerField(default=1, blank=False)
    Storage = models.ForeignKey(Storage, blank=False)
    Recycle = models.BooleanField(default=True, blank=False)
    PurgeOldestVolume = models.BooleanField(default=True, blank=False)
    AutoPrune = models.BooleanField(default=True, blank=False)

    def __unicode__(self):
        return "%s [%s:%s]" % (self.Name, self.Storage, self.PoolType,)

