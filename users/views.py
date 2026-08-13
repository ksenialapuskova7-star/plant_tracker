from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login
from .forms import UserRegistrationForm


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            
            # Если указан Telegram username, пробуем получить chat_id
            if user.telegram_username:
                chat_id = get_chat_id_by_username(user.telegram_username)
                if chat_id:
                    user.telegram_id = chat_id
                    user.notification_telegram = True
                    user.save()
                    messages.success(request, f'Telegram подключен!')
                else:
                    messages.warning(request, 'Не удалось найти Telegram username. Проверьте правильность написания.')
            
            login(request, user)
            messages.success(request, 'Регистрация успешна!')
            return redirect('plants:list')
    else:
        form = UserRegistrationForm()
    
    return render(request, 'users/register.html', {'form': form})