from django import forms

class LoginForm(forms.Form):
    username = forms.CharField(min_length=4,
                               widget=forms.TextInput(
                                   attrs={"placeholder": "아이디 (4자리 이상)"}
                               ))
    password = forms.CharField(min_length=4,
                               widget=forms.TextInput(
                                   attrs={"placeholder": "비밀번호 (4자리 이상)"}
                               ))

class SignupForm(forms.Form):
    nickname = forms.CharField()
    username = forms.CharField()
    password1 = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)
    profile_image = forms.ImageField(required= False)
    short_description = forms.CharField()
