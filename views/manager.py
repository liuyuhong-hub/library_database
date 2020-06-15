from django.shortcuts import render
import library.database as db
import json
from django.shortcuts import HttpResponse

def manage_book_search(request):
    request.encoding = 'utf-8'
    if request.method == "POST":
        search = request.POST['search']
        print(search)
        book_db = db.global_db
    args = '%' + search + '%'
    sqil = "select title,editor,publishing_house,published_date,ISBN,callno,price from book_msg where title like '%s' or barcode like '%s' or editor like '%s' or publishing_house like '%s' or published_date like '%s' or abstract_notes like '%s' group by ISBN" % (args, args, args, args, args, args)
    # sqil = "select title,editor from book_msg where title like '%s' or barcode like '%s' or editor like '%s' or publishing_house like '%s' or published_date like '%s' or abstract_notes like '%s' order by barcode asc" % (args, args, args, args, args, args)
    # sqil = "select title,editor,publishing_house,published_date,callno,barcode,collections,ISBN,price,book_status,subject,abstract_notes from book_msg where title like '%s' or barcode like '%s' or editor like '%s' or publishing_house like '%s' or published_date like '%s' or abstract_notes like '%s' order by barcode asc" % (
    # args, args, args, args, args, args)
    fields = ['书名','主编','出版信息','ISBN','索书号','馆藏复本','可借复本','编辑']
    # '出版日期','索书号','条码号','馆藏地','ISBN','定价','书刊状态','学科主题','摘要文注','操作']
    search_result = book_db.select_sql(sqil)
    book_table = []
    for single_book in search_result:
        sqil = "select count(*) from book_msg where ISBN= '%s'" % single_book[4]
        collection_copy = book_db.select_sql(sqil)

        sqil = "select count(*) from book_msg where ISBN= '%s' and book_status='可借'" % single_book[4]
        borrowable_copy = book_db.select_sql(sqil)

        print(search_result)
        print(collection_copy[0][0])
        print(borrowable_copy[0][0])
        book_table.append(
            [single_book[0], single_book[1], single_book[2] + ', ' + date2str(single_book[3]) + ', ' + single_book[6],
             single_book[4], single_book[5], collection_copy[0][0], borrowable_copy[0][0]])
    # 已借出书籍详细信息
    sqil = "select ISBN,book_msg.barcode,collections,book_status,subject,abstract_notes, DATE_FORMAT(due_date,\"%%Y-%%m-%%d\") from book_msg,borrow_msg where (title like '%s%%' or book_msg.barcode like '%s%%' or editor like '%s%%' or publishing_house like '%s%%' or published_date like '%s%%' or abstract_notes like '%s%%') and book_msg.barcode=borrow_msg.barcode and book_status='借出' group by book_msg.barcode;" % (
    args, args, args, args, args, args)
    detail_borrowed = book_db.select_sql(sqil)
    # 未借出书籍详细信息
    sqil = "select ISBN,barcode,collections,book_status,subject,abstract_notes,null from book_msg where (title like '%s%%' or barcode like '%s%%' or editor like '%s%%' or publishing_house like '%s%%' or published_date like '%s%%' or abstract_notes like '%s%%') and book_status='可借';" % (
    args, args, args, args, args, args)
    detail_notborrow = book_db.select_sql(sqil)

    detail = detail_borrowed + detail_notborrow
    detail_json = json.dumps(detail)
    # save_editbookHtml(table=make_table(search_result, fields), search_name=search, prefix='edit',book_json=detail_json)
    # return render(request, "edit.html", {'book_json': detail_json})
    save_bookSearchHtml(table=make_table(book_table, fields), search_name=search, prefix='manager_search', book_json=detail_json)
    return render(request,"manager_search.html", {'book_json': detail_json})

def date2str(date,date_format = "%Y%m"):
    str = date.strftime(date_format)
    return str

def ym2date(year, month):
    return "%s-"%year + "%s-"%month + "01"

