---
title:  mysql的各种锁
description: 深入理解mysql的各种锁，深度好文，一文搞懂mysql常用的各种锁，及其范围。
image: 1.png
date: 2025-07-20
slug: mysql-Lock
categories: 
  - 精选
  - mysql
tags:
  - mysql
  - 锁
---



# mysql的各种锁





## 表锁（元数据锁的一种）

锁整个表，主要由MyISAM、MEMORY等存储引擎使用。由Mysql提供。

> 上锁方式与表名息息相关，如果上锁时使用别名，那所有的操作都需要通过相同别名才有效。（原名称或其他别名访问上表锁数据，则无锁）

表级锁的优点是实现简单，性能开销小，但并发性较低，因为整个表被锁定，可能会导致其他会话等待。



### 读锁（READ LOCK)

> 允许当前事务和其他事务读取表，但禁止事务写入操作。



- 锁定范围：整个表，所有行和操作均受影响
- 使用场景：适合保护整表数据一致性的读操作，例如报表生成。
- 限制：读锁情况下，其他会话无法insert、update或Delete操作



#### 坑（重点）

1. 使用lock指令上读锁后，会话也只能访问被读锁锁定的表，其他表无法访问：

``` mysql
mysql> LOCK TABLES t1 READ;
mysql> SELECT COUNT(*) FROM t1;
+----------+
| COUNT(*) |
+----------+
|        3 |
+----------+
mysql> SELECT COUNT(*) FROM t2;
ERROR 1100 (HY000): Table 't2' was not locked with LOCK TABLES
```



2. 使用别名上锁时，也只能锁定别名单独的锁

``` mysql
mysql> LOCK TABLE t WRITE, t AS t1 READ;
mysql> INSERT INTO t SELECT * FROM t;
ERROR 1100: Table 't' was not locked with LOCK TABLES
mysql> INSERT INTO t SELECT * FROM t AS t1;
```

