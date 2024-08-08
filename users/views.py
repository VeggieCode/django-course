from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from .models import Profile

def register(request):    
    if request.method == 'POST':
        user_creation_form = UserRegisterForm(request.POST)
        if user_creation_form.is_valid():
            user_creation_form.save()            
            messages.success(request, f'Your account has been created! You are now able to log in!')
            return redirect('login')
    else:
        user_creation_form = UserRegisterForm()
    return render(request, 'users/register.html', context={'form': user_creation_form})

@login_required
def profile(request):
    try:
        profile = request.user.profile
    except Profile.DoesNotExist:
        profile = Profile(user=request.user)
        profile.save()

    if request.method == 'POST':
        # Due this are model forms we can populate them with model instances.    
        u_form = UserUpdateForm(data=request.POST, instance=request.user)
        p_form = ProfileUpdateForm(data=request.POST, files=request.FILES, instance=profile)

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('profile') # POST, GET, redirect pattern
    else:                
        u_form = UserUpdateForm(instance=request.user)        
        p_form = ProfileUpdateForm(instance=profile)        

    context = {
        'u_form': u_form,
        'p_form': p_form
    }

    return render(request, template_name='users/profile.html', context=context)

