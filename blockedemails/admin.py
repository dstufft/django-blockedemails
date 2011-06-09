from django.contrib import admin
from blockedemails.models import Domain, Email

class DomainAdmin(admin.ModelAdmin):
    search_fields = ["domain"]

class EmailAdmin(admin.ModelAdmin):
    search_fields = ["email"]

admin.site.register(Domain, DomainAdmin)
admin.site.register(Email, EmailAdmin)