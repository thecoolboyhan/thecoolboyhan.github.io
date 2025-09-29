---
title:  从seata入手分布式事务
description:  最近分布式事务又重新刮起了热风，今天就从seata来总结主流的分布式事务的实现
image: 1.png
date: 2025-09-29
slug: seataTransactional
categories: 
  - 精选
  - 分布式事务
  - 架构
tags:
  - 分布式
  - 源码
  - 架构
---


# 从seata入手分布式事务



## AT模式

> 借用本地ACID事务（硬性事务）数据库实现的分布式事务。
>
> 通过Seata 在内部做了对数据库操作的代理层，让本地数据库操作时会检测全局事务，插入回滚日志等。（**目前仅java支持**）



### 概述

- 整体机制

大致分为两个阶段：

1. 本地提交：把业务数据和undo_log（回滚日志）同时在本地数据库提交，本地数据库释放锁和数据库连接。（**没有释放全局锁**）
2. 全局提交阶段：
   1. 提交事务：异步化提交事务，**释放全局锁**
   2. 事务回滚：执行undo_log中记录的回滚sql，回滚后**释放全局锁**



- 写隔离

对于同一全局锁的数据：一阶段时，A事务持有全局锁，只要A事务不进行二阶段释放全局锁。B事务就始终无法一阶段提交，一阶段提交的必要条件是需要获取全局锁。

**回滚**：如果A事务二阶段回滚，此时B事务持有A事务一阶段相同的本地锁，A事务会回滚失败，但A事务会无限重试回滚（最大努力交付），直到B事务由于获取全局锁超时而回滚释放本地锁。A事务又可以获取本地锁，A事务回滚成功，释放全局锁。（**有效避免了脏写**）

![Write-Isolation: Rollback](https://seata.apache.org/zh-cn/assets/images/seata_at-2-c7537b8cd8036580215240d037ea4278.png)



- 读隔离

> 普通select语句是没有读隔离的，可能会读到中间阶段的数据。**读隔离只对select forUpdate语句生效**

A事务持有全局锁没有释放，B事务for update查询数据时，会尝试获取全局锁，获取失败后B事务回滚（**回滚是为了防止出现死锁**），然后重试B事务流程。

![Read Isolation: SELECT FOR UPDATE](https://seata.apache.org/zh-cn/assets/images/seata_at-3-f5d071f55ecde9189c4f2c0d9dec7f5d.png)





### 如何做到代理JDBC操作



- 前置知识：

  > Spring的类在IOC的过程中（依赖注入）需要创建BeanDefinition，每个BeanDefinition都需要通过BeanPostProcessors（后置处理器）阶段来完成，**通过这两个阶段是判断在创建对象时，是否要根据AOP来创建代理对象**。

Seata的AT模式通过创建名为GlobalTransactionScanner的bean，来实现AOP。

```java
public class GlobalTransactionScanner extends AbstractAutoProxyCreator
```

实现了AbstractAutoProxyCreator从而达到AOP的效果。



- 如何保证可以拦截@GlobalTransactional注解的类？

> Spring BeanDefinition创建过程中，需通过后置处理器的postProcessAfterInitialization来判断经过哪些后置处理（增加AOP代码或者调用）。

Seata实现了AbstractAutoProxyCreator并重写了wrapIfNecessary方法，来对所有有@GlobalTransactional注解的类，@GlobalLock注解，类型为SeataDataSourceProxy的数据库实现代理。



> 创建代理类的过程中，会全程对于存放所有BeanName的PROXYED_SET加锁，来避免多线程创建bean出现冲突。





### 本地事务提交

SQL执行时：会现在被seata代理的ConnectionProxy连接代理类中的commit方法。

1. 检测本地上下文中是否有本lockkey的事务如果有直接返回，表示本次请求已经持有锁。

   持有锁，向远程服务器注册锁。

2. 如果没有尝试去远程服务器获取锁，没有就注册锁。

3. 如果远程服务器中已存在其他事务获取该锁，抛出以后，事务提交失败，走回滚流程。

4. 以上获取到锁后，提交本地事务。



### 事务回滚

当前事务回滚，直接执行ACID的回滚逻辑。

本地AT事务回滚，查询undo_log中记录的回滚日志，循环尝试执行，最大努力交付。

并向seata，sever发送当前事务回滚请求，提示让全局事务回滚。



### 全局事务提交

GlobalTransaction 对象向 TC 发起 commit 请求
TC 接收到全局提交请求

TC 将分支事务标记为完成状态
异步删除各个分支的 undo_log 记录
释放相关资源

主要实现在 Seata Server 端：
DefaultCore.commit() 方法：处理全局事务提交
AbstractCore.doGlobalCommit() 方法：执行具体的提交逻辑
FileManager.removeUndoLog() 方法：清理 undo_log 文件

![1759133601762.png](https://fastly.jsdelivr.net/gh/thecoolboyhan/th_blogs@main/image/2025-09/1759133601762_1759133601774.png)



### Selectforupdate

对于当前读也是和上面类似的逻辑，获取对应sql，在ACID的基础上增加获取锁，释放锁，提交锁等。
