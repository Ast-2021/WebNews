from django.contrib import admin
from .models import *


admin.site.register(Articles)
admin.site.register(Comments)
admin.site.register(Categories)
admin.site.register(Tags)

