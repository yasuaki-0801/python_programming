from django.forms import ModelForm, TextInput, Textarea
from cms.models import Comment, Reply
from django import forms
from django.conf import settings
from django.core.mail import BadHeaderError, send_mail
from django.http import HttpResponse
from django.utils.translation import gettext as _

class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ('author', 'text')
        widgets = {
            'author': TextInput(attrs={
                'class': 'form-control',
                'placeholder': _('Name'),
            }),
            'text': Textarea(attrs={
                'class': 'form-control',
                'placeholder': _('Cotent'),
            }),
        }
        labels = {
            'author': '',
            'text': '',
        }


class ReplyForm(ModelForm):
    class Meta:
        model = Reply
        fields = ('author', 'text')
        widgets = {
            'author': TextInput(attrs={
                'class': 'form-control',
                'placeholder': _('Name'),
            }),
            'text': Textarea(attrs={
                'class': 'form-control',
                'placeholder': _(''),
            }),
        }
        labels = {
            'author': '',
            'text': '',
        }


class ContactForm(forms.Form):
    name = forms.CharField(
        label='',
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': _("Name"),
        }),

    )

    email = forms.EmailField(
        label='',
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': _("mail address"),
        }),
    )

    message = forms.CharField(
        label='',
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': _(""),
        }),
    )

    def send_email(self):
        subject = _("お問い合わせ")
        message = self.cleaned_data['message']
        name = self.cleaned_data['name']
        email = self.cleaned_data['email']
        from_email = '{name} <{email}>'.format(name=name, email=email)
        recipient_list = [settings.EMAIL_HOST_USER]  # 受信者リスト
        try:
            send_mail(subject, message, from_email, recipient_list)
        except BadHeaderError:
            return HttpResponse(_("無効なヘッダが検出されました。"))