第一个 [`INSERT`](https://dev.mysql.com/doc/refman/8.0/en/insert.html) 发生错误，因为有两个 对锁定表的相同名称的引用。第二个 [`INSERT`](https://dev.mysql.com/doc/refman/8.0/en/insert.html) 成功，因为 对表的引用使用不同的名称。





### 写锁(WRITE LOCK)

> 允许当前会话独占表，禁止其他会话读取或写入。（**当前会话可以写入数据**）



- 锁定范围：整个表，所有操作均被阻塞
- 使用场景：适合需独占访问批量操作，如数据导入或表结构修改。

<font color='red'>写锁会隐式提交当前事务，不是事务安全的</font>



## 行锁（InnoDB锁）

> InnoDB的核心特性，支持更高的并发，允许多个事务同时操作不同行。

> 参考mysql[官方说明文档](https://dev.mysql.com/doc/refman/8.0/en/innodb-locking.html)





### 共享锁(Shared Lock，S Lock)

> 允许多个事务同时读取同一行（<font color='red'>与读锁并不是同一个锁，上锁范围根据where语句有关，一般会锁定固定的行</font>），但禁止任务事务写入。



- 锁定范围，特定行，仅影响被锁定的行。
- 适用场合：读取操作需要保护数据的一致性，但允许并发读取。

``` sql
SELECT ... LOCK IN SHARE MODE
```



### 排他锁（Exclusive Lock，X Lock）

> 允许一个事务写入特定的行，禁止其他事务读取或写入。



- 锁定范围：特定的行，仅影响被锁定的行。
- 适用场景：写入操作需要独占访问。分布式开始上锁。



``` sql
SELECT ... FOR UPDATE或UPDATE/DELETE语句自动获取。
```





### 意向锁（Intention Locks）

> 意向共享锁IS ，意向排他锁IX 

表示事务打算在表中的某些行上获取共享锁或排他锁

- 锁定范围：整个表，但只表示意图，不锁定具体行。
- 所用：用来协调表级锁和行级锁的兼容性。





- 意向锁与其他锁是否冲突

|      | `X`  | `IX` | `S`  | `IS` |
| :--- | :--- | :--- | :--- | ---- |
| `X`  | 冲突 | 冲突 | 冲突 | 冲突 |
| `IX` | 冲突 | 相容 | 冲突 | 相容 |
| `S`  | 冲突 | 冲突 | 相容 | 相容 |
| `IS` | 冲突 | 相容 | 相容 | 相容 |



``` sql
TABLE LOCK table `test`.`t` trx id 10080 lock mode IX
```



### 记录锁（Record Lock）

> 锁定一个特定的索引记录<font color='red'>**注意上锁范围为索引，可能是聚簇索引，也可以是普通索引**</font>



- 锁定范围：特定的索引记录，如：SELECT c1 FROM t WHERE c1 = 10 FOR UPDATE;会锁定c1=10的行。
- 使用场景：精确锁定特定的行

> 后续会详细详细讲解锁定方式等





### 间隙锁（Gap Lock）

锁定索引之间的间隙，防止其他事务插入新行，保护数据一致性。

<font color='red'>**读已提交级别禁用间隙锁，只有在可重复读级别存在**</font>

- 锁定范围：索引记录间的间隙，例如索引值10和11之间的间隙（并不会锁定特定的行）



### Next-Key Lock

记录锁和间隙锁的组合，及锁定一个索引记录，也锁定该记录前面的间隙。

- 上锁范围：一个索引及其前面的间隙，<font color='red'>**左开又必，一定是间隙锁在前，记录锁在后。(negative infinity, 10]**</font>

- 可重复读级别下可以方式幻读。



### 插入意向锁（Insert Intention Lock）

在插入操作时，表示事务打算插入一个新行

- 锁定范围：插入位置的间隙，允许多个事务并发插入非冲突行。**<font color='red'>如果是冲突行，会阻塞后插入的行</font>**

- 作用：提高插入操作的并发性。





### AUTO-INC锁

处理表中AUTO_INCREMENT列的自增ID分配。

- 锁定范围：整个表
- 使用场景：确保自增ID的唯一性和顺序性。



## mysql各种锁实战（重点）

> 教你如何查看各种锁信息，以及一些使用的tips

![1753022340387.png](https://fastly.jsdelivr.net/gh/thecoolboyhan/th_blogs@main/image/2025-07/1753022340387_1753022340407.png)



### 读锁

1. 使用lock指令上读锁后，会话也只能访问被读锁锁定的表，其他表无法访问：

``` mysql
mysql> LOCK TABLES t1 READ;
mysql> SELECT COUNT(*) FROM t1;
+----------+
| COUNT(*) |
+----------+
|        3 |
+----------+
mysql> SELECT COUNT(*) FROM t2;
ERROR 1100 (HY000): Table 't2' was not locked with LOCK TABLES
```



2. 使用别名上锁时，也只能锁定别名单独的锁

``` mysql
mysql> LOCK TABLE t WRITE, t AS t1 READ;
mysql> INSERT INTO t SELECT * FROM t;
ERROR 1100: Table 't' was not locked with LOCK TABLES
mysql> INSERT INTO t SELECT * FROM t AS t1;
```

第一个 [`INSERT`](https://dev.mysql.com/doc/refman/8.0/en/insert.html) 发生错误，因为有两个 对锁定表的相同名称的引用。第二个 [`INSERT`](https://dev.mysql.com/doc/refman/8.0/en/insert.html) 成功，因为 对表的引用使用不同的名称。



### 行锁、间隙锁和Next-Key锁实战



初始表结构z及其数据如下

![1753014382673.png](https://fastly.jsdelivr.net/gh/thecoolboyhan/th_blogs@main/image/2025-07/1753014382673_1753014382692.png)

模拟两个事务进行锁竞争：

A事务执行如下语句

```sql
select *
from z where b=3 for update ;
```

利用普通索引B，锁住b=3的排他锁

B事务尝试测试A事务对此表的锁定范围



#### 读已提交



- B事务尝试避开索引b，在锁定数据前插入数据：

```sql
insert into z value (4,2);
```

> 可以正常提交，未上锁



- B事务尝试使用相同值b=3，插入数据：

```sql
insert into z value (4,3);
```

> 可以正常提交



- 利用普通索引的等值排他锁，结论

```sql
select *
from z where b=3 for update ;
```

就算事务A通过普通索引来对b=3加锁，但读已提交隔离级别下。InnoDB并<font color='red'>**不会对二级索引上锁，而是在第一次上锁时，通过二级索引确定具体会锁聚簇索引的某几行。一旦锁定行数确定，后续就算其他事务以相同条件的二级索引插入数据，也不会有锁冲突。**</font>



- 如果上锁时的条件为范围呢？



A事务执行如下语句，通过普通索引给B>=3的数据上锁：

```sql
select *
from z where b>=3 for update ;
```



B事务尝试插入b=4的数据

```sql
insert into z value (6,4);
```

> 可以正常提交，无锁。



B事务尝试修改a=7的数据

```sql
update z set b=5 where a=7;
```

> 数据被锁定，无法提交。



- 结论

就算是通过二级索引b>=3条件上锁，依然也只会在上锁时确认具体的行，并对具体的行加锁，后续就算有b=3，或b>3的数据插入也不会有影响。





- 尝试锁定主键的范围呢

事务A修改上锁条件，尝试通过主键a>=5来上锁

```sql
select *
from z where a>=5 for update ;
```

B事务尝试插入满足a>=5的数据：

```sql
insert into z value (6,3);
```

> 可以正常提交，无锁。



- 结论

在读已提交隔离级别下，就算尝试通过主键范围上锁，也只能在上锁时锁定具体的行，后续其他事务插入上锁时满足条件的新行，也不会被阻塞。

> 所以读已提交情况下，只会通过主键索引来上锁，不会锁定二级索引，就算上锁时条件是二级索引，也只会被转换成锁定满足条件的主键索引。



#### 可重复读

还是之前的数据，**测试前一定要清除之前的数据**

``` sql
-- 创建表 z
CREATE TABLE z (
    a INT PRIMARY KEY,
    b INT,
    INDEX idx_b (b)
) ENGINE=InnoDB;

-- 插入数据
INSERT INTO z (a, b) VALUES
(1, 1),
(3, 1),
(5, 3),
(7, 6),
(10, 8);
```



![1753014382673.png](https://fastly.jsdelivr.net/gh/thecoolboyhan/th_blogs@main/image/2025-07/1753014382673_1753014382692.png)

现在尝试在可重复读的情况下，再做一遍上次的操作



- 通过二级索引来上锁

事务A锁定b=3的二级索引

```sql
select *
from z where b=3 for update ;
```

事务B尝试在数据之前插入

```sql
insert into z value (4,2);
```

> 无法提交，被锁定

事务B修改数据重新插入

```sql
insert into z value (6,4)
```

> 无法提交，被锁定

事务B尝试插入数据

```sql
insert into z value (2,2);
```

> 无法提交，被锁定

事务B尝试插入数据

```sql
insert into z value (8,6);
```

> 成功，无锁



- 分析

通过如下语句获取事务A锁定的具体的行

``` sql
SELECT INDEX_NAME,LOCK_MODE,LOCK_STATUS,LOCK_DATA FROM performance_schema.data_locks;
```



输出信息如下：

| INDEX_NAME | LOCK_MODE     | LOCK_STATUS | LOCK_DATA |
| ---------- | ------------- | ----------- | --------- |
| NULL       | IX            | GRANTED     | NULL      |
| b          | X,GAP         | GRANTED     | 6, 7      |
| b          | X             | GRANTED     | 3, 5      |
| PRIMARY    | X,REC_NOT_GAP | GRANTED     | 5         |



<font color='red'> 首先搞清楚，通过二级索引上锁时，数据是按照二级索引来排序的。（不是按照主键来排序的）。如果二级索引相同的值，则再按照主键排序。</font>



1. 意向排他锁，锁定具体表，但并不冲突
2. 第二行的x,GAP锁：间隙锁，锁定b=6，a=7到上一个数据之前的间隙，<font color='red'>b=6,a=7数据本身没有被锁定，可以修改</font>
3. 第三行x：Next-Key锁，锁定范围为：b=3，a=5数据本身，和它前面的一条数据的间隙（不包含前面的数据），也就是（b=1,a=3）之后的间隙。<font color='red'>a=3的数据本身可以被修改，但无法修改b>=2||b<=6的数据，因为都满足Next-Key锁的范围或GAP锁的范围</font>
4. 第四行X,REC_NOT_GAP：普通行锁，上锁范围为主键索引a=5，表示5这行数据本身被锁定





- 但是有特殊情况

为什么要在做本次实验前先清楚表中数据重新插入？

因为如果不删除，第一次实验时：插入的数据及时后续被删除，依然会影响上锁范围。导致锁有问题。

可见，<font color='red'>在读已提交的隔离级别下，GAP和Next-Key锁并不稳定，被删除的数据可能会影响上锁的范围。</font>





- 通过主键上锁

```sql
select *
from z where a=5 for update ;
```

通过锁分析语句分析

```sql
SELECT INDEX_NAME,LOCK_MODE,LOCK_STATUS,LOCK_DATA FROM performance_schema.data_locks;
```



| INDEX_NAME | LOCK_MODE     | LOCK_STATUS | LOCK_DATA |
| ---------- | ------------- | ----------- | --------- |
| NULL       | IX            | GRANTED     | NULL      |
| PRIMARY    | X,REC_NOT_GAP | GRANTED     | 5         |

只会在固定a=5行来上锁。



- 总结



**<font color='red'>在可重复读隔离级别下，通过二级索引上锁，数据会按照二级索引+主键索引的情况排序。即使只是通过排他锁锁定固定值的二级索引。</font>**



**<font color='red'>InnoDB也会在锁定值前：上一个Next-Key锁，锁定范围为上一条数据（不包含），到本条数据。</font>**



**<font color='red'>在锁定值后：上一个GAP间隙锁，锁定范围为指定值到下一条数据（不包含）的间隙。</font>**

<font color='red'>注意，这里提到的上一条数据和下一条数据包括曾经被删除但没有被整理的数据。所以在可重复读下，二级索引上锁并不稳定。</font>



**所以推荐，可重复读隔离级别下，劲量只通过主键索引来上锁，不要通过二级索引上锁，否则会导致上锁范围收到影响。**



## 蛇足



- 表级的意向排它锁（IX）：lock mode IX。
- 表级的插入意向锁（LOCK_INSERT_INTENTION）: lock_mode X locks gap before rec insert intention
- 行级的记录锁（LOCK_REC_NOT_GAP）: lock_mode X locks rec but not gap
- 行级的间隙锁（LOCK_GAP）: lock_mode X locks gap before rec
- 行级的 Next-key 锁（LOCK_ORNIDARY）: lock_mode X



**在「读未提交」隔离级别下，读写操作可以同时进行，但写写操作无法同时进行。与此同时，该隔离级别下只会使用行级别的记录锁，并不会用间隙锁。**



**在「可重复读」隔离级别下，使用了记录锁、间隙锁、Next-Key 锁三种类型的锁。**

**可重复读存在幻读的问题，但实际上在 MySQL 中，因为其使用了间隙锁，所以在「可重复读」隔离级别下，可以通过加 锁解决幻读问题。因此，MySQL 将「可重复读」作为了其默认的隔离级别。**


- 不同版本如何查看各种锁信息

| 方法                              | MySQL 5.6 | MySQL 5.7 | MySQL 8.0 | MySQL 8.4 | 注意事项                         |
|-----------------------------------|-----------|-----------|-----------|-----------|----------------------------------|
| SHOW ENGINE INNODB STATUS         | ✅        | ✅        | ✅        | ✅        | 需启用 innodb_status_output_locks |
| SHOW PROCESSLIST                  | ✅        | ✅        | ✅        | ✅        | 显示线程状态，非锁详情            |
| SHOW OPEN TABLES                  | ✅        | ✅        | ✅        | ✅        | 适合 MyISAM 表锁                 |
| INNODB_LOCKS/WAITS                | ✅        | ✅        | 废弃      | 废弃      | MySQL 8.0.1 起用 data_locks      |
| INNODB_TRX                        | ✅        | ✅        | ✅        | ✅        | 查看活跃事务                     |
| performance_schema.data_locks     | ❌        | ❌        | ✅        | ✅        | 需启用 Performance Schema        |
| performance_schema.metadata_locks | ❌        | ✅        | ✅        | ✅        | 适合元数据锁和用户锁             |
| IS_USED_LOCK                      | ✅        | ✅        | ✅        | ✅        | 查看 GET_LOCK 锁                |
