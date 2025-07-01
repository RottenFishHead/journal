from django.urls import path
from todoapp.views import task_list, task_create, task_edit, task_delete, \
    books_list, books_create, books_edit, books_delete, author_create_ajax, \
    books_by_author, books_search

app_name = 'todoapp'

urlpatterns = [
    path('', task_list, name='task_list'),
    path('create/', task_create, name='task_create'),
    path('edit/<int:pk>/', task_edit, name='task_edit'),
    path('delete/<int:pk>/', task_delete, name='task_delete'),
    path('books/', books_list, name='books_list'),
    path('books/by-author/', books_by_author, name='books_by_author'),
    path('books/search/', books_search, name='books_search'),
    path('books/create/', books_create, name='books_create'),
    path('books/edit/<int:pk>/', books_edit, name='books_edit'),
    path('books/delete/<int:pk>/', books_delete, name='books_delete'),
    path('authors/create/ajax/', author_create_ajax, name='author_create_ajax'),
]