"""library_database URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import url
from django.urls import path, include
import library.views as views
import views.index as index
import views.book as book
import views.return_book as rb
import views.borrow_book as bb
import views.compesate_book as cb
import views.mylibrary as ml
import views.manager as ma
import views.manager_index as mi

urlpatterns = [
    path('admin/', admin.site.urls),
    # 三个网页
    url(r'^home/$',views.home, name='home'),
    # 我的图书馆
    # url(r'^mylibrary/$', views.mylibrary, name='mylibrary'),
    path('mylibrary/', ml.mylibrary),


    # 注册    
    path('signup/', views.signup),
    # 注册提交
    path('register_submit/', index.register_submit),
    # 登录
    path('signin/', views.signin),
    # 登录提交
    path('login_submit/', index.login_submit),
    path('home_afterlogin/', views.home_afterlogin),
    # 书籍查找
    path('book_search/', book.book_search),
    # 书籍查找结果
    path('search_result/', views.search_result),

    #借书服务
    path('reader_borrow_signin/', views.reader_borrow_signin),
    path('borrow_num/', bb.borrow_num),
    path('borrow_book/', bb.borrow_book),
    path('borrow_book_confirm/', bb.borrow_book_confirm),
    #还书服务
    path('reader_return_signin/', views.reader_return_signin),
    path('return_book/', rb.return_book),
    path('borrow_history/', book.borrow_history),

    #赔书服务
    path('reader_compesate_signin/', views.reader_compesate_signin),
    path('lost_book/', cb.lost_book),
    path('overdraft_book/', cb.overdraft_book),
    path('compesate_history/', cb.compesate_history),
    path('pay/',views.pay),

    # 管理员界面
    url(r'^manager/$',views.manager),
    # 管理员登录注册
    path('manager_signin/', views.manager_signin),
    path('manager_signup/', views.manager_signup),

    path('manager_login/', mi.manager_login),
    path('manager_register/', mi.manager_register),

    #管理员编辑书籍信息
    path('manage_book_search/', ma.manage_book_search),
    path('edit/', ma.edit),
    path('change/', ma.change),
    path('delete/', ma.delete),

    #管理员查询服务
    path('manager_overdue_signin/', views.manager_overdue_signin),
    path('manager_borrow_signin/', views.manager_borrow_signin),
    path('manager_compesate_signin/', views.manager_compesate_signin),

]