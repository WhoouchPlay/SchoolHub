from django import forms

from .models import Status, Action, Booking
from Resource.models import Resource


class StatusForm(forms.ModelForm):
    class Meta:
        model = Status
        fields = '__all__'


class ActionForm(forms.ModelForm):
    class Meta:
        model = Action
        fields = '__all__'


class BookingFormUser(forms.ModelForm):
    class Meta:
        model = Booking
        exclude = ["user", "created_at", "reason", "status"]


class BookingFormAdmin(forms.ModelForm):
    start_time = forms.DateTimeField(disabled=True)
    end_time = forms.DateTimeField(disabled=True)
    class Meta:
        model = Booking
        fields = ["status", "reason"]


