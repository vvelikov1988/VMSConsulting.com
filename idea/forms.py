from django import forms

from .models import Comment, Idea


class AddCommentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['text'].widget.attrs.update(
            {
                'class': 'form-control',
            })

    class Meta:
        model = Comment
        fields = ['text']


class AddIdeaForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title'].widget.attrs.update(
            {
                'class': 'form-control',
            })
        self.fields['topic'].widget.attrs.update(
            {
                'class': 'form-control',
            })
        self.fields['description'].widget.attrs.update(
            {
                'class': 'form-control',
            })
        self.fields['image'].widget.attrs.update(
            {
                'class': 'form-control',
            })
        self.fields['file'].widget.attrs.update(
            {
                'class': 'form-control',
            })

    class Meta:
        model = Idea
        fields = ['title', 'topic', 'description', 'image', 'file']
