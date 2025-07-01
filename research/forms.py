from django import forms
from .models import Research, Source, Pics

class ResearchForm(forms.ModelForm):
    class Meta:
        model = Research
        fields = ['name', 'topic', 'notes']

class SourceForm(forms.ModelForm):
    class Meta:
        model = Source
        fields = ['title', 'url', 'description']

class PicsForm(forms.ModelForm):
    class Meta:
        model = Pics
        fields = ['image', 'caption']