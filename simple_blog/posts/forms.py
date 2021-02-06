
from django import forms
from ckeditor.widgets import CKEditorWidget
from ckeditor_uploader.widgets import CKEditorUploadingWidget

from . import models


################################################################################################################


class PostForm(forms.ModelForm):
    class Meta:
        fields = ('title', 'header_image', 'content')
        model = models.Post
        widgets = {
            'title': forms.TextInput(attrs={'class': 'post_title_class input_field'}),
            'content': CKEditorUploadingWidget(),
        }
        

class CommentForm(forms.ModelForm):
    class Meta:
        model = models.Comment
        fields = ('text', )

        widgets = {
            'text': forms.Textarea(attrs={'class': 'comment_text_class input_field'}),
        }

    def __init__(self, *args, **kwargs):
        super(CommentForm, self).__init__(*args, **kwargs)
        self.fields['text'].label = ''






