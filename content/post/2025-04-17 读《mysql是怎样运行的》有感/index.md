---
title:  读《mysql是怎样运行的》有感
description: 感觉是读过最好的mysql书籍
image: 1.png
date: 2025-04-17
categories: 
  - 精选
  - mysql
tags:
  - mysql
  - book
  - 读后感
---

> 1111

# 读《mysql是怎样运行的》有感







> 粗略了解mysql， 模拟一条查询的过程。
>
> 介绍主流的存储引擎

## 第一章、重新认识mysql

### 一条sql会经历的阶段

1. 查询缓存：（8.0后删除）是否可以从缓存中直接得到答案
2. 语法解析：（编译过程）翻译sql语句
3. 查询优化：转换sql，生成执行计划（是否走索引等）
4. 存储引擎：交给存储引擎去真正执行查询



- 查询缓存在什么时候会失效？(mysql 8.0之后删除查询缓存)

如果两个查询请求在任何字符上的不同（如：空格、注释、大小写），都会导致缓存不会命中。如果查询请求中包含某些系统函数、用户自定义变量和函数、一些系统表，如mysql 、information_schema、performance_schema 数据库中的表，那这个请求就不会被缓存。



### 常见的存储引擎



- 常见的存储引擎

| 存储引擎  | 描述                                 |
| --------- | ------------------------------------ |
| ARCHIVE   | 用于数据存档（行被插入后不能再修改） |
| BLACKHOLE | 丢弃写操作，读操作会返回空内容       |
| CSV       | 在存储数据时，以逗号分隔各个数据项   |
| FEDERATED | 用来访问远程表                       |
| InnoDB    | 具备外键支持功能的事务存储引擎       |
| MEMORY    | 置于内存的表                         |
| MERGE     | 用来管理多个MyISAM表构成的表集合     |
| MyISAM    | 主要的非事务处理存储引擎             |
| NDB       | MySQL集群专用存储引擎                |



- 各功能支持情况

| feature                                            | **MyISAM** | **Memory** | **InnoDB** | **Archive** | **NDB** |
| -------------------------------------------------- | ---------- | ---------- | ---------- | ----------- | ------- |
| B-tree indexes 索引                                | Yes        | yes        | yes        | no          | no      |
| Backup/point-in-time recovery 时间镜像备份         | yes        | yes        | yes        | yes         | yes     |
| Cluster database support 集群                      | no         | no         | no         | no          | Yes     |
| Clustered indexes 聚簇索引                         | no         | no         | yes        | no          | no      |
| Compressed data 数据压缩                           | yes        | no         | yes        | yes         | no      |
| Data caches 数据缓存                               | No         | N/A        | Yes        | no          | yes     |
| Encrypted data 数据加密                            | yes        | yes        | yes        | yes         | yes     |
| Foreign key support 外键                           | no         | no         | yes        | no          | yes     |
| Full-text search indexes 全文搜索索引              | Yes        | no         | yes        | no          | no      |
| Geospatial data type support 空间数据类型支持      | yes        | no         | yes        | yes         | yes     |
| Geospatial indexing support 空间索引支持           | yes        | no         | yes        | no          | no      |
| Hash indexes 哈希索引                              | no         | yes        | no         | no          | yes     |
| Index caches 索引缓存                              | yes        | N/A        | yes        | no          | yes     |
| Locking granularity 锁粒度                         | Table      | Table      | Row        | Row         | Row     |
| MVCC 多版本并发控制                                | no         | no         | yes        | no          | no      |
| Query cache support 查询缓存                       | yes        | yes        | yes        | yes         | yes     |
| Replication support 主从复制                       | yes        | Limited    | yes        | yes         | yes     |
| Storage limits 存储限制                            | 256TB      | RAM        | 64TB       | None        | 384EB   |
| T-tree indexes T-tree索引                          | no         | no         | no         | no          | yes     |
| Transactions 事务                                  | no         | no         | yes        | no          | yes     |
| Update statistics for data dictionary 更新数据字典 | yes        | yes        | yes        | yes         | yes     |



> 可以为不同的表设置不同的存储引擎





> 从InnoDB行记录的角度理解一行数据是如何存储的



## 第四章、InnoDB记录结构



- InnoDB的存储方式

将数据划分成若干个页，以页作为磁盘和内存之间交互的基本单位，InnoDB中页的大小一般为16KB。



- 四种行格式

| 行格式     | 紧凑的存储特性 | 增强的可变长度列存储 | 大型索引键前缀支持 | 压缩支持 | 支持的表空间类型         |
| ---------- | -------------- | -------------------- | ------------------ | -------- | ------------------------ |
| REDUNDANT  | 否             | 否                   | 否                 | 否       | 系统，每个表的文件，一般 |
| COMPACT    | 是的           | 否                   | 否                 | 否       | 系统，每个表的文件，一般 |
| DYNAMIC    | 是的           | 是的                 | 是的               | 否       | 系统，每个表的文件，一般 |
| COMPRESSED | 是的           | 是的                 | 是的               | 是的     | 文件每表，一般           |



### **COMPACT**行格式

