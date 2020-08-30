from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text
from django.utils.translation import ugettext_lazy as _
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate, update_session_auth_hash
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.decorators import login_required

from account.models import Account
from account.forms import (
    LoginForm, UpdatePasswordForm, UserCreationFormExtended,
    ProfileUpdateForm, AccountUpdateForm, AvatarUpdateForm,
)
from account.tokens import account_activation_token
from addon.decorators import language_scanner
from idea.models import Idea, Comment


@language_scanner
def index(request):
    if request.GET.get('q'):
        q = request.GET.get('q')
        context = {
            'ideas': Idea.objects.filter(title__icontains=q)
        }
    else:
        context = {
            'ideas': Idea.objects.all()
        }
    return render(request, 'guest/index.html', context)


@language_scanner
def LOGIN(request):
    if request.user.is_authenticated:
        return redirect('account:home')

    context = {
        'form': LoginForm()
    }
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data.get('username_or_email'),
                password=form.cleaned_data.get('password')
            )
            if user:
                login(request, user)
                return redirect(request.META.get('HTTP_REFERER', '/'))
            else:
                messages.error(request, _('One of the coordinates wrong, or both!'))
        else:
            context['form'] = form
    return render(request, 'guest/login.html', context)


@language_scanner
def REGISTER(request):
    if 'register' not in request.META.get('HTTP_REFERER', '/'):
        request.session['next'] = request.META.get('HTTP_REFERER', '/')
    if request.method == 'POST':
        form = UserCreationFormExtended(request.POST)
        if form.is_valid():
            user_form = form.save()
            user_form.is_active = False
            user_form.save()
            current_site = get_current_site(request)
            mail_subject = _('Activate your blog account.')
            message = render_to_string('settings/active_email.html', {
                'user': user_form,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user_form.pk)),
                'token': account_activation_token.make_token(user_form),
                'path': request.session['next'] if 'next' in request.session else None,
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                mail_subject, message, to=[to_email]
            )
            email.send()
            messages.success(request, _('Please, Check Your Email we\'ve sent an activation link for you Profile.'))
        else:
            messages.error(request, _('Please make sure all the inputs are right!'))

    context = {
        'form': UserCreationFormExtended()
    }
    return render(request, 'guest/register.html', context)


@language_scanner
def LOGOUT(request):
    logout(request)
    return redirect('account:home')


@language_scanner
def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = Account.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        if request.GET.get('next'):
            return redirect(request.GET['next'])
        return redirect('account:home')
    else:
        return HttpResponse(_('Activation link is invalid!'))


@login_required
@language_scanner
def change_password(request):
    if request.method == 'POST':
        form = UpdatePasswordForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, _('Your password was successfully updated!'))
            return redirect('account:update-password')
        else:
            messages.error(request, _('Please correct the error below.'))
    else:
        form = UpdatePasswordForm(request.user)

    context = {
        'form': form
    }
    return render(request, 'settings/change_password.html', context)


@login_required
@language_scanner
def update_profile(request):
    instance = get_object_or_404(Account, id=request.user.id)
    user = ProfileUpdateForm(instance=request.user)
    account = AccountUpdateForm(instance=request.user)

    if request.method == 'POST':
        user = ProfileUpdateForm(request.POST or None, instance=instance)
        account = AccountUpdateForm(request.POST or None, request.FILES or None, instance=instance)

        if user.is_valid() and account.is_valid():
            user.save()
            account.save()
            messages.success(request, _('Edits Saved.'))
        else:
            messages.error(request, _('Please Correct any error down below'))
    context = {
        'forms': [
            {'form': user, 'title': _('Personal Information')},
            {'form': account, 'title': ''},
        ]
    }
    return render(request, 'settings/update_profile.html', context)


@language_scanner
def profile(request, pk):
    user = get_object_or_404(Account, pk=pk)
    context = {
        'user': user,
    }
    if request.user.is_authenticated and request.user == user:
        context.update({
            'avatar_form': AvatarUpdateForm(),
        })
    else:
        context.update({
            'login_form': LoginForm(),
        })

    return render(request, 'profile/profile.html', context)


def change_profile_pic(request):
    if request.method == 'POST':
        form = AvatarUpdateForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            user = Account.objects.get(pk=request.user.pk)
            user.profile_pic = form.cleaned_data.get('profile_pic')
            user.save()
            messages.success(request, 'Changed Success')
        else:
            print(False)
            messages.error(request, 'Sorry Something went Wrong please try again!')
    return redirect('account:profile', pk=request.user.pk)
