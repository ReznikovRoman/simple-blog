from ckeditor_uploader.widgets import CKEditorUploadingWidget

from django import forms

from .models import Post, Comment


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'header_image', 'content',)
        widgets = {
            'title': forms.TextInput(attrs={'class': 'post_title_class input_field'}),
            'content': CKEditorUploadingWidget(),
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text',)
        widgets = {
            'text': forms.Textarea(attrs={'class': 'comment_text_class input_field'}),
        }

    def __init__(self, *args, **kwargs):
        super(CommentForm, self).__init__(*args, **kwargs)
        self.fields['text'].label = ''
