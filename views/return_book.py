from django.shortcuts import render
import library.database as db
import library.library as lb
import views.book as book
# 还书服务
# 保存还书服务的界面HTML
# 提供还书后的反馈界面：即当前借阅和借阅历史查看
overdue_table = ()
notoverdue_table = ()

def search_returnbooks(request):
    # request.encoding = 'utf-8'
    book_db = db.global_db
    cur_user = lb.global_lb.now_login
    global overdue_table
    global notoverdue_table

    sqil = 'select borrow_msg.barcode, book_msg.title from borrow_msg, book_msg where borrow_msg.barcode = book_msg.barcode and borrow_msg.rno =%s and return_date is null and due_date < DATE_FORMAT(CURDATE(), \'MM-dd-yyyy\')'%cur_user[0]
    overdue_table = book_db.select_sql(sqil)

    sqil = 'select borrow_msg.barcode, book_msg.title from borrow_msg, book_msg where borrow_msg.barcode = book_msg.barcode and borrow_msg.rno =%s and return_date is null and due_date > DATE_FORMAT(CURDATE(), \'MM-dd-yyyy\')'%cur_user[0]
    notoverdue_table = book_db.select_sql(sqil)

    # print("notoverdue_table")
    # print(notoverdue_table)
    save_ServiceReturnHtml(overdue_table, notoverdue_table, "reader_service_return")
    return render(request,template_name='reader_service_return.html')

def return_book(request):
    request.encoding = 'utf-8'
    book_db = db.global_db
    cur_user = lb.global_lb.now_login
    global overdue_table
    global notoverdue_table
    if request.method == "POST":
        select_book = request.POST.getlist('multiselect')
        print(select_book)
        # print(request.POST)
        # print(request.POST['multiselect'])
        if select_book and select_book[0] == 'multiselect-all':
            sqil = 'update borrow_msg set return_date=CURRENT_DATE() where rno=%s'%cur_user[0] + ' and return_date is null'
            # print(sqil)
            book_db.exec_sql(sqil)
            for i in range(1, len(select_book)):
                sqil = 'update book_msg set book_status="可借" where barcode=%s'%select_book[i]
                book_db.exec_sql(sqil)
        elif select_book and select_book[0] != 'multiselect-all':
            for single_book in select_book:
                sqil = 'update borrow_msg set return_date=CURRENT_DATE() where rno=%s'%cur_user[0] + ' and barcode=%s'%single_book + ' and return_date is null'
                # print(sqil)
                book_db.exec_sql(sqil)
                sqil = 'update book_msg set book_status="可借" where barcode=%s' % single_book

    book.save_BorrowHistoryHTML("reader_service_return")
    return render(request,'reader_service_return.html')

def save_ServiceReturnHtml(overdue_table, notoverdue_table, prefix):
    fname = 'views/' + prefix + '.html'
    with open(fname, 'w', encoding='utf-8') as f:
        f.write(''.join([
            '<!doctype html>\n',
            '{% load static %}\n',
            '<html class ="fixed">\n',
            '   <head>\n',
            '       <meta charset="UTF-8">\n',
            '       <title>同济大学图书馆---还书</title>\n',
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
            '                       <h2 class ="title text-uppercase text-bold m-none"><i class ="fa fa-user mr-xs"></i>还书服务</h2>\n',
            '                   </div>\n',
            '                   <div class ="panel-body">\n',
            '                       <form class ="form-horizontal form-bordered" action="/return_book/" method="post">\n',
            '                           {% csrf_token %}'
            '                           <div class ="form-group">\n',
            '                               <label class ="col-md-3 control-label">选择要还的书</label>\n',
            '                               <div class ="col-md-6" >\n',
            '                                   <select class ="form-control" multiple="multiple" data-plugin-multiselect data-plugin-options=\'{ "includeSelectAllOption": true }\' id="ms_example">\n'
        ]));

        f.write(''.join([
            '                                       <optgroup label="超期图书">'
        ]))
        for slice in overdue_table:
            f.write(''.join([
                '                                   <option value="' + str(slice[0]) + '">' + slice[1] + '(' + str(slice[0]) + ')' + '</option>'
            ]))
        f.write(''.join([
            '                                       </optgroup>'
        ]))
        f.write(''.join([
            '                                       <optgroup label="未超期图书">'
        ]))
        for slice in notoverdue_table:
            f.write(''.join([
                '                                   <option value="' + str(slice[0]) + '">' + slice[1] + '(' + str(slice[0]) + ')' + '</option>'
            ]))
        f.write(''.join([
            '                                       </optgroup>'
        ]))
        f.write(''.join([
            '                                   </select>\n',
            '                               </div>\n',
            '                           </div>\n',
            '                           <div align = "center">\n',
            '                               <button type = "submit" class ="btn btn-primary hidden-xs">还书</button>\n',
            '                               <button type = "submit" class ="btn btn-primary btn-block btn-lg visible-xs mt-lg">return</button>\n',
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

