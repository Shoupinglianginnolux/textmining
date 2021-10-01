from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from .models import SRQs, Cases, Keywords, Logfiles, TMPSRQ, Training

# Register your models here.
admin.site.register(Cases)
admin.site.register(Keywords)
admin.site.register(Logfiles)
admin.site.register(SRQs)
admin.site.register(TMPSRQ)
admin.site.register(Training)


