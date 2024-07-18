from django import forms
from app.models import CustomUser
from django_recaptcha.fields import ReCaptchaField

from django_recaptcha.fields import ReCaptchaField
class LoginForm(forms.Form):
    email = forms.IntegerField()
    password = forms.CharField(max_length=100)

    def clean_email(self):
        email = self.data.get('email')
        if not CustomUser.objects.filter(email=email):
            raise forms.ValidationError("Email doesn't exist")
        return email

    def clean_password(self):
        password = self.data.get('password')
        email = self.clean_email()
        try:
            user = CustomUser.objects.get(email=email)
            if not user.check_password(password):
                raise forms.ValidationError("Email or Password doesn't match")
        except CustomUser.DoesNotExist:
            raise forms.ValidationError("Email or Password doesn't match")
        return password


class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, max_length=100)
    confirm_password = forms.CharField(widget=forms.PasswordInput, max_length=100)
    recaptcha = ReCaptchaField()


    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError("Email already exists")
        return email

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Passwords don't match")

        return cleaned_data


class EmailForm(forms.Form):
    subject = forms.CharField(max_length=100)
    message = forms.CharField(widget=forms.Textarea)
    email_from = forms.EmailField()
    email_to = forms.EmailField()