def make_table(ls_of_ls, fields=None):
    th = '<thead><tr>%s</tr></thead>\n' % ''.join('<th>{}</th>\n'.format(i) for i in fields) if fields else ''
    tr = '\n'.join(
        '<tr>' + ''.join('<td>{}</td>\n'.format(i) for i in ls) + '<td><form action="/edit/" method="post">{% csrf_token %}<input id="callno" name="callno" style="display: none" value='+'"%s"><button type="submit"><span>编辑</span></button></form></td>'%ls[4] + '</tr>'
        for ls in ls_of_ls)
    print("ls")
    # print(ls_of_ls[0][4])
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
        f.write('   						<h2 class="panel-title">管理员可修改书目信息\n')
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
        f.write(''.join([
            '<script>\n',
            'function setNextHtml()\n',
            '{\n',
                'var\n',
                'html = document.getElementsByTagName("p")[0].innerText;\n',
                'document.getElementById("callno").value = Callno;\n',
            '}\n',
            '</script>\n',
        ]))
        f.write('       <script src = "{% static \'js/examples.datatables.row.with.details.js\' %}"></script>\n')
        f.write('</html>\n')

def edit(request):
    request.encoding = 'utf-8'
    book_db = db.global_db
    if request.method == "POST":
        callno = request.POST['callno']
        print("callno")
        print(callno)
        args = '%' + callno + '%'
        sqil = "select * from book_msg where callno='%s'"%callno
        search_result = book_db.select_sql(sqil)
        print(search_result)

        message=[]
        detail=[]

        message.append(search_result[0][0])
        message.append(search_result[0][1])
        message.append(search_result[0][2])
        year = search_result[0][3].strftime("%Y")
        month = search_result[0][3].strftime("%m")
        message.append([year,month])
        print(message[3])
        message.append(search_result[0][4])
        message.append(search_result[0][7])
        message.append(search_result[0][8])
        message.append(search_result[0][10])
        message.append(search_result[0][11])

        for each in search_result:
            list=[each[5],each[6],each[9]]
            detail.append(list)

        save_bookEditHtml(message, detail, "edit")
        # sqil = "select title,editor,publishing_house,published_date,ISBN,callno,price from book_msg where title like '%s' or barcode like '%s' or editor like '%s' or publishing_house like '%s' or published_date like '%s' or abstract_notes like '%s' group by ISBN" % (
        # args, args, args, args, args, args)
    return render(request,"edit.html")

