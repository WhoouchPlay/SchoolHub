from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpRequest
from django.views.decorators.http import require_GET, require_POST

from .models import Schedule
from .forms import ScheduleForm
from Booking.permissions import has_permission

# Create your views here.


@require_GET
def schedule_view(request: HttpRequest):
    messages.success(request, "Використайте фільтр")
    schedule_all = Schedule.objects.all()
    return render(request, "schedule_view.html", dict(schedule_all=schedule_all))


@has_permission("RS")
@require_POST
def schedule_view_filtered(request: HttpRequest):
    day = request.POST.get("day") or None
    study = request.POST.get("study") or None
    schedule = Schedule.objects.all()
    if day:
        schedule = schedule.filter(day=day)
    if study:
        schedule = schedule.filter(study=study)
    return render(request, "schedule_view.html", dict(schedule=schedule))

    # OR

    # day = request.POST.get("day") or None
    # study = request.POST.get("study") or None
    # if day and study:
    #     schedule = Schedule.objects.filter(day=day, study=study).all()
    # elif day:
    #     schedule = Schedule.objects.filter(day=day).all()
    # elif study:
    #     schedule = Schedule.objects.filter(study=study).all()
    #     schedule = []
    # return render(request, "schedule_view.html", dict(schedule=schedule))


@has_permission("CS")
def add_schedule(request: HttpRequest):
    form = ScheduleForm(data=request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            form.save()
            messages.success(request, "Заняття успішно додано")
            return redirect("add_schedule")
    else:
        messages.success(request, "Додати нове заняття")
    return render(request, "schedule_add.html", dict(form=form))


@has_permission("CS")
def edit_schedule(request: HttpRequest, id: int):
    schedule = Schedule.objects.filter(id=id).first()
    if not schedule:
        messages.error(request, f"Заняття не знайдено 🤷‍♂️")
        return redirect("schedule_view")
    
    form = ScheduleForm(data=request.POST or None, instance=schedule)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Дані про заняття успішно оновлено 🎉")
        return redirect("schedule_view")
        
    messages.success(request, f"Оновлення {schedule}")
    return render(request, "schedule_add.html", dict(form=form))
    

@has_permission("CS")
def remove_schedule(request: HttpRequest, id: int):
    schedule = Schedule.objects.filter(id=id).first()
    if not schedule:
        messages.error(request, f"Заняття не знайдено 🤷‍♂️")
        return redirect("schedule_view")
    
    schedule.delete()
    messages.success(request, f"{schedule} успішно видалено")
    return redirect("schedule_view")