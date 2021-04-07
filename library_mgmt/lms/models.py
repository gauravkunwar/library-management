# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import datetime
from django.db import models

class Book (models.Model):
	# name, price and category and image
	name = models.CharField(max_length=100)
	author = models.CharField(max_length=100,null=True,blank=True)
	description = models.TextField(max_length=1500,null=True,blank=True)
	image = models.ImageField(upload_to='book_images',null=True,blank=True)
	price = models.DecimalField(max_digits=8,decimal_places=2)
	rack_number = models.IntegerField(null=True,blank=True)
	edition = models.CharField(max_length=5,null=True,blank=True)
	available = models.IntegerField()
	total = models.IntegerField()

	def __str__(self):
		return self.name

class Member (models.Model):
	mem_no = models.AutoField(primary_key=True)
	name = models.CharField(max_length=100)
	address = models.CharField(max_length=100,null=True,blank=True)
	date_of_Membership = models.DateField(auto_now_add=True)

	CATEGORY_CHOICES = (
            ('Nursing', 'Nursing'),
            ('Radiography', 'Radiography'),
            ('HA', 'HA'),
            ('Laboratory', 'Laboratory'),
        )

	department = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
	phone = models.CharField(max_length=13,null=True,blank=True)
	number_of_Books_Issued = models.IntegerField(default='0')
	maximum_Book_Limit = models.IntegerField()

	def __str__(self):
		return str(self.mem_no)

class Transaction (models.Model):
	member = models.ForeignKey(Member,on_delete=models.CASCADE)
	book = models.ForeignKey(Book,on_delete=models.CASCADE)
	date_of_Issue = models.DateField(auto_now_add=True)
	due_Date = models.DateField()
	status = models.CharField(max_length=500,default='borrowed') # 'returned' is another status
