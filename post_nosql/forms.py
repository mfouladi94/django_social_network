from django import forms

class PostForm(forms.Form):
    body = forms.CharField()
    is_private = forms.BooleanField(required=False , initial=False)
    
    
class AttachmentForm(forms.Form):
    file = forms.FileField(required=True) 
    