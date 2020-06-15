from django.shortcuts import render
# Create your views here.
import library.library as lb
import views.return_book as rb
import views.compesate_book as cb
def home(request):
    return render(request, 'home.html', {"login": '登录/注册'})

def signin(request):
    return render(request, 'signin.html', {"nextHtml": "home.html"})

def signup(request):
    return render(request, 'signup.html')

def mylibrary(request):
    return render(request, 'mylibrary.html', {"mylibrary":mylibrary})
#
def home_afterlogin(request):
    return render(request, 'home.html', {"login": lb.global_lb.now_login[0]})
#
def search_result(request):
    return render(request, 'search.html')

def reader_borrow_signin(request):
    if len(lb.global_lb.now_login) is 0:
        return render(request, 'signin.html', {"nextHtml": "reader_service_borrow_num.html"})
    else:
        return render(request, 'reader_service_borrow.html')
    # return render(request, 'reader_service_borrow.html')

def reader_return_signin(request):
    if len(lb.global_lb.now_login) is 0:
        return render(request, 'signin.html', {"nextHtml": "reader_service_return.html"})
    else:
        return rb.search_returnbooks(request)

def reader_compesate_signin(request):
    if len(lb.global_lb.now_login) is 0:
        return render(request, 'signin.html', {"nextHtml": "reader_service_compesation.html"})
    else:
        return cb.search_lostbooks(request)

def test(request):
    return render(request, 'forms-advanced.html')

def pay(request):
    return render(request, 'pay.html')

def manager(request):
    return render(request, 'manager.html',{"login": '登录'})

def manager_signin(request):
    return render(request, 'manager_signin.html', {"nextHtml": "manager.html"})

def manager_signup(request):
    return render(request, 'manager_signup.html')


def manager_borrow_signin(request):
    return render(request, 'manager_signin.html', {"nextHtml": "manager_service_borrow.html"})
    # return render(request, 'reader_service_borrow.html')

def manager_overdue_signin(request):
    return render(request, 'manager_signin.html', {"nextHtml": "manager_service_overdue.html"})

def manager_compesate_signin(request):
    return render(request, 'manager_signin.html', {"nextHtml": "manager_service_compesate.html"})