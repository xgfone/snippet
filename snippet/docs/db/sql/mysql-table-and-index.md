
Mysql建表与索引使用规范详解
=======================

## 规范

一、MySQL建表，字段需设置为非空，需设置字段默认值。

二、MySQL建表，字段需 `NULL` 时，需设置字段默认值，默认值不为 `NULL`。

三、MySQL建表，如果字段等价于外键，应在该字段加索引。

四、MySQL建表，不同表之间的相同属性值的字段，列类型，类型长度，是否非空，是否默认值，需保持一致，否则无法正确使用索引进行关联对比。

五、MySQL使用时，一条SQL语句只能使用一个表的一个索引。所有的字段类型都可以索引，多列索引的属性最多**`15`**个。

六、如果可以在多个索引中进行选择，MySQL 通常使用找到最少行的索引，索引唯一值最高的索引。

七、建立索引`index(part1,part2,part3)`,相当于建立了 `index(part1)`，`index(part1,part2)`和`index(part1,part2,part3)`三个索引。

八、MySQL针对`like`语法必须如下格式才使用索引：`SELECT * FROM t1 WHERE key_col LIKE 'ab%'；`。

九、`SELECT COUNT(*)`语法在没有`where`条件的语句中执行效率没有`SELECT COUNT(col_name)`快，但是在有`where`条件的语句中执行效率要快。

十、在`where`条件中多个`and`的条件中，必须都是一个多列索引的 key_part 属性而且必须包含 key_part1。各自单一索引的话，只使用遍历最少行的那个索引。

十一、在 `where` 条件中多个 `or` 的条件中，每一个条件，都必须是一个有效索引。

十二、`ORDER BY`后面的条件必须是同一索引的属性，排序顺序必须一致（比如都是升序或都是降序）。

十三、所有`GROUP BY`列引用同一索引的属性，并且索引必须是按顺序保存其关键字的。

十四、`JOIN`索引，所有匹配`ON`和`where`的字段应建立合适的索引。

十五、对智能的扫描全表使用`FORCE INDEX`告知MySQL，使用索引效率更高。

十六、定期`ANALYZE TABLE tbl_name`为扫描的表更新关键字分布 。

十七、定期使用慢日志检查语句，执行`explain`，分析可能改进的索引。

十八、条件允许的话，设置较大的`key_buffer_size`和`query_cache_size`的值（全局参数），和`sort_buffer_size`的值（session变量，建议不要超过4M）。


## 备注
### 主键的命名采用如下规则
主键名用`pk_`开头，后面跟该主键所在的表名。主键名长度不能超过**`30`**个字符。如果过长，可对表名进行缩写。缩写规则同表名的缩写规则。主键名用小写的英文单词来表示。

### 外键的命名采用如下规则
外键名用`fk_`开头，后面跟该外键所在的表名和对应的主表名（不含`t_`）。子表名和父表名自己用下划线（`_`）分隔。外键名长度不能超过**`30`**个字符。如果过长，可对表名进行缩写。缩写规则同表名的缩写规则。外键名用小写的英文单词来表示。

### 索引的命名采用如下规则
    (1) 索引名用小写的英文字母和数字表示。索引名的长度不能超过 30 个字符。
    (2) 主键对应的索引和主键同名。
    (3) 唯一性索引用 uni_ 开头，后面跟表名。一般性索引用 ind_ 开头，后面跟表名。
    (4) 如果索引长度过长，可对表名进行缩写。缩写规则同表名的缩写规则。

例: index 相关语法
```sql
------ 创建索引
-- 添加全文索引：
ALTER TABLE `table_name` ADD FULLTEXT `index_name` (`column_name`, ...)

-- 添加主键索引：
ALTER TABLE `table_name` ADD PRIMARY KEY [`index_name`] (`column_name`, ...)

-- 添加唯一索引：
ALTER TABLE `table_name` ADD UNIQUE [`index_name`] (`column_name`, ...)
CREATE UNIQUE INDEX `index_name` ON `table_name` (`column_name`, ...)

-- 添加普通索引：
ALTER TABLE `table_name` ADD INDEX `index_name` (`column_name`, ...)
CREATE INDEX `index_name` ON `table_name` (`column_name`, ...)

-- 如果被索引的列是字符串或文本类型，可以指定列名后设置被索引的长度，如 (userid, username(8))

------ 查看索引
SHOW INDEX FROM `table_name`;


------ 删除索引
DROP INDEX `index_name` ON `table_name`;
ALTER TABLE `table_name` DROP INDEX `index_name`；
ALTER TABLE `table_name` DROP PRIMARY KEY;
```

### SQL执行效率检测EXPLAIN
`explain`显示了 mysql 如何使用索引来处理`select`语句以及连接表。可以帮助选择更好的索引和写出更优化的查询语句。

#### 使用方法
在`select`语句前加上`explain`就可以了，如：
```sql
explain select surname,first_name form a,b where a.id=b.id;
```

#### 分析结果形式如下
```
table |  type | possible_keys | key | key_len  | ref | rows | Extra
```

**_EXPLAIN列的解释_**

