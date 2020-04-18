from django.shortcuts import render
import library.database as db
import library.library as lb
import views.return_book as rb
import views.compesate_book as cb
import views.mylibrary as ml
#接收index.html提交的登录信息，包括name/password并进行判断
#登录成功后跳转到home.html
def login_submit(request):
    request.encoding = 'utf-8'
    if request.method == "POST":
        name = request.POST['username']
        password = request.POST['pwd']
        next_html = request.POST['next_html']
        login_db = db.global_db
        sqil = "select password from reader_msg where rno=%s;"%name
        true_pwd = login_db.select_sql(sqil)
        sqil = "select rname from reader_msg where rno=%s;"%name
        user_name = db.global_db.select_sql(sqil)
        # print(true_pwd[0][0])
        if true_pwd and password == true_pwd[0][0]:
            lb.global_lb.now_login.clear()
            lb.global_lb.now_login.append(name)
            print(next_html)
            print(lb.global_lb.now_login)
            if next_html == 'home.html':
                return render(request, 'home.html', {'login': name})
            elif next_html == 'reader_service_return.html':
                return rb.search_returnbooks(request)
            elif next_html == 'reader_service_compesation.html':
                return cb.search_lostbooks(request)
            elif next_html == 'mylibrary.html':
                # return render(req)
                return ml.mylibrary(request)
                # return render(request, 'mylibrary.html', {'cur_user': lb.global_lb.now_login[0], 'cur_user_name': user_name[0][0], 'borrow_num': 1, 'overdue_num': 3, 'borrow_percent': 10, 'overdue_percent':30})
            else:
                return render(request, next_html)
            # return render(request, 'home.html', {'login': name})
        else:
            return render(request, 'signin.html', {'error_message_login': "用户名或密码不正确"} )

def register_submit(request):
    request.encoding = 'utf-8'
    if request.method == "POST":
        no = request.POST['no']
        name = request.POST['name']
        faulty = request.POST['faulty']
        password = request.POST['pwd']
        repassword = request.POST['pwd_confirm']
        if len(no) != 7:
            return render(request, 'signup.html', {'error_message_register': '用户名应该用学号(7位)注册'})
        reg_db = db.global_db
        sqil = 'select password from reader_msg where rno='
        select_result = reg_db.select_sql(sqil+no)
        print(select_result)
        if select_result:
            return render(request, 'signup.html', {'error_message_register': '该用户名已注册，请使用自己的学号注册'})
        else:
            if len(password) < 8:
                return render(request, 'signup.html', {'error_message_register': '用户密码长度不得小于8位'})
            elif len(password) > 20:
                return render(request, 'signup.html', {'error_message_register': '用户密码长度不得大于20位'})
            else:
                if password != repassword:
                    return render(request, 'signup.html', {'error_message_register': '两次密码不同'})
                else:
                    sqil = 'insert into reader_msg values(' + no + ',\'' + name + '\',' + '\'\',' + '\'' + faulty + '\',\'' + password + '\');'
                    print(sqil)
                    reg_db.exec_sql(sqil)
                    return render(request, 'signup.html', {'error_message_register': '注册成功请重新登录'})