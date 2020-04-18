from django.shortcuts import render
from flask import render_template
import library.database as db
import library.library as lb
import json
# 图书查找结果界面HTML的保存，每条查找结果可以展示详细信息
# 个人借阅历史界面HTML的保存
def book_search(request):
    request.encoding = 'utf-8'
    if request.method == "POST":
        search = request.POST['search']
        print(search)
        book_db = db.global_db
        args = '%' + search + '%'
        sqil = "select title,editor,publishing_house,published_date,ISBN,callno,price from book_msg where title like '%s%%' or barcode like '%s%%' or editor like '%s%%' or publishing_house like '%s%%' or published_date like '%s%%' or abstract_notes like '%s%%' group by ISBN"%(args,args,args,args,args,args)
        # ,args,args,args,args,args)

        print(sqil)
        search_result = book_db.select_sql(sqil)
        print(search_result)
        book_table = []
        for single_book in search_result:
            sqil = "select count(*) from book_msg where ISBN= '%s'"%single_book[4]
            collection_copy = book_db.select_sql(sqil)

            sqil = "select count(*) from book_msg where ISBN= '%s' and book_status='可借'"%single_book[4]
            borrowable_copy = book_db.select_sql(sqil)

            print(search_result)
            print(collection_copy[0][0])
            print(borrowable_copy[0][0])
            book_table.append([single_book[0], single_book[1], single_book[2]+', '+date2str(single_book[3])+', '+single_book[6], single_book[4], single_book[5], collection_copy[0][0],borrowable_copy[0][0]])
        fields = ['书名','主编','出版信息','ISBN','索书号','馆藏复本','可借复本']
        print(book_table)
        # 已借出书籍详细信息
        sqil = "select ISBN,book_msg.barcode,collections,book_status,subject,abstract_notes, DATE_FORMAT(due_date,\"%%Y-%%m-%%d\") from book_msg,borrow_msg where (title like '%s%%' or book_msg.barcode like '%s%%' or editor like '%s%%' or publishing_house like '%s%%' or published_date like '%s%%' or abstract_notes like '%s%%') and book_msg.barcode=borrow_msg.barcode and book_status='借出' group by book_msg.barcode;" % (args,args,args,args,args,args)
        detail_borrowed = book_db.select_sql(sqil)
        # 未借出书籍详细信息
        sqil = "select ISBN,barcode,collections,book_status,subject,abstract_notes,null from book_msg where (title like '%s%%' or barcode like '%s%%' or editor like '%s%%' or publishing_house like '%s%%' or published_date like '%s%%' or abstract_notes like '%s%%') and book_status='可借';" % (args,args,args,args,args,args)
        detail_notborrow = book_db.select_sql(sqil)

        detail = detail_borrowed + detail_notborrow
        detail_json = json.dumps(detail)

        save_bookSearchHtml(table=make_table(book_table, fields), search_name=search, prefix='search', book_json=detail_json)
        return render(request,"search.html", {'book_json': detail_json})


def date2str(date,date_format = "%Y%m"):
    str = date.strftime(date_format)
    return str

def make_table(ls_of_ls, fields=None):
    th = '<thead><tr>%s</tr></thead>\n' % ''.join('<th>{}</th>\n'.format(i) for i in fields) if fields else ''
    tr = '\n'.join(
        '<tr>' + ''.join('<td>{}</td>\n'.format(i) for i in ls) + '</tr>'
        for ls in ls_of_ls)
    return '%s\n</table>' % (th + tr)

