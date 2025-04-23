from urllib.parse import unquote
import random
import re
import os

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
from django.contrib import messages

from .models import Record, Categories, Author
from .forms import SignUpForm


def home(request):
    records = Record.objects.filter(author_id__activate_status='Y', subject_id__activate_status='Y').order_by('-created_at')
    categories = Categories.objects.filter(activate_status='Y').order_by('name')
    
    return render(request, "home.html", {'records': records, 'categories': categories})


def category(request, category):
    category = unquote(category).strip().rstrip('/')  # Remove a barra final, se existir
    all_categories = Categories.objects.filter(activate_status='Y').order_by('name')
    selected_category = all_categories.filter(name__iexact=category.strip()).first()

    if selected_category:
        records = Record.objects.filter(subject_id=selected_category.id).order_by('-created_at')
    else:
        records = Record.objects.none()

    return render(request, "categories.html", {'selected_category': selected_category,
                                                'categories': all_categories,
                                                'records': records})


def record(request, pk, author_id, subject_id):
    article_record = get_object_or_404(Record, id=pk, author_id=author_id, subject_id=subject_id)
    file_path = article_record.thumb_image.removeprefix('/')
    print(file_path)

    if request.method == 'POST':
        if request.user.id == author_id:

            file_path = article_record.thumb_image.removeprefix('/')
            if os.path.exists(file_path):
                os.remove(file_path)

            article_record.delete()
            nome_resumido = f'{article_record.title[:50]}...' if len(article_record.title) > 50 else article_record.title
            messages.success(request, f'Artigo "{nome_resumido}" Apagado Com Sucesso !!')
            return redirect('meus_artigos')
        

    else:
        categories = Categories.objects.filter(activate_status='Y').order_by('name')

        return render(request, 'record.html', {'article_record': article_record, 'categories': categories})


def edit_record(request, pk, author_id, subject_id):
    record = get_object_or_404(Record, id=pk, author_id=author_id, subject_id=subject_id)
    categories = Categories.objects.filter(activate_status='Y').order_by('name')

    if request.method == 'POST':
        record.title = request.POST.get('title')
        record.article = request.POST.get('content')

        subject_id = request.POST['subject']
        record.subject_id = Categories.objects.get(id=subject_id)

        if request.FILES.get('thumb_image'):

            # Apaga Imagem Anterior
            file_path = record.thumb_image.removeprefix('/')
            if os.path.exists(file_path):
                os.remove(file_path)

            image = request.FILES['thumb_image']
            fs = FileSystemStorage()

            chave_aleatoria = [random.randint(0, 9) for _ in range(5)]

            key = ''.join(str(num) for num in chave_aleatoria)

            filename = fs.save(f'{key}_{pk}_{author_id}_{subject_id}_{str(image.name).replace(' ', '_')}', image)

            image_url = fs.url(filename)  
            record.thumb_image = image_url

        record.save()
        messages.success(request, f'Artigo Atualizado Com Sucesso!!')
        return redirect('edit_record', pk=record.id, author_id=record.author_id.id, subject_id=record.subject_id.id)


    return render(request, 'edit_record.html', {'record': record, 'categories': categories})


@login_required
def novo_artigo(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        article = request.POST.get('content')
        subject = request.POST['subject']
        subject_id = Categories.objects.get(id=subject)
        user_id = Author.objects.get(id=request.user.id)

        record = Record.objects.create(
            title=title,
            article=article,
            subject_id=subject_id,
            author_id=user_id
        )   

        if request.FILES.get('thumb_image'):

            image = request.FILES['thumb_image']
            fs = FileSystemStorage()

            chave_aleatoria = [random.randint(0, 9) for _ in range(5)]

            key = ''.join(str(num) for num in chave_aleatoria)

            filename = fs.save(f'{key}_{record.id}_{request.user.id}_{record.subject_id}_{str(image.name).replace(' ', '_')}', image)

            image_url = fs.url(filename)
            record.thumb_image = image_url

        record.save()
        messages.success(request, f'Artigo Criado Com Sucesso!!')
        return redirect('edit_record', pk=record.id, author_id=record.author_id.id, subject_id=record.subject_id.id)            


    categories = Categories.objects.filter(activate_status='Y').order_by('name')
    return render(request, 'new_record.html', {'categories': categories})


def articles_by_author(request, author_id):
    records = Record.objects.filter(author_id=author_id).order_by('-created_at')
    categories = Categories.objects.filter(activate_status='Y').order_by('name')
    return render(request, 'articles_by_author.html', {'records': records, 'categories': categories})


def user_login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f"Login realizado com sucesso! Seja bem-vindo, { user.first_name }!")
            return redirect('home')
        else:
            messages.error(request, "Usuário ou senha incorretos. Verifique seus dados e tente novamente.")
            return redirect('login')
    else:
        return render(request, "login.html",)


def user_logout(request):
    logout(request)
    messages.success(request, "Você foi desconectado com sucesso.")
    return redirect('home')


def user_register(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()

            username = form.cleaned_data["username"]
            password = form.cleaned_data["password1"]

            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, f"Você foi registrado com sucesso! Seja bem-vindo, { user.first_name }!")
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'register.html', {"form": form})


def portal_do_autor(request):
    records = Record.objects.filter(author_id=request.user.id).order_by('-created_at')[:5]
    categories = Categories.objects.filter(activate_status='Y').order_by('name')
    return render(request, 'portal_do_autor.html', {'categories': categories, 'records': records})


def meus_artigos(request):
    records = Record.objects.filter(author_id=request.user.id).order_by('-created_at')
    categories = Categories.objects.filter(activate_status='Y').order_by('name')
    return render(request, 'meus_artigos.html', {'categories': categories, 'records': records})
