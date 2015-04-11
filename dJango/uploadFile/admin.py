from django.contrib import admin

from uploadFile import models


class ReportAdmin(admin.ModelAdmin):
    fields = ('title', 'short_desc', 'detailed_desc', 'location', 'file', 'tag', 'private', 'groups')
    list_display = ('title', 'private')


admin.site.register(models.Report, ReportAdmin)
