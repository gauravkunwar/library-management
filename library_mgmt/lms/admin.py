# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from lms.models import Book, Member, Transaction
from django.contrib import admin

# Register your models here.
admin.site.register(Book)
admin.site.register(Member)
admin.site.register(Transaction)