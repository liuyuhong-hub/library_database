from django.shortcuts import render
import library.database as db
import library.library as lb
import views.book as book

# 赔书服务
# 保存赔书服务的界面HTML
# 提供赔书后的反馈界面：赔偿历史

overdue_table = ()      #超期图书
notoverdue_table = ()   #未超期图书
overdraft_table = ()    #欠款图书（超期未还）

def search_lostbooks(request):
    # request.encoding = 'utf-8'
    book_db = db.global_db
    cur_user = lb.global_lb.now_login
    global overdue_table
    global notoverdue_table
    global overdraft_table
    sqil = 'select borrow_msg.barcode, book_msg.title, book_msg.price from borrow_msg, book_msg where borrow_msg.barcode = book_msg.barcode and borrow_msg.rno =%s and return_date is null and due_date < DATE_FORMAT(CURDATE(), \'MM-dd-yyyy\')'%cur_user[0]
    overdue_table = book_db.select_sql(sqil)

    sqil = 'select borrow_msg.barcode, book_msg.title, book_msg.price from borrow_msg, book_msg where borrow_msg.barcode = book_msg.barcode and borrow_msg.rno =%s and return_date is null and due_date > DATE_FORMAT(CURDATE(), \'MM-dd-yyyy\')'%cur_user[0]
    notoverdue_table = book_db.select_sql(sqil)

    sqil = 'select borrow_msg.barcode, book_msg.title, 0.05*DATEDIFF(borrow_msg.return_date,borrow_msg.due_date), borrow_msg.return_date from borrow_msg,book_msg where borrow_msg.barcode=book_msg.barcode and return_date > due_date and rno=%s and return_date not in (select fine_date from fine_msg where fine_msg.barcode=borrow_msg.barcode and fine_msg.rno=%s and fine_msg.fine_date=return_date);' % (cur_user[0], cur_user[0])
    overdraft_table = book_db.select_sql(sqil)

    save_ServiceCompesateHtml(overdue_table, notoverdue_table, overdraft_table, "reader_service_compesation")
    return render(request,template_name='reader_service_compesation.html')

# 遗失图书赔偿
def lost_book(request):
    request.encoding = 'utf-8'
    book_db = db.global_db
    cur_user = lb.global_lb.now_login
    global overdue_table
    global notoverdue_table
    if request.method == "POST":
        print(request.POST)
        select_book = request.POST.getlist('multiselect')
        print(select_book)
        if select_book and select_book[0] == 'multiselect-all':
            #更新borrow_msg
            sqil = 'update borrow_msg set return_date=CURRENT_DATE() where rno=%s'%cur_user[0] + ' and return_date is null'
            print(sqil)
            book_db.exec_sql(sqil)
            # 更新book_msg\fine_msg\lost_msg
            for i in range(1, len(select_book)):
                sqil = 'update book_msg set book_status="遗失" where barcode=%s'%select_book[i]
                book_db.exec_sql(sqil)
                sqil = 'insert fine_msg values(%s,%s,"遗失",(select price from book_msg where barcode=%s),CURRENT_DATE());'%(select_book[i], cur_user[0], select_book[i])
                book_db.exec_sql(sqil)
                sqil = 'insert lost_msg values(%s, CURRENT_DATE(),%s);'%(select_book[i], cur_user[0])
                book_db.exec_sql(sqil)
        elif select_book and select_book[0] != 'multiselect-all':
            #更新borrow_msg\book_msg\fine_msg\lost_msg
            for single_book in select_book:
                sqil = 'update borrow_msg set return_date=CURRENT_DATE() where rno=%s'%cur_user[0] + ' and barcode=%s'%single_book + ' and return_date is null'
                book_db.exec_sql(sqil)
                sqil = 'update book_msg set book_status="遗失" where barcode=%s' % single_book
                book_db.exec_sql(sqil)
                sqil = 'insert fine_msg values(%s,%s,"遗失",(select price from book_msg where barcode=%s),CURRENT_DATE());' % (single_book, cur_user[0], single_book)
                book_db.exec_sql(sqil)
                sqil = 'insert lost_msg values(%s, CURRENT_DATE(),%s);' % (single_book, cur_user[0])
                book_db.exec_sql(sqil)
    # 给出支付界面
    return render(request, 'pay.html')
