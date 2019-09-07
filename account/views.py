from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate,login
from .forms import LoginForm, RegidtrationFrom,UserprofileForm,UserForm,UserInfoForm
from django.contrib.auth.decorators import login_required
from .models import UserProfile,UserInfo
from django.contrib.auth.models import User
from django.urls import reverse
from django.contrib import messages

def user_login(request):
    if request.method == "POST":
        login_form=LoginForm(request.POST)
        if login_form.is_valid():
            cd = login_form.cleaned_data
            user = authenticate(username = cd['username'],password=cd['password'])
            if user:
                login(request,user)
                messages.info(request,'Wellcome you ,you have been authenticated successfully')  
                return#return HttpResponse("Wellcome you ,you have been authenticated successfully")
                #return HttpResponseRedirect(reverse("home:"))
            else:
                messages.error(request,'对不起，用户或者密码输入错误')
                return HttpResponseRedirect(reverse("account:user_login"))
                #return HttpResponse("Sorry, your username or password is not right.")
        else:
            messages.error(request,'对不起，用户或者密码格式输入错误')
            return HttpResponseRedirect(reverse("account:user_login"))
            #return HttpResponse("Invalid login")
    
    if request.method == "GET":
        login_form=LoginForm()
        return render(request, "account/login2.html",{"form":login_form})


def register(request):
    if request.method == "POST":
        user_form=RegidtrationFrom(request.POST)
        userprofile_form = UserprofileForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password2'])
            new_user.save()
            new_profile = userprofile_form.save(commit = False)
            new_profile.user = new_user
            new_profile.save()
            UserInfo.objects.create(user=new_user)
            messages.info(request,'register successfull, please login!')
            return HttpResponseRedirect(reverse("account:user_login"))
        else:
            messages.error(request,'注册失败，请检查输入格式是否有误，Birth Date的格式为1995-10-4')
            return HttpResponseRedirect(reverse("account:user_register"))
    if request.method == "GET" :
        user_form = RegidtrationFrom()
        userprofile_form = UserprofileForm()
        return render(request,"account/register.html",{"form": user_form,"profile":userprofile_form})


@login_required(login_url='/account/login/')
def myself(request):
    userprofile = UserProfile.objects.get(user=request.user) if hasattr(request.user, 'userprofile') else UserProfile.objects.create(user=request.user)
    userinfo = UserInfo.objects.get(user=request.user) if hasattr(request.user, 'userinfo') else UserInfo.objects.create(user=request.user)
    #print('myself function')
    return render(request, "account/myselfinfo.html", {"user":request.user, "userinfo":userinfo, "userprofile":userprofile})

@login_required(login_url='/account/login/')
def myself_edit(request):
    userprofile = UserProfile.objects.get(user=request.user) if hasattr(request.user, 'userprofile') else UserProfile.objects.create(user=request.user)
    userinfo = UserInfo.objects.get(user=request.user) if hasattr(request.user, 'userinfo') else UserInfo.objects.create(user=request.user)
    
    if request.method == "POST":
        user_form = UserForm(request.POST)
        userprofile_form = UserprofileForm(request.POST)
        userinfo_form = UserInfoForm(request.POST)
        #print('the userform is'+str(user_form.is_valid())+' the profile form is'+str(userprofile_form.is_valid())+'  '+str(userinfo_form.is_valid()))
        #print(userprofile_form)
        #print(user_form.is_valid() * userprofile_form.is_valid() * userinfo_form.is_valid())
        if user_form.is_valid() * userprofile_form.is_valid() * userinfo_form.is_valid():
            user_cd = user_form.cleaned_data
            userprofile_cd = userprofile_form.cleaned_data
            userinfo_cd = userinfo_form.cleaned_data
            #print(user_cd["email"])
            request.user.email = user_cd["email"]
            userprofile.birth = userprofile_cd["birth"]
            userprofile.phone = userprofile_cd['phone']
            userprofile.sex = userprofile_cd["sex"]
            userinfo.school = userinfo_cd['school']
            userinfo.company = userinfo_cd['company']
            userinfo.profession = userinfo_cd['profession']
            userinfo.address = userinfo_cd['address']
            userinfo.aboutme = userinfo_cd['aboutme']
            request.user.save()
            userprofile.save()
            userinfo.save()
            messages.success(request,'修改个人信息成功')
        return HttpResponseRedirect('/account/my-information/')
    
    if request.method == "GET":
        user_form = UserForm(instance=request.user)
        userprofile_form = UserprofileForm(initial={"birth":userprofile.birth, "phone":userprofile.phone,"sex":userprofile.sex})
        userinfo_form = UserInfoForm(initial={"school":userinfo.school,"company":userinfo.company,"profession":userinfo.profession,"address":userinfo.address,"aboutme":userinfo.aboutme})
        return render(request,"account/myself_edit.html",{"user_form":user_form,"userprofile_form":userprofile_form,"userinfo_form":userinfo_form})


@login_required(login_url='/account/login/')
def my_image(request):
    if request.method == "POST":
        img = request.POST['img']
        userinfo =UserInfo.objects.get(user=request.user.id)
        userinfo.photo = img
        userinfo.save()
        return HttpResponse("1")
    else:
        return render(request,'account/imagecrop.html/',)
# Create your views here.
