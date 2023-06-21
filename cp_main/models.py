import uuid
from django.db import models
from django.contrib.auth.models import User
from tinymce.models import HTMLField
from django.dispatch import receiver
from django.db.models.signals import post_save
# Create your models here.

ROLE_CHOICES=[
    ("Lead","Lead"),
    ("Member","Member"),
    ("Co-lead","Co-lead"),
]


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=100,choices=ROLE_CHOICES, blank=True, null=True)
    Bio = HTMLField()
    registration_no = models.CharField(max_length=10,blank=True)
    codeforces_username = models.CharField(max_length=100,blank=True)
    leetcode_username = models.CharField(max_length=100,blank=True)
    codechef_username = models.CharField(max_length=100,blank=True)
    admitted_year = models.CharField(max_length = 500,blank=True)
    slug = models.SlugField(blank=True)
    def __str__(self):
        return self.user.username
    def save(self,*args,**kwargs):
        if not self.slug:
            self.slug = uuid.uuid4()
        super(Profile, self).save(*args,**kwargs)
@receiver(post_save,sender = User)
def create_profile(sender,instance,created,**kwargs):
    if created:
        Profile.objects.create(user = instance,role = "Member")
        instance.profile.save()