def save_bookSearchHtml(table, search_name, prefix, book_json):
    fname = 'views/' + prefix + '.html'
    with open(fname, 'w', encoding='utf-8') as f:
        f.write('<!doctype html>\n')
        f.write('{% load static %}\n')
        f.write('<html class="fixed">\n')
        f.write('   <head>\n')
        f.write('       <!-- Basic -->\n')
        f.write('       <meta charset="UTF-8">\n')
        f.write('       <title>同济大学图书馆数目检索系统</title>\n')
        f.write('       <!-- Vendor CSS -->\n')
        f.write('       <link rel="stylesheet" href="{% static \'css/bootstrap.css\' %}" />\n')
        f.write('       <link rel="stylesheet" href="{% static \'css/font-awesome.css\' %}" />\n')

        f.write('       <!-- Specific Page Vendor CSS -->\n')
        f.write('       <link rel="stylesheet" href="{% static \'css/select2.css\' %}" />\n')

        f.write('       <!-- Theme CSS -->\n')
        f.write('       <link rel="stylesheet" href="{% static \'css/theme-search.css\' %}" />\n')

        f.write('       <!-- Skin CSS -->\n')
        f.write('       <link rel="stylesheet" href="{% static \'css/default.css\' %}" />\n')

        f.write('       <!-- Head Libs -->\n')
        f.write('       <script src="{% static \'js/modernizr.js\' %}"></script>\n')
        f.write('       <style type="text/css">\n')
        f.write('           body {\n')
        f.write('           background-image: url("{% static \'images/bg.png\' %}");\n')
        f.write('           }\n')
        f.write('       </style>\n')
        f.write('   </head>\n')
        f.write('   <body>\n')
        f.write('       <section class="body">\n')
        f.write('           <div class="inner-wrapper">\n')
        f.write('       		<section role="main" class="content-body">\n')
        f.write('					<header class="page-header">\n')
        f.write('       				<h2>同济大学图书馆检索系统</h2>\n')
        f.write('       			</header>\n')
        f.write('      				<section class="panel">\n')
        f.write('						<header class="panel-heading">\n')
        f.write('   						<h2 class="panel-title">当前检索词为：%s</h2>\n'%search_name)
        f.write('   					</header>\n')
        f.write('   					<div class="panel-body">\n')
        f.write('                           <table class="table table-bordered table-striped mb-none" id="datatable-details">\n')

        f.write(table)

        f.write('                       </div>\n')
        f.write('                   </section>\n')
        f.write('               <!-- end: page-->\n')
        f.write('               </section>\n')
        f.write('           </div>\n')
        f.write('       </section>\n')

        f.write('       <!-- Vendor -->\n')
        f.write('       <script src = "{% static \'js/jquery.js\' %}"></script>\n')
        f.write('       <script src = "{% static \'js/nanoscroller.js\' %}"></script>\n')

        f.write('       <!-- Specific Page Vendor -->\n')
        f.write('       <script src = "{% static \'js/select2.js\' %}"></script>\n')
        f.write('       <script src = "{% static \'js/jquery.dataTables.js\' %}"></script>\n')
        f.write('       <script src = "{% static \'js/datatables.js\' %}"></script>\n')

        f.write('       < !-- Theme Base, Components and Settings -->\n')
        f.write('       <script src = "{% static \'js/theme.js\' %}"></script>\n')

        f.write('       < !-- Examples -->\n')

        f.write('   </body >\n')

        f.write(''.join([
            '<script>',
            'var book_data={{ book_json | safe }};',
            '</script>'
        ]))

        f.write('       <script src = "{% static \'js/examples.datatables.row.with.details.js\' %}"></script>\n')
        f.write('</html>\n')

def borrow_history(request):
    save_BorrowHistoryHTML("borrow_history")
    return render(request, 'borrow_history.html')

