from django.contrib import admin
from .models import Contact, Experience, ExperienceTask, Profile, Project, Technology

admin.site.site_header = "baranczov · управление сайтом"
admin.site.site_title = "baranczov"
admin.site.index_title = "Контент портфолио"

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return super().has_add_permission(request) and not Profile.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False

class OrderedAdmin(admin.ModelAdmin):
    list_display = ("__str__", "position", "published")
    list_editable = ("position", "published")
    list_filter = ("published",)

class ExperienceTaskInline(admin.StackedInline):
    model = ExperienceTask
    extra = 0
    fields = ("position", "published", ("title_ru", "title_en"), "description_ru", "description_en")

@admin.register(Experience)
class ExperienceAdmin(OrderedAdmin):
    exclude = ("tasks_ru", "tasks_en")
    inlines = (ExperienceTaskInline,)

for model in (Project, Technology, Contact):
    admin.site.register(model, OrderedAdmin)

