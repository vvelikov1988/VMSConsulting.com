from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Idea, Comment
from .forms import AddCommentForm, AddIdeaForm


def index(request):
    return render(request, '')


def idea_detail(request, pk):
    idea = get_object_or_404(Idea, pk=pk)
    if request.method == 'POST':
        form = AddCommentForm(request.POST)
        if form.is_valid():
            Comment.objects.create(user=request.user, idea=idea, text=form.cleaned_data.get('text'))

    context = {
        'idea': idea,
        'comment_form': AddCommentForm,

    }
    return render(request, 'idea/detail.html', context)


def add_idea(request):
    if request.method == 'POST':
        form = AddIdeaForm(request.POST)
        if form.is_valid():
            idea = form.save(commit=False)
            idea.user = request.user
            idea.save()
            messages.success(request, 'Idea Add Successful')
            return redirect('idea:detail', pk=idea.pk)
        else:
            context = {
                'idea_form': AddIdeaForm(request.POST)
            }
    else:
        context = {
            'idea_form': AddIdeaForm()
        }
    return render(request, 'idea/new.html', context)


def delete(request, pk):
    idea = Idea.objects.get(pk=pk)
    if request.user == idea.user:
        idea.delete()
    return redirect('account:home')


def edit(request, pk):
    idea = Idea.objects.get(pk=pk)
    if request.method == 'POST':
        form = AddIdeaForm(request.POST or None, request.FILES or None, instance=idea)
        if form.is_valid():
            form.save()
            messages.success(request, 'Idea edited!')
            return redirect('idea:detail', pk=pk)
    if request.user == idea.user:
        context = {
            'edit_form': AddIdeaForm(instance=idea),
        }
        return render(request, 'idea/edit.html', context)

