from bitfield.admin import BitFieldListFilter
from bitfield.forms import BitFieldCheckboxSelectMultiple
from bitfield.models import BitField
from django.contrib import admin

from . import models


# Register your models here.


class MonitoringModelAdmin(admin.ModelAdmin):
    formfield_overrides = {
        BitField: {'widget': BitFieldCheckboxSelectMultiple},
    }


admin.site.register(models.Profile)
admin.site.register(models.Address)
admin.site.register(models.Monitoring, MonitoringModelAdmin)
admin.site.register(models.Symptom)
admin.site.register(models.Trip)
admin.site.register(models.ActionLog)
