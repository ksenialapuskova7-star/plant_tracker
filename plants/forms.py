from django import forms
from .models import Plant, CareLog, Reminder, PlantPhoto, Category  



class PlantForm(forms.ModelForm):
    # Новое поле: выбор категории
    category_choice = forms.ModelChoiceField(
        queryset=Category.objects.none(),
        required=False,
        label="Категория",
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    
    # Новое поле: пользовательская категория
    custom_category = forms.CharField(
        max_length=100,
        required=False,
        label="Или введите свою категорию",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Например: "Суккуленты"'})
    )
    
    # Новое поле: плодоносящее
    is_fruiting = forms.BooleanField(
        required=False,
        label="Плодоносящее",
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )

    class Meta:
        model = Plant
        fields = [
            'name', 'scientific_name', 'location',
            'category_choice', 'custom_category',
            'is_fruiting',
            'light_preference', 'watering_frequency', 'watering_volume',
            'fertilizer_frequency', 'repot_frequency',
            'temperature_min', 'temperature_max', 'humidity_preference',
            'needs_misting', 'is_toxic',
            'dormant_period_start', 'dormant_period_end',
            'purchased_at', 'health_status', 'notes'
        ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'scientific_name': forms.TextInput(attrs={'class': 'form-control'}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
            'light_preference': forms.Select(attrs={'class': 'form-select'}),
            'watering_frequency': forms.Select(attrs={'class': 'form-select'}),
            'watering_volume': forms.NumberInput(attrs={'class': 'form-control'}),
            'fertilizer_frequency': forms.NumberInput(attrs={'class': 'form-control'}),
            'repot_frequency': forms.NumberInput(attrs={'class': 'form-control'}),
            'temperature_min': forms.NumberInput(attrs={'class': 'form-control'}),
            'temperature_max': forms.NumberInput(attrs={'class': 'form-control'}),
            'humidity_preference': forms.NumberInput(attrs={'class': 'form-control'}),
            'needs_misting': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_toxic': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'dormant_period_start': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'dormant_period_end': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'purchased_at': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'last_watered': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'last_fertilized': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'last_repotted': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'health_status': forms.Select(attrs={'class': 'form-select'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        if user:
            self.fields['category_choice'].queryset = Category.objects.filter(user=user)
        
        if self.instance and self.instance.pk:
            if self.instance.custom_category:
                self.fields['custom_category'].initial = self.instance.custom_category
            elif self.instance.category:
                self.fields['category_choice'].initial = self.instance.category
    def save(self, commit=True):
        instance = super().save(commit=False)
        
        # Обработка категории
        category_choice = self.cleaned_data.get('category_choice')
        custom_category = self.cleaned_data.get('custom_category')
        
        if custom_category:
            instance.custom_category = custom_category
            instance.category = None
        elif category_choice:
            instance.category = category_choice
            instance.custom_category = None
        else:
            instance.category = None
            instance.custom_category = None
        
        if commit:
            instance.save()
        return instance


class CareLogForm(forms.ModelForm):
    class Meta:
        model = CareLog
        fields = ['action_type', 'notes']
        widgets = {
            'action_type': forms.Select(attrs={'class': 'form-select'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }

class ReminderForm(forms.ModelForm):
    class Meta:
        model = Reminder
        fields = ['plant', 'action_type', 'custom_action_name', 'frequency', 
                  'interval_days', 'reminder_date', 'reminder_time', 'notes']
        widgets = {
            'plant': forms.Select(attrs={'class': 'form-select'}),
            'action_type': forms.Select(attrs={'class': 'form-select'}),
            'custom_action_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Своё действие'}),
            'frequency': forms.Select(attrs={'class': 'form-select'}),
            'interval_days': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
            'reminder_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'reminder_time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }
    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['plant'].queryset = Plant.objects.filter(user=user)