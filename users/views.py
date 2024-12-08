from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render,redirect
from django.contrib import messages
from .forms import UserRegisterForm, ProfileUpdateForm
from .models import Profile

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Aссount was created for {username}')
            Profile.objects.create(user=user)
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form':form})


def home(request):
    return render(request, 'shop/home.html')


@login_required
def profile(request):
    profile = Profile.objects.get(user=request.user)
    return render(request, 'users/profile.html', {'profile':profile})

@login_required
def profile_edit(request):
    profile = request.user.profile
    print(f"Profile data: {profile.first_name}, {profile.last_name}, {profile.avatar}")


    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            print(form.cleaned_data)
            form.save()
            return redirect('profile')
        else:
            print(form.errors)

    else:
        form = ProfileUpdateForm(instance=profile)



    return render(request,'users/profile_edit.html', {'form':form})

