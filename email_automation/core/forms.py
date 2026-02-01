from django import forms

class EmailRunForm(forms.Form):
    email = forms.EmailField(
        label="Email Address",
        widget=forms.EmailInput(attrs={
            'placeholder': 'exam@gmail.com'
        })
    )

    app_password = forms.CharField(
        label="App Password",
        widget=forms.PasswordInput(attrs={
            'placeholder': 'App password'
        })
    )
