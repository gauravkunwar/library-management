# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import requests
from django.views import generic
from django.views.generic import View
from django.db.models import Q
# from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.http import HttpResponse, HttpResponseRedirect, Http404
from lms.models import Book, Transaction, Member
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, get_user_model, login, logout
from django.contrib.auth.decorators import login_required
from lms.forms import *
from datetime import datetime, timedelta, time

@login_required
def home(request):
		return render(request,'home.html')

@login_required
def addbook(request):
	if request.method =='POST':
		forms = BookForm(request.POST,request.FILES)
		if forms.is_valid():
			#extracting data from form
			data = forms.cleaned_data 
			#data from form in variables
			name = data['name']
			author = data['author']
			description = data['description']
			image = data['image']
			price = data['price']
			rack_number = data['rack_number']
			edition = data['edition']
			total = data['total']
			available = total
			# forms.save()
			Book.objects.create(name=name,author=author,description=description,image=image,price=price,rack_number=rack_number,edition=edition,available=available,total=total)
			return HttpResponseRedirect('/viewbook')
	else:
		forms = BookForm()
	context_dict = {'forms':forms}
	return render(request,'addbook.html',context_dict)

## Using generic view
# class ViewBook(generic.ListView):
# 	template_name = 'viewbook.html'
# 	context_object_name = 'book'

# 	def get_queryset(self):
# 		return Book.objects.all()

@login_required
def viewbook(request):
	query = Book.objects.all()
	context_dict = {'book':query}
	return render(request,'viewbook.html',context_dict)

class BookDetail(generic.DetailView):
	model = Book
	template_name = 'bookdetail.html'

# def bookdetail(request, book_id):
# 	try:
# 		book = Book.objects.get(id=book_id)
# 	except Book.DoesNotExist:
# 		raise Http404("Book doesn't exist")
# 	context = {'book':book}
# 	return render(request,'bookdetail.html', context)

@login_required
def updatebook(request, pid):
	if request.method=='GET':
		p = Book.objects.get(pk=pid)
		forms = BookFormUpdate(instance=p)
		return render(request,'updatebook.html',{'forms':forms})
	else:
		p = Book.objects.get(pk=pid)
		forms = BookFormUpdate(instance=p,data=request.POST)
		if forms.is_valid():
			forms.save()
		return HttpResponseRedirect('/viewbook')

@login_required
def deletebook(request, pid):
	p = Book.objects.get(pk=pid)
	p.delete()
	return HttpResponseRedirect('/viewbook')

@login_required
def maketransaction(request):
	if request.method =='POST':
		forms = TransactionForm(request.POST,request.FILES)
		if forms.is_valid():
			data = forms.cleaned_data #extracting data from form
			
			#data from form in variables
			book = data['book'] 
			member = data['member']

			#extracting the primary keys
			bok = Book.objects.get(id=int(book.id))
			membr = Member.objects.get(mem_no=int(member.mem_no))

			# Performing calculations
			if int(bok.available) == 0: #if book is not available
				message = 'Sorry! Book is out of Stock.'
				return render(request,'message.html',{'message':message})
			elif int(membr.number_of_Books_Issued) == int(membr.maximum_Book_Limit):
				message = 'Maximum books issued. Return books to borrow.'
				return render(request,'message.html',{'message':message})
			else:
				bok.available =int(bok.available) - 1
				membr.number_of_Books_Issued = int(membr.number_of_Books_Issued) + 1

				bok.save()
				membr.save()
				today = datetime.now().date()
				due_date = today + timedelta(days=15)
				Transaction.objects.create(member=membr,book=bok,due_Date=due_date)
				# forms.save()
				return HttpResponseRedirect('/viewtransaction')
	else:
		forms = TransactionForm()
	context_dict = {'forms':forms}
	return render(request,'maketransaction.html',context_dict)

@login_required
def viewtransaction(request): #active transactions
	today = datetime.now().date()
	if request.method =='POST':
		forms = TransactionForm2(request.POST,request.FILES)
		if forms.is_valid():
			data = forms.cleaned_data
			member = data['member']
			query = Transaction.objects.filter(member=member,status='borrowed').order_by('-id')
	else:
		forms = TransactionForm2()
		query = Transaction.objects.filter(status='borrowed').order_by('-id')
	context_dict = {'transaction':query,'forms':forms,'today':today}
	return render(request,'viewtransaction.html',context_dict)

