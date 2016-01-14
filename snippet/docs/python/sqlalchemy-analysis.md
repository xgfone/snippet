
SQLAlchemy分析
=============

Copyright © 2013 - 2016 xgfone(三界). All Rights Reserved.


## 一、介绍
`SQLAlchemy` 的一个目标是提供能兼容众多数据库（如 `SQLite`、`MySQL`、`Postgres`、`Oracle`、`MS-SQL`、`SQLServer` 和 `Firebird`）的企业级持久性模型。它是用 `Python` 实现的。

为了更大的灵活性，`SQLAlchemy` 分为两部分：`SQLAlchemy Expression Language（SQLAlchemy表达式语言）`和 `SQLAlchemy ORM（SQLAlchemy对象关系模型）`。

在使用`SQLAlchemy`时所要涉及到的类有`Engine`、`MetaData`、`Table`、`Column`、`ResultProxy`、`RowProxy`以及`sql`模块中的各函数和类。

  Engine类：管理数据库————建立连接（连接数据库驱动）；执行SQL语句（得到ResultProxy对象——包含多个RowProxy对象）。
  MetaData类：包含所有的Table表对象
  Table类：定义数据库表字段，并产生SQL语句（字段通过参数c/columns属性获取）
  Column类：表示数据库表字段
  ResultProxy类：SQL语句的执行结果（经常是在执行SELECT语句后使用），它相当于一个容器，其中包含着多个RowProxy对象
  RowProxy类：每条查询记录结果，支持元组、字典等获取方式
  sql模块：包含产生SQL语句的函数和类（被Table包含，但可单独使用）

注：以下分析基于 SQLAlchemy 0.8 版本。不过，由于接口是公共的，因此对于后续版本，变化应该不是很大。


第一部分  SQLAlchemy Expression Language
=======================================

## 二、SQLAlchemy代码大致分析
### 入口 `create_engine`
```python
function create_engine(url, **kwargs)  # ==> Engine(pool, dialect, url, ...)类实例对象
```

    (1) u = engine.url.make_url(url)   =>   URL对象
    (2) dialect_cls = u.get_dialect( )   =>   具体的dialect类，其包装了dbapi——具体的、实际上的驱动器（如MySQLdb）
    (3) kwargs["dbapi"] = dialect_cls.dbapi(**args)  =>  得到具体的驱动器类实例对象(dbapi是个类方法)
    (4) dialect = dialect_cls(**kwargs)  =>  得到dialect类实例对象（此时该方言对象中已包含了具体的驱动器对象）
    (5) return Engine(pool, dialect, u, ...)

**注：**

(1) `dbapi`是具体的驱动器，如`MySQLdb`、`sqlite3`等；`dialect`是方言，即具体的某一类SQL数据库（如mysql、sqlite等）；`dbapi`和`dialect`之间的关系：具体的某一类`dialect`有多种`dbapi`实现，比如：mysql数据库的Python接口有多种实现，如MySQLdb、pymysql、pyodbc等；换句话说就是，如果`dialect`是`mysql`，`dbapi`可以是`MySQLdb`、`pymysql`或`pyodbc`中任一个。

(2) 参数`url`的规范是 `RFC-1738`:
```
dialect+driver://user:password@host[:port]/dbname[?key=value&...]
```
其中的查询字符串作为参数传递给驱动器类（如MySQLdb.Connection(...)）来生成dbapi。

### class `Engine`(pool, dialect, url, ...)
    (1) _connection_cls = Connection类 （类属性）
    (2) engine = self
    (3) dialect = dialect对象（对dbapi的包装）
    (4) name = self.dialect.name        某一方言的名字（如“mysql”）
    (5) driver = self.dialect.driver    该方言所使用的驱动吕的名字（如“mysqldb”）
    (6) connect(**kwargs)  ==>  self.Connection(self, **kwargs)  ==>   返回一个Connection类实例对象
    (7) execute(statement, *multiparams, **params)                     返回一个ResultProxy类实例
            return self.connect(...).execute(statement, *multiparams, **params)
    (8) has_table(table_name, schema=None)    ==>   True/False
        通过dialect.has_table(...)向SQL服务器发出查询请求——SQL服务器是否拥有此表
    (9) execute_options(**opt)    返回OptionEngine（Engine类的子类）类实例

