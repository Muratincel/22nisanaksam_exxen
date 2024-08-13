from django.shortcuts import render,redirect
from .forms import *
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash



# Create your views here.
def userRegister(request):
    form = UserForm()

    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():

            # email işlemleri
            email = form.cleaned_data['email']
            subject = "Başarılı Kayıt"
            message = "Aramıza hoşgeldiniz!!!"

            send_mail(
                subject,
                message,
                settings.EMAIL_HOST_USER,
                [email]
            )

            form.save()

            messages.success(request, "Kayıt başarılı!")
            return redirect('index')

    context = {
        'form':form
    }

    return render(request, "register.html", context)



def userLogin(request):

    if request.method == "POST":
        kullanici = request.POST['kullanici']
        sifre = request.POST['sifre']

        user = authenticate(request, username = kullanici, password = sifre)

        if user is not None:
            login(request, user)
            messages.success(request, "Giriş başarılı!")
            return redirect('index')
        else:
            messages.error(request, "Kulanıcı adı ya da şifre hatalı!")
            return redirect('userlogin')


    return render(request, "login.html")


def userLogout(request):
    logout(request)
    messages.success(request, "Oturum kapatıldı!")

    return redirect('index')


def passwordChange(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)

        if form.is_valid():
            form.save()
            update_session_auth_hash(request, request.user)
            messages.success(request, "sifreniz basariyla degistirildi!")
            return redirect("userlogin")
        
        else:
            messages.error(request, "bilgileriniz yanlis!")
    
    else:
        form = PasswordChangeForm(request.user)

    context = {
        'form':form
    }

    return render(request, "password_change.html", context)


def delete_account(request):
    if request.method == 'POST':
        form = ConfirmDeleteAccountForm(request.POST)
        
        if form.is_valid() and form.cleaned_data.get('confirm'):
            user = request.user
            user.delete()  # Delete the user account
            logout(request)  # Log the user out
            messages.success(request, "Your account has been deleted successfully.")
            return redirect('index')  # Redirect to the homepage or any other page after deletion
        else:
            messages.error(request, "Please confirm to delete your account.")
    
    else:
        form = ConfirmDeleteAccountForm()
    
    context = {
        'form': form
    }
    
    return render(request, 'delete_account.html', context)

# Burasi Furkan hocanin yazdigi fonksiyon, chatgpt ile farkina bakarsin, su an bu fonksiyon aktif, eger ustteki sil i aktif etmek istiyorsan _navbar.html de sil hrefine {% url 'delete_account' %} yaz

def accountDelete(request):
    user = request.user

    if request.method == "POST":
        if user.is_authenticated:
            user = request.user
            user.delete()
            logout(request)
            messages.success(request, "hesabiniz basariyla silindi. TEBRIKLER !!")
        else:
            messages.error(request, "hesabi silmek icin giris yapmalisin")
            return redirect('login')
    
    return render(request, "account_delete.html")