from django.contrib import admin
from .models import PageURL, Ad, Visit, Token, Campaign

# Register your models here.
class PageURLAdmin(admin.ModelAdmin):
	class Meta:
		model = PageURL

admin.site.register(PageURL, PageURLAdmin)

class AdAdmin(admin.ModelAdmin):
	class Meta:
		model = Ad


admin.site.register(Ad, AdAdmin)

class VisitAdmin(admin.ModelAdmin):
	class Meta:
		model = Visit

admin.site.register(Visit, VisitAdmin)

admin.site.register(Token)

admin.site.register(Campaign)