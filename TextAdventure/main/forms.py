from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm

# form to to process login data in views.py
class LoginForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ['username', 'password']

# form to process register data in views.py
class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password', 'email', 'first_name']
        widgets = {
            'password': forms.PasswordInput(),
        }


# form to prcocess ui customization changes and save
class TerminalSettingsForm(forms.Form):
    background_color = forms.CharField(widget=forms.TextInput(attrs={'type': 'color'}))
    font_color = forms.CharField(widget=forms.TextInput(attrs={'type': 'color'})) 
    zoom_level = forms.CharField(required=False)  
    bold = forms.BooleanField(required=False)
    text_speed = forms.IntegerField(min_value=1, max_value=100, required=False)   
    italics = forms.BooleanField(required=False)
    underline = forms.BooleanField(required=False)
    line_spacing = forms.FloatField(min_value=1.0, max_value=2.0, required=False)
