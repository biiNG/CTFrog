from django import forms


class RegisterForm(forms.Form):
    team_name = forms.CharField(label='团队名', max_length=10, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': "Username", 'autofocus': "required"}))
    team_mail = forms.EmailField(label='邮箱地址', widget=forms.EmailInput(
        attrs={'class': 'form-control','placeholder':"Email Address"}))