##### table
    显示这一行的数据是关于哪张表的。

##### type
    这是重要的列，显示连接使用了何种类型。
    从最好到最差的连接类型为 const、eq_reg、ref、range、indexhe 和 ALL。

见下文“**_不同连接类型的解释_**”。

##### possible_keys
    显示可能应用在这张表中的索引。如果为空，没有可能的索引。可以为相关的域从 WHERE 语句中选择一个合适的语句。

##### key
    实际使用的索引。如果为 NULL，则没有使用索引。很少的情况下，MYSQL 会选择优化不足的索引。
    这种情况下，可以在 SELECT 语句中使用 USE INDEX(indexname) 来强制使用一个索引或者用 IGNORE INDEX(indexname)
    来强制MYSQL忽略索引。

##### key_len
    使用的索引的长度。在不损失精确性的情况下，长度越短越好。

##### ref
    显示索引的哪一列被使用了，如果可能的话，是一个常数。

##### rows
    MYSQL 认为必须检查的用来返回请求数据的行数。

##### Extra
    关于 MYSQL 如何解析查询的额外信息。
    坏的例子有 Using temporary 和 Using filesort，意思 MYSQL 根本不能使用索引，结果是检索会很慢。

**EXPLAIN列返回的描述的意义**

Distinct

    一旦 MYSQL 找到了与行相联合匹配的行，就不再搜索了。

Not exists

    MYSQL 优化了 LEFT JOIN，一旦它找到了匹配 LEFT JOIN 标准的行，就不再搜索了。
        Range checked for each
        Record（index map:#）
    没有找到理想的索引，因此对于从前面表中来的每一个行组合，MYSQL 检查使用哪个索引，并用它来从表中返回行。
    这是使用索引的最慢的连接之一。

Using filesort

    看到这个的时候，查询就需要优化了。MYSQL 需要进行额外的步骤来发现如何对返回的行排序。
    它根据连接类型以及存储排序键值和匹配条件的全部行的行指针来排序全部行。

Using index

    列数据是从仅仅使用了索引中的信息而没有读取实际的行动的表返回的，这发生在对表的全部的请求列都是同一个索引的部分的时候。

Using temporary

    看到这个的时候，查询需要优化了。
    这里，MYSQL 需要创建一个临时表来存储结果，这通常发生在对不同的列集进行 ORDER BY 上，而不是 GROUP BY 上。

Where used

    使用了 WHERE 从句来限制哪些行将与下一张表匹配或者是返回给用户。
    如果不想返回表中的全部行，并且连接类型 ALL 或 index，这就会发生，或者是查询有问题。

#### 不同连接类型的解释
以下按照效率高低的顺序排序。

##### system
    表只有一行：system 表。这是 const 连接类型的特殊情况。

##### const
    表中的一个记录的最大值能够匹配这个查询（索引可以是主键或惟一索引）。
    因为只有一行，这个值实际就是常数，因为 MYSQL 先读这个值然后把它当做常数来对待。

##### eq_ref
    在连接中，MYSQL在查询时，从前面的表中对每一个记录的联合都从表中读取一个记录，它在查询使用了索引为主键或惟一键的全部时使用。

##### ref
    这个连接类型只有在查询使用了不是惟一或主键的键或者是这些类型的部分（比如，利用最左边前缀）时发生。
    对于之前的表的每一个行联合，全部记录都将从表中读出。
    这个类型严重依赖于根据索引匹配的记录多少—越少越好。

##### range
    这个连接类型使用索引返回一个范围中的行，比如使用 > 。

## FAQ

表中包含 10 万条记录，有一个 datetime 类型的字段。取数据的语句：
```sql
SELECT * FROM my_table WHERE created_at < '2010-01-20';
```
用 EXPLAIN 检查，发现 type 是 ALL， key 是 NULL，根本没用上索引。可以确定的是，created_at 字段设定索引了。

什么原因呢？

用 `SELECT COUNT(*)` 看了一下符合 WHERE 条件的记录总数，居然是 6W 多条！！

难怪不用索引，这时用索引毫无意义，就好像 10 万条记录的用户表，有个性别字段，不是男就是女，在这种字段设置索引是错误的决定。

稍微改造一下上述语句：
```sql
SELECT * FROM my_table WHERE created_at BETWEEN '2009-12-06' AND '2010-01-20';
```
这回问题解决！

符合条件的记录只有几百条，EXPLAIN 的 type 是 range，key 是 created_at，Extra 是 Using where 。

自己总结个准则，**_索引的目的就是尽量缩小结果集_**，这样才能做到快速查询。

6万条记录符合条件，已经超出总记录数的一半，这时索引已经没有意义了，因此 MySQL 放弃使用索引。

这与设置 gender 字段，并加上索引的情况相似，当你要把所有男性记录都选取出来，符合条件的记录数约占总数的一半，MySQL 同样不会使用这个索引。

    唯一值越多的字段，使用索引的效果越好。
    设置联合索引时，唯一值越多的，越应该放在“左侧”。

---

From: http://www.jb51.net/article/39198.htm
