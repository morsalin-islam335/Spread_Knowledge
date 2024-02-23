''''from django import forms
from django.contrib.auth.models import User

from account.models import Account

class Registration(forms.ModelForm):
    # username = forms.CharField(max_length = 70)
    # first_name = forms.CharField(max_length = 80)
    # last_name = forms.CharField(max_length = 60)
    # email = forms.EmailField()

    # password = forms.CharField(max_length= 20, widget= forms.PasswordInput())
    # password2 = forms.CharField(max_length=20, widget = forms.PasswordInput(), label = 'conform password')


    profile_pic = forms.ImageField()

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password']
    # def clean_password2(self):
    #     password = self.cleaned_data.get('password')
    #     conform_password = self.cleaned_data.get('password2')

    #     if password != conform_password:
    #         raise forms.ValidationError("password and conform password didn't match")
        
    
    def save(self, commit = True):
        # user = super().save(commit = False)
        # if user.username in User.objects.all():
        #     raise forms.ValidationError("This username is already exist")
        # elif(forms.cleaned_data.get("password1") != forms.cleaned_data.get("password2")):
        #     raise forms.ValidationError("Password and conform password are not same")
        
        # elif(len(forms.cleaned_data.get("password1"))<7 ):
        #     raise forms.ValidationError("Password is too common")
        
        # # it is not possible to have more than 1 user as same name

        # elif(forms.cleaned_data.get("email") in User.objects.filter(email = forms.cleaned_data.get("email"))):
        #     raise forms.ValidationError("This email is already in used")
        

        # else:
        #     user.save() # save user model
        #     profile_pic = forms.cleaned_data.get('profile_pic')
        #     account = Account(user = user, profile_pic = profile_pic, balance = 0) # after creating an account an user initial balance will be 0
        #     account.save()
        #     return user
        
        user =super().save() # save user model
        profile_pic = self.cleaned_data.get('profile_pic')
        account = Account(user = user, profile_pic = profile_pic, balance = 0) # after creating an account an user initial balance will be 0
        account.save()
        return user

'''




from django import forms
from django.contrib.auth.models import User

from account.models import Account

class Registration(forms.ModelForm):
    password = forms.CharField(max_length=20, widget=forms.PasswordInput())
    conform_password = forms.CharField(max_length = 20, widget = forms.PasswordInput(), label = 'Confirm password')
    
    profile_pic = forms.ImageField()

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password']

    def clean_password2(self):
        password = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('password2')

        if password != password2:
            raise forms.ValidationError("Password and conform password didn't match") # 2 ta password match na korla exception throw korbo
        
    
    def clean(self):
        data = super().clean()
        password = data.get("password")
        password2 = data.get("password2")

        if password and len(password) <8:
            raise forms.ValidationError("Minimum 8 digits is required")
        
       

    # def save(self, commit = True):
    #     user = super().save(commit = False)
    #     user.set_password(self.cleaned_data["password"]) # user er password set korlam.
        
    #     if commit:
    #         user.save()
    #         profile_pic = self.cleaned_data.get('profile_pic')
    #         account = Account(user=user, profile_pic=profile_pic, balance=0)
    #         account.save()
        
    #     return user

