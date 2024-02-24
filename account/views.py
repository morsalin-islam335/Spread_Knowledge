from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.views import LoginView

from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm

from book.models import Borrow, Account

# Create your views here.

from django.views.generic import View
from .forms import Registration
from django.contrib.auth.models import User 


# email send process

from django.core.mail import EmailMessage, EmailMultiAlternatives
from django.template.loader import render_to_string


# verification mail korar jonno

from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes

def registration(request):
    if request.user.is_authenticated:
        return redirect("profile") # a log in user can't register with out logout
    if request.method == 'POST':
        form = Registration(request.POST, request.FILES)
        if form.is_valid():
            # form.save()

            #  set user
            username = form.cleaned_data.get("username")
            first_name = form.cleaned_data.get("first_name")
            last_name = form.cleaned_data.get("last_name")
            email = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password")
            profile_pic = form.cleaned_data.get("profile_pic")

            user = User.objects.create(username = username, first_name = first_name, last_name = last_name, email = email)


           

            user.set_password(password)
            user.is_active = False
            user.save()
            user = User.objects.get(username = username)
           
            account = Account(user=user, profile_pic=profile_pic, balance=0) # initial balance of user will be  0

            account.save()





            token = default_token_generator.make_token(user) # user er jonno token generate korba
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            conform_link = f"https://spread-knowledge/account/activate/{uid}/{token}.onerender.com"
            # conform_link = f"http://127.0.0.1:8000/account/activate/{uid}/{token}"



            mail_subject = "Account Verification Mail"
            message = render_to_string("verificationMail.html", {"conform_link": conform_link})

            to_email = email

            send_message = EmailMultiAlternatives(mail_subject, "", to = [to_email])

            send_message.attach_alternative(message, 'text/html')

            send_message.send()
            

            messages.success(request, "Registration Complete. Please Check your email for conformation email")
          
           
            return redirect("homepage")
        

    else:
        form = Registration(request.POST, request.FILES)
    return render(request, 'register.html', {"form": form})
    
    

class LoginView(LoginView):
    template_name = 'login.html'
    # form class nia kaj korar ei lagba na
    def get_success_url(self):
        return reverse_lazy('profile')
    def form_valid(self, form):
        messages.success(self.request, 'Login Successful')
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self. request, "Login Information incorrect")
        return super().form_invalid(form)
    
    def get_context_data(self, **kwargs):
        context  = super().get_context_data(**kwargs)
        context['form'] = AuthenticationForm()
        return context

def UserLogout(request):
    if not request.user.is_authenticated:
        return redirect("login")
    logout(request)
    messages.success(request, 'logout successfully')
    return redirect("homepage")






def profile(request):
    if request.user.is_authenticated:
        items = Borrow.objects.filter(account = request.user.account)
        total = len(items)
        return render(request, 'profile.html', {"items": items, "total": total})
    else:
        return redirect("login")
        

    
 
def activate(request, uid64, token):
    try:
        uid = urlsafe_base64_decode(uid64).decode()
        user = User._default_manager.get(pk = uid)
    except:
        user = None
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True 
        user.save()
        return redirect("login")
    else:
        messages.error(request, "Something is wrong.")
        return redirect("register")