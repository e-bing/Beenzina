from django import forms
from .models import Article, Comment

class ArticleForm(forms.ModelForm):

    class Meta:
        model = Article
        fields = ['movie', 'stars', 'oneline_comment', 'content', ]
        widgets = {
            # 'stars': forms.ChoiceField(),
            
            'oneline_comment': forms.TextInput(attrs={
                'class': "form-control",
                'style': 'max-width: 700px;',
                'placeholder': '영화는 어땠나요?'
            }), 

            'content': forms.Textarea(attrs={
                'class': "form-control",
                'style': 'max-width: 700px;',
                'placeholder': '자유롭게 내용을 입력해주세요.'
            }),
        }
        labels = {
            'stars': '별점',
            'oneline_comment': '한줄평',
            'content': '나의 다이어리',
            'movie': '영화'
        }


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        exclude = ['article', 'user']
        widgets = {
            'content': forms.TextInput(attrs={
                'class': 'form-control',
                'style': 'max-width: 500px; display: inline-block;',
                'placeholder': '댓글을 작성해보세요.'
            })
        }
        labels = {
            'content': ''
        }