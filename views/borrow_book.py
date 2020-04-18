from django.shortcuts import render
import datetime
import library.database as db
import library.library as lb
import views.book as book

borrow_nums = 0
borrow_barcode = []
error_message = []
info_message = []
# 提供借书服务的接口
# 根据借书的本数从而给出借书页面
def borrow_num(request):
    request.encoding = 'utf-8'
    book_db = db.global_db
    cur_user = lb.global_lb.now_login
    global borrow_nums
    if request.method == "POST":
        borrow_nums = int(request.POST['book_num'])
        sqil = 'select count(*) from borrow_msg where return_date is null and rno=%s;'%cur_user[0]
        result = book_db.select_sql(sqil)
        if result[0][0] + borrow_nums > 10:
            return render(request, 'reader_service_borrow_num.html', {'error_message': '您已超过最多可借图书的本数！！！'})
    save_ServiceBorrowHtml(borrow_nums, 'reader_service_borrow')
    return render(request,'reader_service_borrow.html')

def borrow_book(request):
    request.encoding = 'utf-8'
    global borrow_nums
    global borrow_barcode
    if request.method == "POST":
        borrow_barcode.clear()
        for i in range(1, borrow_nums+1):
            borrow_barcode.append(request.POST['barcode_'+str(i)])
    save_borrowConfirmHtml(borrow_barcode, 'reader_service_borrow_confirm')
    return render(request, 'reader_service_borrow_confirm.html')

def borrow_book_confirm(request):
    request.encoding = 'utf-8'
    global borrow_barcode
    book_db = db.global_db
    cur_user = lb.global_lb.now_login
    if request.method == "POST":
        if len(error_message)!=0:
            return render(request, 'reader_service_borrow.html')
        else:
            now = datetime.datetime.now()
            delta = datetime.timedelta(days=30)
            n_days = now + delta
            now = now.strftime('%Y-%m-%d')
            next = n_days.strftime('%Y-%m-%d')
            for single_book in borrow_barcode:
                #更新数据表book_msg的信息
                sqil = 'update book_msg set book_status=\'借出\' where barcode=%s;'%single_book
                book_db.exec_sql(sqil)
                #在数据表borrow_msg中插入读者借阅的信息
                sqil = 'insert into borrow_msg values (%s, %s, "%s", null, "%s");'%(single_book,cur_user[0],now,next)
                book_db.exec_sql(sqil)
            book.save_BorrowHistoryHTML("reader_service_return")
            return render(request, 'reader_service_return.html')

def save_ServiceBorrowHtml(num, prefix):
    fname = 'views/' + prefix + '.html'
    with open(fname, 'w', encoding='utf-8') as f:
        f.write(''.join([
            '<!doctype html>\n',
            '{% load static %}\n',
            '<html class ="fixed">\n',
            '   <head>\n',
            '       <meta charset="UTF-8">\n',
            '       <title>还书</title>\n',
            '       <link rel="stylesheet" href="{% static \'css/bootstrap.css\' %}" />\n',
            '		<link rel="stylesheet" href="{% static \'css/font-awesome.css\' %}" />\n',
            '       <!-- Theme CSS -->\n',
            '       <link rel="stylesheet" href="{% static \'css/theme.css\' %}" />\n',

            '       <!-- Skin CSS -->\n',
            '		<link rel="stylesheet" href="{% static \'css/default.css\' %}" />\n',
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
            '                       <h2 class ="title text-uppercase text-bold m-none"><i class ="fa fa-user mr-xs"></i>借书服务</h2>\n',
            '                   </div>\n',
            '                   <div class ="panel-body">\n',
            '                       <form action = "/borrow_book/" method = "post">\n',
            '                           {% csrf_token %}\n',
            '                           <div class ="form-group mb-lg">\n',
            '                               <label> 借书条码号 </label>\n',
            '                               <input name = "barcode_1" type="text" class="form-control input-lg"/>\n',
            '                           </div>\n',
        ]))

        for i in range(0, num-1):
            f.write(''.join([
                '                           <div class ="form-group mb-lg">\n',
                '                               <input name = "barcode_',
                str(i+2),
                '" type="text" class="form-control input-lg"/>\n',
                '                           </div>\n',
            ]))

        f.write(''.join([
            '                           <div class ="col-sm-16 text-center">\n',
            '                              <button type = "submit" class ="btn btn-primary hidden-xs"">借阅</button>\n',
            '                              <button type = "submit" class ="btn btn-primary btn-block btn-lg visible-xs mt-lg">borrow</button>\n',
            '                           </div>\n',
            '                       </form>\n',
            '                   </div>\n',
            '               </div>\n',
            '           </div>\n',
            '       </section>\n',
            '   </body>\n',
            '</html>\n',
        ]))

