from django.shortcuts import render
import library.database as db
import library.library as lb

def mylibrary(request):
    cur_user = lb.global_lb.now_login
    print("cur_user")
    print(cur_user)
    print(len(cur_user))
    if len(cur_user)!=0:
        sqil = 'select rname from reader_msg where rno=%s;' % cur_user[0]
        user_name = db.global_db.select_sql(sqil)
        sqil = 'select count(*) from borrow_msg where rno=%s and return_date is null'%cur_user[0]
        borrow_num = db.global_db.select_sql(sqil)
        sqil = 'select count(*) from borrow_msg where rno=%s and return_date is null and CURRENT_DATE > due_date'%cur_user[0]
        overdue_num = db.global_db.select_sql(sqil)
        return render(request, "mylibrary.html", {'cur_user': cur_user[0], 'cur_user_name': user_name[0][0], 'borrow_num': borrow_num[0][0], 'overdue_num': overdue_num[0][0], 'borrow_percent': borrow_num[0][0]*10, 'overdue_percent':overdue_num[0][0]*10})
    else:
        return render(request, 'signin.html', {"nextHtml": "mylibrary.html"})

