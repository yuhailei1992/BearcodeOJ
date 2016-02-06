from django.db import models

# User class for built-in authentication module
from django.contrib.auth.models import User


class UserProfile(models.Model):
    """
    the model for the user profile to store the relative required information
    """
    user = models.OneToOneField(User, unique=True, primary_key=True)
    username = models.EmailField(unique=True, default="username")
    first_name = models.CharField(max_length=200, null=True)
    last_name = models.CharField(max_length=200, null=True)
    age = models.PositiveIntegerField(default=0)
    bio = models.CharField(max_length=420, default="", blank=True, null=True)
    image = models.ImageField(upload_to='/', default='/static/photos/none_photo.jpg', null=True, blank=True)
    following = models.ManyToManyField(User, related_name='following_list')
    success_rate = models.CharField(max_length=10, default="0.00%")
    role = models.CharField(max_length=10, default="nuser")

    @staticmethod
    def get_profile(user_profile_id=-1):
        return UserProfile.objects.get(user_id=user_profile_id)

    def __unicode__(self):
        return self.first_name + " " + self.last_name


class Problem(models.Model):
    """
    the model for the problem to solve
    """
    DIFFICULTY_EASY = 'Easy'
    DIFFICULTY_MIDD = 'Medium'
    DIFFICULTY_HARD = 'Hard'
    DIFFICULTY_CHOICES = [(DIFFICULTY_EASY, 'Easy'),
                          (DIFFICULTY_MIDD, 'Medium'),
                          (DIFFICULTY_HARD, 'Hard')]

    CATEGORY_GENERAL = 'General'
    CATEGORY_ARRAY = 'Array'
    CATEGORY_STRING = 'String'
    CATEGORY_DP = 'Dynamic Programing'
    CATEGORY_GREEDY = 'Greedy'
    CATEGORY_SORT = 'Sort'
    CATEGORY_MATH = 'Math'
    CATEGORY_STACK = 'Stack'
    CATEGORY_HEAP = 'Heap'
    CATEGORY_CHOICES = [(CATEGORY_GENERAL, 'General'),
                        (CATEGORY_ARRAY, 'Array'),
                        (CATEGORY_STRING, 'String'),
                        (CATEGORY_DP, 'Dynamic Programing'),
                        (CATEGORY_GREEDY, 'Greedy'),
                        (CATEGORY_SORT, 'Sort'),
                        (CATEGORY_MATH, 'Math'),
                        (CATEGORY_STACK, 'Stack'),
                        (CATEGORY_HEAP, 'Heap')]

    name = models.CharField(max_length=50, default="newproblem")
    description = models.TextField(max_length=420, default="", blank=True)
    example = models.TextField(max_length=420, default="", blank=True)
    difficulty = models.CharField(choices=DIFFICULTY_CHOICES, default=DIFFICULTY_EASY, max_length=30)
    category = models.CharField(choices=CATEGORY_CHOICES, default=CATEGORY_GENERAL, max_length=30)

    java_default = models.TextField(max_length=420, default="", blank=True)
    python_default = models.TextField(max_length=420, default="", blank=True)
    tle_limit = models.PositiveIntegerField(default=1)
    mle_limit = models.PositiveIntegerField(default=500)
    java_tests = models.TextField(max_length=1000, default="", blank=True)
    python_tests = models.TextField(max_length=1000, default="", blank=True)
    visible = models.BooleanField(default=False)
    success_rate = models.CharField(max_length=10, default="0.00%")

    def __unicode__(self):
        return self.name


class Discussion(models.Model):
    """
    the model for the discussion for each problem
    """
    title = models.CharField(max_length=50)
    text = models.CharField(max_length=1000)
    user = models.ForeignKey(User)
    problem = models.ForeignKey(Problem)
    created_at = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.text


class Post(models.Model):
    """
    the model for the post for each problem
    """
    text = models.CharField(max_length=42)
    user = models.ForeignKey(User)
    created_at = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.text


class Comment(models.Model):
    """
    the model for the comment for each discussion
    """
    text = models.CharField(max_length=100)
    user = models.ForeignKey(User)
    discussion = models.ForeignKey(Discussion)
    created_at = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.text


class SubmitHistory(models.Model):
    """
    the model for the submission history for each problem
    """
    text = models.CharField(max_length=10000)
    user = models.ForeignKey(User)
    problem = models.ForeignKey(Problem)
    created_at = models.DateTimeField(auto_now_add=True)
    result = models.CharField(max_length=42)
    runtime = models.PositiveIntegerField(null=True)

    def __unicode__(self):
        return self.text

