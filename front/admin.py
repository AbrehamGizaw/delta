from django.contrib import admin
from .models import *
from django.apps import apps 
from django.contrib.auth.models import Group 

models = apps.get_app_config('front').get_models()

for model in models:
    admin.site.register(model)
admin.site.unregister(Group)
# admin.site.register(Events)
# admin.site.register(Gallery)
# admin.site.register(ResearchOutput)
# admin.site.register(Application)
# admin.site.register(Contact)
