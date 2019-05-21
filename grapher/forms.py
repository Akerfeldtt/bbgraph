from django.db import models
from django import forms
from .models import Inputdata
# Create your models here.
'''
class Inputdata(models.Model):
    temperature=models.DecimalField(max_digits=6, decimal_places=3)
    radius=models.DecimalField(max_digits=19, decimal_places=3)
'''

class ParamForm(forms.Form):
    temperature = forms.DecimalField(max_digits=6, decimal_places=3)
    radius = forms.DecimalField(max_digits=19, decimal_places=3)
    redshift = forms.DecimalField(max_digits=6, decimal_places=3)
    '''
    class Meta:
        fields = ('temperature', 'radius')
        # This is the association between the model and the model form
        model = Inputdata
    '''
    # def clean(self):
    #     data = self.cleaned_data
    #     DATA.append(data)
    #     if len(DATA)<4:
    #         return data
    #     else:
    #         raise forms.ValidationError('To many requests made, please reload the page to refresh your requests.')
    def clean(self):
        from .views import ID
        cd = self.cleaned_data
        if len(ID)>4:
            self.add_error(None, "You are limited to 5 images at once.")
        return cd
