from django.shortcuts import render
import library.database as db
import library.library as lb
import views.return_book as rb
import views.compesate_book as cb
import views.manager_overdue as mo
import views.manager_borrow as mb
import views.manager_compesate as mc
import views.mylibrary as ml
#接收index.html提交的登录信息，包括name/password并进行判断
#登录成功后跳转到home.html
def manager_login(request):
    request.encoding = 'utf-8'
    if request.method == "POST":
        name = request.POST['username']
        password = request.POST['pwd']
        next_html = request.POST['next_html']
        login_db = db.global_db
        sqil = "select password from manage_msg where mno=%s;"%name
        true_pwd = login_db.select_sql(sqil)
        sqil = "select mname from manage_msg where mno=%s;"%name
        user_name = db.global_db.select_sql(sqil)
        # print(true_pwd[0][0])
        if true_pwd and password == true_pwd[0][0]:
            lb.global_lb.manager_login.clear()
            lb.global_lb.manager_login.append(name)
            print(next_html)
            print(lb.global_lb.now_login)
            if next_html == 'manager.html':
                return render(request, 'manager.html', {'login': name})

            ###   待改        ###
            elif next_html == 'manager_service_overdue.html':
                return rb.search_returnbooks(request)
            elif next_html == 'manager_service_borrow.html':
                return cb.search_lostbooks(request)
            elif next_html == 'manager_service_compesate.html':
                return cb.search_lostbooks(request)
                # return render(request, 'mylibrary.html', {'cur_user': lb.global_lb.now_login[0], 'cur_user_name': user_name[0][0], 'borrow_num': 1, 'overdue_num': 3, 'borrow_percent': 10, 'overdue_percent':30})
            else:
                return render(request, next_html)
            # return render(request, 'home.html', {'login': name})
        else:
            return render(request, 'manager_signin.html', {'error_message_login': "用户名或密码不正确"} )

def manager_register(request):
    request.encoding = 'utf-8'
    if request.method == "POST":
        no = request.POST['no']
        name = request.POST['name']
        sex = request.POST['sex']
        faulty = request.POST['faulty']
        email =  request.POST['email']
        phoneno =  request.POST['phoneno']

        password = request.POST['pwd']
        repassword = request.POST['pwd_confirm']
        if len(no) != 5:
            return render(request, 'manager_signup.html', {'error_message_register': '用户名应该用共号(5位)注册'})
        reg_db = db.global_db
        sqil = 'select password from manage_msg where mno='
        select_result = reg_db.select_sql(sqil+no)
        print(select_result)
        if select_result:
            return render(request, 'manager_signup.html', {'error_message_register': '该用户名已注册，请使用自己的共号注册'})
        else:
            if len(password) < 8:
                return render(request, 'manager_signup.html', {'error_message_register': '用户密码长度不得小于8位'})
            elif len(password) > 20:
                return render(request, 'manager_signup.html', {'error_message_register': '用户密码长度不得大于20位'})
            else:
                if password != repassword:
                    return render(request, 'manager_signup.html', {'error_message_register': '两次密码不同'})
                else:
                    sqil = 'insert into manage_msg values(' + no + ',' + '"' + name + '",' + '"' + sex + '",' + '"' +  faulty + '",' + '"' + email  + '",' + '"' + phoneno + '",' + '"' + password + '")'
                    # sqil = 'insert into reader_msg values(' + no + ',\'' + name + '\',' + '\'\',' + '\'' + faulty + '\',\'' + password + '\');'
                    print(sqil)
                    reg_db.exec_sql(sqil)
                    return render(request, 'manager_signup.html', {'error_message_register': '注册成功请重新登录'})