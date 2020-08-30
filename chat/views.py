from django.http import HttpResponseForbidden
from django.shortcuts import render, get_object_or_404
from django.http import Http404
from django.contrib.auth.decorators import login_required

from .forms import ComposeForm
from .models import Thread, ChatMessage

from account.models import Account


def index(request):
    pass


@login_required()
def thread(request, username):
    obj, created = Thread.objects.get_or_new(request.user, username)
    if obj is None:
        raise Http404

    if request.method == 'POST':
        if not request.user.is_authenticated:
            return HttpResponseForbidden()
        object = obj
        form = ComposeForm()
        if form.is_valid():
            _thread = object
            user = request.user
            message = form.cleaned_data.get("message")
            ChatMessage.objects.create(user=user, thread=_thread, message=message)
        else:
            pass

    context = {
        'thread': obj,
        'form': ComposeForm(),
        'receiver': get_object_or_404(Account, username=username),
    }
    return render(request, 'chat/room.html', context)


def test(request):
    return render(request, 'chat/test.html')
