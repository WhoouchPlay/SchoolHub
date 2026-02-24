from django.db import models
from Resource.models import Resource
from Profile.models import Subject

class Schedule(models.Model):
    DAYS = [
        ("Понеділок", "Понеділок"),
        ("Вівторок", "Вівторок"),
        ("Середа", "Середа"),
        ("Четвер", "Четвер"),
        ("П'ятниця", "П'ятниця"),
    ]

    resource = models.ForeignKey(Resource, on_delete=models.CASCADE, blank=True, verbose_name="Кабінет")
    meet_url = models.URLField(verbose_name="Посилання на зустріч", max_length=1000, default=None, blank=True, null=True)
    day = models.CharField(max_length=20, verbose_name="День тижня", choices=DAYS)
    number = models.PositiveIntegerField(verbose_name="Година")
    study = models.PositiveIntegerField("Клас")
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, verbose_name="Предмет")

    def __str__(self):
        return f"{self.subject} на {self.number} годині ({self.study} клас)"