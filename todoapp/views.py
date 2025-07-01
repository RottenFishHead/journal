from django.shortcuts import render, redirect, get_object_or_404
from .models import Task, Entry, Author, Books
from django.http import JsonResponse
from .forms import TaskForm, BooksForm
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q

@login_required
def task_list(request):
    tasks = Task.objects.filter(user=request.user)
    return render(request, 'todo/task_list.html', {'tasks': tasks})

@login_required
def task_create(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            return redirect('todoapp:task_list')
    else:
        form = TaskForm()
    return render(request, 'todo/task_form.html', {'form': form})

@login_required
def task_edit(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('todoapp:task_list')
    else:
        form = TaskForm(instance=task)
    return render(request, 'todo/task_form.html', {'form': form})

@login_required
def task_delete(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)
    if request.method == 'POST':
        task.delete()
        return redirect('todoapp:task_list')
    return render(request, 'todo/task_confirm_delete.html', {'task': task})


@login_required
def books_list(request):
    books = Books.objects.select_related('author').all()
    return render(request, 'todo/books_list.html', {'books': books})

@login_required
def books_create(request):
    if request.method == 'POST':
        form = BooksForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('todoapp:books_list')
    else:
        form = BooksForm()
    return render(request, 'todo/books_form.html', {'form': form})

@login_required
def books_edit(request, pk):
    book = get_object_or_404(Books, pk=pk)
    if request.method == 'POST':
        form = BooksForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            return redirect('todoapp:books_list')
    else:
        form = BooksForm(instance=book)
    return render(request, 'todo/books_form.html', {'form': form})

@login_required
def books_delete(request, pk):
    book = get_object_or_404(Books, pk=pk)
    if request.method == 'POST':
        book.delete()
        return redirect('todoapp:books_list')
    return render(request, 'todo/books_confirm_delete.html', {'book': book})

@login_required
def author_create_ajax(request):
    if request.method == "POST":
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        email = request.POST.get("email")
        bio = request.POST.get("bio", "")
        if Author.objects.filter(email=email).exists():
            return JsonResponse({"success": False, "error": "Email already exists."})
        author = Author.objects.create(
            first_name=first_name,
            last_name=last_name,
            email=email,
            bio=bio
        )
        return JsonResponse({
            "success": True,
            "author": {
                "id": author.id,
                "name": f"{author.first_name} {author.last_name}"
            }
        })
    return JsonResponse({"success": False, "error": "Invalid request."})

@login_required
def books_by_author(request):
    authors = Author.objects.all().order_by('last_name', 'first_name')
    selected_author_id = request.GET.get('author')
    books = Books.objects.none()
    page_obj = None

    if selected_author_id:
        books = Books.objects.filter(author_id=selected_author_id).order_by('-date_created')
        paginator = Paginator(books, 10)  # 10 books per page
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

    return render(request, 'todo/books_by_author.html', {
        'authors': authors,
        'selected_author_id': int(selected_author_id) if selected_author_id else None,
        'page_obj': page_obj,
    })


@login_required
def books_search(request):
    query = request.GET.get('q', '')
    books = Books.objects.none()
    page_obj = None

    if query:
        books = Books.objects.filter(
            Q(title__icontains=query) |
            Q(isbn__icontains=query) |
            Q(publisher__icontains=query) |
            Q(author__first_name__icontains=query) |
            Q(author__last_name__icontains=query)
        ).select_related('author').order_by('-date_created')
        paginator = Paginator(books, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

    return render(request, 'todo/books_search.html', {
        'query': query,
        'page_obj': page_obj,
    })