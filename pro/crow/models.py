from django.db import models
from django.contrib.auth.models import User
from stdimage import StdImageField


class item(models.Model):
    id = models.AutoField(primary_key=True)
    text =models.CharField(max_length=140)
    user =models.ForeignKey(User)
    url=models.CharField(max_length=100)
    image = models.ImageField(upload_to="images/",blank=True)
    date=models.DateTimeField("date published",auto_now_add=True)
    isImage=models.NullBooleanField()
    isVideo=models.NullBooleanField()
    isText=models.NullBooleanField()
    def __unicode__(self):
        return self.text

class tag(models.Model):
    tagname = models.CharField(max_length=50)
    users=models.ManyToManyField(User,blank=True)
    items=models.ManyToManyField(item,blank=True)
    def __unicode__(self):
        return self.tag
     
class profile(models.Model):
    user=models.OneToOneField(User)
    profilepic=models.FileField(upload_to="dp/" ,blank=True)
    description=models.CharField(max_length=140)
    followers=models.ManyToManyField(User,blank=True,related_name="followers+")
    following=models.ManyToManyField(User,blank=True,related_name="following+")
    #medium=models.FileField(upload_to="dp/" ,blank=True)
    small=models.FileField(upload_to="dp/" ,blank=True)
    #tbd 
    def __unicode__(self):
        return self.description

   
    def get_absolute_url(self):
        return ('sites_profile_detail', (), { 'username': self.user.username })
    get_absolute_url = models.permalink(get_absolute_url)

