---
title:  mysql的各种锁
description: 深入理解mysql的各种锁
image: 1.png
date: 2025-04-18
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

