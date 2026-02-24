from django import forms
from .models import Schedule

class ScheduleForm(forms.ModelForm):
    class Meta:
        model = Schedule
        fields = '__all__'

class ScheduleFilterForm(forms.Form):
    day = forms.ChoiceField(
        choices=[("", "— Всі дні —")] + Schedule.DAYS,
        required=False,
        label="День тижня"
    )
    study = forms.IntegerField(
        required=False,
        label="Клас",
        widget=forms.NumberInput(attrs={"placeholder": "Наприклад: 9"})
    )