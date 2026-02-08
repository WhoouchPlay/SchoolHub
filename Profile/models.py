from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

# Create your models here.

class Action(models.Model):
    class ActionChoise(models.TextChoices):
        CREATEBOOKING = "CB", _("CreateBooking")
        READBOOKING = "RB", _("ReadBooking")
        UPDATEBOOKING = "UB", _("UpdateBooking")
        
    name = models.CharField(
        max_length=100,
        verbose_name="Дозволена дія",
        help_text="Введіть назву дії",
        choices=ActionChoise.choices,
        default=ActionChoise.READBOOKING
    )

    def __str__(self):
        return f"Назва дії: {self.name}"


class Position(models.Model):
    name = models.CharField(max_length=255, verbose_name="Посада", help_text="Введіть назву посади")
    actions = models.ManyToManyField(Action, verbose_name="Список дозволів", help_text="Виберіть дії, які можна виконувати")

    def __str__(self):
        return f"Посада: {self.name}|Дії: {','.join(self.actions.all())}"


class Subject(models.Model):
    name = models.CharField(max_length=150, verbose_name="Назва предмету", help_text="Введіть назву предмету")

    def __str__(self):
        return f"Назва предмету: {self.name}"


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    position = models.ForeignKey(Position, on_delete=models.SET_NULL, null=True, blank=True, default=None)
    subjects = models.ManyToManyField(Subject, verbose_name="Список предметів")
    avatar = models.ImageField(upload_to=".", verbose_name="Аватарка", null=True, blank=True, default=None)
    bio = models.TextField(verbose_name="Біографія", null=True, blank=True, default=None)
    phone_number = models.CharField(max_length=20, null=True, blank=True, default=None, verbose_name="Номер телефону", help_text="Введіть номер телефону")

    def __str__(self):
        return f"Користувач: {self.user.get_full_name()}|Предмети: {','.join(self.subjects.all())}"