### class `Connection`(engine, ...)
    (1)  engine ＝ Engine实例
    (2)  dialect ＝ engine.dialect
    (3)  closed = True/False                连接是否关闭
    (4)  invalidated = True/False           连接是否有效
    (5)  __connection                       连接对象
    (6)  connection = self.__connection
    (7)  invalidate(...) = None             进行连接验证
    (8)  connect( ) = Connection类实例对象   返回的对象和本对象的属性值几乎相同，即用本对象再包装出另一个Connection类实例对象
    (9)  close( )                           关闭连接（调用self.__connection.close()）
    (10) scalar(obj, *multiparams, **params)
            return  self.execute(obj, *multiparams, **params).scalar()
    (11) execute(obj, *multiparams, **params)   =>  ResultProxy类实例
         self.dialect.execution_ctx_cls (该属性是一个ExecuteContext类——对执行环境的封装) ==> ResultProxy实例对象
         注： A. obj可以是
                 1) 字符串（SQL语句）
                 2) sql表达式  ==>  SQL语句对象（在sql.expression模块中）
                 3) 其他
              B. multiparams是用来填充参数：
                 1) 如果obj不是字符串，则multiparams应该用字典表示，一个字典表示语句的一次执行，多个表示多次执行；
                    当只有一次执行时，可以使用位置参数而非字典。
                 2) 如果obj是字符串，应该使用 text 函数来包装，使其成为一个SQL语句对象。
    (12)  info( )                    ==>  连接信息（一个字典）
    (13)  execution_options(**opts)  ==>  返回新的Connection类实例


### class `Dialect`
    (1)  name     方言的名字（如“mysql”）       （类属性）
    (2)  driver   驱动器的名字（如“mysqldb”）   （类属性）
    (3)  dbapi    被导入的驱动器对象（如：MySQLdb对象）
         注：在dialect实例被创建之前创建（参见create_engine函数）。
    (4)  connect(*args, **kwargs)  返回一个驱动器的连接对象（如：MySQLdb.Connection类实例）
            return self.dbapi.connect(*args, **kwargs)
    (5)  do_execute(...)
    (6)  do_executemany(...)
    (7)  do_rollback(...)
    (8)  do_commit(...)
    (9)  do_close(...)
    (10) .......

注： (5)(6)(7)(8)(9)最终转交 `dbapi` 来完成——与`SQL服务器`进行交互。

### function `text`(text, bind=None, bindparams=None, typemap=None)

#### 功能
将一个SQL字面值转换成SQLAlchemy SQL表达式对象。

#### 参数
`text`：SQL语句字符串，如果其中有占位符（或绑定参数），使用“`:<name>`”格式。
`bindparams`：一个`bindparams()`实例列表。

#### 注
在一个大的查询语句中，`text()`将自动被使用。

#### 例子
```python
conn.execute(text("select * from users"))                                                              # (1)
conn.execute(text("select * from users where id=:user_id"), user_id=22)                                # (2)
conn.execute(select([users.c.id]).where("id=:user_id"), user_id = 22)                                  # (3)
text("select * from users where update_at > :updated", bindparams=[bindparam("updated", DateTime())])  # (4)
text("select id, name from users", typemap={"id": Integer, "name": Unicode})                           # (5)
```

### class `ResultProxy`(context)
    (1)  context = dialect.execution_ctx_cls（即ExecutionContext类）实例
    (2)  dialect = context.dialect
    (3)  closed = True/False(默认)
    (4)  cursor = context.cursor
    (5)  _saved_cursor = context.cursor
    (6)  connection = context.root_connection
    (7)  __iter__()    =>  每个迭代结果都是一个RowProxy实例
    (8)  keys()        =>  列表（每个元素都是一个字段名）
    (9)  rowcount      =>  返回execute执行结果影响的记录的条数
    (10) lastrowid     =>  self._saved_cursor.lastrowid （有的方言没有实现，sqlite3实现了）
    (11) is_insert     =>  self.context.isinsert  =>  True/False        表明execute执行的是否是INSERT命令
    (12) close()           关闭self.cursor
    (13) fetch_all()   =>  列表（每个元素都是RowProxy实例）
    (14) fetchmany(size=None)   =>  列表（每个元素都是RowProxy实例），默认返回所有的查询记录（即同fetch_all()）
    (15) fetchone()             =>  None/RowProxy实例
    (16) first()                =>  None/RowProxy实例
    (17) scalar()               =>  None/RowProxy[0]   返回第一条查询记录的第一列的值（等同于 self.first()[0]）

