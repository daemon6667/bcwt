from django.contrib import admin
from resources.models import Director, Console, Storage, Device, Pool

# Register your models here.
class DirectorAdmin(admin.ModelAdmin):
    list_display = ('Name', 'Address', 'DirPort')

class StorageAdmin(admin.ModelAdmin):
    list_display = ('Name', 'SDAddress', 'SDPort', 'MaximumConcurrentJobs')

class DeviceAdmin(admin.ModelAdmin):
    list_display = ('Name', 'DeviceType', 'MaximumConcurrentJobs')

class PoolAdmin(admin.ModelAdmin):
    list_display = ('Name', 'PoolType', 'Storage', 'LabelFormat',)

admin.site.register(Director, DirectorAdmin)
admin.site.register(Console)
admin.site.register(Storage, StorageAdmin)
admin.site.register(Device, DeviceAdmin)
admin.site.register(Pool, PoolAdmin);