def save_bookEditHtml(message, detail, prefix):
    fname = 'views/' + prefix + '.html'
    with open(fname, 'w', encoding='utf-8') as f:
        f.write(''.join([
        '<!doctype html>\n',
        '{% load static %}\n',
        '<html class="fixed">\n',
	    '<head>\n',
		    '<!-- Basic -->\n',
		    '<meta charset="UTF-8">\n',
		    '<title>管理员界面---修改图书信息</title>\n',
		    '<!-- Mobile Metas -->\n',
		    '<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no" />\n',
		    '<!-- Vendor CSS -->\n',

            '<link rel="stylesheet" href="{% static \'css/bootstrap.css\' %}" />\n',
		    '<link rel="stylesheet" href="{% static \'css/magnific-popup.css\' %}" />\n',
            # '<link rel="stylesheet" href="{% static \'css/datepicker.css\' %}" />\n',
            # '<link rel="stylesheet" href="{% static \'css/datepicker3.css\' %}" />\n',
            
		    '<!-- Theme CSS -->\n',
		    '<link rel="stylesheet" href="{% static \'css/theme.css\' %}" />\n',

		    '<!-- Skin CSS -->\n',
		    '<link rel="stylesheet" href="{% static \'css/default.css\' %}" />\n',

		    '<!-- Theme Custom CSS -->\n',
		    '<link rel="stylesheet" href="{% static \'css/theme-custom.css\' %}">\n',

		    '<!-- Head Libs -->\n',
            '<style type = "text/css" >\n',
            'body {\n',
            'background-image: url("{% static \'images/bg.png\' %}");\n',
            '}\n',
            '</style>\n',
            '<script src="{% static \'js/modernizr.js\' %}"></script>\n',
	    '</head>\n',
	    '<body>\n',
        '<section class="panel">\n',
		    '<header class="panel-heading">\n',
			    '<h2 class="panel-title">修改图书信息</h2>\n',
		    '</header>\n',
		    '<div class="panel-body">\n',
			    '<form class="form-horizontal form-bordered" action="/change/" method="post">\n',
                    '{% csrf_token %}\n',
                    '<input id="callno_before" name="callno_before" style="display: none" value="%s">\n'%message[4],
                    '<div class="form-group">\n',
					    '<label class="col-md-3 control-label" for="inputDefault">书名</label>\n',
						    '<div class="col-md-6">\n',
							    '<input type="text" class="form-control" id="title" name="title" value="%s">\n'%message[0],
						    '</div>\n',
                    '</div>\n',
                    '<div class="form-group">\n',
                        '<label class="col-md-3 control-label" for="inputDefault">编者</label>\n',
                            '<div class="col-md-6">\n',
                                '<input type="text" class="form-control" id="editor" name="editor" value="%s">\n'%message[1],
                        '</div>\n',
				    '</div>\n',
                    '<div class="form-group">\n',
                        '<label class="col-md-3 control-label" for="inputDefault">出版社</label>\n',
                            '<div class="col-md-6">\n',
                                '<input type="text" class="form-control" id="publishing_house" name="publishing_house" value="%s">\n' % message[2],
                            '</div>\n',
                    '</div>\n',
                    '<div class="form-group">\n',
                         '<label class="col-md-3 control-label" for="inputDefault">出版日期</label>\n',
                            '<div class="col-md-3">\n',
                                '<input type="text" class="form-control" id="published_year" name="published_year" value="%s">\n' % message[3][0],
                            '</div>\n',
                            '<div class="col-md-3">\n',
                            '<input type="text" class="form-control" id="published_month" name="published_month" value="%s">\n' % message[3][1],
                            '</div>\n',
                    '</div>\n',
                    '<div class="form-group">\n',
                        '<label class="col-md-3 control-label" for="inputDefault">索书号</label>\n',
                            '<div class="col-md-6">\n',
                                '<input type="text" class="form-control" id="callno" name="callno" value="%s">\n' % message[4],
                            '</div>\n',
                    '</div>\n',
                    '<div class="form-group">\n',
                        '<label class="col-md-3 control-label" for="inputDefault">ISBN</label>\n',
                            '<div class="col-md-6">\n',
                                '<input type="text" class="form-control" id="ISBN" name="ISBN" value="%s">\n' % message[5],
                            '</div>\n',
                    '</div>\n',
                    '<div class="form-group">\n',
                        '<label class="col-md-3 control-label" for="inputDefault">价格</label>\n',
                            '<div class="col-md-6">\n',
                                '<input type="text" class="form-control" id="price" name="price" value="%s">\n' % message[6],
                            '</div>\n',
                    '</div>\n',
                    '<div class="form-group">\n',
                        '<label class="col-md-3 control-label" for="inputDefault">所属科目</label>\n',
                            '<div class="col-md-6">\n',
                                '<input type="text" class="form-control" id="subject" name="subject" value="%s">\n' % message[7],
                            '</div>\n',
                    '</div>\n',
                    '<div class="form-group">\n',
                        '<label class="col-md-3 control-label" for="inputDefault">摘要注释</label>\n',
                            '<div class="col-md-6">\n',
                                '<input type="text" class="form-control" id="abstract_notes" name="abstract_notes" value="%s">\n' % message[8],
                            '</div>\n',
                    '</div>\n'
        ]))
        i=1
        for each in detail:
            f.write(''.join([
                '<h3>图书%s</h3>\n'%i,
                '<div class="form-group">\n',
                '<label class="col-md-3 control-label" for="inputDefault">条码号</label>\n',
                '<div class="col-md-6">\n',
                '<input type="text" class="form-control" id="barcode_%s"'%i + ' name="barcode_%s'%i + '" value="%s">\n'% each[0],
                '</div>\n',
                '</div>\n',
                '<div class="form-group">\n',
                '<label class="col-md-3 control-label" for="inputDefault">馆藏地</label>\n',
                '<div class="col-md-6">\n',
                '<input type="text" class="form-control" id="collections_%s"' % i + ' name="collections_%s'%i + '" value="%s">\n' % each[1],
                # '<input type="text" class="form-control" id="inputDefault" value="%s">\n' % each[1],
                '</div>\n',
                '</div>\n',
                '<div class="form-group">\n',
                '<label class="col-md-3 control-label" for="inputDefault">状态</label>\n',
                '<div class="col-md-6">\n',
                '<input type="text" class="form-control" id="status_%s"' % i + ' name="status_%s'%i + '" value="%s">\n' % each[2],
                # '<input type="text" class="form-control" id="inputDefault" value="%s">\n' % each[2],
                '</div>\n',
                '</div>\n',
                ]))
            i+=1
        f.write(''.join([
                '<div class="button">\n',
                    '<button type="submit" class="mb-xs mt-xs mr-xs btn btn-primary">保存\n',
                    '</button>\n',
                '</div>\n',
            '</form>\n',
            '<form action="/delete/" method="post">\n',
            '{% csrf_token %}\n',
            '<input id="callno_before" name="callno_before" style="display: none" value="%s">\n' % message[4],
            '<div class="button">\n',
                    '<button type="submit" class="mb-xs mt-xs mr-xs btn btn-danger">删除\n',
                    '</button>\n',
                '</div>\n',
		    '</div>\n',
            '</form>\n',
	    '</section>\n',
        '<script src="{% static \'js/jquery.js\' %}></script>\n',
		'<script src="{% static \'js/bootstrap.js\' %}"></script>\n',
        '<script src="{% static \'js/nanoscroller.js\' %}"></script>\n',
        '<script src="{% static \'js/jquery.placeholder.js\' %}"></script>\n',
        '<script src="{% static \'js/jquery.maskedinput.js\' %}"></script>\n',
        '<script src="{% static \'js/bootstrap-datepicker.js\' %}"></script>\n',
		'<script src="{% static \'js/theme.js\' %}"></script>\n',
        '<script src="{% static \'js/theme.custom.js\' %}"></script>\n',
		'<script src="{% static \'js/theme.init.js\' %}"></script>\n',
	    '</body>\n',
        '</html>\n']))

