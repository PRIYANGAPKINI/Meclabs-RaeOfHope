from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from accounts.models import UserProfile

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User

        fields = ('username', 'email', 'password1', 'password2')

    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        user.username = self.cleaned_data['username']
        user.email = self.cleaned_data['email']
        user.password1 = self.cleaned_data['password1']
        user.password2 = self.cleaned_data['password2']

        if commit:
            user.save()

        return user

class RegistrationForm2(forms.ModelForm):
    FirstName = forms.CharField()
    LastName = forms.CharField()
    PhoneNumber = forms.CharField()
    Email = forms.CharField()
    class Meta:
        model = UserProfile
        fields = ('FirstName', 'LastName', 'PhoneNumber', 'Email')

class EditprofileForm(UserChangeForm):

    class Meta:
        model = UserProfile
        fields = ('FirstName', 'LastName', 'PhoneNumber', 'Email')

