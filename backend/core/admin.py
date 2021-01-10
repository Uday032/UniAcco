from django.contrib import admin
from django.http import HttpResponse
import csv

# Register your models here.
from .models import UserLoginHistory, UserProfile

def export_history(modeladmin, request, queryset):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="loginhistory.csv"'
    writer = csv.writer(response)
    writer.writerow(['ipaddress', 'user'])
    histories = queryset.values_list('ipaddress', 'user')
    for history in histories:
        writer.writerow(history)
    return response
export_history.short_description = 'Export to csv'

class HistoryAdmin(admin.ModelAdmin):
    list_display = ['ipaddress', 'user']
    actions = [export_history, ]

admin.site.register(UserLoginHistory, HistoryAdmin)
admin.site.register(UserProfile)