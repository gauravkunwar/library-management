"""library_mgmt URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from lms import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    # url(r'^$',views.home,name='home'),
    url(r'^$',views.maketransaction,name='maketransaction'),

    #Users
    url(r'^register/$', views.register, name='register'),
    url(r'^login_user/$', views.login_user, name='login_user'),
    url(r'^logout_user/$', views.logout_user, name='logout_user'),

    #Books
    url(r'^addbook/$',views.addbook,name='addbook'),
    url(r'^viewbook/$',views.viewbook,name='viewbook'),
    url(r'^viewbook/(?P<pk>[0-9]+)/$', views.BookDetail.as_view(), name = 'bookdetail'),
    url(r'^update/book/(?P<pid>\d+)/$', views.updatebook, name='updatebook'),
    url(r'^delete/book/(?P<pid>\d+)/$', views.deletebook, name='deletebook'),

    #Transactions
    url(r'^maketransaction/$',views.maketransaction,name='maketransaction'),
    url(r'^viewtransaction/$',views.viewtransaction,name='viewtransaction'),
    url(r'^transaction/history/$',views.transactionhistory,name='transactionhistory'),
    url(r'^returnbook/(?P<pid>\d+)/$',views.returnbook,name='returnbook'),

    #Members
    url(r'^addmember/$',views.addmember,name='addmember'),
    url(r'^viewmember/$',views.viewmember,name='viewmember'),
    url(r'^viewmember/(?P<pk>[0-9]+)/$', views.MemberDetail.as_view(), name = 'memberdetail'),
    url(r'^update/member/(?P<pid>\d+)/$', views.updatemember, name='updatemember'),
    url(r'^delete/member/(?P<pid>\d+)/$', views.deletemember, name='deletemember'),

]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
