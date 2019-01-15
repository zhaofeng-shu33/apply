from django.apps import AppConfig
from django.contrib.admin.apps import AdminConfig
from django.contrib import admin

class VolunteerAdminConfig(AdminConfig):
    default_site = 'apply.apps.VolunteerAdminSite'

class ApplyConfig(AppConfig):
    name = 'apply'

class VolunteerAdminSite(admin.AdminSite):
    site_header = 'Volunteer administration'