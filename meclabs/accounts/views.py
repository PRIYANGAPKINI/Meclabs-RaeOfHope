from django.shortcuts import render
from django.shortcuts import render, redirect
from accounts.forms import RegistrationForm, RegistrationForm2, EditprofileForm

from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required

from django.views.generic import TemplateView
from accounts.models import User, UserProfile
from accounts.database import *

@login_required
def home(request):

    return render(request, 'accounts/home.html')

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            if User.objects.filter(email=form.cleaned_data.get('email')).exists():
                args = {'error': 'User already exists', 'erlink': '/account/register'}
                return render(request, 'accounts/regerror.html', args)
            else:
                form.save()
                return redirect('/account')
        else:
            args = {'error': 'Password not strong', 'erlink': '/account/register'}
            return render(request, 'accounts/regerror.html', args)

    else:
        form = RegistrationForm()
        args = {'form': form}
        return render(request, 'accounts/reg_form.html', args)

class RegView(TemplateView):
    template_name = 'accounts/reg_form_2.html'

    def get(self, request):
        form = RegistrationForm2()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = RegistrationForm2(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()

            FirstName = form.cleaned_data['FirstName']
            LastName = form.cleaned_data['LastName']
            PhoneNumber = form.cleaned_data['PhoneNumber']
            Email = form.cleaned_data['Email']
            form = RegistrationForm2()
            #return redirect('/account/profile/')
            args = {'form': form, 'FirstName': FirstName, 'LastName': LastName, 'PhoneNumber': PhoneNumber, 'Email ': Email }
            return render(request, self.template_name, args)

O = RegView()

@login_required
def profile(request):
    form = RegistrationForm(request.POST)
    if request.user.is_authenticated:
        if UserProfile.objects.filter(user=request.user).exists():
            details = UserProfile.objects.get(user=request.user)
            args = {'data': details}
            return render(request, 'accounts/profile.html', args)
        else:
            if request.method == 'POST':
                return O.post(request)
            else:
                return O.get(request)
            # return render(request, 'accounts/reg_form_2.html', {'form': form})
    else:
         pass

@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = EditprofileForm(request.POST, instance=request.user)

        if form.is_valid():
            form.save()
            return redirect('/account/profile')

    else:
        form = EditprofileForm(instance=request.user)
        args = {'form': form}
        return render(request, 'accounts/edit_profile.html', args)

@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(data=request.POST, user=request.user)

        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return redirect('/account/profile')
        else:
            return redirect('/account/change-password')

    else:
        form = PasswordChangeForm(user=request.user)
        args = {'form': form}
        return render(request, 'accounts/change_password.html', args)
