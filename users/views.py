from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm

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
    return render(request, template_name='users/profile.html')
