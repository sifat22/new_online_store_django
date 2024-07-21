from django.shortcuts import render,redirect, get_object_or_404
from .forms import UserRegistrationForm,UserProfileForm,UserForm
from .models import Account, UserProfile
from django.contrib import messages,auth
from django.contrib.auth.decorators import login_required

# Create your views here.

def user_register(request):
    if request.method=='POST':
        form=UserRegistrationForm(request.POST)
        if form.is_valid():
            first_name=form.cleaned_data.get('first_name')
            last_name=form.cleaned_data.get('last_name')
            phone_number=form.cleaned_data.get('phone_number')
            email=form.cleaned_data.get('email')
            password=form.cleaned_data.get('password')
            username=email.split("@")[0]

            user = Account.objects.create_user(first_name=first_name, last_name=last_name, email=email, username=username, password=password)
            user.phone_number=phone_number
            user.save()
            messages.success(request,"Registration Successfull")
            return redirect("register")
    else:
        form = UserRegistrationForm
    return render(request,"app_account/register.html",{
        'form' : form,
    })


def user_login(request):
    if request.method=='POST':
        email=request.POST['email']
        password=request.POST['password']

        user=auth.authenticate(email=email,password=password)
        if user is not None:
            auth.login(request, user)
            #messages.success(request,"Login Successfull")
            return redirect("home")
        else:
            messages.error(request, "Invalid login credentials")
            return redirect("login")
    return render(request,"app_account/login.html")




#user logout
@login_required(login_url = 'login')
def user_logout(request):
    auth.logout(request)
    messages.success(request,"You are Logged Out")
    return redirect("login")



#dashboard
@login_required
def dashboard(request):
    user_profile=UserProfile.objects.get(user=request.user)
    return render (request,'app_account/dashboard.html',{
        "userprofile" : user_profile
    })


#edit profile

@login_required(login_url= 'login')
def edit_profile(request):
    userprofile = get_object_or_404(UserProfile, user = request.user)
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance = request.user)
        profile_form = UserProfileForm(request.POST, request.FILES, instance = userprofile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, "User Profile Updated Successfully")
            return redirect ('edit_profile')
    else:
        user_form = UserForm(instance = request.user)
        profile_form = UserProfileForm(instance = userprofile)

    return render(request,"app_account/edit_profile.html",{
        'user_form':user_form,
        'profile_form':profile_form,
        'userprofile':userprofile,
    })
    #return render(request,"app_account/edit_profile.html")
