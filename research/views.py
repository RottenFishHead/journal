from django.shortcuts import render, redirect, get_object_or_404
from .models import Research, Source, Pics
from .forms import ResearchForm, SourceForm, PicsForm
from django.contrib.auth.decorators import login_required

@login_required
def research_list(request):
    researches = Research.objects.all().order_by('-date_created')
    return render(request, 'research/research_list.html', {'researches': researches})

@login_required
def research_detail(request, pk):
    research = get_object_or_404(Research, pk=pk)
    source_form = SourceForm()
    pics_form = PicsForm()
    if request.method == 'POST':
        if 'add_source' in request.POST:
            source_form = SourceForm(request.POST)
            if source_form.is_valid():
                source = source_form.save(commit=False)
                source.research = research
                source.save()
                return redirect('research:research_detail', pk=pk)
        elif 'add_pic' in request.POST:
            pics_form = PicsForm(request.POST, request.FILES)
            if pics_form.is_valid():
                pic = pics_form.save(commit=False)
                pic.research = research
                pic.save()
                return redirect('research:research_detail', pk=pk)
    return render(request, 'research/research_detail.html', {
        'research': research,
        'source_form': source_form,
        'pics_form': pics_form,
    })

@login_required
def research_create(request):
    if request.method == 'POST':
        form = ResearchForm(request.POST)
        if form.is_valid():
            research = form.save()
            return redirect('research:research_detail', pk=research.pk)
    else:
        form = ResearchForm()
    return render(request, 'research/research_form.html', {'form': form})

@login_required
def research_edit(request, pk):
    research = get_object_or_404(Research, pk=pk)
    if request.method == 'POST':
        form = ResearchForm(request.POST, instance=research)
        if form.is_valid():
            form.save()
            return redirect('research:research_detail', pk=research.pk)
    else:
        form = ResearchForm(instance=research)
    return render(request, 'research/research_edit.html', {'form': form, 'research': research})

@login_required
def research_delete(request, pk):
    research = get_object_or_404(Research, pk=pk)
    if request.method == 'POST':
        research.delete()
        return redirect('research:research_list')
    return render(request, 'research/research_delete.html', {'research': research})