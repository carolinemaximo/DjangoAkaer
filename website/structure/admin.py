from django.contrib import admin
from structure.models import Topic, Entry


admin.site.register(Topic)
# topic = empresa
admin.site.register(Entry)
# entry = projeto