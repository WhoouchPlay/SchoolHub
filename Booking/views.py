from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpRequest
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied

from .forms import BookingFormAdmin, BookingFormUser
from Profile.models import Position, Action
from .models import Booking, Status

# Create your views here.


@login_required
def create_book(request: HttpRequest):
    if not request.user.profile.positions.filter(actions__name="CB").exists():
        # raise PermissionDenied
        messages.error(request, "У Вас недостатньо прав 🤷")
        return redirect("resource")
    
    form = BookingFormUser(data=request.POST or None)
    if form.is_valid():
        book: Booking = form.save(commit=False)
        book.user = request.user
        book.status = Status.objects.filter(name="Waiting")
        book.save()
        messages.success(request, "Кабінет заброньовано. Очікуйте підтвердження від адміністратора.")
        return redirect("resource")
    return render(request, "booking_user.html", dict(form=form))


@login_required
def update_book(request: HttpRequest, id: int):
    positions = Position.objects.filter(actions__name="UB").all()
    if not any(position in request.user.profile.positions.all() for position in positions):
        messages.error(request, "У Вас недостатньо прав")
        return redirect("resource")
    
    form = BookingFormAdmin(data=request.POST or None, instance=Booking.objects.get(pk=id))
    if form.is_valid():
        form.save()
        messages.success(request, "Інформацію оновлено")
        return redirect("resource")
    return render(request, "booking_admin.html", dict(form=form))


@login_required
def resources(request: HttpRequest):
    return render(request, "Resource.html", dict(booking=Booking.objects.all()))