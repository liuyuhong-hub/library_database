from django.shortcuts import render
import library.database as db
def manage_book_search(request):
    request.encoding = 'utf-8'
    if request.method == "POST":
        search = request.POST['search']
        print(search)
        book_db = db.global_db
    args = '%' + search + '%'
    sqil = "select title,editor from book_msg where title like '%s' or barcode like '%s' or editor like '%s' or publishing_house like '%s' or published_date like '%s' or abstract_notes like '%s' order by barcode asc" % (args, args, args, args, args, args)
    # sqil = "select title,editor,publishing_house,published_date,callno,barcode,collections,ISBN,price,book_status,subject,abstract_notes from book_msg where title like '%s' or barcode like '%s' or editor like '%s' or publishing_house like '%s' or published_date like '%s' or abstract_notes like '%s' order by barcode asc" % (
    # args, args, args, args, args, args)
    fields = ['书名','编者','操作']
    # '出版日期','索书号','条码号','馆藏地','ISBN','定价','书刊状态','学科主题','摘要文注','操作']
    search_result = book_db.select_sql(sqil)
    save_editbookHtml(table=make_table(search_result, fields), prefix='edit_test')
    return render(request, 'edit_test.html')

def make_table(ls_of_ls, fields=None):
    th = '<thead><tr>%s</tr></thead>\n' % ''.join('<th>{}</th>\n'.format(i) for i in fields) if fields else ''
    tr = '\n'.join(
        '<tr>' + ''.join('<td>{}</td>\n'.format(i) for i in ls) + ''.join([
        '<td class ="actions">\n',
        '   <a href = "#" class="hidden on-editing save-row"><i class ="fa fa-save"></i></a>\n',
        '   <a href = "#" class="hidden on-editing cancel-row"><i class ="fa fa-times"></i></a>\n',
        '   <a href = "#" class="on-default edit-row"><i class="fa fa-pencil"></i></a>\n',
        '   <a href = "#" class="on-default remove-row"><i class="fa fa-trash-o"></i></a>\n',
        '</td>'
        ]) + '</tr>'  for ls in ls_of_ls)
    return '%s\n</table>' % (th + tr)


def save_editbookHtml(table, prefix):
    fname = 'views/' + prefix + '.html'
    with open(fname, 'w', encoding='utf-8') as f:
        f.write('<!doctype html>\n')
        f.write('{% load static %}\n')
        f.write('<html class="fixed">\n')
        f.write('   <head>\n')
        f.write('       <!-- Basic -->\n')
        f.write('       <meta charset="UTF-8">\n')
        f.write('       <title>管理员界面---修改图书信息</title>\n')
        f.write('       <meta name = "viewport" content = "width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no"/>\n')
        f.write('       <!-- Vendor CSS -->\n')
        f.write('       <link rel="stylesheet" href="{% static \'css/bootstrap.css\' %}" />\n')
        f.write('       <link rel="stylesheet" href="{% static \'css/font-awesome.css\' %}" />\n')
        f.write('       <link rel = "stylesheet" href ="{% static \'css/magnific-popup.css\' %}"/>\n')
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
        f.write('   						<h2 class="panel-title">管理员可修改书目信息</h2>\n')
        f.write('   					</header>\n')
        f.write('   					<div class="panel-body">\n')
        f.write('   					    <div class="row">\n')
        f.write('                               <div class ="col-sm-6">\n')
        f.write('                                       <div class ="mb-md">\n')
        f.write('                                       <button id = "addToTable" class ="btn btn-primary">添加图书<i class="fa fa-plus"></i></button>\n')
        f.write('                                   </div>\n')
        f.write('                               </div>\n')
        f.write('                           </div>\n')
        f.write('                           <table class="table table-bordered table-striped mb-none" id="datatable-editable">\n')

        f.write(table)

        f.write('                       </div>\n')
        f.write('                   </section>\n')
        f.write('               <!-- end: page-->\n')
        f.write('               </section>\n')
        f.write('           </div>\n')
        f.write('       </section>\n')
        f.write('       <div id = "dialog" class ="modal-block mfp-hide" >\n')
        f.write('           <section class ="panel">\n')
        f.write('               <header class ="panel-heading">\n')
        f.write('                   <h2 class ="panel-title"> 确认 </h2>\n')
        f.write('               </header>\n')
        f.write('               <div class ="panel-body">\n')
        f.write('                   <div class ="modal-wrapper">\n')
        f.write('                       <div class ="modal-text">\n')
        f.write('                           <p> 确定要删除该书目？ </p>\n')
        f.write('                       </div>\n')
        f.write('                   </div>\n')
        f.write('               </div>\n')
        f.write('               <footer class="panel-footer">\n')
        f.write('                   <div class="row">\n')
        f.write('                       <div class ="col-md-12 text-right">\n')
        f.write('                           <button id="dialogConfirm" class="btn btn-primary">确定</button>\n')
        f.write('                           <button id="dialogCancel" class="btn btn-default">取消</button>\n')
        f.write('                       </div>\n')
        f.write('                   </div>\n')
        f.write('               </footer>\n')
        f.write('           </section>\n')
        f.write('       </div>\n')
        f.write('       <!-- Vendor -->\n')
        f.write('       <script src = "{% static \'js/jquery.js\' %}"></script>\n')
        f.write('       <script src = "{% static \'js/bootstrap.js\' %}"></script>\n')
        f.write('       <script src = "{% static \'js/nanoscroller.js\' %}"></script>\n')
        f.write('       <script src = "{% static \'js/magnific-popup.js\' %}"></script>\n')
        f.write('       <!-- Specific Page Vendor -->\n')
        f.write('       <script src = "{% static \'js/select2.js\' %}"></script>\n')
        f.write('       <script src = "{% static \'js/jquery.dataTables.js\' %}"></script>\n')
        f.write('       <script src = "{% static \'js/datatables.js\' %}"></script>\n')

        f.write('       <!-- Theme Base, Components and Settings -->\n')
        f.write('       <script src = "{% static \'js/theme.js\' %}"></script>\n')
        f.write('       <script src = "{% static \'js/theme.init.js\' %}"></script>\n')
        f.write('       <!-- Examples -->\n')
        f.write('       <script src="{% static \'js/examples.datatables.editable.js\' %}"></script>\n')
        f.write('   </body >\n')
        f.write('</html>\n')
