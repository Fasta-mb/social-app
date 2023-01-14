from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse, reverse_lazy

from auths.forms import LoginForm



def register(request):
    if request.user.is_authenticated:
        return redirect(reverse('home'))
    
    if request.method == "POST":
        form = UserCreationForm(data=request.POST)
        if form.is_valid():
            new_form = form.save(commit=False)
            new_form.username = new_form.username.lower()
            new_form.save()
            login(request, new_form)
            return redirect(reverse('create-profile'))
    else:
        form = UserCreationForm()
    context = {'form': form}
    return render(request, 'auths/register.html', context)

def login_user(request):
    if request.user.is_authenticated:
        return redirect(reverse('home'))
    
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = authenticate(username=data['username'], password=data['password'])
            if user is not None:
                login(request, user)
                return redirect(reverse('home'))
    else:
        form = LoginForm()
        
    context = {'form': form}
    return render(request, 'auths/login.html', context)
    
class ChangePassword(PasswordChangeView):
    fields = '__all__'
    success_url = reverse_lazy('password-change-done')
    redirect_authenticated_user = True
    template_name = 'auths/password_change.html'
    
  