def save_BorrowHistoryHTML(prefix):
    fname = 'views/' + prefix + '.html'
    cur_user = lb.library.now_login
    # 已还图书
    sqil = 'select borrow_msg.barcode, book_msg.title, borrow_msg.borrow_date, borrow_msg.return_date from borrow_msg,book_msg where borrow_msg.barcode=book_msg.barcode and rno=%s'%cur_user[0] + ' and return_date is not null order by return_date desc;'
    borrow_returned_history = db.global_db.select_sql(sqil)
    print("returned_history")
    print(borrow_returned_history)
    print(sqil)
    # 未还图书
    sqil = 'select borrow_msg.barcode, book_msg.title, borrow_msg.borrow_date, borrow_msg.due_date from borrow_msg,book_msg where borrow_msg.barcode=book_msg.barcode and rno=%s'%cur_user[0] + ' and return_date is null order by borrow_date asc;'
    borrow_notreturn_history = db.global_db.select_sql(sqil)
    print(borrow_notreturn_history)

    fields_returned = ['条码号','书名', '借书日期','还书日期']
    fields_notreturn = ['条码号','书名', '借书日期','截止日期']

    returned_table = make_table(borrow_returned_history, fields_returned)
    notreturned_table = make_table(borrow_notreturn_history, fields_notreturn)

    with open(fname, 'w', encoding='utf-8') as f:
        with open(fname, 'w', encoding='utf-8') as f:
            f.write('<!doctype html>\n')
            f.write('{% load static %}\n')
            f.write('<html class="fixed">\n')
            f.write('   <head>\n')
            f.write('       <!-- Basic -->\n')
            f.write('       <meta charset="UTF-8">\n')
            f.write('       <title>借阅历史查询</title>\n')
            f.write('       <!-- Vendor CSS -->\n')
            f.write('       <link rel="stylesheet" href="{% static \'css/bootstrap.css\' %}" />\n')
            f.write('       <link rel="stylesheet" href="{% static \'css/font-awesome.css\' %}" />\n')

            f.write('       <!-- Specific Page Vendor CSS -->\n')
            f.write('       <link rel="stylesheet" href="{% static \'css/select2.css\' %}" />\n')

            f.write('       <!-- Theme CSS -->\n')
            f.write('       <link rel="stylesheet" href="{% static \'css/theme-search.css\' %}" />\n')

            f.write('       <!-- Skin CSS -->\n')
            f.write('       <link rel="stylesheet" href="{% static \'css/default.css\' %}" />\n')

            f.write('       <!-- Head Libs -->\n')
            f.write('       <script src="{% static \'js/modernizr.js\' %}"></script>\n')
            f.write('       <style type="text/css">\n')
            f.write('           body {\n')
            f.write('           background-image: url("{% static \'images/bg.png\' %}");\n')
            f.write('           }\n')
            f.write('       </style>\n')
            f.write('   </head>\n')
            f.write('   <body>\n')
            f.write('       <section class="body">\n')
            f.write('           <div class="inner-wrapper">\n')
            f.write('       		<section role="main" class="content-body">\n')
            f.write('					<header class="page-header">\n')
            f.write('       				<h2>借阅历史查询：%s</h2>\n' % cur_user[0])
            f.write('       			</header>\n')

            f.write('      				<section class="panel">\n')
            f.write('						<header class="panel-heading">\n')
            f.write('   						<h2 class="panel-title">当前借阅</h2>\n')
            f.write('   					</header>\n')
            f.write('   					<div class="panel-body">\n')
            f.write('   					    <table class ="table table-bordered table-striped mb-none" id="datatable-default" name="table-notreturn">\n')
            f.write(notreturned_table)
            f.write('                       </div>\n')
            f.write('                   </section>\n')
            # f.write('               </section>\n')
            #
            f.write('      				<section class="panel">\n')
            f.write('						<header class="panel-heading">\n')
            f.write('   						<h2 class="panel-title">借阅历史</h2>\n')
            f.write('   					</header>\n')
            f.write('   					<div class="panel-body">\n')
            f.write('   					    <table class ="table table-bordered table-striped mb-none" id="datatable-default" name="table-returned">\n')
            f.write(returned_table)
            f.write('                       </div>\n')
            f.write('                   </section>\n')

            f.write('               <!-- end: page-->\n')
            f.write('               </section>\n')
            f.write('           </div>\n')
            f.write('       </section>\n')

            f.write('       <!-- Vendor -->\n')
            f.write('       <script src = "{% static \'js/jquery.js\' %}"></script>\n')
            f.write('       <script src = "{% static \'js/nanoscroller.js\' %}"></script>\n')

            f.write('       <!-- Specific Page Vendor -->\n')
            f.write('       <script src = "{% static \'js/select2.js\' %}"></script>\n')
            f.write('       <script src = "{% static \'js/jquery.dataTables.js\' %}"></script>\n')
            f.write('       <script src = "{% static \'js/datatables.js\' %}"></script>\n')

            f.write('       < !-- Theme Base, Components and Settings -->\n')
            f.write('       <script src = "{% static \'js/theme.js\' %}"></script>\n')
            f.write('       <script src = "{% static \'js/examples.datatables.row.with.details.js\' %}"></script>\n')
            f.write('       < !-- Examples -->\n')

            f.write('   </body >\n')
            f.write('</html >\n')

