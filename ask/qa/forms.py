from django import forms
from django.contrib.auth.models import User
from qa.models import Question, Answer


class AskForm(forms.Form):
    title = forms.CharField(max_length=100) 
    text = forms.CharField(widget=forms.Textarea)

    def clean(self):
        pass

    def save(self, author=None):
        question = Question(author=author, **self.cleaned_data)
        question.save()
        return question



class AnswerForm(forms.Form):
    text = forms.CharField(widget=forms.Textarea)
    question = forms.IntegerField() 

    def clean(self):
        pass

    def save(self, author):
        answer = Answer(author=author, **self.cleaned_data)
        answer.save()
        return answer   


class SignUpForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'password', )
    
    def save(self, commit=True):
        user = super(SignUpForm, self).save(commit=False)
        user.set_password(user.password) # set password properly before commit
        if commit:
            user.save()
        return user


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
