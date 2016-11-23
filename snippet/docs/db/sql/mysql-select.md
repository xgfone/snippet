
mysql的查询、子查询及连接查询
=========================

## 一、mysql查询的五种子句
	where    条件查询
	having   筛选
	group by 分组
	order by 排序
	limit    限制结果数

### 1、where常用运算符
#### 比较运算符
	> ,  < ,=  , != （< >）,>=   ,   <=
	in(v1,v2..vn)
	between v1 and v2   在v1至v2之间（包含v1,v2）

#### 逻辑运算符
	not(!)  逻辑非
	or(||)  逻辑或
	and(&&) 逻辑与

```sql
where price>=3000 and price <= 5000 or price >=500 and price <=1000
```
取500-1000或者3000-5000的值。

```sql
where price not between 3000 and 5000
```
不在3000与5000之间的值。

#### 模糊查询
	like  像
	通配符:
		%  任意字符
		_  单个字符
		   where goods_name like '诺基亚%'
		   where goods_name like '诺基亚N__'

### 2、group by 分组
一般情况下`group`需与`统计函数（聚合函数）`一起使用才有意义。如：
```sql
select goods_id,goods_name,cat_id,max(shop_price) from goods group by cat_id;
```
这里取出来的结果中的`good_name`是错误的！因为`shop_price`使用了`max`函数，那么它是取最大的，而语句中使用了`group by`分组，那么`goods_name`并没有使用聚合函数，它只是`cat_id`下的第一个商品，并不会因为`shop_price`改变而改变。

#### mysql中的五种统计函数

##### max：求最大值
```sql
select max(goods_price) from goods;
```
这里会取出最大的价格的值，只有值。

```sql
select cat_id,max(goods_price) from goos group by cat_id;
```
查询每个栏目下价格最高的。

```sql
select goods_id,max(goods_price) from goods group by goods_id;
```
查出价格最高的商品编号。

##### min：求最小值

##### sum：求总数和
```sql
select sum(goods_number) from goods;
```
求商品库存总和。

##### avg：求平均值
```sql
select cat_id,avg(goods_price) from goods group by cat_id;
```
求每个栏目的商品平均价格。

##### count：求总行数
```sql
select cat_id,count(*) from goods group by cat_id;
```
求每个栏目下商品种类。

**要把每个字段名当成变量来理解，它可以进行运算**

```sql
select goods_id,goods_name,goods_price-market_price from goods;
```
查询本店每个商品价格比市场价低多少。

```sql
select cat_id,sum(goods_price*goods_number) from goods group by cat_id;
```
查询每个栏目下面积压的货款。

**可以用as来给计算结果取个别名**
```sql
select cat_id,sum(goods_price * goods_number)  as hk from goods group by cat_id
```

**不仅列名可以取别名，表单也可以取别名**

### 3、having 与 where 的异同点
	having与where类似，可以筛选数据，where后的表达式怎么写，having后就怎么写。
	where针对表中的列发挥作用，查询数据。
	having对查询结果中的列发挥作用，筛选数据。

```sql
select goods_id,good_name,market_price - shop_price as s from goods having s>200 ;
```
查询本店商品价格比市场价低多少钱，输出低200元以上的商品。
注：这里不能用where因为s是查询结果，而where只能对表中的字段名筛选；如果用where的话则是：
```sql
select goods_id,goods_name from goods where market_price - shop_price > 200;
```

```sql
select cat_id,goods_name,market_price - shop_price as s from goods where cat_id = 3 having s > 200;
```
同时使用where与having。

```sql
select cat_id,sum(shop_price * goods_number) as t from goods group by cat_id having s > 20000
```
查询积压货款超过2万元的栏目，以及该栏目积压的货款。

**_查询两门及两门以上科目不及格的学生的平均分_**

思路：
```sql
#(1) 先计算所有学生的平均分
select name,avg(score) as pj from stu group by name;

#(2) 查出所有学生的挂科情况
select name,score<60 from stu;
#这里score<60是判断语句，所以结果为真或假，mysql中真为1假为0

#(3) 查出两门及两门以上不及格的学生
select name,sum(score<60) as gk from stu group by name having gk > 1;

#(4) 综合结果
select name,sum(score<60) as gk,avg(score) as pj from stu group by name having gk >1;
```

### 4、order by
```sql
order by price  	//默认升序排列
order by price desc //降序排列
order by price asc 	//升序排列，与默认一样
order by rand() 	//随机排列，效率不高
```

