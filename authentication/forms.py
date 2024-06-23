from django import forms
from app.models import CustomUser


class LoginForm(forms.Form):
    phone_number = forms.IntegerField()
    password = forms.CharField(max_length=100)

    def clean_phone_number(self):
        phone_number = self.data.get('phone_number')
        if not CustomUser.objects.filter(phone_number=phone_number):
            raise forms.ValidationError("Email doesn't exist")
        return phone_number

    def clean_password(self):
        phone_number = self.clean_phone_number()
        password = self.data.get('password')

        try:
            user = CustomUser.objects.get(phone_number=phone_number)
            if not user.check_password(password):
                raise forms.ValidationError(" Email or Password doesn't match")
        except CustomUser.DoesNotExist:
            raise forms.ValidationError("Email or Password doesn't match")
        return password
