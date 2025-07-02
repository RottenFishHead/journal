from django import forms
from .models import Task, Books, Author

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['user', 'title', 'description', 'due_date', 'priority', 'is_completed', 'star_rating']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'star_rating': forms.Select(choices=[(i, f'{i} Stars') for i in range(6)], attrs={'class': 'form-select'}),
        }


class BooksForm(forms.ModelForm):
    class Meta:
        model = Books
        fields = ['author', 'title', 'isbn', 'publisher', 'notes']