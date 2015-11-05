from django.db import models
from django.db.models.signals import post_save
from time import time

#from django.contrib.auth.models import AbstractUser
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
		#print "asjdlasj"
		return UserProfile.objects.get(user_id=user_profile_id)

	def __unicode__(self):
		return self.first_name + " " + self.last_name


class Problem(models.Model):
    name = models.CharField(max_length=50, default="newproblem")
    # created_at = models.DateTimeField(auto_now_add=True)
    description = models.TextField(max_length=420, default="", blank=True)
    example = models.TextField(max_length=420, default="", blank=True)
    default = models.TextField(max_length=420, default="", blank=True)
    tle_limit = models.PositiveIntegerField(default=1000)
    mle_limit = models.PositiveIntegerField(default=500)
    javaTests = models.FileField(upload_to="/javatests", default="/tests/", null=False)
    pythonTests = models.FileField(upload_to="/pythontests", default="/tests/", null=False)

    def __unicode__(self):
        return self.name

class Post(models.Model):
	text = models.CharField(max_length=42)
	user = models.ForeignKey(User)
	created_at = models.DateTimeField(auto_now_add=True)
	def __unicode__(self):
		return self.text

class Comment(models.Model):
	post = models.ForeignKey(Post)
	text = models.CharField(max_length=250)
	created_at = models.DateTimeField(auto_now_add=True)
	user = models.ForeignKey(UserProfile)

	def __unicode__(self):
		return self.text
    
	def __str__(self):
		return self.__unicode__()

    # Returns all comments associated with a specific post id
	@staticmethod
	def get_comments(post=-1):
		return Comment.objects.filter(post_id=post).order_by('-created_at')