```sql
select * from goods where cat_id !=2 order by cat_id,price desc;
```
按栏目号升序排列，每个栏目下的商品价格降序排列。

### 5、limit
	limit [offset,] N
	offset 	偏移量，可选，不写则相当于 limit 0,N
	N     	取出条目

```sql
select good_id,goods_name,goods_price from goods order by good_price desc limit 3,3;
```
取价格第4-6高的商品。

###查询每个栏目下最贵的商品
思路：
```sql
#(1) 先对每个栏目下的商品价格排序
select cat_id,goods_id,goods_name,shop_price from goods order by cat_id,shop_price desc;
#上面的查询结果中每个栏目的第一行的商品就是最贵的商品。把上面的查询结果理解为一个临时表[存在于内存中]【子查询】。

#(2) 再从临时表中选出每个栏目最贵的商品
select * from (select goods_id,goods_name,cat_id,shop_price from goods order by cat_id,shop_price desc) \
as t group by cat_id;
#这里使用group by cat_id是因为临时表中每个栏目的第一个商品就是最贵的商品，而group by前面没有使用聚合函数，
#所以默认就取每个分组的第一行数据，这里以cat_id分组。
```

良好的理解模型：

	1、where后面的表达式，把表达式放在每一行中，看是否成立；
	2、字段(列)，理解为变量，可以进行运算（算术运算和逻辑运算）；
	3、取出结果可以理解成一张临时表。


## 二、mysql子查询
### 1、where型子查询
**`把内层查询结果当作外层查询的比较条件`**

```sql
select goods_id,goods_name from goods where goods_id = (select max(goods_id) from goods);
```
不用`order by`来查询最新的商品。

```sql
select cat_id,goods_id,goods_name from goods where goods_id in(select max(goods_id) from goods \
group by cat_id);
```
取出每个栏目下最新的产品(`goods_id`唯一)。

### 2、from型子查询
**`把内层的查询结果供外层再次查询`**

用子查询查出挂科两门及以上的同学的平均成绩，思路：
```sql
#(1) 先查出哪些同学挂科两门以上
select name,count(*) as gk from stu where score < 60 having gk >=2;

#(2) 以上查询结果，我们只要名字就可以了，所以再取一次名字
select name from (select name,count(*) as gk from stu having gk >=2) as t;

#(3) 找出这些同学了，那么再计算他们的平均分
select name,avg(score) from stu where name in (select name from (select name,count(*) as gk \
from stu having gk >=2) as t) group by name;
```

### 3、exists型子查询
**`把外层查询结果拿到内层，看内层的查询是否成立`**

```sql
select cat_id,cat_name from category where exists(select * from goods where goods.cat_id = category.cat_id);
```
查询哪些栏目下有商品，栏目表`category`,商品表`goods`。

## 三、union的用法
把两次或多次 `SELECT` 的查询结果合并起来，要求查询的列数一致，推荐查询的对应的列类型一致，可以查询多张表，多次查询语句时如果列名不一样，则取第一次的列名！如果不同的语句中取出的行的每个列的值都一样，那么结果将自动会去重复，如果不想去重复则要加`all`来声明，即`union all`。

### 例子
现有表a如下

	id  num
	a    5
	b    10
	c    15
	d    10

表b如下

	id  num
	b    5
	c    10
	d    20
	e    99

求两个表中id相同的和：
```sql
select id,sum(num) from (select * from ta union select * from tb) as tmp group by id;
```
以上查询结果在本例中的确能正确输出结果，但是，如果把`tb`中的b的值改为`10`以查询结果的b的值就是`10`了，因为`ta`中的`b`也是`10`，所以`union`后会被过滤掉一个重复的结果，这时就要用`union all`。
```sql
select id,sum(num) from (select * from ta union all select * from tb) as tmp group by id;
```

取第4、5栏目的商品，按栏目升序排列，每个栏目的商品价格降序排列，用union完成：
```sql
select goods_id,goods_name,cat_id,shop_price from goods where cat_id=4 union \
select goods_id,goods_name,cat_id,shop_price from goods where cat_id=5 order by cat_id,shop_price desc;
```
如果子句中有`order by`需要用`()`包起来，但是推荐在最后使用`order by`，即对最终合并后的结果来排序。

取第3、4个栏目，每个栏目价格最高的前3个商品，结果按价格降序排列：
```sql
(select goods_id,goods_name,cat_id,shop_price from goods where cat_id=3 order by shop_price desc limit 3) \
union \
(select goods_id,goods_name,cat_id,shop_price from goods where cat_id=4 order by shop_price desc limit 3) \
order by shop_price desc;
```


