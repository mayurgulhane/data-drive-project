from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.core.files.storage import FileSystemStorage
from django.contrib import messages
from django.views.decorators.csrf import csrf_protect
import json

from .models import Folder, File


# User Authentication Views
def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        # Validate input
        if password1 != password2:
            return render(request, 'register.html', {'error': 'Passwords do not match'})
        if User.objects.filter(username=username).exists():
            return render(request, 'register.html', {'error': 'Username already exists'})
        if User.objects.filter(email=email).exists():
            return render(request, 'register.html', {'error': 'Email already exists'})

        # Create and log in the user
        user = User.objects.create_user(username=username, email=email, password=password1)
        login(request, user)
        return redirect('home')

    return render(request, 'register.html')


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('home')
        return render(request, 'login.html', {'error': 'Invalid credentials'})

    return render(request, 'login.html')


def logout_view(request):
    logout(request)
    return redirect('login')


# Home View
@login_required
def home(request):
    folder_id = request.GET.get('folder_id')
    folder = None

    if folder_id:
        folder = get_object_or_404(Folder, id=folder_id, owner=request.user)
        folders = Folder.objects.filter(owner=request.user, parent=folder)
        files = File.objects.filter(owner=request.user, folder=folder)
    else:
        folders = Folder.objects.filter(owner=request.user, parent=None)
        files = File.objects.filter(owner=request.user, folder=None)

    ancestors = folder.get_ancestors() if folder else []
    return render(request, 'home.html', {
        'folders': folders,
        'files': files,
        'current_folder': folder,
        'ancestors': ancestors,
    })

@login_required
def create_folder(request):
    if request.method == 'POST':
        folder_name = request.POST.get('name')
        parent_folder_id = request.POST.get('parent')

        # Check if parent folder exists
        parent_folder = None
        if parent_folder_id:
            try:
                parent_folder = Folder.objects.get(id=parent_folder_id)
            except Folder.DoesNotExist:
                return JsonResponse({'error': 'Parent folder not found'}, status=400)

        # Create the folder
        folder = Folder(name=folder_name, owner=request.user, parent=parent_folder)
        folder.save()

        return JsonResponse({'status': 'success', 'message': 'Folder created successfully.'})

    return JsonResponse({'error': 'Invalid request'}, status=400)

@login_required
def delete_folder(request, folder_id):
    folder = get_object_or_404(Folder, id=folder_id, owner=request.user)

    if folder.subfolders.exists() or File.objects.filter(folder=folder).exists():
        messages.error(request, "Cannot delete a folder containing files or subfolders.")
    else:
        folder.delete()
        messages.success(request, "Folder deleted successfully.")

    return redirect('home')


@csrf_protect
@login_required
def update_folder_name(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        folder_id = data.get('id')
        new_name = data.get('new_name')

        folder = get_object_or_404(Folder, id=folder_id, owner=request.user)
        folder.name = new_name
        folder.save()

        return JsonResponse({'success': True})
    return JsonResponse({'success': False})


@login_required
def upload_file(request):
    if request.method == 'POST' and request.FILES['file']:
        file = request.FILES['file']
        folder_id = request.POST.get('folder_id')  

        # Get the folder object if folder_id is provided
        folder = None
        if folder_id:
            folder = get_object_or_404(Folder, id=folder_id, owner=request.user)

        fs = FileSystemStorage()
        filename = fs.save(file.name, file)

        # Create a File object and associate it with the folder if it exists
        file_instance = File(name=filename, folder=folder, owner=request.user)
        file_instance.save()

        return JsonResponse({'message': 'File uploaded successfully.'}, status=200)

    return JsonResponse({'message': 'Failed to upload file.'}, status=400)





@login_required
def delete_file(request, file_id):
    file = get_object_or_404(File, id=file_id, owner=request.user)
    file.delete()
    messages.success(request, "File deleted successfully.")
    return redirect('home')


@csrf_protect
@login_required
def update_file_name(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        file_id = data.get('id')
        new_name = data.get('new_name')

        file = get_object_or_404(File, id=file_id, owner=request.user)
        file.name = new_name
        file.save()

        return JsonResponse({'success': True})
    return JsonResponse({'success': False})
