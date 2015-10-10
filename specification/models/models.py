from django.db import models

# User class for built-in authentication module
from django.contrib.auth.models import User

class UserProfile(models.Model):
	user = models.ForeignKey(User, null=False)
	username = models.CharField(max_length=200)
	firstname = models.CharField(max_length=200)
	lastname = models.CharField(max_length=200)
	image = models.ImageField(upload_to='/', default='/static/photos/none_photo.jpg', null=True, blank=True)
	bio = models.CharField(max_length=420, default="", blank=True, null=True)
	age = models.PositiveIntegerField(default=0)
	def __unicode__(self):
		return self.firstname + " " + self.lastname

class Submission(models.Model):
	user = models.ForeignKey(User, null=False)
	problem = models.ForeignKey(Problem, null=False)
	result = models.BooleanField(null=False)
	createdAt = models.DateTimeField(auto_now_add=True)
	def __unicode__(self):
		return str(self.user.id) + " " + str(self.problem.id)

class Problem(models.Model):
	name = models.CharField(max_length=42)
	createdUser = models.ForeignKey(User, null=False)
	createdAt = models.DateTimeField(auto_now_add=True)
	description = models.CharField(max_length=420)
	tests = models.FileField(upload_to='/', default='/tests/', null=False)
	def __unicode__(self):
		return self.name

class DiscussionPost(models.Model):
	createdUser = models.ForeignKey(User, null=False)
	createdAt = models.DateTimeField(auto_now_add=True)
	problem = models.ForeignKey(Problem, null=False)
	title = models.CharField(max_length=42)
	body = models.CharField(max_length=420)
	def __unicode__(self):
		return self.title

class FolowUp(modesl.Model):
	createdUser = models.ForeignKey(User, null=False)
	createdAt = models.DateTimeField(auto_now_add=True)
	discussionPost = models.ForeignKey(DiscussionPost, null=False)
	body = models.CharField(max_length=420)
	def __unicode__(self):
		return self.body

class Vote(models.Model):
	user = models.ForeignKey(User, null=False)
	problem = models.ForeignKey(Problem, null=False)
	option = models.BooleanField(null=True)
	def __unicode__(self):
		return str(self.user.id) + " " + str(self.problem.id)

class Tag(models.Model):
	name = models.CharField(max_length=40)
	problems = models.ManyToManyField(Problem, related_name='related_problems')
	def __unicode__(self):
		return self.name
