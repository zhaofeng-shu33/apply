from django import forms
from django.forms import ModelForm
from .models import Person, Activity

class PersonForm(ModelForm):
    class Meta:
        model = Person
        fields = ['name', 'choices']
    # overwrite clean method
    # self.instance is valid
    def clean(self):
        cleaned_data = super().clean()
        choices = cleaned_data.get("choices")
        activity_cnt = {}
        if choices is None:
            return
        for i in choices:
            activity = Activity.objects.get(choice = i)
            key = activity.id
            if(activity_cnt.get(key) is None):
                activity_cnt[key] = i.name
            else:
                raise forms.ValidationError(
                    "%(choice_1)s and %(choice_2)s belong to the same activity %(activity)s.",
                    code = 'collision',
                    params = {'choice_1': i.name, 
                              'choice_2': activity_cnt[key],
                              'activity': activity.name
                              }
                )
                