from django import forms
from Object.models import CreateObject


class CreateObjForm(forms.ModelForm):
    class Meta:
        model = CreateObject
        fields = '__all__'

