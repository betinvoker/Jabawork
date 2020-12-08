from django.contrib import admin
from .models import Universities, Opinions

@admin.register(Universities)
class UniversitiesAdmin(admin.ModelAdmin):
    list_display = ("id", "abbreviated", "name", "link", "logo", "link_universitiy")
    search_fields = ("abbreviated",)

@admin.register(Opinions)
class OpinionsAdmin(admin.ModelAdmin):
    list_display = ("id", "text", "date_opinion", "opinion", "university")
    list_filter = ("date_opinion", "opinion")
    search_fields = ("text",)