## 四、左连接，右连接，内连接

- `INNER JOIN`(交集)：如果表中有至少一个匹配，则返回行。（默认，即等同于 `JOIN`）
- `LEFT  JOIN`(左集)：即使右表中没有匹配，也从左表返回所有的行。
- `RIGHT JOIN`(右集)：即使左表中没有匹配，也从右表返回所有的行。
- `FULL  JOIN`(并集)：只要其中一个表中存在匹配，则返回行。


现有表a有10条数据，表b有8条数据，那么表a与表b的笛尔卡积是多少？
```sql
select * from ta,tb   // 输出结果为8*10=80条
```

### 1、左连接
以`左表`为准，去`右表`找数据，如果没有匹配的数据，则以`null`补空位，所以`输出结果数>=左表原数据数`。

语法：
```sql
select n1,n2,n3 from ta left join tb on ta.n1 = ta.n2;
```
这里`on`后面的表达式，不一定为`=`，也可以`>`，`<`等算术、逻辑运算符。

连接完成后，可以当成一张新表来看待，运用where等查询。

```sql
select goods_id,goods_name,goods.cat_id,cat_name,shop_price from goods left join \
category on goods.cat_id = category.cat_id order by  shop_price desc limit 5;
```
取出价格最高的五个商品，并显示商品的分类名称。

### 2、右连接

`a left join b` 等价于 `b right join a`。

推荐使用`左连接`代替`右连接`。

语法：
```sql
select n1,n2,n3 from ta right join tb on ta.n1 = ta.n2;
```

### 3、内连接
查询结果是`左右连接的交集`，即左右连接的结果去除null项后的并集（去除了重复项）。

mysql目前还不支持`外连接`，即左右连接结果的并集,不去除null项。

语法：
```sql
select n1,n2,n3 from ta inner join tb on ta.n1 = ta.n2;
```

#### 例子
现有表a

	name  hot
	a     12
	b     10
	c     15

表b:

	name   hot
	d      12
	e      10
	f      10
	g      8

表a左连接表b，查询hot相同的数据：
```sql
select a.*,b.* from a left join b on a.hot = b.hot;
```
查询结果：

	name  hot   name   hot
	a     12     d     12
	b     10     e     10
	b     10     f     10
	c     15     null  null

从上面可以看出，查询结果表a的列都存在，表b的数据只显示符合条件的项目。

再如表b左连接表a，查询hot相同的数据：
```sql
select a.*,b.* from b left join a on a.hot = b.hot;
```
查询结果为：

	name  hot   name   hot
	d     12     a     12
	e     10     b     10
	f     10     b     10
	g     8      null  null

再如表a右连接表b，查询hot相同的数据：
```sql
select a.*,b.* from a right join b on a.hot = b.hot;
```
查询结果和上面的`b left join a`一样。

## 练习
查询商品的名称，所属分类，所属品牌：
```sql
select goods_id,goods_name,goods.cat_id,goods.brand_id,category.cat_name,brand.brand_name from goods \
left join category on goods.cat_id = category.cat_id \
left join brand on goods.brand_id = brand.brand_id limit 5;
```
理解：每一次连接之后的结果都可以看作是一张新表。

现创建如下表
```sql
create table m(
	id int,
	zid int,
	kid int,
	res varchar(10),
	mtime date
) charset utf8;

insert into m values
	(1,1,2,'2:0','2006-05-21'),
	(2,3,2,'2:1','2006-06-21'),
	(3,1,3,'2:2','2006-06-11'),
	(4,2,1,'2:4','2006-07-01');

create table t(tid int, tname varchar(10)) charset utf8;

insert into t values
	(1,'申花'),
	(2,'红牛'),
	(3,'火箭');
```
　　
要求按下面样式打印2006-0601至2006-07-01期间的比赛结果

样式：

	火箭   2:0    红牛  2006-06-11

查询语句为：
```sql
select zid,t1.tname as t1name,res,kid,t2.tname as t2name,mtime from m left join t as t1 on m.zid = t1.tid \
left join t as t2 on m.kid = t2.tid where mtime between '2006-06-01' and '2006-07-01';
```
总结：可以对同一张表连接多次，以分别取多次数据

---

From: http://www.cnblogs.com/rollenholt/archive/2012/05/15/2502551.html
