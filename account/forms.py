from django import forms
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import PasswordChangeForm
from django.db.models import Q

from account.models import Account


class UserCreationFormExtended(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs.update(
            {
                'id': 'FirstNameCreation',
                'class': 'form-control',

                'data_column': '6',
                'first': 'true'
            })
        self.fields['last_name'].widget.attrs.update(
            {
                'id': 'LastNameCreation',
                'class': 'form-control',
                'data_column': '6',
                'last': 'true'
            })
        self.fields['email'].widget.attrs.update(
            {
                'id': 'EmailCreation',
                'class': 'form-control',
                'autofocus': 'off',
            })
        self.fields['username'].widget.attrs.update(
            {
                'id': 'UsernameCreation',
                'class': 'form-control',
                'autocomplete': 'off'})
        self.fields['password1'].widget.attrs.update(
            {
                'id': 'PasswordCreation',
                'class': 'form-control',
                'data_column': '6', 'first': True
            })
        self.fields['password2'].widget.attrs.update(
            {
                'id': 'ConfirmPasswordCreation',
                'class': 'form-control',
                'data_column': '6',
                'last': True
            })

    class Meta:
        model = Account
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2']


class LoginForm(forms.Form):
    username_or_email = forms.CharField(required=True, label=_('Username or Email'),
                                        widget=forms.TextInput(attrs={
                                            'id': 'UserLogin',
                                            'class': 'form-control',
                                            'required': 'required',
                                            'autofocus': True,
                                        }))
    password = forms.CharField(strip=False, label=_('Password'), required=True,
                               widget=forms.PasswordInput(attrs={
                                   'id': 'PasswordLogin',
                                   'class': 'form-control',
                                   'required': 'required',
                               }))

    error_messages = {
        'invalid_login': _(
            "Please enter a correct Email and password. Note that both fields may be case-sensitive."
        ),
        'inactive': _("This account is inactive."),
    }

    class Meta:
        model = Account

    def clean_username_or_email(self):
        username_or_email = self.cleaned_data['username_or_email']

        user = Account.objects.filter(Q(username=username_or_email) | Q(email__iexact=username_or_email)).first()
        if not user:
            raise forms.ValidationError(_('We can\'t found any user with that Username/Email!'))

        if not user.is_active:
            raise forms.ValidationError(_('User is not Activated please check you Username/Email'))

        return self.cleaned_data['username_or_email']


class UpdatePasswordForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['old_password'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': _('Old password')})
        self.fields['new_password1'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': _('New password')})
        self.fields['new_password1'].help_text = _('''
        <ul>
        <li>Your password can’t be too similar to your other personal information.</li>
        <li>Your password must contain at least 8 characters.</li>
        <li>Your password can’t be a commonly used password.</li>
        <li>Your password can’t be entirely numeric.</li>
        </ul>
        ''')
        self.fields['new_password2'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': _('Confirm password')})


class AccountUpdateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['profile_pic'].widget = forms.FileInput(
            attrs={'class': 'form-control'}
        )
        self.fields['country'].widget.attrs.update(
            {'class': 'form-control'})
        self.fields['country'].required = False
        self.fields['profile_pic'].required = False

    class Meta:
        model = Account
        fields = ['profile_pic', 'country']


class ProfileUpdateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs.update(
            {'class': 'form-control'})
        self.fields['last_name'].widget.attrs.update(
            {'class': 'form-control'})

    class Meta:
        model = Account
        fields = ['first_name', 'last_name']


class AvatarUpdateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['profile_pic'].widget = forms.FileInput(
            attrs={'class': 'form-control', 'onchange': 'loadFile(event,"output_avatar")'}
        )

    class Meta:
        model = Account
        fields = ['profile_pic']
