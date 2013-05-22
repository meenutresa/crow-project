from django import forms

class uploadImageForm(forms.Form):
    text=forms.CharField(max_length=140)
    url=forms.CharField(max_length=100)
    
    
