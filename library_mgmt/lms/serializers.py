from rest_framework import serializers
from lms.models import Book, Member, Transaction

class BookSerializer(serializers.ModelSerializer):
	class Meta:
		model = Book
		fields = '__all__'

class MemberSerializer(serializers.ModelSerializer):
	class Meta:
		model = Member
		fields = '__all__'

class TransactionSerializer(serializers.ModelSerializer):
	class Meta:
		model = Transaction
		fields = '__all__'
		