### class `RowProxy`(parent, row, processors, keymap)
    (1)  __contains__(key)     key为字段名字，该条记录中是否包含名为key的字段
    (2)  __eq__(...)
    (3)  __ne__(...)
    (4)  __repr__(...)
    (5)  __len__( )            => 值的个数，即有多少个字段
    (6)  __getitem__(key)      key为字段名字
    (7)  __getattr__(name)     name为字段名字
    (8)  __iter__()            等同于itervalues方法
    (9)  has_key(key)          同__contains__方法
    (10) items( )              => [(key, value), (key, value), ...] ，其中key为字段名，value为字段的值
    (11) keys( )               => [key, key, ...]   返回字段名的列表
    (12) values( )             => list(self)        返回字段的值的列表
    (13) iterkeys( )           相当于iter(self.keys())
    (14) itemvalues( )         相当于iter(self.values())

### class `Table`(name, metadata, *args, **kwargs)
    (1) name         表的名字
    (2) metadata     => MetaData实例
    (3) schema       => None/...
    (3) key          => self.name/self.schema + self.name
    (4) bind         => None/Engine实例
    (5) exists(bind=None)                    =>  True/False 判断数据库中是否存在该表
    (6) create(bind=None, checkfirst=False)  在数据库创建本表（处理流程同MetaData.create_all方法）
    (7) drop(bind=None, checkfirst=False)    在数据库删除本表（处理流程同MetaData.drop_all方法）

