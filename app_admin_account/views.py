from django.shortcuts import render,redirect, get_object_or_404
from .forms import UserRegistrationForm,UserProfileForm,UserForm,CreateProfileForm
from .models import Account, UserProfile
from django.contrib import messages,auth
from django.contrib.auth.decorators import login_required
from app_order.models import Order,OrderProduct,Payment
from app_cart.models import CartItem

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
            return redirect("login")
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
            return redirect("dashboard")
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
    #get order
    # orders=Order.objects.order_by('created_at').filter(user=request.user,is_ordered=True)
    # order_count=orders.count()
    user = request.user
    
    in_profile = UserProfile.objects.filter(user= user).exists()
    if in_profile:
        userprofile = UserProfile.objects.get(user= user)
        return render(request,"app_account/dashboard.html",{
            'in_profile' : in_profile,
            'userprofile' : userprofile
        })
    else:
        return render(request,"app_account/dashboard.html")
        
    


#my profile
@login_required(login_url= 'login')
def create_profile(request,user_id):
    user = get_object_or_404(Account, id = user_id)
    if request.method=='POST':
        form = CreateProfileForm(request.POST, request.FILES)
        if form.is_valid():
            print('valid')
            data= UserProfile()
            data.user = user
            data.address_line_1 = form.cleaned_data['address_line_1']
            data.address_line_2 = form.cleaned_data['address_line_2']
            data.profile_picture = form.cleaned_data['profile_picture']
            data.city = form.cleaned_data['city']
            data.state = form.cleaned_data['state']
            data.country = form.cleaned_data['country']
            data.save()
            messages.success(request,"User Profile Created Successfully")
            return redirect("dashboard")
    else:
        
        return render(request,"app_account/my_profile.html")
            
    






#Edit Profile
@login_required(login_url= 'login')
def edit_profile(request, user_id):
    userprofile = get_object_or_404(UserProfile, user__id = user_id)
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance = request.user)
        profile_form = UserProfileForm(request.POST, request.FILES, instance = userprofile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, "User Profile Updated Successfully")
            return redirect ('dashboard')
    else:
        user_form = UserForm(instance = request.user)
        profile_form = UserProfileForm(instance = userprofile)

    return render(request,"app_account/edit_profile.html",{
        'user_form':user_form,
        'profile_form':profile_form,
        'userprofile':userprofile,
    })

#change password
@login_required(login_url= 'login')
def change_password(request):
    if request.method == 'POST':
        current_password= request.POST['current_password']
        new_password=request.POST['new_password']
        confirm_password=request.POST['confirm_password'] 

        user = Account.objects.get(username__exact= request.user.username)

        if new_password== confirm_password:
            sucess = user.check_password(current_password)
            if sucess:
                user.set_password(new_password)
                user.save()
                #auth.logout-----for this line after resetting the password it will be logout
                messages.success(request,"Password Updated Succesfully!")
                return redirect('change_password')
            else:
                messages.error(request,'Invalid Current passwordQ')
                return redirect('change_password')
        else:
            messages.error(request,'Password doesnot match!')
            return redirect('change_password')

    return render(request,'app_account/change_pass.html')


#my order
@login_required(login_url='login')
def my_order(request):
    orders=Order.objects.filter(user=request.user,is_ordered=True).order_by('-created_at')
    return render(request,'app_account/my_order.html',{
        'order':orders,
    })

def view_order(request, order_id):
    order_detail=OrderProduct.objects.filter(order__order_number=order_id)
    order=Order.objects.get(order_number=order_id)
    payment_status = order.cash_payment.status
    
    subtotal=0
    grand_total = 0
    for i in order_detail:
        subtotal+=(i.product_price * i.quantity)
    grand_total = order.tax + subtotal
    return render(request,'app_account/view_order.html',{
        'order_detail':order_detail,
        'order':order,
        'subtotal':subtotal,
        "grand_total":grand_total,
        'payment' : payment_status,
    })

def delete_order(request, order_id):
    order=Order.objects.get(order_number=order_id)
    order.delete()
    return redirect("my_order")