# transaction history
@login_required
def transactionhistory(request):
	transaction = Transaction.objects.all().order_by('-id')
	# search
	query = request.GET.get("q")
	if query:
		transaction2 = transaction.filter(
			Q(book__name__icontains=query) |
			Q(member__name__icontains=query) |
			Q(member__mem_no__icontains=query)
			).distinct()
		return render(request, 'transaction_history.html', {'transaction': transaction2})
	else:
		return render(request,'transaction_history.html',{'transaction':transaction})

@login_required
def returnbook(request, pid):
	transaction = Transaction.objects.get(id=pid)
	bok = Book.objects.get(id=int(transaction.book.id)) #getting Book from Transaction
	membr = Member.objects.get(mem_no=int(transaction.member.mem_no)) #getting member from Transaction
	
	#Calculation
	if transaction.status == 'borrowed':
		bok.available =int(bok.available) + 1
		membr.number_of_Books_Issued = int(membr.number_of_Books_Issued) - 1
		bok.save()
		membr.save()
		transaction.status = 'returned'
		transaction.save()

	# Fine condition
	duedate=transaction.due_Date
	today = datetime.now().date()	
	if duedate < today:
		print ("Fine")
		days_passed = today - duedate
		num_days_passed = days_passed.days
		print (num_days_passed)
		if num_days_passed < 6: #first 5 days
			fine = num_days_passed*0.5 #$0.5 fine
		elif num_days_passed <16: #first 15 days
			fine = num_days_passed*1
		elif num_days_passed <31: #first month
			fine = num_days_passed*2
		else:
			fine = num_days_passed*5
		print (fine)
		return render(request,'fine.html',{
			'num_days_passed':num_days_passed,
			'fine':fine,
			'transaction':transaction,
			'today':today
			})
	return HttpResponseRedirect('/viewtransaction')

#generic view to add member
# class AddMember(CreateView):
# 	model = Member
# 	fields = ['name','address','department','phone','maxBookLimit']

@login_required		
def addmember(request):
	if request.method =='POST':
		forms = MemberForm(request.POST,request.FILES)
		if forms.is_valid():
			forms.save()
			return HttpResponseRedirect('/viewmember')
	else:
		forms = MemberForm()
	context_dict = {'forms':forms}
	return render(request,'addmember.html',context_dict)

@login_required
def viewmember(request):
	query = Member.objects.all()
	context_dict = {
	'member':query
	}
	return render(request,'viewmember.html',context_dict)

class MemberDetail(generic.DetailView):
	model = Member
	template_name = 'memberdetail.html'

@login_required
def updatemember(request, pid):
	if request.method=='GET':
		p = Member.objects.get(pk=pid)
		forms = MemberFormUpdate(instance=p)
		return render(request,'updatemember.html',{'forms':forms})
	else:
		p = Member.objects.get(pk=pid)
		forms = MemberFormUpdate(instance=p,data=request.POST)
		if forms.is_valid():
			forms.save()
		return HttpResponseRedirect('/viewmember')

@login_required
def deletemember(request, pid):
	p = Member.objects.get(pk=pid)
	p.delete()
	return HttpResponseRedirect('/viewmember')

def register(request):
	title = "Register"
	forms = UserRegisterForm(request.POST or None)
	if forms.is_valid():
		user = forms.save(commit=False)
		username = forms.cleaned_data['username']
		password = forms.cleaned_data['password']
		user.set_password(password)
		user.save()
		#login
		new_user = authenticate(username=username, password=password)
		login(request, user)
		return redirect('/')
	return render(request, 'register.html', {"forms": forms, "title":title})

def login_user(request):
	title = "Login"
	forms = UserLoginForm(request.POST or None)
	if forms.is_valid():
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(username=username, password=password)
		login(request, user)
		return redirect('/')
	return render(request, 'login.html', {"forms": forms, "title":title})

def logout_user(request):
	title = "Login"
	logout(request)
	return redirect('/')
