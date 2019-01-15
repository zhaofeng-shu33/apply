from django.contrib import admin
from .models import ActivityManager, Activity, Choice, Person
from .forms import PersonForm



class ChoiceInline(admin.StackedInline):
    model = Choice
    extra = 1

class PersonInline(admin.TabularInline):
    model = Person.choices.through
    extra = 0

class ActivityInline(admin.StackedInline):
    model = Activity
    extra = 1

@admin.register(ActivityManager)
class ActivityManagerAdmin(admin.ModelAdmin):
    inlines = [ActivityInline]

@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    fields = ['name', 'gender', 'choices']
    form = PersonForm
    search_fields = ['name']

@admin.register(Activity)    
class ActivityAdmin(admin.ModelAdmin):
    inlines = [ChoiceInline]

@admin.register(Choice)
class ChoiceAdmin(admin.ModelAdmin):
    fields = ['activity', 'name', 'description', 'required_number']
    list_display = ('__str__','required_number', 'left_number')
    inlines = [PersonInline]



