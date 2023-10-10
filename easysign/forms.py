from django import forms
from .models import User

class CustomUserChangeForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(CustomUserChangeForm, self).__init__(*args, **kwargs)
        
        for field_name, field in self.fields.items():
            field.help_text = ''

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'username', 'user_api_key',)

        widgets = {
            'user_api_key': forms.TextInput(attrs={'type': 'password'}),
        }
        