from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User


class UserRegistrationForm(UserCreationForm):
    telegram_username = forms.CharField(
        max_length=100,
        required=False,
        help_text="Укажите ваш Telegram username (без @)",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'username'})
    )
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'telegram_username']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['class'] = 'form-control'
    
    def save(self, commit=True):
        user = super().save(commit=False)
        telegram_username = self.cleaned_data.get('telegram_username')
        if telegram_username:
            user.telegram_username = telegram_username
            user.notification_telegram = True
            # TODO: Получить chat_id по username (нужно написать функцию)
        if commit:
            user.save()
        return user