# 超期图书赔偿
def overdraft_book(request):
    request.encoding = 'utf-8'
    book_db = db.global_db
    cur_user = lb.global_lb.now_login
    global overdraft_table
    if request.method == "POST":
        select_book = request.POST.getlist('multiselect')
        if select_book and select_book[0] == 'multiselect-all':
            # 更新fine_msg
            for i in range(1, len(select_book)):
                for j in range(0, len(overdraft_table)):
                    if select_book[i] == str(overdraft_table[j][0]) + str(overdraft_table[j][3]):
                        sqil = 'insert fine_msg values(%s,%s,"超期",%f,"%s");' % (overdraft_table[j][0], cur_user[0], overdraft_table[j][2], overdraft_table[j][3])
                        book_db.exec_sql(sqil)
                        break

        elif select_book and select_book[0] != 'multiselect-all':
            # 更新fine_msg
            for single_book in select_book:
                for i in range (0,len(overdraft_table)):
                    if single_book == str(overdraft_table[i][0]) + str(overdraft_table[i][3]):
                        sqil = 'insert fine_msg values(%s,%s,"超期",%f,"%s");' % (overdraft_table[i][0], cur_user[0], overdraft_table[i][2], overdraft_table[i][3])
                        book_db.exec_sql(sqil)
                        break
    # 给出支付界面
    return render(request, 'pay.html')

def compesate_history(request):
    book.save_CompesateHistoryHtml('reader_service_compesation')
    return render(request, 'reader_service_compesation.html')