def save_borrowConfirmHtml(borrow_barcode, prefix):
    fname = 'views/' + prefix + '.html'
    with open(fname, 'w', encoding='utf-8') as f:
        f.write(''.join([
            '<!doctype html>\n',
            '{% load static %}\n',
            '<html class ="fixed">\n',
            '   <head>\n',
            '       <meta charset="UTF-8">\n',
            '       <title>同济大学图书馆---借书</title>\n',
            '       <link rel="stylesheet" href="{% static \'css/bootstrap.css\' %}" />\n',
            '		<link rel="stylesheet" href="{% static \'css/font-awesome.css\' %}" />\n',
            '       <!-- Theme CSS -->\n',
            '       <link rel="stylesheet" href="{% static \'css/theme.css\' %}" />\n',

            '       <!-- Skin CSS -->\n',
            '		<link rel="stylesheet" href="{% static \'css/default.css\' %}" />\n',
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
            '                       <h2 class ="title text-uppercase text-bold m-none"><i class ="fa fa-user mr-xs"></i>借书服务</h2>\n',
            '                   </div>\n',
            '                   <div class ="panel-body">\n',
            '                       <form action = "/borrow_book_confirm/" method = "post">\n',
            '                           {% csrf_token %}\n'
        ]))

        book_db = db.global_db
        book_title = []
        global error_message
        error_message.clear()
        for single_book in borrow_barcode:
            sqil = 'select book_status,title from book_msg where barcode=%s'%single_book
            result = book_db.select_sql(sqil)
            if len(result)!=0:
                if result[0][0]=='可借':
                    book_title.append(result[0][1] + ',' + single_book)
                elif result[0][0] == '借出':
                    error_message.append('图书"%s"已借出'%result[0][1])
                else:
                    error_message.append('馆藏目录中条码号为%s的图书已遗失'%single_book)
            else:
                error_message.append('馆藏目录中无条码号为%s的图书'%single_book)

        global info_message
        info_message.clear()
        if len(error_message)==0:
            info_message.append("确定借阅以下图书？\n")
            for single_book in book_title:
                info_message.append(single_book+'\n')

        if error_message:
            for each in error_message:
                f.write(''.join([
                    '                               <p>%s</p>\n'%each,
                ]))
            f.write(''.join([
                '                               <input type="text" style="display:none" name="value">\n'
                '                               <button type = "submit" class ="btn btn-primary hidden-xs" value="return" onclick="">返回</button>\n',
            ]))
        else:
            for each in info_message:
                f.write(''.join([
                    '                               <p>%s</p>\n' % each
                ]))
            f.write(''.join([
                '                               <button type="submit" class ="btn btn-primary hidden-xs" value="confirm" onclick="alert(\'借阅成功！！！\')">确定</button>\n',
            ]))

        f.write(''.join([
            '                       </form>\n',
            '                       {{info_message}}\n'
            '                   </div>\n',
            '               </div>\n',
            '           </div>\n',
            '       </section>\n',
            '   </body>\n',
            '</html>\n',
        ]))