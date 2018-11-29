from django.db import models
from django.db.models import Max
from django.utils.html import escape
from django.contrib.auth.models import User
# Create your models here.



class User_profile(models.Model):
    # user = models.ForeignKey(User, on_delete=models.CASCADE)
    username = models.CharField(max_length=50, null=True)
    first_name = models.CharField(max_length=50,null=True)
    last_name = models.CharField(max_length=50, null=True)
    email = models.CharField(max_length=50, null=True)
    password = models.CharField(max_length=50, null=True)
    age = models.IntegerField(default=0, blank=True, null=True)
    self_intro = models.CharField(max_length=420, default="This person is lazy, (s)he didn't leave anything", blank=True)
    location = models.CharField(max_length=50, default="NA", blank=True)
    job = models.CharField(max_length=50, default="NA", blank=True)
    # img_url = models.CharField(max_length=50, default="../static/photo_id/default.png", blank=True)
    picture = models.ImageField(upload_to='profile_photos', blank=True, default="photo_id/default.png")
    friends = models.ManyToManyField("self", symmetrical=False, blank=True)
    confirm = models.BooleanField(default=False)
    token_reg = models.CharField(max_length=100, default='', blank=True)
    token_reset = models.CharField(max_length=100, default='', blank=True)

    def __str__(self):
        return self.first_name + " " + self.last_name + self.email





class Message(models.Model):
    # user = models.ForeignKey(User, on_delete=models.CASCADE)
    user_profile = models.ForeignKey(User_profile, on_delete=models.CASCADE)
    content = models.CharField(max_length=42)
    # last = models.DateTimeField(auto_now=True)
    last_changed = models.DateTimeField(auto_now=True)
    deleted = models.BooleanField(default=False)

    # Returns all recent additions and deletions to the to-do list.
    @staticmethod
    def get_changes(time="1970-01-01T00:00+00:00"):
        return Message.objects.filter(last_changed__gt=time).distinct()

    # Returns all recent additions to the to-do list.
    @staticmethod
    def get_messages(time="1970-01-01T00:00+00:00"):
        return Message.objects.filter(deleted=False,
                                   last_changed__gt=time).distinct()

    # Generates the HTML-representation of a single to-do list item.
    # @property

    @staticmethod
    def get_max_time():
        return Message.objects.all().aggregate(Max('last_changed'))['last_changed__max'] or "1970-01-01T00:00+00:00"
    # def __str__(self):
    #     return self.content

class Comment(models.Model):
    user_profile = models.ForeignKey(User_profile, on_delete=models.CASCADE)
    message = models.ForeignKey(Message, on_delete=models.CASCADE)
    content = models.CharField(max_length = 1000)
    time = models.DateTimeField(auto_now=True)
