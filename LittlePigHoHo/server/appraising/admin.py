from django.contrib import admin
from .models import AppraisingScoreTemplate, AppraisingScore

# Register your models here.


admin.site.register(AppraisingScore)
admin.site.register(AppraisingScoreTemplate)
