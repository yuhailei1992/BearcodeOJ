from django.db import models

# User class for built-in authentication module
from django.contrib.auth.models import User

class UserProfile(models.Model):
	user = models.OneToOneField(User, unique=True, primary_key=True)
	username = models.EmailField(unique=True, default="username")
	first_name = models.CharField(max_length=200, null=True)
	last_name = models.CharField(max_length=200, null=True)
	age = models.PositiveIntegerField(default=0)
	bio = models.CharField(max_length=420, default="", blank=True, null=True)
	image = models.ImageField(upload_to='/', default = '/static/photos/none_photo.jpg', null=True, blank=True)
	following = models.ManyToManyField(User, related_name='following_list')

	# Returns all comments associated with a specific post id
	@staticmethod
	def get_profile(user_profile_id=-1):
		return UserProfile.objects.get(user_id=user_profile_id)

	def __unicode__(self):
		return self.first_name + " " + self.last_name


class Problem(models.Model):
    name = models.CharField(max_length=50, default="newproblem")
    description = models.TextField(max_length=420, default="", blank=True)
    example = models.TextField(max_length=420, default="", blank=True)
    default = models.TextField(max_length=420, default="", blank=True)
    tle_limit = models.PositiveIntegerField(default=1)
    mle_limit = models.PositiveIntegerField(default=500)
    java_tests = models.TextField(max_length=1000, default="", blank=True)
    python_tests = models.TextField(max_length=1000, default="", blank=True)
    def __unicode__(self):
        return self.name

class Discussion(models.Model):
	title = models.CharField(max_length=30)
	text = models.CharField(max_length=100)
	user = models.ForeignKey(User)
	problem = models.ForeignKey(Problem)
	created_at = models.DateTimeField(auto_now_add=True)
	def __unicode__(self):
		return self.text

class Post(models.Model):
	text = models.CharField(max_length=42)
	user = models.ForeignKey(User)
	created_at = models.DateTimeField(auto_now_add=True)
	def __unicode__(self):
		return self.text

class Comment(models.Model):
	text = models.CharField(max_length=42)
	user = models.ForeignKey(User)
	discussion = models.ForeignKey(Discussion)
	created_at = models.DateTimeField(auto_now_add=True)
	def __unicode__(self):
		return self.text

class SubmitHistory(models.Model):
	text = models.CharField(max_length=400)
	user = models.ForeignKey(User)
	problem = models.ForeignKey(Problem)
	created_at = models.DateTimeField(auto_now_add=True)
	result = models.CharField(max_length=42)
	runtime = models.PositiveIntegerField(null=True)
	def __unicode__(self):
		return self.text