![1744855104065.png](https://fastly.jsdelivr.net/gh/thecoolboyhan/th_blogs@main/image/2025-04/1744855104065_1744855104091.png)



#### 记录的额外信息

> 服务器为了描述这条记录而不得不额外添加的信息。



#### 变长字段长度列表

> 变长字段的长度不是固定的，所以在存储时，需要占用两部分空间

1. 真正的数据内容
2. 占用的字节数

把所有变长字段的真实数据数据占用的字节长度都存放在记录的开头部位，从而形成一个变长字段长度列表，各变长字段占用的字节数按照列的顺序 <font color='red'>**逆序 **</font> 存放。



<font color='red'>  **如果该可变字段允许存储的最大字节数（ M×W ）超过255字节并且真实存储的字节数（ L ）超过127字节，则使用2个字节，否则使用1个字节。**</font>



> 变长字段长度列表中只存储值为非NULL的列内容占用的长度，值为NULL的列的长度是不需要存储的。



#### NULL值列表

COMPACT行格式会把这些值为NULL的列统一管理起来。

1. 首先统计表中允许存储NULL的列有哪些
2. 如果表中没有允许存储NULL的列，则NULL值列表也不存在了
3. mysql规定NUll列表必须用整数个字节的位表示，如果使用的二进制位个数不是整数个字节，则字节的高位补0.（8bit）



#### 记录头信息

> 用于描述记录的记录头信息




| 名称         | 大小（单位：bit） | 描述                                                         |
| ------------ | ----------------- | ------------------------------------------------------------ |
| 预留位1      | 1                 | 没有使用                                                     |
| 预留位2      | 1                 | 没有使用                                                     |
| delete_mask  | 1                 | 标记该记录是否被删除                                         |
| min_rec_mask | 1                 | B+树的每层非叶子节点中的最小记录都会添加该标记               |
| n_owned      | 4                 | 表示当前记录拥有的记录数                                     |
| heap_no      | 13                | 表示当前记录在记录堆的位置信息                               |
| record_type  | 3                 | 表示当前记录的类型，0 表示普通记录，1 表示B+树非叶子节点记录，2 表示最小记录，3 表示最大记录 |
| next_record  | 16                | 表示下一条记录的相对位置                                     |



#### 记录的真实数据

真实存储的数据，除了这些数据外，mysql还会默认生成以下列：



- mysql隐藏列

| 列名           | 是否必须                     | 占用空间 | 描述                   |
| -------------- | ---------------------------- | -------- | ---------------------- |
| row_id         | 否（InnoDB指定主键时才存在） | 6 字节   | 行ID，唯一标识一条记录 |
| transaction_id | 是                           | 6 字节   | 事务ID                 |
| roll_pointer   | 是                           | 7 字节   | 回滚指针               |



- <font color='red'>mysql主键的生成策略</font>

优先使用用户自定义主键作为主键，如果用户没有定义主键，则选取一个Unique键作为主键，如果连Unique键都没有，则InnoDB会为表添加一个名为row_id的隐藏列作为主键。



### 行溢出数据

varchar最多可以占用65535个字节，除了BLOB或者TEXT类型的列之外，其他所有的列占用字节长度加起来不能超过65535个字节。



mysql一页大小为16kb，也就是16384字节。对于占用空间非常大的也，真实数据区域只会存储该列的一部分数据，把剩余数据分散存储到其他的也中。

>  不只是 ***VARCHAR(M)*** 类型的列，其他的 ***TEXT***、***BLOB*** 类型的列在存储数据非常多的时候也会发生 行溢出 







> 解释InnoDB一页数据是如何存放的

## 第五章、InnoDB数据页结构





![1744855192735.png](https://fastly.jsdelivr.net/gh/thecoolboyhan/th_blogs@main/image/2025-04/1744855192735_1744855192753.png)



| 名称               | 中文名             | 占用空间大小 | 简单描述                 |
| ------------------ | ------------------ | ------------ | ------------------------ |
| File Header        | 文件头部           | 38 字节      | 页的一些通用信息         |
| Page Header        | 页面头部           | 56 字节      | 数据页专有的一些信息     |
| Infimum + Supremum | 最小记录和最大记录 | 26 字节      | 两个虚拟的行记录         |
| User Records       | 用户记录           | 不确定       | 实际存储的行记录内容     |
| Free Space         | 空闲空间           | 不确定       | 页中尚未使用的空间       |
| Page Directory     | 页面目录           | 不确定       | 页中的某些记录的相对位置 |
| File Trailer       | 文件尾部           | 8 字节       | 校验页是否完整           |



### 记录头信息





| 名称         | 大小 (单位: bit) | 描述                                                         |
| ------------ | ---------------- | ------------------------------------------------------------ |
| 预留位1      | 1                | 没有使用                                                     |
| 预留位2      | 1                | 没有使用                                                     |
| delete_mask  | 1                | 标记该记录是否被删除                                         |
| min_rec_mask | 1                | B+树的每层非叶子节点中的最小记录都会添加该标记               |
| n_owned      | 4                | 表示当前记录拥有的记录数                                     |
| heap_no      | 13               | 表示当前记录在记录堆的位置信息                               |
| record_type  | 3                | 表示当前记录的类型：0-普通记录，1-B+树非叶节点记录，2-最小记录，3-最大记录 |
| next_record  | 16               | 表示下一条记录的相对位置                                     |



- delete_mask

> 标记当前记录是否被删除

被删除的数据会被标记，并放入一个*垃圾链表* ，链表中的记录占用的空间是可重用空间。

- next_record

>  从当前记录的真实数据到下一条记录的真实数据地址偏移量。



<font color='red'>下一条记录： </font>

指得并不是按照我们插入顺序的下一条记录，而是按照主键值由小到大的顺序的下一条记录。



***Infimum\*****记录（也就是最小记录）** 的下一条记录就是本页中主键值最小的用户记录，而本页中主键值最大的用户记录的下一条记录就是 ***Supremum\*****记录（也就是最大记录）**。



- 模拟删除一条记录

原记录：

![1744855231499.png](https://fastly.jsdelivr.net/gh/thecoolboyhan/th_blogs@main/image/2025-04/1744855231499_1744855231519.png)



删除第二条数据：

![1744855254240.png](https://fastly.jsdelivr.net/gh/thecoolboyhan/th_blogs@main/image/2025-04/1744855254240_1744855254257.png)



不论我们怎样对页中的记录做增删改操作，InnoDB始终维护一条记录的单链表，链表中的各个节点是按照主键值由小到大连接起来的。



再插入一条记录：

![1744855310294.png](https://fastly.jsdelivr.net/gh/thecoolboyhan/th_blogs@main/image/2025-04/1744855310294_1744855310312.png)



### 蛇足



- 查询



InnoDB会把页中的记录划分为若干个组，每个组的最后一个记录的地址偏移量作为一个槽，存放在page Directory中，所以在一页中根据主键去查找记录非常快：

1. 通过二分查找确定记录所在的槽
2. 通过记录的next_rocord属性遍历该槽所在的组中的各个记录。（通过偏移量直接定位地址）





- 存储方式

每个数据页的fileHeader部分都有上一个和下一个页的编号，所以所有的数据页会组成一个双链表。



- 如何确保数据完整

为了保证数据的完整性，页的首部和尾部都会存储页中数据的校验和，和页面最后修改时的LSN值。如果两个校验不通过，表示数据同步过程中出现了问题。








> InnoDB的索引结构

## 第六章B+树索引



### 索引方案



复用存储用户记录的数据页来存储目录项。通过record_type来区分。



![1744855340206.png](https://fastly.jsdelivr.net/gh/thecoolboyhan/th_blogs@main/image/2025-04/1744855340206_1744855340223.png)



1. 索引页的record_type值为1，用户记录的record_type值为0
2. 索引页记录只有主键值和页的编号两列，用户记录是用户自己定义的。



- 如何根据主键值查找

1. 先到存储索引记录的页，通过二分查找快速定位到对应的目录项。如定位到记录在页9
2. 通过偏移量找到页9，在通过二分查找找到对应的记录。



- 数据结构

![1744855362514.png](https://fastly.jsdelivr.net/gh/thecoolboyhan/th_blogs@main/image/2025-04/1744855362514_1744855362530.png)

用户的记录都存放在B+树的最底层的节点上，其他的非叶子节点用来存储目录（索引页）



- 我们大概需要多少层数据？



1、如果 B+ 树只有1层，也就是只有1个用于存放用户记录的节点，最多能存放 100 条记录。

2、如果 B+ 树有2层，最多能存放 1000×100=100000 条记录。

3、如果 B+ 树有3层，最多能存放 1000×1000×100=100000000 条记录。

4、如果 B+ 树有4层，最多能存放 1000×1000×1000×100=100000000000 条记录。



### 聚簇索引

> InnoDB的数据默认使用聚簇索引来存储。<font color='red'>索引即数据，数据即索引</font>。

#### 聚簇索引的特点：



- 使用记录主键值的大小进行记录和页的排序
  - 页内的记录按照主键的大小顺序排成一个单向链表
  - 存放用户记录的页是根据也中用户记录的主键大小排成一个双向链表
  - 存放目录项记录的页分为不同的层次，同一层中的页是根据目录项页中的主键大小顺序排成的一个双向链表
- B+树的叶子节点存储完整的用户记录



### 二级索引

>  用户根据自己的规则给非主键值建立的索引。

同样使用B+树来存储，不过叶子节点用来存储的是主键值，而不是完整的用户记录。

所以想要通过二级索引来查询一条记录，需要先在二级索引上搜索出主键值。

<font color='red'>再根据主键值去聚簇索引中再查找一遍完整的用户记录（回表）</font>



### 总结



- 每个索引都对应一棵 B+ 树， B+ 树分为好多层，最下边一层是叶子节点，其余的是内节点。所有 用户记录都存储在 B+ 树的叶子节点，所有 目录项记录 都存储在内节点。



- InnoDB 存储引擎会自动为主键（如果没有它会自动帮我们添加）建立 聚簇索引 ，聚簇索引的叶子节点包含完整的用户记录。



- 我们可以为自己感兴趣的列建立 二级索引 ， 二级索引 的叶子节点包含的用户记录由 索引列 + 主键 组成，所以如果想通过 二级索引 来查找完整的用户记录的话，需要通过 回表 操作，也就是在通过 二级索引找到主键值之后再到 聚簇索引 中查找完整的用户记录。



- B+ 树中每层节点都是按照索引列值从小到大的顺序排序而组成了双向链表，而且每个页内的记录（不论是用户记录还是目录项记录）都是按照索引列的值从小到大的顺序而形成了一个单链表。如果是 联合索引 的话，则页面和记录先按照 联合索引 前边的列排序，如果该列值相同，再按照 联合索引 后边的列排序。



- 通过索引查找记录是从 B+ 树的根节点开始，一层一层向下搜索。由于每个页面都按照索引列的值建立了Page Directory （页目录），所以在这些页面中的查找非常快。



<font color='red'>一个表上索引建的越多，就会占用越多的存储空间，在增删改记录的时候性能就越差。</font>



- 在使用索引时需要注意下边这些事项：
  1. 只为用于搜索、排序或分组的列创建索引

  1. 为列的基数大的列创建索引

  1. 索引列的类型尽量小

  1. 可以只对字符串值的前缀建立索引

  1. 只有索引列在比较表达式中单独出现才可以适用索引

  1. 为了尽可能少的让 聚簇索引 发生页面分裂和记录移位的情况，建议让主键拥有 AUTO_INCREMENT 属性。

  1. 定位并删除表中的重复和冗余索引

  1. 尽量使用 覆盖索引 进行查询，避免 回表 带来的性能损耗。











> 数据是如何在mysql中存储的，默认的数据库大概有哪些



## 第八章、mysql的数据目录

> 数据目录：用来存储mysql在运行过程中产生的数据



### 数据库在文件系统

每个数据库都对应数据目录下的一个子文件夹，当我们创建数据库时，mysql会：

1. 在数据目录下创建一个和数据库同名的子目录
2. 在与数据库同名的子目录下创建一个名为db.opt的文件，这文件中包含了该数据库的各种属性。



### 表在文件系统中



- 表结构

在数据目录下对应的数据库子目录下创建一个专门描述表结构的文件。（表名.frm）

> 这个frm文件是以二进制的形式存储的



#### InnoDB的表数据



- 表空间（table space）

文件系统上一个或多个真实的文件，每个表空间可以被划分为很多个页，表数据就存在表空间下的某些页里。



- 系统表空间

> 在数据目录下名为ibdata1，大小为12M的文件。

5.5.7到5.6.6(不包括)之间的版本，数据都会默认被存储到系统表空间中。



- 独立表空间

5.6.6及以后得版本，每一个表都会建立独立表空间（表名.ibd）





#### MyISAM表数据



表数据都存放到对应的数据库子目录下。共三个文件：

test.frm：表结构

test.MYD：表的数据文件

test.MYI：表的索引



### mysql默认的系统数据库



- mysql

存储了MySQL的用户账户和权限信息，一些存储过程、事件的定义信息，一些运行过程中产生的日志信息，一些帮助信息以及时区信息等。



- information_schema

保存着MySQL服务器维护的所有其他数据库的信息，比如有哪些表、哪些视图、哪些触发器、哪些列、哪些索引，这些信息不是用户的真实数据，而是一些描述信息。也被成为元数据。



- performance_schema

主要保存MySQL服务器运行过程中的一些状态信息，算是对MySQL服务器的一个性能监控。

包括统计最近执行了哪些语句，在执行过程的每个阶段都花费了多长时间，内存的使用情况等等信息。



- sys

主要是通过视图的形式把 information_schema 和 performance_schema 结合起来，让程序员可以更方便的了解MySQL服务器的一些性能信息。








> 详细描述表空间的数据结构

## 第九章、InnoDB表空间



### 一个数据页



- 每个页通用的结构

![1744855397911.png](https://fastly.jsdelivr.net/gh/thecoolboyhan/th_blogs@main/image/2025-04/1744855397911_1744855397927.png)



- file Header：记录一些通用信息

| 名称                             | 占用空间大小 | 描述                                                         |
| -------------------------------- | ------------ | ------------------------------------------------------------ |
| FIL_PAGE_SPACE_OR_CHKSUM         | 4 字节       | 页的校验和（checksum 值）                                    |
| FIL_PAGE_OFFSET                  | 4 字节       | 页号                                                         |
| FIL_PAGE_PREV                    | 4 字节       | 上一个页的页号                                               |
| FIL_PAGE_NEXT                    | 4 字节       | 下一个页的页号                                               |
| FIL_PAGE_LSN                     | 8 字节       | 页面被最后修改时对应的日志序列位置 (Log Sequence Number)     |
| FIL_PAGE_TYPE                    | 2 字节       | 该页的类型                                                   |
| FIL_PAGE_FILE_FLUSH_LSN          | 8 字节       | 仅在系统表空间的一个页中定义，代表文件至少被刷新到了对应的 LSN 值 |
| FIL_PAGE_ARCH_LOG_NO_OR_SPACE_ID | 4 字节       | 页属于哪个表空间                                             |



- File Trailer：检查页是否完整，保证从内存到磁盘刷新时内容的一致性。



> 一个表空间最多支持64TB的数据。



### 独立表空间



#### 区（extent）

表空间中的页实在太多了，为了更好的管理这些页，提出了区的概念。

对于默认16k的页来说，连续64页就是一个区（1MB左右）。每个256个区就被划分成一组。



![1744855427995.png](https://fastly.jsdelivr.net/gh/thecoolboyhan/th_blogs@main/image/2025-04/1744855427995_1744855462433.png)

> 区0到区255是第一组，256~511是第二组



表空间被划分为许多连续的区 ，每个区默认由64个页组成，每256个区划分为一组。



#### 段（segment）



- 为什么要引入区？



<font color='red'>没有区的情况</font>：存放数据的多个页其实是双向链表，上一个页和它的下一个页之间，在磁盘上可能不是连续的。这样在不同的页之间扫描，会触发磁盘的<font color='red'>随机IO</font>。



<font color='red'>有区之后</font>：当引入区之后，一个区内的页是顺序且连续的，每个逻辑相邻的页在物理磁盘上页也是相邻的。这样就可以<font color='red'>触发顺序IO。有效提高性能。</font>



- 什么是段？

> 段是用于区分不同类型区的概念。

叶子节点有自己独有的区，非叶子节点也有自己独有的区。

存放叶子节点的多个区就算是一个段。

存放非叶子节点的多个区也算是一个段。

<font color='red'>一个索引会产生2个段，一个叶子节点段。一个非叶子节点段。</font>

> 不止包含上面提到的两种段，还存在别的段（回滚段等）



| 状态名    | 含义                 |
| --------- | -------------------- |
| FREE      | 空闲的区             |
| FREE_FRAG | 有剩余空间的碎片区   |
| FULL_FRAG | 没有剩余空间的碎片区 |
| FSEG      | 附属于某个段的区     |



> 以上表格中的区，只有FSEG属于段，其他的区都直接属于mysql，不属于某个段。



#### 模拟插入一条数据





``` mermaid
graph TD
a[插入一条数据]-->b{判断是否有剩余空间的碎片区}
b-->|yes|c[插入到碎片区]
b-->|no|d[到表空间下申请一个状态为空闲的区,把数据插入到新申请区中的碎片页里.\n此区中零碎的页会为多个段服务,如果该区已满,此区就变为没有剩余空间的碎片区]
```







> 讲解单表查询过程

## 第10章、单表查询

### const

> 直接通过主键来确认记录



- 直接通过id查询

![1744855506669.png](https://fastly.jsdelivr.net/gh/thecoolboyhan/th_blogs@main/image/2025-04/1744855506669_1744855506684.png)

- 通过唯一二级索引可以确定到唯一的id，然后同上

![1744855581630.png](https://fastly.jsdelivr.net/gh/thecoolboyhan/th_blogs@main/image/2025-04/1744855581630_1744855581646.png)



### ref

> 通过非唯一的二级索引<font color='red'>等值</font>获取到多个id，然后回聚簇索引来查询

![1744855603236.png](https://fastly.jsdelivr.net/gh/thecoolboyhan/th_blogs@main/image/2025-04/1744855603236_1744855603253.png)

### range

> 通过索引进行的范围扫描

比如id大于10小于30



### index

> 通过二级索引的全索引扫描可以确认当前值

假设二级索引是联合索引（a-b-c），查询的where条件只有b没有a，无法通过二级索引查询策略，但是可以在二级索引上扫描到当前数据。



### all

全表扫描，直接扫描聚簇索引。



### 回表



1. 步骤1：使用二级索引定位记录的阶段，也就是根据条件 key1 = 'abc' 从 idx_key1 索引代表的 B+ 树中找到对应的二级索引记录。

2. 步骤2：回表阶段，也就是根据上一步骤中找到的记录的主键值进行 回表 操作，也就是到聚簇索引中找到对应的完整的用户记录，再根据条件 key2 > 1000 到完整的用户记录继续过滤。将最终符合过滤条件的记录返回给用户。



- <font color='red'>为什么要尽量避免出现回表操作？</font>

因为在二级索引扫描，之前提到都是顺序IO，扫描速度快。但如果回到局促索引中确定数据，需要进行随机IO，扫描速度慢。（慢很多）



### 索引合并

> 查询条件会用到多个不同的二级索引，mysql可以组装两个二级索引查询出的数据的交集，然后在回表去聚簇索引中查询。

合并索引是为了尽量避免回表操作，减少随机IO。



- 会触发索引合并的条件：

1. 用到的两个不同索引的查询条件都是等值匹配时。（一个等值，一个范围则无法使用）
2. 查询条件中有主键，且只有主键是范围查询，其他二级索引都是等值查询时开会生效

> 因为只有上面两个条件下从二级索引查出的数据都是按照主键排序的。






> 各种join查询

## 第11章、两表连接与基于成本的优化

### 连接的原理

> 两表join查询，驱动的表只会访问一遍，被去驱动的表要被访问多次。



1. 步骤1：选取驱动表，使用与驱动表相关的过滤条件，选取代价最低的单表访问方法来执行对驱动表的单表查询。

2. 步骤2：对上一步骤中查询驱动表得到的结果集中每一条记录，都分别到被驱动表中查找匹配的记录。



![1744855639611.png](https://fastly.jsdelivr.net/gh/thecoolboyhan/th_blogs@main/image/2025-04/1744855639611_1744855639628.png)

> 驱动表只访问一次，但被驱动表却可能被多次访问，访问次数取决于对驱动表执行单表查询后的结果集中的记录条数



### 成本



mysql有默认的成本常量，可以通过成本常量来计算出不同方案查询需要的成本。mysql再选择成本最低的方案来执行。

| 成本常数名称                 | 默认值 | 描述                                                         |
| ---------------------------- | ------ | ------------------------------------------------------------ |
| disk_temptable_create_cost   | 40.0   | 创建基于磁盘的临时表的成本，增大该值可减少磁盘临时表的创建   |
| disk_temptable_row_cost      | 1.0    | 向磁盘临时表写入或读取一条记录的成本，增大该值可减少磁盘临时表的创建 |
| key_compare_cost             | 0.1    | 两条记录比较操作的成本，多用于排序，增大该值可提高 filesort 成本，使优化器更倾向于使用索引排序 |
| memory_temptable_create_cost | 2.0    | 创建基于内存的临时表的成本，增大该值可减少内存临时表的创建   |
| memory_temptable_row_cost    | 0.2    | 向内存临时表写入或读取一条记录的成本，增大该值可减少内存临时表的创建 |
| row_evaluate_cost            | 0.2    | 记录是否符合搜索条件的成本，增大该值可能让优化器更倾向于使用索引而非全表扫描 |



> InnoDB的表信息是不准确的估值



- 内外连接的区别？

外连接驱动表的记录，无法被找到匹配on自居中的过滤条件的记录，该记录仍然会被加入到结果集中，对应的被驱动表记录的各个字段顺手NULL值填充。

内连接驱动表的记录无法在被驱动表中找到的匹配on语句中过滤条件的记录，该记录会被舍弃。



![1744855661461.png](https://fastly.jsdelivr.net/gh/thecoolboyhan/th_blogs@main/image/2025-04/1744855661461_1744855661476.png)



### in查询



不直接将不相关子查询的结果集当作外层查询的参数，而是将该结果集写入一个临时表里。










> 详细介绍Explain

## 第15章、Explain详解



| 列名            | 描述                                      |
|---------------|----------------------------------------|
| id           | 在一个大的查询语句中每个 SELECT 关键字都对应一个唯一的 id |
| select_type  | SELECT 关键字对应的那个查询的类型          |
| table        | 表名                                    |
| partitions   | 匹配的分区信息                          |
| type        | 针对单表的访问方法                        |
| possible_keys | 可能用到的索引                          |
| key         | 实际上使用的索引                          |
| key_len     | 实际使用到的索引长度                      |
| ref         | 当使用索引列等值查询时，与索引列进行等值匹配的对象信息 |
| rows        | 预估的需要读取的记录条数                  |
| filtered    | 某个表经过搜索条件过滤后剩余记录条数的百分比 |
| Extra       | 一些额外的信息                          |

### 各属性的介绍



#### id

每次查询都会生成一个id，如果一条查询需要查询多个表，就会生成多条id相同的记录。

如果有union子句需要把两个查询的结果合并起来，mysql会使用内部的临时表（临时表id为null）



#### Select_type



| 名称                 | 描述                                                         |
| -------------------- | ------------------------------------------------------------ |
| SIMPLE               | 不包含union或者子查询的查询（连接查询也是simple）            |
| PRIMARY              | union、union All或者子查询的大查询等，由多个小查询组成的，其中最左面的查询就是primary |
| UNION                | UNION 中的第二个或更后续的 SELECT 是union                    |
| UNION RESULT         | UNION 的结果                                                 |
| SUBQUERY             | 子查询中的第一个 SELECT                                      |
| DEPENDENT SUBQUERY   | 依赖于外部查询的子查询中的第一个 SELECT                      |
| DEPENDENT UNION      | 依赖于外部查询的 UNION 中的第二个或更后续的 SELECT 语句      |
| DERIVED              | 派生表（需要临时表）                                         |
| MATERIALIZED         | 物化子查询                                                   |
| UNCACHEABLE SUBQUERY | 结果无法缓存并且必须针对外部查询的每一行重新评估的子查询     |
| UNCACHEABLE UNION    | 属于不可缓存子查询的 UNION 中的第二个或更后续的 SELECT 语句 (见 UNCACHEABLE SUBQUERY) |



#### type

前面文章提到的执行计划



| type            | 备注                                                    |
| --------------- | ------------------------------------------------------- |
| system          | 查询系统表，如myisam的数量（InnoDB的数量是不可靠的）    |
| const           | 主键等值匹配（通过唯一二级索引确定唯一id到也算）        |
| eq_ref          | 非唯一的二级索引等值获取到多个id，会聚簇索引查询        |
| index_merge     | 第十章中提到的索引合并                                  |
| Unique_subquery | 两表连接中的eq_ref等值查询（经常出现在in id关联查询中） |
| index_subquery  | 与上面类似，只是关联条键是普通索引                      |
| range           | 使用索引的范围扫描                                      |
| index           | 全索引扫描                                              |
| All             | 全表扫描                                                |



#### extra（扩展信息）



|                                       | 解释                                                         |
| ------------------------------------- | ------------------------------------------------------------ |
| No tables used                        | 没有from子句，不查表                                         |
| Impossible WHERE                      | where语句无效，永远不成立                                    |
| No matching min/max row               | 使用min/max函数，但where条件过滤掉了所有数据（没有数据）时   |
| Using index                           | 只需要使用索引数据，不需要回表                               |
| Using index condition                 | where条件中有索引，但不能使用索引（新版本表示使用了索引下推） |
| Using where                           | 使用where条件进行了全表扫描                                  |
| Using join buffer (Block Nested Loop) | 无法使用索引的关联查询，mysql需要建立临时的buffer块来加快查询 |
| Using filesort                        | 需要使用文件重排序，如果数据很多会非常慢                     |
| Using temporary                       | 多个查询的过程中，需要临时表，一般在排序、去重等查询中常见 DISTINCT 、 GROUP BY 、 UNION |



### 蛇足



- 查看成本

如果想看某个执行计划的成本，可以在explain后添加FORMAT=JSON



- <font color='red'>查询优化器的过程</font>

1. 解析sql语句：把查询等转换成具体的语句，如select* 转换成查询具体字段
2. 优化：计算各种成本，如是否可以走索引，直接查聚簇索引，索引合并，先在哪个条件再走哪个，是否可以用缓存，用之前提到的mysql成本概念来计算每种方式的成本，然后选择一个最优。
3. 执行阶段：通过2中选出的最优方案来执行








> 详细介绍bufferPool

## 第18章、Buffer Pool

- 缓存页

buffer pool中有多个大小为16k的缓存页（与mysql默认一页大小一样），用于缓存从磁盘读取的页数据。



- 控制块

用来存放缓存页控制信息的内存，<font color='red'>控制块和缓存页是一一对应的，它们都被存储在Buffer Pool中，控制块存储在前面，缓存页在后面。</font>



![1744855692816.png](https://fastly.jsdelivr.net/gh/thecoolboyhan/th_blogs@main/image/2025-04/1744855692816_1744855692829.png)



### free链表



![1744855712630.png](https://fastly.jsdelivr.net/gh/thecoolboyhan/th_blogs@main/image/2025-04/1744855712630_1744855712645.png)

> 用来存储空闲的缓存页和控制页，当需要读取时，就从free链表中读取缓存页和控制块



mysql把所有空闲的缓存页对应的控制块作为一个节点放到free链表中。



### flush链表

<font color='red'> mysql不会立刻把修改的数据页同步到磁盘，而是采用flush链表方式来同步。</font>

结构与free链表类似，flush链表会缓存一些已经修改过的缓存页，在到达同步的时间点时，mysql会从flush链表中读取缓存页来同步到磁盘。



![1744855734142.png](https://fastly.jsdelivr.net/gh/thecoolboyhan/th_blogs@main/image/2025-04/1744855734142_1744855734160.png)



### LRU链表

> 类似于垃圾回收链表，用来判断哪些缓存页可以清除

![1744855790805.png](https://fastly.jsdelivr.net/gh/thecoolboyhan/th_blogs@main/image/2025-04/1744855790805_1744855790820.png)

<font color='red'>所有首次被加载到Buffer Pool的缓存页，该缓存页会被放到old区域的头部</font>

- why？

如果我们进行全表扫描，大量数据会被加载到buffer pool为了不使young区缓存的数据直接全部失效，就把新数据放到old区的头部。

全表扫描不断有数据会插入old区头部，超出的从old区尾部被淘汰，来保证不会由于无效数据的加载而是缓存失效。



- 那么young区的数据是如何被添加的？

在LRU缓存中，数据首次进入进入缓存，会在old区的头部，并会在缓存控制块中记录添加的时间。如果又一次访问刚刚添加的缓存，就会计算本次访问的上次添加的间隔时间，如果时间少于mysql系统设定的缓存间隔时间（默认1秒），就把本缓存控制块从old区取出，并添加到young区的头部






> 事务

## 第19章、事务



- AICD

原子性、隔离性、一致性、持久性



### 事务的几种状态



- 活动的（active）

事务对应的数据库正在执行过程中



- 部分提交（partially committed）

事务在内存中的操作已经完成，还没有被写入到磁盘中（在buffer pool中，还没有被写入到磁盘页中）

- 失败（failed）

事务处于活动或者部分提交状态时，出现了错误，事务就会变成失败状态。

- 中止（aborted）

失败的事务被回滚后，就处于中止状态

- 已提交（committed）

事务被修改的数据已经成功同步到磁盘上，就变为已提交状态。



![1744353227133.png](https://fastly.jsdelivr.net/gh/thecoolboyhan/th_blogs@main/image/2025-04/1744353227133_1744353227153.png)




## 第20章、redo日志



mysql访问数据，需要把磁盘中对应的数据页加载到内存中的bufferpool中。每次加载和修改都是以页为单位，落盘刷新也是以页为单位。



- <font color='red'>存在的弊端</font>

1. 资源浪费：每次刷新都是一个完整的数据页，太浪费资源，即使只修改数据页中的一个字节，也要刷新16k的数据到磁盘。
2. 随机IO：由于一条语句可能修改多个数据页的数据，而不同数据页在磁盘中可能不是连续的。会产生随机IO寻址（速度非常慢）



- redo log的做法

在事务提交完成之前，把修改了哪些东西的记录都落在磁盘中。如果系统中间崩溃，也可以从磁盘中恢复刚刚修改的内容。



- redo log 的优点

1. redo log占用空间极小，只记录表空间id、页号、偏移量和需要更新的值
2. redo log是顺序写入磁盘的，使用顺序IO，速度快



### redo log的结构





![1744357032403.png](https://fastly.jsdelivr.net/gh/thecoolboyhan/th_blogs@main/image/2025-04/1744357032403_1744357032426.png)



- type：该redo log的类型
- space id：表空间id
- page number：页号
- data：具体内容



### logbuffer

同样的，想要将redolog落入磁盘，也不是每次直接写到磁盘里。

InnoDB有一块专门缓存日志的缓存叫logbuffer。



- 如何写入一条redolog



1. 先将redolog的内容写入logbuffer中。
2. InnoDB每秒/每次事务提交之前都会将logbuffer中的内容写入到磁盘中。



- logbuffer如何垃圾回收

logbuffer几乎没有垃圾回收，固定的内存空间会记录一个脏点，有点类似于直接内存的概念，不会真的去删除内存中的数据，而是在下次写入时直接覆盖已经失效的内存空间。





## 第22章、undo log

> 用于回滚时的日志



### 事务id

聚簇索引的记录中，存在名为trx_id(事务id)、roll_pointer的隐藏列。



当进行增删改操作时，InnoDB会自动生成对应的undo log和对应的事务id。



### insert



![1744361675334.png](https://fastly.jsdelivr.net/gh/thecoolboyhan/th_blogs@main/image/2025-04/1744361675334_1744361675354.png)

类似链表的形式，开头内存指向当前属性结尾的地址，结尾内存指向上一条结尾的地址，方便遍历，增删改。



### roll_pointer

> 一个指针，指向记录对应的undo日志。

![1744696670326.png](https://fastly.jsdelivr.net/gh/thecoolboyhan/th_blogs@main/image/2025-04/1744696670326_1744696670345.png)



### DELETE

之前提过，mysql在删除数据时，并不是直接删除数据，而是把需要删除的数据放入垃圾回收链表，等待系统来删除。



下面来详细解释删除的过程



- 阶段一（delete mark）事务提交前

![1744697317539.png](https://fastly.jsdelivr.net/gh/thecoolboyhan/th_blogs@main/image/2025-04/1744697317539_1744697317578.png)

mysql会修改记录的trx_id、roll_pointer这些隐藏列的值）

> 删除操作是为了实现MVCC



- 阶段二（purge）事务提交后

当上面删除语句的事务提交之后，会有专门的垃圾回收线程把记录删除掉。

删除过程就是把此记录加入垃圾回收链表，修改页面的其他信息（如数量、删除插入记录的位置，页面可重用的大小等）

![1744697597883.png](https://fastly.jsdelivr.net/gh/thecoolboyhan/th_blogs@main/image/2025-04/1744697597883_1744697597915.png)



### UPDATE



#### 不更新主键的情况



- 原地更新（in-place update）

> 更新前的列和更新后的列占用空间大小一样

会直接更新原来的数据，不做特殊操作

- 空间变化的情况

>  被修改的字段空间减小或者变大

1. mysql会先执行删除操作（这里是真正的删除）
2. 没有dlelete mark阶段，由用户线程来把此记录从正常记录链表移除，然后添加到垃圾回收链表里。并修改页面相关的信息（统计信息等）

3. 然后把新的值插入到正常记录链表里

<font color='red'>上述操作均由用户线程完成，所以一直流传着mysql更新速度会非常慢。</font>



#### 更新主键的情况

> 在局促索引中，mysql的记录是按照主键值的大小连成一个单向链表的，如果要修改主键的值，则可能要记录的移动。



具体操作步骤：

1. 将旧记录进行delete mark操作：（主线程进行了delete mark，后续有专门的垃圾回收线程来把它加入到垃圾回收链表并回收）

   > 原因是为了适配MVCC，这样操作后，其他事务查询还是可以查到之前的值）

2. 根据更新后的值，再创建一条新的记录，重新定位位置并插入





### 回滚



回滚过程中，需要从回滚段中找到Undo页面，把对应的记录恢复回来。（恢复过程中，正常表会产生回滚的redo日志，临时表不产生redo日志）






> 从事务和undo 日志的角度详细介绍MVCC

## 第24章、MVCC



### 事务的隔离级别



#### <font color='red'>事务并发执行遇到的问题（重点）</font>



- 脏写

一个事务修改了另一个未提交事务修改过的数据



- 脏读

一个事务读到了另一个未提交事务修改过的数据



- 不可重复读

一个事务只能读到另一个已经提交的事务修改过的数据，并且其他事务每对该数据进行一次修改并提交后，该事务都能查询得到最新值



- 幻读

一个事务先根据某些条件查询出一些记录，之后另一个事务又向表中插入了符合条件的记录，原先的事务再次按照该条件查询时，能把另一个事务插入的记录也读出来。





#### 四种隔离级别

| 隔离级别                           | 脏读   | 不可重复读 | 幻读                             |
| ---------------------------------- | ------ | ---------- | -------------------------------- |
| 读未提交 (READ UNCOMMITTED)        | 可能   | 可能       | 可能                             |
| 读已提交 (READ COMMITTED)          | 不可能 | 可能       | 可能                             |
| 可重复读 (REPEATABLE READ)（默认） | 不可能 | 不可能     | 可能（有特殊方法，避免出现幻读） |
| 可串行化 (SERIALIZABLE)            | 不可能 | 不可能     | 不可能                           |

> 无论哪种事务隔离级别，都不允许出现脏写情况



### MVCC

#### 版本链

mysql记录中有两个必要的隐藏列（row_id不是不要的，只有在没有主见的情况下才有）



- trx_id：每次事务对某条聚簇索引记录进行了修改，就把事务id赋值到trx_id列
- roll_pointer：每次对聚簇索引记录进行修改时，都会把旧的版本写入到undo日志中，然后roll_pointer列就相当于一个指针，可以通过它找到修改前的信息。

![1744784304336.png](https://fastly.jsdelivr.net/gh/thecoolboyhan/th_blogs@main/image/2025-04/1744784304336_1744784304388.png)

每次对记录进行修改，都会记录一条undo日志，每条undo日志都有一个roll_pointer属性，可以将这些undo连接起来，串成一个链表



![1744784566914.png](https://fastly.jsdelivr.net/gh/thecoolboyhan/th_blogs@main/image/2025-04/1744784566914_1744784566950.png)



每次记录被更新后，都会将旧值放到一条undo日志中，所有版本的roll_pointer连接成一个链表。<font color='red'>版本链的头节点就是当前记录最新的值。</font>（每条版本的undo日志都有一个事务id  trx_id）



#### ReadView

> 判断版本链中哪个版本是当前事务可见的



- ReadView的主要内容
  - m_ids：生成ReadView时当前系统活跃的读写事务的事务id列表
  - min_trx_id：活跃事务列表中的最小事务id
  - max_trx_id：生成ReadView时下一条事务id（不是只事务列表中的最大id，因为有可能较大的事务id在生成ReadView之前就已经被提交了）
  - creator_trx_id：生成该ReadView的事务id。





- 如何判断某个版本记录是否可见？

1. 被访问版本的trx_id和ReadView中的creator_trx_id相同，（该事务在访问自己修改过的版本）当前版本可见。
2. 如果被访问的版本trx_id小于ReadView的最小事务id，（生成该版本事务在ReadView生成前就已经提交了），当前版本可见。
3. 如果访问版本的trx_id大于ReadView中max_trx_id下一条事务的id，（访问版本的事务在当前事务生成ReadView之后才开始），当前版本不可见。
4. 访问版本的trx_id在ReadView的min_trx_id和max_trx_id之间，则判断访问版本的trx_id是否在ReadView活跃事务id列表中。如果在则不可见（生成ReadView时，事务还没有提交，还在修改数据），不在则可见(生成ReadView时，该事务已经被提交了)。





> 不同的事务隔离级别，生成ReadView的时机不同



| 隔离级别 | 生成ReadView的时机               | 影响                                                         |
| -------- | -------------------------------- | ------------------------------------------------------------ |
| 读已提交 | 每次读取数据前都生成一个ReadView | 每次查询时都独立生成一个ReadView，这样每次查询都会读到本次ReadView之前已经提交的版本 |
| 可重复读 | 第一次读取数据时生成ReadView     | 第一次查询时才生成ReadView，这样即使ReadView事务列表中的其他事务后面提交了，当前事务也无法读到它的版本 |
| 串行化   | 用锁实现                         |                                                              |




> 详细介绍mysql的各种锁

## 第25章、锁

### 上锁

> mysql聚簇索引记录上本身是没有锁的，但为什么常常说mysql是根据索引来上锁的呢？

mysql在查询或者增、删改时，都先会去锁结构中来获取当前记录的上锁状态。（锁结构只有在上锁时才有，且结构与聚簇索引类似）

由于需要通过聚簇索引去索结构中获取对应记录的上锁情况，所以常说mysql上锁是根据索引来上的。

![1744792329148.png](https://fastly.jsdelivr.net/gh/thecoolboyhan/th_blogs@main/image/2025-04/1744792329148_1744792329181.png)





之前说过mysql在可重复读隔离级别就已经解决了幻读问题：具体的借据方案如下:



- 读操作利用多版本并发控制（MVCC），写操作进行加锁

读：

由于可重复读只会在第一查询时来生成对应的ReadView，而此时之前提交的事务已经被快照了，本事务也只能查到历史的版本数据，就算有最新的事务修改并提交了新的版本。本事务也无法读到。

写：

所有的写操作都是修改最新的版本，修改时会上锁，多个事务不会冲突。



- 读、写操作都加锁

如果有业务读取记录时不允许读取旧版本，每次查询都只能获取最新版本的记录，则需在要读写的时候都加锁。





> MVCC方式读写操作不冲突，性能更高



### 读锁

#### 共享锁和独占锁



- 共享锁：S锁，事务读取记录时，需要先获取该记录的S锁。
- 独占锁：排它锁，x锁，事务修改记录时，需要先获取该记录的X锁。



### 写锁



- delete

1. 先在B+树中获取该记录的位置
2. 获取这条记录的X锁
3. 再执行delete mark操作





- update
  - 修改后空间没有变化的：
    1. 先在B+树中定位位置
    2. 获取X锁
    3. 原地修改
  - 空间发生变化的
    1. 在B+树中定位位置
    2. 获取X锁
    3. 将该记录彻底删除掉（把此记录添加到垃圾链表）
    4. 插入一条新记录（新插入的记录被隐式锁保护）
  - 修改了主键
    1. 在原记录上执行Delete操作
    2. 在执行一条insert操作





- insert

一般情况插入不加锁，插入后InnoDB会添加隐式锁，来保护此记录不被别的事务访问



### 不同锁的粒度（对齐颗粒度:-)）



#### 表锁

> 在执行DDL语句时会上表锁，上锁方式时通过元数据锁来实现的。





#### 行锁（重点）



- Record Locks（记录锁）

按记录的维度来上锁，一条记录一个锁



- Gap Locks（间隙锁）

> 用来解决幻读问题

上锁范围为要锁的记录（可能有多条记录）的上一条记录结尾，和下一条记录的开始。

<font color='red'>保证锁定范围与上一条和下一条之间都不能插入数据</font>

![1744792054712.png](https://fastly.jsdelivr.net/gh/thecoolboyhan/th_blogs@main/image/2025-04/1744792054712_1744792054748.png)



- Next-Key Locks：

与Gap锁类似，只不过只是不允许在锁定记录与上一条之间插入数据。

锁定记录的后面允许插入数据。





- 隐式锁



之前说ReadView时，会判断事务id，相当于上了隐式锁。





### InnoDB锁的内存结构

![1744792681344.png](https://fastly.jsdelivr.net/gh/thecoolboyhan/th_blogs@main/image/2025-04/1744792681344_1744792681377.png)



