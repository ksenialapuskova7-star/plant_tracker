from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Plant, CareLog
from .forms import PlantForm, CareLogForm


@login_required
def plant_list(request):
    plants = Plant.objects.filter(user=request.user)
    return render(request, 'plants/list.html', {'plants': plants})


@login_required
def plant_detail(request, pk):
    plant = get_object_or_404(Plant, pk=pk, user=request.user)
    care_logs = plant.care_logs.all()[:10]
    return render(request, 'plants/detail.html', {'plant': plant, 'care_logs': care_logs})


@login_required
def plant_create(request):
    if request.method == 'POST':
        form = PlantForm(request.POST, request.FILES)
        if form.is_valid():
            plant = form.save(commit=False)
            plant.user = request.user
            plant.save()
            messages.success(request, 'Растение добавлено!')
            return redirect('plants:detail', pk=plant.pk)
    else:
        form = PlantForm()
    return render(request, 'plants/form.html', {'form': form, 'title': 'Добавить растение'})


@login_required
def plant_edit(request, pk):
    plant = get_object_or_404(Plant, pk=pk, user=request.user)
    if request.method == 'POST':
        form = PlantForm(request.POST, request.FILES, instance=plant)
        if form.is_valid():
            form.save()
            messages.success(request, 'Растение обновлено!')
            return redirect('plants:detail', pk=plant.pk)
    else:
        form = PlantForm(instance=plant)
    return render(request, 'plants/form.html', {'form': form, 'title': 'Редактировать растение'})


@login_required
def plant_delete(request, pk):
    plant = get_object_or_404(Plant, pk=pk, user=request.user)
    if request.method == 'POST':
        plant.delete()
        messages.success(request, 'Растение удалено!')
        return redirect('plants:list')
    return render(request, 'plants/confirm_delete.html', {'plant': plant})


@login_required
def add_care(request, pk):
    plant = get_object_or_404(Plant, pk=pk, user=request.user)
    if request.method == 'POST':
        form = CareLogForm(request.POST)
        if form.is_valid():
            care = form.save(commit=False)
            care.plant = plant
            care.save()
            
            if care.action_type == 'watering':
                plant.last_watered = care.date
            elif care.action_type == 'fertilizing':
                plant.last_fertilized = care.date
            elif care.action_type == 'repotting':
                plant.last_repotted = care.date
            plant.save()
            
            messages.success(request, 'Запись добавлена!')
            return redirect('plants:detail', pk=plant.pk)
    else:
        form = CareLogForm()
    return render(request, 'plants/add_care.html', {'form': form, 'plant': plant})