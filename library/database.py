import pymysql
# 提供图书馆数据库的接口
# global_db 为全局变量，可提供select语句的查找结果和数据库的更新等等。
class database():
    conn = pymysql.connect(host='localhost',user='root',password='6750765lyh',db='library',charset='utf8')
    book_msg = []                   #图书信息表
    manage_msg = []                 #管理人员表
    reader_msg = []                 #读者表
    borrow_msg = []                 #借阅归还表
    fine_msg = []                   #罚款表
    purchase_msg = []               #采购表
    scrap_msg = []                  #报废表
    lost_msg = []                   #遗失表
    def exec_sql(self, exec_sqli):
        cur = self.conn.cursor()
        try:
            cur.execute(exec_sqli)
        except Exception as Error:
            print('sql execute failed:', Error)
        else:
            print('sql execute success!')
        #提交sql语句， 作用于数据库;
        self.conn.commit()
        #关闭游标
        cur.close()

    def select_sql(self, select_sqli):
        cur = self.conn.cursor()
        try:
            cur.execute(select_sqli)
            result = cur.fetchall()
        except Exception as Error:
            print('sql execute failed:', Error)
        else:
            print('sql execute success!')
        #提交sql语句， 作用于数据库;
        self.conn.commit()
        #关闭游标
        cur.close()
        return result

global_db = database()
# d1.get_index()
