from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.http import HttpRequest

from .models import Profile, Action, Position, Subject
from .forms import UserForm, UserFormEdit, SignInForm, ActionForm, SubjectForm, ProfileForm, PositionForm


# Create your views here.


def sign_up(request: HttpRequest):
    if request.method == "POST":
        sign_up_form = UserForm(request.POST)
        profile_form = ProfileForm(data=request.POST, files=request.FILES)
        if sign_up_form.is_valid():
            user = sign_up_form.save()
            if profile_form.is_valid():
                profile = profile_form.save(commit=False)
                profile.user = user
                profile.save()
            else:
                profile = Profile(user=user)
                profile.save()

            messages.success(request, "Вітаємо з реєстрацією! 🎉")
            return redirect("sign_in")

        messages.error(request, sign_up_form.errors)
        return redirect("sign_up")
    
    return render(request, "sign_up.html", dict(sign_up_form=UserForm(), profile_form=ProfileForm()))


def sign_in(request: HttpRequest):
    if request.method == "POST":
        form = SignInForm(request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data.get('username'),
                password=form.cleaned_data.get('password')            
            )
            if user:
                login(request, user)
                messages.success(request, "Вітаємо в нашій системі! 🤗")
                return redirect("index")
            else:
                messages.error(request, "Користувача не знайдено 🙁")
                return redirect("sign_in")
            
        messages.error(request, form.errors)
        return redirect("sign_in")
    
    return render(request, "sign_in.html", dict(form=SignInForm()))


@login_required
def update_profile(request: HttpRequest):
    if request.method == "POST":
        user_form = UserFormEdit(data=request.POST, instance=request.user)
        if user_form.changed_data:
            user_form.save()

        profile_form = ProfileForm(data=request.POST, files=request.FILES, instance=request.user.profile)
        if profile_form.changed_data:
            profile_form.save()

        messages.success(request, "Дані успішно оновлено 😎")
        return redirect("profile")
    return render(
        request,
        "profile.html", 
        dict(user_form=UserFormEdit(instance=request.user), profile_form=ProfileForm(instance=request.user.profile))
    )


@login_required
def index(request: HttpRequest):
    return render(request, "index.html")


@login_required
def logout_view(request: HttpRequest):
    logout(request)
    messages.success(request, "Ви вийшли з системи. До зустрічі 👋")
    return redirect("sign_in")