from django.contrib import admin
from .models import *
from parler.admin import TranslatableAdmin
# Register your models here.
admin.site.register(CustomUser)
admin.site.register(Project, TranslatableAdmin)
admin.site.register(Comment)
admin.site.register(Label, TranslatableAdmin)
admin.site.register(News, TranslatableAdmin)
admin.site.register(NewsContent, TranslatableAdmin)
admin.site.register(NewsImage)
admin.site.register(Course, TranslatableAdmin)
admin.site.register(Module, TranslatableAdmin)


# Make CustomUser at Authentication and Authorization in the admin site
# Add TranslatableAdmin to enable the translation of the model

