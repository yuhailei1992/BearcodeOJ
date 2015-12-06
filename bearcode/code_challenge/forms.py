from django import forms
from django.core.files.images import get_image_dimensions
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordResetForm
from models import *
from django.forms import ModelForm, Textarea

class RegistrationForm(forms.Form):
    username = forms.EmailField()
    email = forms.EmailField()
    password1 = forms.CharField(max_length = 200, 
                                label='Password', 
                                widget = forms.PasswordInput())
    password2 = forms.CharField(max_length = 200, 
                                label='Confirm password',  
                                widget = forms.PasswordInput())
    firstname = forms.CharField(max_length = 200,
                                label='firstname')
    lastname = forms.CharField(max_length = 200,
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
        # Confirms that the username is not already present in the
        # User model database.
        username = self.cleaned_data.get('username')
        if User.objects.filter(username__exact=username):
            raise forms.ValidationError("This email address has already been registered.")

        # Generally return the cleaned data we got from the cleaned_data
        # dictionary
        return username

#class ImageUploadForm(forms.Form):
#   """Image upload form."""
#  image = forms.ImageField()

class ProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        exclude = ('user', 'username', 'following', 'ranking_score', 'success_rate','role', 'image')
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

        text = cleaned_data.get('posttext')
        #if not text:
        #    raise forms.ValidationError("You must input something to send")

        return cleaned_data

class ProblemForm(forms.ModelForm):
    class Meta:
        model = Problem
        exclude = {'visible', 'success_rate'}
        field = ('name', 'description', 'example', 'difficulty', 'java_default','python_default', 'tle_limit', 'mle_limit','java_tests','python_tests')

class DiscussionForm(forms.ModelForm):
    class Meta:
        model = Discussion
        exclude = {}
        field = ('title', 'text', 'user', 'problem', 'created_at')

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        exclude = {}
        field = ('text', 'user', 'discussion', 'created_at')

class HistoryForm(forms.ModelForm):
    class Meta:
        model = SubmitHistory
        exclude = {}
        field = ('text', 'user', 'problem', 'created_at', 'result', 'runtime')
        