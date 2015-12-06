from django import forms
from django.forms import Textarea

from models import *


class RegistrationForm(forms.Form):
    username = forms.EmailField()
    email = forms.EmailField()
    password1 = forms.CharField(max_length=200,
                                label='Password',
                                widget=forms.PasswordInput())
    password2 = forms.CharField(max_length=200,
                                label='Confirm password',
                                widget=forms.PasswordInput())
    firstname = forms.CharField(max_length=200,
                                label='firstname')
    lastname = forms.CharField(max_length=200,
                               label='lastname')

    # Customizes form validation for properties that apply to more
    # than one field.  Overrides the forms.Form.clean function.
    def clean(self):
        # Calls our parent (forms.Form) .clean function, gets a dictionary
        # of cleaned data as a result
        cleaned_data = super(RegistrationForm, self).clean()

        # Confirms that the two password fields match
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords did not match.")

        # Generally return the cleaned data we got from our parent.
        return cleaned_data

    # Customizes form validation for the username field.
    def clean_username(self):
        # Confirms that the username is not already present in the user model database.
        username = self.cleaned_data.get('username')
        if User.objects.filter(username__exact=username):
            raise forms.ValidationError("This email address has already been registered.")

        # Generally return the cleaned data we got from the cleaned_data dictionary.
        return username


class ProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        exclude = (
            'user', 'username', 'following', 'ranking_score', 'success_rate', 'role', 'image')
        widgets = {
            'description': Textarea(attrs={'cols': 80, 'rows': 50}),
        }
        field = ('firstname', 'lastname', 'age', 'bio')


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        exclude = {'user', }

    def clean(self):
        cleaned_data = super(PostForm, self).clean()
        return cleaned_data


class ProblemForm(forms.ModelForm):
    class Meta:
        model = Problem
        exclude = {'visible', 'success_rate'}
        field = ('name', 'description', 'example', 'difficulty', 'java_default', 'python_default',
                 'tle_limit', 'mle_limit', 'java_tests', 'python_tests')


class DiscussionForm(forms.Form):
    discussiontitle = forms.CharField(max_length=50)
    discussiontext = forms.CharField(max_length=1000)

    def clean(self):
        cleaned_data = super(DiscussionForm, self).clean()
        return cleaned_data


class CommentForm(forms.Form):
    commenttext = forms.CharField(max_length=100)

    def clean(self):
        cleaned_data = super(CommentForm, self).clean()
        return cleaned_data


class HistoryForm(forms.Form):
    codecontent = forms.CharField(max_length=10000)

    def clean(self):
        cleaned_data = super(HistoryForm, self).clean()
        return cleaned_data
