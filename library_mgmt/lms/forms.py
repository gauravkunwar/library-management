from django import forms
# from django.contrib.auth.models import User
from django.contrib.auth import authenticate, get_user_model, login, logout
from lms.models import Book, Transaction, Member

class BookForm(forms.ModelForm):
	class Meta:
		model = Book
		fields = ['name','author','description','image','price','rack_number','edition','total']

class BookFormUpdate(forms.ModelForm):
	class Meta:
		model = Book
		fields = '__all__'

class TransactionForm(forms.ModelForm):
	class Meta:
		model = Transaction
		fields = ['member','book']

class TransactionForm2(forms.ModelForm): #for searching transaction via member
	class Meta:
		model = Transaction
		fields = ['member']

class MemberForm(forms.ModelForm):
	class Meta:
		model = Member
		fields = ['name','address','department','phone','maximum_Book_Limit']

class MemberFormUpdate(forms.ModelForm):
	class Meta:
		model = Member
		fields = '__all__'

User = get_user_model()

class UserLoginForm(forms.Form):
	username = forms.CharField()
	password = forms.CharField(widget=forms.PasswordInput)

	def clean(self, *args, **kwargs):
		username = self.cleaned_data.get("username")
		password = self.cleaned_data.get("password")
		user=authenticate(username=username, password=password)
		user_qs= User.objects.filter(username=username)
		if user_qs.count() == 1:
			user = user_qs.first()
		if not user:
			raise forms.ValidationError("This user doesn't exist.")
		if not user.check_password(password):
			raise forms.ValidationError("Incorrect Password.")
		if not user.is_active:
			raise forms.ValidationError("The user is no longer active.")
		return super(UserLoginForm, self).clean(*args, **kwargs)
	
class UserRegisterForm(forms.ModelForm):
	password = forms.CharField(widget=forms.PasswordInput)
	class Meta:
		model = User
		fields=['username','email','password',]