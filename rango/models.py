from __future__ import unicode_literals

from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length = 120, unique = True)
    views = models.IntegerField(default = 0)
    likes = models.IntegerField(default = 0)
    slug = models.SlugField()

    def save(self,*args,**kwargs):

        '''
        Uncomment if you don't want the slug to change everytime the name changes
        if self.id is None:
            self.slug = slugify(self.name)
        '''
        if self.views < 0:
            self.views = 0
        self.slug = slugify(self.name)
        super(Category, self).save(*args,**kwargs)

    def __unicode__(self):
        return self.name

class Page(models.Model):
    category = models.ForeignKey(Category)
    title = models.CharField(max_length = 120)
    url = models.URLField()
    views = models.IntegerField(default = 0)

    def __unicode__(self):
        return self.title

class UserProfile(models.Model):
    user = models.OneToOneField(User)
    website = models.URLField(blank = True)
    picture = models.ImageField(upload_to = 'profile_images',blank = True)
    has_profile = models.BooleanField(default = False)

    def __unicode__(self):
        return self.user.username
