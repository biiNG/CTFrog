from django import forms


class UserForm(forms.Form):
    username = forms.CharField(label="用户名", max_length=128, widget=forms.TextInput(attrs={'class': 'form-control',
                                                                                          'placeholder': "Username",
                                                                                          'autofocus': "required"}))

    password = forms.CharField(
        label="密码", max_length=256, widget=forms.PasswordInput(attrs={'class': 'form-control',
                                                                      'placeholder': "Password"}))


class RegisterForm(forms.Form):
    gender = (
        ('male', "男"),
        ('female', "女"),
    )
    username = forms.CharField(label="用户名", max_length=128, widget=forms.TextInput(
        attrs={'class': 'form-control'}))
    password1 = forms.CharField(label="密码", max_length=256, widget=forms.PasswordInput(
        attrs={'class': 'form-control'}))
    password2 = forms.CharField(label="确认密码", max_length=256, widget=forms.PasswordInput(
        attrs={'class': 'form-control'}))
    email = forms.EmailField(label="邮箱地址", widget=forms.EmailInput(
        attrs={'class': 'form-control'}))
    sex = forms.ChoiceField(label='性别', choices=gender)
    # captcha = CaptchaField(label='验证码')
    studentid = forms.IntegerField(label="学号", max_value=2018999999, min_value=2018000000, widget=forms.TextInput(
        attrs={'class': 'form-control'}))
    realname = forms.CharField(label="真实姓名", max_length=10, widget=forms.TextInput(
        attrs={'class': 'form-control'}))


class UpdateProfileForm(forms.Form):
    student_id = forms.CharField(
        label="学生号", max_length=20, widget=forms.NumberInput(), required=False)


class ChangePasswordForm(forms.Form):
    password1 = forms.CharField(label='新密码', max_length=20, widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': "Password"}))
    password2 = forms.CharField(label='确认密码', max_length=20, widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': "Confirm your password"}))