def save_ServiceCompesateHtml(overdue_table, notoverdue_table, overdraft_table, prefix):
    fname = 'views/' + prefix + '.html'
    with open(fname, 'w', encoding='utf-8') as f:
        f.write(''.join([
            '<!doctype html>\n',
            '{% load static %}\n',
            '<html class ="fixed">\n',
            '   <head>\n',
            '       <meta charset="UTF-8">\n',
            '       <title>同济大学图书馆---赔书</title>\n',
            '       <link rel="stylesheet" href="{% static \'css/bootstrap.css\' %}" />\n',
            '		<link rel="stylesheet" href="{% static \'css/font-awesome.css\' %}" />\n',

		    '       <link rel="stylesheet" href="{% static \'css/bootstrap-multiselect.css\' %}" />\n',

		    '       <!-- Theme CSS -->\n',
		    '       <link rel="stylesheet" href="{% static \'css/theme.css\' %}" />\n',

		    '       <!-- Skin CSS -->\n',
            '		<link rel="stylesheet" href="{% static \'css/default.css\' %}" />\n',

		    '       <!-- Head Libs -->\n',
		    '       <script src="{% static \'js/modernizr.js\' %}"></script>\n',
            '       <style type="text/css">\n',
            '           body {\n',
            '           background-image: url("{% static \'images/bg.png\'%}");\n',
            '           }\n',
            '       </style>\n',
	        '   </head>\n',
            '   <body>\n',
            '       <section class ="body-sign">\n',
            '           <div class ="center-sign">\n',
            '               <div class ="panel panel-sign">\n',
            '                   <div class ="panel-title-sign mt-xl text-right">\n',
            '                       <h2 class ="title text-uppercase text-bold m-none"><i class ="fa fa-user mr-xs"></i>赔书服务</h2>\n',
            '                   </div>\n',
            '                   <div class ="panel-body">\n',
            '                       <form class ="form-horizontal form-bordered" action="/lost_book/" method="post">\n',
            '                           {% csrf_token %}\n'
            '                           <div class ="form-group">\n',
            '                               <label class ="col-md-4 control-label">选择遗失图书</label>\n',
            '                               <div class ="col-md-6" >\n',
            '                                   <select class ="form-control" multiple="multiple" data-plugin-multiselect data-plugin-options=\'{ "includeSelectAllOption": true }\' id="ms_example">\n'
        ]));

        f.write(''.join([
            '                                       <optgroup label="超期图书">'
        ]))
        for slice in overdue_table:
            f.write(''.join([
                '                                   <option value="' + str(slice[0]) + '">' + slice[1] + '(' + str(slice[0]) + ',' + slice[2] + ')' + '</option>'
            ]))
        f.write(''.join([
            '                                       </optgroup>'
        ]))
        f.write(''.join([
            '                                       <optgroup label="未超期图书">'
        ]))
        for slice in notoverdue_table:
            f.write(''.join([
                '                                   <option value="' + str(slice[0]) + '">' + slice[1] + '(' + str(slice[0]) + ',' + slice[2] + ')' + '</option>'
            ]))
        f.write(''.join([
            '                                       </optgroup>'
        ]))
        f.write(''.join([
            '                                   </select>\n',
            '                               </div>\n',
            '                           </div>\n',
            '                           <div align = "center">\n',
            '                               <button type = "submit" class ="btn btn-primary hidden-xs">遗失赔书</button>\n',
            '                               <button type = "submit" class ="btn btn-primary btn-block btn-lg visible-xs mt-lg">lost</button>\n',
            '                           </div>\n',
            '                       </form>\n',
            '                   </div>\n',
            '                   <div class ="panel-body"> \n',
            '                       <form class ="form-horizontal form-bordered" action="/overdraft_book/" method="post">\n',
            '                           {% csrf_token %}\n'
            '                           <div class ="form-group">\n',
            '                               <label class ="col-md-4 control-label">选择超期欠款图书</label>\n',
            '                               <div class ="col-md-6" >\n',
            '                                   <select class ="form-control" multiple="multiple" data-plugin-multiselect data-plugin-options=\'{ "includeSelectAllOption": true }\' id="ms_example">\n'
        ]));

        f.write(''.join([
            '                                       <optgroup label="超期图书">'
        ]))
        for slice in overdraft_table:
            f.write(''.join([
                '                                   <option value="' + str(slice[0]) + str(slice[3]) + '">' + slice[1] + '(' + str(slice[0]) + ', CNY' + str(slice[2]) + ')' + '</option>'
            ]))
        f.write(''.join([
            '                                       </optgroup>\n',
            '                                   </select>\n',
            '                               </div>\n',
            '                           </div>\n',
            '                           <div align = "center">\n',
            '                               <button type = "submit" class ="btn btn-primary hidden-xs">超期赔偿</button>\n',
            '                               <button type = "submit" class ="btn btn-primary btn-block btn-lg visible-xs mt-lg">overdraft</button>\n',
            '                           </div>\n',
            '                       </form>\n',
            '                   </div>\n',
            '               </div>\n',
            '           </div>\n',
            '       </section>\n',
            '       <!-- Vendor -->\n',
            '       <script src = "{% static \'js/jquery.js\' %}"></script>\n',
            '       <script src = "{% static \'js/bootstrap.js\' %}"></script>\n',
            '       <script src = "{% static \'js/nanoscroller.js\' %}"></script>\n',
            '       <script src = "{% static \'js/bootstrap-multiselect.js\' %}"></script>\n',
            '       <!-- Theme Base, Components and Settings -->\n',
            '       <script src = "{% static \'js/theme.js\' %}"></script>\n',

            '       <!-- Theme  Initialization Files -->\n',
            '       <script src = "{% static \'js/theme.init.js\' %}"></script>\n',
            '   </body>\n',
            '</html>\n',
        ]))