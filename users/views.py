from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login
from .forms import UserRegistrationForm


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Регистрация успешна!')
            return redirect('plants:list')
        else:
            # Если форма невалидна — показываем ошибки
            messages.error(request, 'Ошибка регистрации. Проверьте данные.')
    else:
        form = UserRegistrationForm()
    
    return render(request, 'users/register.html', {'form': form})
