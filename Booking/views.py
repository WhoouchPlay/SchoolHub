from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpRequest
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied

from .forms import BookingFormAdmin, BookingFormUser
from Profile.models import Position, Action
from .models import Booking, Status
from .permissions import has_permission
# Create your views here.


@has_permission("CB")
@login_required
def create_book(request: HttpRequest):
    form = BookingFormUser(data=request.POST or None)
    if form.is_valid():
        book: Booking = form.save(commit=False)
        book.user = request.user
        book.status = Status.objects.filter(name="Waiting").first()
        book.save()
        messages.success(request, "Кабінет заброньовано. Очікуйте підтвердження від адміністратора.")
        return redirect("resource")
    return render(request, "booking_user.html", dict(form=form))


@has_permission("UB")
@login_required
def update_book(request: HttpRequest, id: int):
    book = Booking.objects.get(pk=id)
    form = BookingFormAdmin(data=request.POST or None, instance=book)
    if form.is_valid():
        form.save()
        messages.success(request, "Інформацію оновлено")
        return redirect("resource")
    return render(request, "booking_admin.html", dict(form=form, book=book))


@has_permission("RB")
@login_required
def resources(request: HttpRequest):
    return render(request, "Resource.html", dict(booking=Booking.objects.all()))