### class `MetaData`(bind=None, reflect=False, schema=None, quote_schema=None)
    (1)  tables = util,immutabledict( )     包含所有的Table实例
    (2)  bind   = None / Engine实例
    (3)  schema
    (4)  is_bound        =>  True/False  该MetaData是不绑定Engine实例
    (5)  clear()         从MetaData中移除所有表
    (6)  remove(table)   从MetaData中移除指定的表（table为Table实例）
    (7)  sorted_tables   返回排过序的Table实例列表
    (8)  drop_all(bind=None, tables=None, checkfirst=True)    流程几乎与create_all相同，但行为为“删除”。
    (9)  create_all(bind=None, tables=None, checkfirst=True)
         A. bind._run_visitor(ddl.SchemaGenerator, self, checkfirst, tables)
         B. Connection._run_visitor(ddl.SchemaGenerator, self, checkfirst, tables)
         C. ddl.SchemaGenerator(Connection.dialect, Connection, checkfirst, tables, ...).traverse_single(MetaData)
             a. self._visitor_iterator
             b. visit_metadata(MetaData,
         注：traverse_single(MetaData)中的MetaData即是 B 中的self。
    (10) __contains__(table_or_key)  => True/False  返回MetaData中是否包含名为table_or_key的表


### 说明
1、当创建`Engine`时

    (1) 先导入驱动器模块dbapi（对于MySQLdb驱动器来说，就是MySQLdb模块对象，换句话说，dbapi==MySQLdb），
        然后把dbapi包装在dialect中，生成dialect实例对象；
    (2) 把creator函数（创建连接对象——连接到实际的数据库，可以自定义，即把自定义的creator函数作为参数传递给create_engine）
        包装在pool实例对象中；
    (3) 把dialect和pool作为参数创建Engine实例对象。

2、当首次调用`Engine.connect()`方法时，会生成`Connection`对象。该对象有一个属性`connection`（引用`self.__connection`的值），它是一个`_ConnectionFairy`类实例对象；在创建该实例对象时，会调用`_ConnectionRecord`类中的方法`get_connection()`来创建连接对象（通过调用`creator`函数）——连接到低层数据库的连接类实例（一般是方言中的`Connection`类，如`MySQLdb.Connection`），并成为`Connection.__connection.connection`的属性值。

3、如果以后再次使用相同的Engine实例对象来调用`connect()`方法，则会创建新的`Connection`和`_ConnectionFairy`实例对象，但`Connection.__connection.connection`的属性值不会变，始终是同一个连接对象（如`MySQLdb.Connection`的实例）————从`pool`中取出。

注：真正连接到低层数据库的时机是在第一次调用`Engine.connect`方法时。

## 三、SQLAlchemy框架分析

![IMG1](./_static/1.png)

**一般的使用方法：**

先创建一个`Engine`实例，再用`Engine`实例创建`Connection`实例，然后用`Connection.execute(...)`方法执行`SQL表达式对象`；尽量不要使用`SQL字面值`语句，如果非要使用时，请用`text(...)`对其进行包装。

## 四、例子
```python
from sqlalchemy import *
metadata = MeataData( )
users = Table("users", metadata,
              Column("id", Integer, primary_key=True),
              Column("name", String),
              Column("fullname", String))
address = Table("address", metadata,
                Column("id", Integer, primary_key=True),
                Column("user_id", None, ForeignKey("users.id")),
                Column("email", String, nullable=False))
metadata.create_all(engine)        # 在第一次运行时，要先在数据库中创建所有的表
conn = engine.connect()
ins = users.insert()               # 产生SQLAlchemy  SQL  INSERT表达式对象
result = conn.execute(ins.values(name="Jack", fullname="Jack Jones"))           # 执行单条命令
conn.execute(address.insert(), [{"user_id": 1, "email": "jack@yahoo.com"},     # 执行多条命令
                                {"user_id": 1, "email": "jack@msn.com"},
                                {"user_id": 2, "email": "www@www.org"},
                                {"user_id": 2, "email": "wendy@aol.com"}])
s = select([users])         # 产生SQL语句  select  *  from  users
result = conn.execute(s)
for row in result:
    print  row.id, row.name, row.fullname   # 或 print row["id"], row["name"], row["fullname"]

result = select([users.c.name, users.c.fullname])   # 产生SQL语句 select name, fullname from users
for row in result:
    print row.name, row.fullname                    # 或 print row["name"], row["fullname"]

result = conn.execute(select([users, address]))
s = select([users, address]).where(users.c.id==address.c.user_id)
result = conn.execute(s)
```


第二部分  SQLAlchemy ORM
=======================

## 五、SQLAlchemy ORM 介绍

`对象-关系映射`（Object/Relation Mapping，简称`ORM`），是随着面向对象的软件开发方法发展而产生的。面向对象的开发方法是当今企业级应用开发环境中的主流开发方法，关系数据库是企业级应用环境中永久存放数据的主流数据存储系统。对象和关系数据是业务实体的两种表现形式，业务实体在内存中表现为对象，在数据库中表现为关系数据。内存中的对象之间存在关联和继承关系，而在数据库中，关系数据无法直接表达多对多关联和继承关系。因此，对象-关系映射(ORM)系统一般以中间件的形式存在，主要实现程序对象到关系数据库数据的映射。

**ORM方法论基于三个核心原则：**

    简单：  以最基本的形式建模数据。
    传达性：数据库结构被任何人都能理解的语言文档化。
    精确性：基于数据模型创建正确标准化了的结构。

在`SQLAlchemy`中，也实现了`ORM`；同样，为了更大的灵活性，`SQLAlchemy`也将`ORM`分为两种模式：

    Classic：经典模式，又称Classical Mappings——经典映射
    Modern： 现代模式


## 六、SQLAlchemy ORM `经典模式`

在使用经典模式时，分三步：

    (1) 首先要先创建一个表描述（即SQLAlchemy Expression Language中的Table实例），
    (2) 然后创建一个表类（用于与表描述相关联的“新式类”），
    (3) 最后用mapper函数将表描述与表类关联起来。

以后就可以直接使用表类来操作与它关联的表在数据库中的呈现——具体地与数据库交互，是通过`Session`来完成的。

**如：**
```python
#  第一部分：实现对象-关系数据库表的映射
from sqlalchemy import Table, MetaData, Column, ForeignKey, Integer, String
from sqlalchemy.orm import mapper
metadata = MetaData()
user = Table('user', metadata,
             Column('id', Integer, primary_key=True),
             Column('name', String(50)),
             Column('fullname', String(50)),
             Column('password', String(12)))

class User(object):
    def __init__(self, name, fullname, password):
        self.name = name
        self.fullname = fullname
        self.password = password

mapper(User, user)
```

```python
#  第二部分：打开会话，完成事务
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
engine = create_engine('sqlite:///:memory:', echo=True)
Session = sessionmaker(bind=engine)                 # 创建一个Session类
session = Session()                                 # 创建一个Session实例
ed_user = User('ed', 'Ed Jones', 'edspassword')
session.add(ed_user)                                # 将对象加入到事务当中
session.commit()                                    # 提交事务
```
注：`mapper`返回一个`Mapper`映射类对象，它实现`对象-关系数据库表`的映射；在实现关系映射时，它还可指定映射参数等，具体地请参见`mapper函数`的参考手册。如：
```python
address =  Table('address', metadata,
                 Column('id', Integer, primary_key=True),
                 Column('user_id', Integer, ForeignKey('user.id')),
                 Column('email_address', String(50)))

class Address(object):
    def __init__(self, user_id, email):
        self.user_id = user_id
        self.email = email

# 经过下面的映射，在User实例中可以通过addresses属性来访问与User实例相关的Address对象；
# 反过来，也可在Address实例中通过user属性来访问与Address实现相关的User对象。
mapper(User, user, properties={ 'addresses' : relationship(Address, backref='user', order_by=address.c.id)})
mapper(Address, address)
```

注：一般来说，很少有人使用经典模式，而是使用现代模式，因为现代模式比经典模式更加精简。


## 七、SQLAlchemy ORM `现代模式`

可以粗略地认为，`现代模式`是`经典模式`的封装，其使用关系映射更加简单。

现代模式使用了一个`Declarative`系统，**`任何映射类都是一个Declarative基类的子类`**。

使用现代模式的步骤一般有二：

    (1) 创建一个Declarative基类；
    (2) 继承基类实现映射类——映射类是将表描述与表类合二为一，并继承自Declarative基类。

**如：**
```python
#  第一部分：创建一个Declarative基类
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base( )
```

```python
#  第二部分：继承自Declarative基类以创建一个映射子类
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy import relationship, backref

class User(Base):
    __tablename__ = 'users'              #  指定数据库表的名字

    #  数据库表字段的描述
    id = Column(Integer, primary_key=True)
    name = Column(String)
    fullname = Column(String)
    password = Column(String)

    def __init__(self, name, fullname, password):
        self.name = name
        self.fullname = fullname
        self.password = password

    def __repr__(self):
        return "<User('%s','%s', '%s')>" % (self.name, self.fullname, self.password)

class Address(Base):
    __tablename__ = "address"

    id = Column(Integer, primary_key=True)
    email = Column(String(50),  nullable=True)
    user_id = Column(Integer, ForeignKey("users.id"))

    # relationship表明：在Address实例中，可以通过user属性来访问与该Address实例相关的User实例对象；
    # backref（反向引用）表明：在User实例中，可以通过address属性来访问与该User实例相关的Address实例对象。
    user = relationship("User", backref=backref("address", order_by=id))

    def __init__(self, email):
        self.email = email

    def __repr__(self):
        return "<Address(%s)>" % self.email
```

注：

（1）在`Base`基类中，其实现了一个元类，在该元类中，根据子类中列出的信息，它会创建一个`Table`实例（表名使用`__tablename__`的值，字段描述使用子类的`Column`字段属性）——在创建`Table`对象之前，会先创建一个`MetaData`实例（每个`Declarative`基类只有唯一一个`MetaData`实例，即基于同一个`Declarative`基类的映射表类中的`metadata`属性是同一个实例对象）；最后在进行对象-关系映射（即调用`mapper`函数）。

（2）在`Declarative`基类中有个比较重要的类属性（所有实例共有的）：

    a. __tablename__   ==>  数据库表的名字
    b. __table__       ==>  Table实例对象（Declarative基类的每个子类单独拥有）
    c. __mapper__      ==>  Mapper实例对象（即mapper函数的返回值）（Declarative基类的每个子类单独拥有）
    d. metadata        ==>  MetaData实例对象（Declarative基类的所有子类共同拥有）
    e. 数据库表字段的描述（如上面的：id、name、fullname、password等）
       说明：
          (1) 单独拥有指各子类的值互不相同；共同拥有指所有子类的值一样，修改某个子类的该属性，其他子类的该属性也会变。
          (2) 对于每个子类的实例对象，类属性中的表字段描述属性也有其对应的实例属性，默认为None。
              如：user = User("xgfone",  "xgfone sangay", "123456")
              则 user.id等于None，user.name等于"xgfone"，user.fullname等于"xgfone sangay"，user.password等于"123456"。
              注：一旦该条目插入到数据库中，则user.id的值就不再是None了，而是一个整数值（如：1）；
                 但并不是所有的就是这种情况（当字段允许为 null 时，该字段的值还将是None）。


## 八、`Session` 和 `Query` 接口

略，待写。
