from django import forms
from app.models import CustomUser


class LoginForm(forms.Form):
    phone_number = forms.IntegerField()
    password = forms.CharField(max_length=100)

    def clean_phone_number(self):
        phone_number = self.data.get('phone_number')
        if not CustomUser.objects.filter(phone_number=phone_number):
            raise forms.ValidationError("Phone number doesn't exist")
        return phone_number

    def clean_password(self):
        password = self.data.get('password')
        phone_number = self.clean_phone_number()
        try:
            user = CustomUser.objects.get(phone_number=phone_number)
            if not user.check_password(password):
                raise forms.ValidationError("Phone number or Password doesn't match")
        except CustomUser.DoesNotExist:
            raise forms.ValidationError("Phone number or Password doesn't match")
        return password


class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, max_length=100)
    confirm_password = forms.CharField(widget=forms.PasswordInput, max_length=100)

    class Meta:
        model = CustomUser
        fields = ('username', 'phone_number', 'password')

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        if CustomUser.objects.filter(phone_number=phone_number).exists():
            raise forms.ValidationError("Phone number already exists")
        return phone_number

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




