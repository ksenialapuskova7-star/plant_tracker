from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Plant, CareLog, Reminder, PlantPhoto
from .forms import PlantForm, CareLogForm, ReminderForm


@login_required
def plant_list(request):
    plants = Plant.objects.filter(user=request.user)
    return render(request, 'plants/list.html', {'plants': plants})


@login_required
def plant_detail(request, pk):
    plant = get_object_or_404(Plant, pk=pk, user=request.user)
    care_logs = plant.care_logs.all()[:10]
    return render(request, 'plants/detail.html', {'plant': plant, 'care_logs': care_logs})


MAX_PHOTOS = 10

@login_required
def plant_create(request):
    if request.method == 'POST':
        form = PlantForm(request.POST, request.FILES, user=request.user)
        photos = [p for p in request.FILES.getlist('photos') if p]

    if not photos:
        form.add_error(None, 'Добавьте хотя бы одно фото')
        return render(request, 'plants/form.html', {
            'form': form,
            'title': 'Добавить растение',
            'button_text': 'Создать'
        })

    if len(photos) > 10:
        form.add_error(None, 'Максимум 10 фото')
        return render(request, 'plants/form.html', {
            'form': form,
            'title': 'Добавить растение',
            'button_text': 'Создать'
        })

    if form.is_valid():
        plant = form.save(commit=False)
        plant.user = request.user
        plant.save()

        main_index = None
        for idx in range(len(photos)):
            if request.POST.get(f'is_main_{idx}') == 'on' and main_index is None:
                main_index = idx

        for idx, photo in enumerate(photos):
            is_main = (idx == main_index) if main_index is not None else (idx == 0)
            PlantPhoto.objects.create(
                plant=plant,
                image=photo,
                caption=request.POST.get(f'caption_{idx}', ''),
                order=idx,
                is_main=is_main,
            )

        messages.success(request, 'Растение добавлено!')
        return redirect('plants:detail', pk=plant.pk)

@login_required
def plant_edit(request, pk):
    plant = get_object_or_404(Plant, pk=pk, user=request.user)

    if request.method == 'POST':
        form = PlantForm(request.POST, request.FILES, instance=plant, user=request.user)

        if form.is_valid():
            form.save()

            # ===== УДАЛЕНИЕ ФОТО =====
            delete_photos = request.POST.getlist('delete_photos')
            if delete_photos:
                PlantPhoto.objects.filter(id__in=delete_photos, plant=plant).delete()

            # ===== НОВЫЕ ФОТО =====
            photos = [p for p in request.FILES.getlist('photos') if p]

            # Определяем главное фото среди НОВЫХ
            main_index = None
            for idx in range(len(photos)):
                if request.POST.get(f'is_main_{idx}') == 'on' and main_index is None:
                    main_index = idx

            # Если пользователь отметил главное среди новых —
            # снимаем флаг "главное" со всех старых
            if main_index is not None:
                plant.photos.update(is_main=False)

            # Сохраняем новые фото
            start_order = plant.photos.count()
            for idx, photo in enumerate(photos):
                is_main = (idx == main_index) if main_index is not None else False
                PlantPhoto.objects.create(
                    plant=plant,
                    image=photo,
                    caption=request.POST.get(f'caption_{idx}', ''),
                    order=start_order + idx,
                    is_main=is_main,
                )

            # Если вообще ни одного главного — назначим первое
            if not plant.photos.filter(is_main=True).exists():
                first = plant.photos.order_by('order').first()
                if first:
                    first.is_main = True
                    first.save(update_fields=['is_main'])

            messages.success(request, 'Растение обновлено!')
            return redirect('plants:detail', pk=plant.pk)

    else:
        form = PlantForm(instance=plant, user=request.user)

    return render(request, 'plants/form.html', {
        'form': form,
        'plant': plant,
        'title': 'Редактировать растение',
        'button_text': 'Сохранить'
    })

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


@login_required
def reminder_create(request, plant_id=None):
    if plant_id:
        plant = get_object_or_404(Plant, pk=plant_id, user=request.user)
    else:
        plant = None
    
    if request.method == 'POST':
        form = ReminderForm(request.POST, user=request.user)
        if form.is_valid():
            reminder = form.save(commit=False)
            reminder.user = request.user
            reminder.save()
            messages.success(request, 'Напоминание создано!')
            return redirect('plants:detail', pk=reminder.plant.pk)
    else:
        initial = {}
        if plant:
            initial['plant'] = plant
        form = ReminderForm(user=request.user, initial=initial)
    
    return render(request, 'plants/reminder_form.html', {
        'form': form,
        'plant': plant,
        'title': 'Создать напоминание',
        'button_text': 'Создать',
    })


@login_required
def reminder_list(request):
    reminders = Reminder.objects.filter(user=request.user).order_by('reminder_date', 'reminder_time')
    return render(request, 'plants/reminder_list.html', {'reminders': reminders})


@login_required
def reminder_edit(request, pk):
    reminder = get_object_or_404(Reminder, pk=pk, user=request.user)
    
    if request.method == 'POST':
        form = ReminderForm(request.POST, instance=reminder, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Напоминание обновлено!')
            return redirect('plants:reminder_list')
    else:
        form = ReminderForm(instance=reminder, user=request.user)
    
    return render(request, 'plants/reminder_form.html', {
        'form': form,
        'plant': reminder.plant,
        'title': 'Редактировать напоминание',
        'button_text': 'Сохранить',
    })


@login_required
def reminder_delete(request, pk):
    reminder = get_object_or_404(Reminder, pk=pk, user=request.user)
    if request.method == 'POST':
        reminder.delete()
        messages.success(request, 'Напоминание удалено!')
        return redirect('plants:reminder_list')
    return render(request, 'plants/reminder_confirm_delete.html', {'reminder': reminder})