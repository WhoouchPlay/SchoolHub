from django import forms

from .models import Resource, Location


class ResourceForm(forms.ModelForm):
    class Meta:
        model = Resource
        fields = '__all__'


class LocationForm(forms.ModelForm):
    class Meta:
        model = Location
        fields = '__all__'