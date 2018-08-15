from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from tornado.options import options, define, parse_config_file
from day05.app.myapp import MyApplication, IndexHandler, LoginHandler, BlogHandler, RegistHandler, LoginModule, \
    BlogModule, RegistModule, CheckHandler

import time
import pymysql


# 连接数据库 并添加cursor游标
conn = pymysql.connect('localhost','root','123456',charset='utf8')
cursor = conn.cursor()
sql_createDB = '''create database if not exists blog_db default charset=utf8; use blog_db;'''
#  创建数据表的sql 语句  并设置name_id 为主键自增长不为空
sql_createTb = """create table if not exists tb_user(
user_id int auto_increment,
user_name varchar(32) not null,
user_password varchar(64) not null,
user_avatar varchar(128) default null,
user_city varchar(32) not null,
user_createdat datetime default current_timestamp,
user_updatedat datetime default current_timestamp on update current_timestamp, 
primary key(user_id),
unique(user_name)
)default charset = utf8;
create table if not exists tb_blog(
blog_id int auto_increment,
blog_user_id int not null,
blog_title varchar(100) not null,
blog_content varchar(1024) not null,
blog_createdat datetime default current_timestamp,
blog_updatedat datetime default current_timestamp on update current_timestamp,
primary key(blog_id),
foreign key(blog_user_id) references tb_user(user_id) on delete cascade on update cascade
)default charset=utf8;
create table if not exists tb_tag(
tag_id int auto_increment,
tag_content varchar(16) not null,
primary key(tag_id)
)default charset = utf8;
create table if not exists tb_blog_tag(
blog_tag_id int auto_increment,
rel_blog_id int not null,
rel_tag_id int not null,
primary key(blog_tag_id),
foreign key(rel_blog_id) references tb_blog(blog_id) on delete cascade on update cascade,
foreign key(rel_tag_id) references tb_tag(tag_id) on delete cascade on update cascade
)default charset=utf8;
create table if not exists tb_comment(
comment_id int auto_increment,
comment_blog_id int not null,
comment_user_id int not null,
comment_content varchar(256) not null,
comment_createdat datetime default current_timestamp,
comment_updatedat datetime default current_timestamp on update current_timestamp,
primary key(comment_id),
foreign key(comment_blog_id) references tb_blog(blog_id) on delete cascade on update cascade,
foreign key(comment_user_id) references tb_user(user_id) on delete cascade on update cascade
)default charset = utf8;
                 """
# 插入一条数据到moneytb 里面。
sql_insert = ['''insert into 
tb_user(user_name,user_password,user_city)
values ('abc','202cb962ac59075b964b07152d234b70','beijing');''','''
insert into 
tb_user(user_name,user_password,user_city)
values ('bcd','456','shanghai');''','''
insert into 
tb_user(user_name,user_password,user_city)
values ('cde','789','guangzhou');''','''
insert into 
tb_user(user_name,user_password,user_city)
values ('aaa','202cb962ac59075b964b07152d234b70','beijing');''','''
insert into 
tb_user(user_name,user_password,user_city)
values ('bbb','456','shanghai');''','''
insert into 
tb_user(user_name,user_password,user_city)
values ('ccc','789','guangzhou');''','''
insert into 
tb_user(user_name,user_password,user_city)
values ('ddd','202cb962ac59075b964b07152d234b70','beijing');''','''
insert into 
tb_user(user_name,user_password,user_city)
values ('eee','456','shanghai');''','''
insert into 
tb_user(user_name,user_password,user_city)
values ('fff','789','guangzhou');''','''
insert into 
tb_tag (tag_content) values ("体育"),("情感"),("星座"),("爱情"),("娱乐")
,("教育"),("科技"),("财经"),("动漫");''','''
insert into 
tb_blog(blog_user_id, blog_title, blog_content)
values (1,'第一篇博客','哈哈，开心的一天'),
(1,'第二篇博客','呜呜，伤心的一天'),
(1,'第三篇博客','今天的饭真难吃'),
(2,'第一篇博客','伤心的一天'),
(3,'第一篇博客','去超市'),
(4,'第一篇博客','呜呜'),
(5,'第一篇博客','今天吃烤肉'),
(6,'第一篇博客','与女友分手'),
(6,'第二篇博客','瑞典八强'),
(7,'第一篇博客','一天'),
(8,'第一篇博客','开一个皇马'),
(9,'第一篇博客','呜呜，伤心');''','''
insert into 
tb_blog_tag(rel_blog_id, rel_tag_id)
values (1,1),(1,6),(1,8),(3,1),(3,2),(4,3),
(4,5),(4,8),(6,2),(6,7),(8,5),(8,2);''','''
insert into 
tb_comment(comment_blog_id, comment_user_id, comment_content)
values (1,4,"沙发"),(1,3,"好人一生平安"),
(1,9,'ok'),(1,7,"1024"),(1,6,"nice"),
(2,2,"好文"),(7,3,'ok'),(4,1,'ok'),
(4,9,'1024'),(4,8,'已阅'),(6,1,'顶'),
(6,2,'666'),(5,5,'888'),(8,1,'888'),
(8,2,'666'),(8,4,'好'),(8,5,'喜闻乐见'),
(9,5,'1111'),(9,6,'ok'),(9,2,'hehe');
''']

# 在 execute里面执行SQL语句
cursor.execute(sql_createDB)
cursor.execute(sql_createTb)
for i in sql_insert:
    cursor.execute(i)
    time.sleep(0.5)
# print(cursor.rowcount)
conn.commit()

cursor.close()
conn.close()

define('duankou',type=int,default=8888)
parse_config_file('../config/config')
app = MyApplication(hs=[('/',IndexHandler),
                            ('/login',LoginHandler),
                            ('/blog',BlogHandler),
                            ('/regist',RegistHandler),
                            ('/check',CheckHandler)
                        ],
                  tp='mytemplate',
                  sp='mystatics',
                  um={'loginmodule':LoginModule,
                              'blogmodule':BlogModule,
                              'registmodule':RegistModule})

server = HTTPServer(app)
server.listen(options.duankou)
IOLoop.current().start()