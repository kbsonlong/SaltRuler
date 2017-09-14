from django.contrib import admin
from .models import Users,department

# Register your models here.
class UserAdmin(admin.ModelAdmin):
    list_display = ('username','password')


class FlatPageAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': ('url', 'title', 'content', 'sites')
        }),
        ('Advanced options', {
            'classes': ('collapse',),
            'fields': ('enable_comments', 'registration_required', 'template_name')
        }),
    )

# admin.site.register(Author,FlatPageAdmin)
admin.site.register([Users,department])




