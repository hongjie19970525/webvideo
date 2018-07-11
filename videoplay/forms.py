from django import forms

class UserForm(forms.Form):
    username=forms.CharField(max_length=20)
    password=forms.IntegerField()
    
class UserCommentForm(forms.Form):
    user_comment=forms.CharField(max_length=300)
    
class MoviePayForm(forms.Form):
    movie_pay=forms.IntegerField()