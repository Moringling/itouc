from django import forms
from .models import Article

class ArticleForm(forms.ModelForm):

    class Meta:
        model = Article
        fields = ["title", "content", "author", "is_published"]

        widgets = {
            "title" : forms.TextInput(attrs = {"placeholder":"标题...", "size":60}),
            "content" : forms.Textarea(attrs = {"placeholder":"正文...", "rows":12})
        }

        labels = {
            "title": "标题",
            "content": "正文",
            "author": "作者",
            "is_published": "是否公开"
        }
