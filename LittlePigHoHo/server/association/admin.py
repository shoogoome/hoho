from django.contrib import admin
from .models import Association, AssociationAttendance, AssociationDepartment, AssociationAccount
# Register your models here.

admin.site.register(Association)
admin.site.register(AssociationAttendance)
admin.site.register(AssociationDepartment)
admin.site.register(AssociationAccount)