def save_CompesateHistoryHtml(prefix):
    fname = 'views/' + prefix + '.html'
    cur_user = lb.library.now_login
    # 遗失已赔图书
    sqil = 'select fine_msg.barcode, title, fine_date, fine_msg.price from fine_msg,book_msg where fine_msg.barcode=book_msg.barcode and reason="遗失" and rno=%s order by fine_date desc'%cur_user[0]
    lost_payed_history = db.global_db.select_sql(sqil)
    print("returned_history")
    print(lost_payed_history)
    print(sqil)
    # 超期已赔图书
    sqil = 'select fine_msg.barcode, title, fine_date, fine_msg.price from fine_msg,book_msg where fine_msg.barcode=book_msg.barcode and reason="超期" and rno=%s order by fine_date desc'%cur_user[0]
    overdraft_payed_history = db.global_db.select_sql(sqil)
    print(overdraft_payed_history)
    # 超期未处理图书
    sqil = 'select borrow_msg.barcode, book_msg.title, borrow_msg.borrow_date, borrow_msg.return_date, borrow_msg.due_date, 0.05*DATEDIFF(borrow_msg.return_date,borrow_msg.due_date) from borrow_msg,book_msg where borrow_msg.barcode=book_msg.barcode and return_date > due_date and rno=%s and return_date not in (select fine_date from fine_msg where fine_msg.barcode=borrow_msg.barcode and fine_msg.rno=%s and fine_msg.fine_date=return_date);' % (cur_user[0], cur_user[0])
    unprocessed_history = db.global_db.select_sql(sqil)
    print(unprocessed_history)
    fields_lost = ['条码号', '书名', '罚款日期', '赔偿价格']
    fields_overdraft = ['条码号', '书名', '罚款日期', '赔偿价格']
    fields_unprocessed = ['条码号', '书名', '借书日期', '还书日期','应还日期','应赔价格']
    lost_table = make_table(lost_payed_history , fields_lost)
    overdraft_table = make_table(overdraft_payed_history, fields_overdraft)
    unprocessed_table = make_table(unprocessed_history, fields_unprocessed)
    with open(fname, 'w', encoding='utf-8') as f:
        with open(fname, 'w', encoding='utf-8') as f:
            f.write('<!doctype html>\n')
            f.write('{% load static %}\n')
            f.write('<html class="fixed">\n')
            f.write('   <head>\n')
            f.write('       <!-- Basic -->\n')
            f.write('       <meta charset="UTF-8">\n')
            f.write('       <title>赔偿历史查询</title>\n')
            f.write('       <!-- Vendor CSS -->\n')
            f.write('       <link rel="stylesheet" href="{% static \'css/bootstrap.css\' %}" />\n')
            f.write('       <link rel="stylesheet" href="{% static \'css/font-awesome.css\' %}" />\n')

            f.write('       <!-- Specific Page Vendor CSS -->\n')
            f.write('       <link rel="stylesheet" href="{% static \'css/select2.css\' %}" />\n')

            f.write('       <!-- Theme CSS -->\n')
            f.write('       <link rel="stylesheet" href="{% static \'css/theme-search.css\' %}" />\n')

            f.write('       <!-- Skin CSS -->\n')
            f.write('       <link rel="stylesheet" href="{% static \'css/default.css\' %}" />\n')

            f.write('       <!-- Head Libs -->\n')
            f.write('       <script src="{% static \'js/modernizr.js\' %}"></script>\n')
            f.write('       <style type="text/css">\n')
            f.write('           body {\n')
            f.write('           background-image: url("{% static \'images/bg.png\' %}");\n')
            f.write('           }\n')
            f.write('       </style>\n')
            f.write('   </head>\n')
            f.write('   <body>\n')
            f.write('       <section class="body">\n')
            f.write('           <div class="inner-wrapper">\n')
            f.write('       		<section role="main" class="content-body">\n')
            f.write('					<header class="page-header">\n')
            f.write('       				<h2>赔偿历史查询：%s</h2>\n' % cur_user[0])
            f.write('       			</header>\n')

            f.write('      				<section class="panel">\n')
            f.write('						<header class="panel-heading">\n')
            f.write('   						<h2 class="panel-title">超期未处理图书</h2>\n')
            f.write('   					</header>\n')
            f.write('   					<div class="panel-body">\n')
            f.write(
                '   					    <table class ="table table-bordered table-striped mb-none" id="datatable-default" name="table-notreturn">\n')
            f.write(unprocessed_table)
            f.write('                       </div>\n')
            f.write('                   </section>\n')
            # f.write('               </section>\n')
            #
            f.write('      				<section class="panel">\n')
            f.write('						<header class="panel-heading">\n')
            f.write('   						<h2 class="panel-title">遗失图书赔偿历史</h2>\n')
            f.write('   					</header>\n')
            f.write('   					<div class="panel-body">\n')
            f.write(
                '   					    <table class ="table table-bordered table-striped mb-none" id="datatable-default" name="table-returned">\n')
            f.write(lost_table)
            f.write('                       </div>\n')
            f.write('                   </section>\n')

            f.write('      				<section class="panel">\n')
            f.write('						<header class="panel-heading">\n')
            f.write('   						<h2 class="panel-title">超期图书赔偿历史</h2>\n')
            f.write('   					</header>\n')
            f.write('   					<div class="panel-body">\n')
            f.write(
                '   					    <table class ="table table-bordered table-striped mb-none" id="datatable-default" name="table-returned">\n')
            f.write(overdraft_table)
            f.write('                       </div>\n')
            f.write('                   </section>\n')

            f.write('               <!-- end: page-->\n')
            f.write('               </section>\n')
            f.write('           </div>\n')
            f.write('       </section>\n')

            f.write('       <!-- Vendor -->\n')
            f.write('       <script src = "{% static \'js/jquery.js\' %}"></script>\n')
            f.write('       <script src = "{% static \'js/nanoscroller.js\' %}"></script>\n')

            f.write('       <!-- Specific Page Vendor -->\n')
            f.write('       <script src = "{% static \'js/select2.js\' %}"></script>\n')
            f.write('       <script src = "{% static \'js/jquery.dataTables.js\' %}"></script>\n')
            f.write('       <script src = "{% static \'js/datatables.js\' %}"></script>\n')

            f.write('       < !-- Theme Base, Components and Settings -->\n')
            f.write('       <script src = "{% static \'js/theme.js\' %}"></script>\n')
            f.write('       <script src = "{% static \'js/examples.datatables.row.with.details.js\' %}"></script>\n')
            f.write('       < !-- Examples -->\n')

            f.write('   </body >\n')
            f.write('</html >\n')