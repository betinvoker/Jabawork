from django.contrib import admin
from .models import Universities, Opinions

#   Показывает комментарии относящиеся к выбранному университету
class UniversitiesInline(admin.TabularInline):
    model = Opinions

@admin.register(Universities)
class UniversitiesAdmin(admin.ModelAdmin):
    list_display = ("id", "abbreviated", "name", "link", "logo", "link_universitiy")
    search_fields = ("abbreviated",)
    #   Показывает комментарии относящиеся к выбранному университету
    inlines = [UniversitiesInline]

@admin.register(Opinions)
class OpinionsAdmin(admin.ModelAdmin):
    list_display = ("id", "text", "date_opinion", "opinion", "university")
    list_filter = ("opinion",)
    search_fields = ("text",)
