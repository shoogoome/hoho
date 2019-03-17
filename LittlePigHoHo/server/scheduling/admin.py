from django.contrib import admin
from .models import AssociationAccountCurriculum, AssociationCurriculum, AssociationScheduling
# Register your models here.

admin.site.register(AssociationAccountCurriculum)
admin.site.register(AssociationCurriculum)
admin.site.register(AssociationScheduling)