from django.contrib import admin
from resources.models import Job, Client, Director, Console, Storage, Device, Pool

# Register your models here.
class DirectorAdmin(admin.ModelAdmin):
    list_display = ('Name', 'Address', 'DirPort')

class StorageAdmin(admin.ModelAdmin):
    list_display = ('Name', 'SDAddress', 'SDPort', 'MaximumConcurrentJobs')

class DeviceAdmin(admin.ModelAdmin):
    list_display = ('Name', 'DeviceType', 'MaximumConcurrentJobs')

class PoolAdmin(admin.ModelAdmin):
    list_display = ('Name', 'PoolType', 'Storage', 'LabelFormat',)

class ClientAdmin(admin.ModelAdmin):
    list_display = ('Name', 'FDAddress', 'FDPort', 'Comment')
    
#class JobDefs(admin.ModelAdmin):
#    list_display = ('Name', 'Type', 'Level',)

class JobAdmin(admin.ModelAdmin):
    list_display = ('Name', 'Type', 'Level', 'Client', 'Pool', )

admin.site.register(Director, DirectorAdmin)
admin.site.register(Storage, StorageAdmin)
admin.site.register(Client, ClientAdmin)
admin.site.register(Device, DeviceAdmin)
admin.site.register(Pool, PoolAdmin)
admin.site.register(Job, JobAdmin)
