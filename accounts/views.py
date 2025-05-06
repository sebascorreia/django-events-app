from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
# Create your views here.
from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser 

def register(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("index")
    else:
        form = CustomUserCreationForm()
    return render(request, "accounts/register.html", {"form": form})
@login_required
def profile(request):
    user = request.user
    return render(request, "accounts/profile.html", {"user": user})
@login_required
def edit_profile(request):
    if request.method == "POST":
        form = CustomUserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect("profile")
    else:
        form = CustomUserChangeForm(instance=request.user)
    return render(request, "accounts/edit_profile.html", {"form": form})