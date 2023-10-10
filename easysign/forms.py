from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

class CustomUserChangeForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(CustomUserChangeForm, self).__init__(*args, **kwargs)
        
        for field_name, field in self.fields.items():
            field.help_text = ''

    class Meta:
        model = get_user_model()
        fields = ('first_name', 'last_name', 'email', 'username', 'user_api_key',)

        widgets = {
            'user_api_key': forms.TextInput(attrs={'type': 'password'}),
        }

class CustomUserCreateForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ('username', 'first_name', 'last_name', 'password')