def change(request):
    request.encoding = 'utf-8'
    book_db = db.global_db
    if request.method == "POST":
        title = request.POST['title']
        editor = request.POST['editor']
        publishing_house = request.POST['publishing_house']
        published_year = request.POST['published_year']
        published_month = request.POST['published_month']
        callno = request.POST['callno']
        ISBN = request.POST['ISBN']
        price = request.POST['price']
        subject = request.POST['subject']
        abstract_notes = request.POST['abstract_notes']
        callno_before = request.POST['callno_before']
        print(request.POST.keys())
        print(request.POST)
        print(callno_before)

        i=1
        detail=[]
        while("barcode_%s"%i in request.POST.keys() and [request.POST["barcode_%s"%i] != None and request.POST["collections_%s"%i]!= None and request.POST["status_%s"%i]]!= None):
            detail.append([request.POST["barcode_%s"%i],request.POST["collections_%s"%i],request.POST["status_%s"%i]])
            i+=1
        print(detail)

    sqil = 'delete from book_msg where callno="%s"'%callno_before
    book_db.exec_sql(sqil)
    for each in detail:
        sqil = 'insert into book_msg values("' + title + '","' + editor + '","' + publishing_house + '","' + ym2date(published_year,published_month) + '","' + callno + '","' + each[0] + '","' + each[1] + '","' + ISBN + '","' + price + '","' + each[2] + '","' + subject + '","' + abstract_notes + '");'
        print(sqil)
        book_db.exec_sql(sqil)
    # return render(request,'manage_book_search', request="数据库")
    return HttpResponse("保存成功")

def delete(request):
    request.encoding = 'utf-8'
    book_db = db.global_db
    if request.method == "POST":
        callno_before = request.POST['callno_before']
        sqil = 'delete from book_msg where callno="%s"'%callno_before
        book_db.exec_sql(sqil)

    return HttpResponse("删除成功")
