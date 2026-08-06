from django import forms
from .models import Plant, CareLog, Reminder



class PlantForm(forms.ModelForm):
    class Meta:
        model = Plant
        fields = '__all__'
        exclude = ['user', 'created_at', 'updated_at']
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
                  'interval_days', 'next_reminder_date', 'notes']
        widgets = {
            'plant': forms.Select(attrs={'class': 'form-select'}),
            'action_type': forms.Select(attrs={'class': 'form-select'}),
            'custom_action_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Своё действие'}),
            'frequency': forms.Select(attrs={'class': 'form-select'}),
            'interval_days': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
            'next_reminder_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }
    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['plant'].queryset = Plant.objects.filter(user=user)