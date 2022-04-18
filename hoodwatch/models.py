from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.
class NeighbourHood(models.Model):
    name = models.CharField(max_length=50)
    location = models.CharField(max_length=60)
    occupants_count =  models.IntegerField(null=True, blank=True)
    picture = models.ImageField(upload_to='images/', default='default.png')
    description = models.TextField()
    contact = models.CharField(max_length = 10,blank =True)
    health_department = models.CharField(max_length = 10,blank =True)
    police_authorities = models.CharField(max_length = 10,blank =True)
    def __str__(self):
            return f'{self.name} hood'

    def create_neighborhood(self):
        self.save()

    def delete_neighborhood(self):
        self.delete()

    @classmethod
    def find_neighbourhood(cls,name):
        neighbour = cls.objects.filter(title__icontains=name)
        return neighbour


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    name = models.CharField(max_length=80, blank=True)
    bio = models.TextField(max_length=254, blank=True)
    email = models.EmailField()
    profile_picture = models.ImageField(upload_to='images/', default='default.png')
    neighbourhood = models.ForeignKey(NeighbourHood, on_delete=models.SET_NULL, null=True, related_name='members', blank=True)
    location = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return f'{self.user.username} profile'

    @receiver(post_save, sender=User)
    def save_user(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

class Business(models.Model):
    name = models.CharField(max_length=120)
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='person')
    description = models.TextField(blank=True)
    neighbourhood = models.ForeignKey(NeighbourHood, on_delete=models.CASCADE, related_name='business')
    email = models.EmailField(max_length=254)

    def __str__(self):
        return f'{self.name} Business'

    def create_business(self):
        self.save()

    def delete_business(self):
        self.delete()

    @classmethod
    def search_by_name(cls,search_term):
        biz = cls.objects.filter(title__icontains=search_term)
        return biz


class Post(models.Model):
    title = models.CharField(max_length=120, null=True)
    post = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='post_owner')
    hood = models.ForeignKey(NeighbourHood, on_delete=models.CASCADE, related_name='hood_post')
