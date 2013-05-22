from django.db import models
from django import forms
from django.forms import ModelForm
from crow.models import item,profile,tag
from PIL import Image
#from crow.models.profile import description
from django.utils.translation import ugettext_lazy as _
attrs_dict = {'class': 'required'}

"""
#theUser=User.objects.get(username=username)
userProfile=profile.objects.get(user=theUser)
description=userProfile.description
"""
class ProfileForm(ModelForm):
    profilepic = forms.FileField(label=_("Select a pic"),widget=forms.FileInput())
    description = forms.CharField(label=_("New Description"),widget=forms.TextInput(attrs=dict(attrs_dict,maxlength=75)))
    #description = forms.CharField(initial = description)
    #description = forms.CharField(label=_("New Description"),widget=forms.TextInput(attrs={'size':75, 'id':'abc'}))
    class Meta:
        model = profile
        fields = ['profilepic', 'description']

    """    
    def __init__(self, *args, **kwargs):
        #self.user = user
        
        super(ProfileForm, self).__init__( *args, **kwargs)
        description=kwargs.pop("des")
    """   
    
    
    def clean_description(self):
        description = self.cleaned_data['description']
        return description
    def clean_profilepic(self):
        profilepic = self.cleaned_data['profilepic']
        return profilepic
    
  


    """
     
    def save(self):
        u=self.instance.user
        u.save()
        self.user.profile.description(self.cleaned_data['new_description'])
        self.user.profile.save()
        return self.user
    """


class uploadImageForm(forms.Form):
    text=forms.CharField(max_length=140)
    url=forms.CharField(max_length=100)

