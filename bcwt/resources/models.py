from django.db import models

# Create your models here.

class BaseResource(models.Model):
    Name = models.CharField(max_length=100, blank=False, unique=True)
    Comment = models.CharField(max_length=200, blank=True)
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
    HeartBeatInterval = models.IntegerField("Heartbeat Interval", default=0)

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
    MaximumConcurrentJobs = models.IntegerField("Maximum Concurrent Jobs", default=5)
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

class Client(BaseResource):
    MaximumConcurrentJobs = models.IntegerField(default=2, blank=True)
    FDPort = models.IntegerField(default=9102, blank=True)
    FDAddress = models.IPAddressField(default='0.0.0.0', blank=True)
    FDSouceAddress = models.IPAddressField(blank=True)
    SDConnectTimeout = models.IntegerField(default=30, blank=True)
    MaximumNetworkBufferSize = models.IntegerField(default=65536, blank=True)
    def __unicode__(self):
        return "%s %s:%d" % (self.Name, self.FDAddress, self.FDPort)

class Job(BaseResource):
    BACKUP  = "Backup"
    RESTORE = "Restore"
    JOB_TYPES = (
        (BACKUP, "Backup"),
        (RESTORE, "Restore"),
    )
    FULL = "Full"
    INCREMENTAL = "Incremental"
    DIFFERENTIAL = "Differential"
    JOB_LEVELS = (
        (FULL, FULL),
        (INCREMENTAL, INCREMENTAL),
        (DIFFERENTIAL, DIFFERENTIAL),
    )
    Enabled = models.BooleanField(default=True)
    Type = models.CharField(max_length=7, choices=JOB_TYPES, default=BACKUP)
    Level = models.CharField(max_length=len(DIFFERENTIAL), choices=JOB_LEVELS, default=FULL)
    Client = models.ForeignKey(Client, blank=False)
    Pool = models.ForeignKey(Pool, blank=False)
    Storage = models.ForeignKey(Storage, blank=False)
    def __unicode__(self):
        return "%s of %s type by %s level on %s client" % (self.Name, self.Type, self.Level, self.Client)

class FileSetOptions(BaseResource):
    GZIP = "GZIP"
    LZO = "LZO"
    COMPRESSION_TYPES = (
        (GZIP, GZIP),
        (LZO , LZO),
    )
    SHA1 = "SHA1"
    MD5  = "MD5"
    SIGNATURE_TYPES = (
        (MD5,  MD5),
        (SHA1, SHA1),
    )
    Exclude = models.BooleanField(blank=False)
    WildFile = models.TextField(blank=False)
    Compression = models.CharField(max_length=4, choices=COMPRESSION_TYPES, default=GZIP)
    Signature = models.CharField(max_length=4, choices=SIGNATURE_TYPES, default=MD5)
    OneFs = models.BooleanField(default=False)
    
    def __unicode__(self):
        return "%s, compression=%s, signature=%s" % (self.Name, self.Compression, self.Signature)

class FileSetInclude(BaseResource):
    File = models.TextField("List of included files",)

class FileSetExclude(BaseResource):
    File = models.TextField("List of excluded files",)

class FileSet(BaseResource):
    IgnoreFileSetChanges = models.BooleanField("Ignore FileSet Changes", default=False)
    Options = models.ForeignKey(FileSetOptions, null=True, blank=True)
    Include = models.ForeignKey(FileSetInclude, blank=False)
    Exclude = models.ForeignKey(FileSetExclude, null=True, blank=True)
    
    def __unicode__(self):
        return "%s o: %s, i: %s, e: %s" % (self.Name, self.Options, self.Include, self.Exclude)
    
