---
title: 状态机（FSM）
description: 从状态机基本概念，到spring状态机，分布式事务状态和如何利用状态机减少if else
slug: FSM
date: 2025-07-17 00:00:00+0000
image: 1.png
categories:
    - java
    - 精选
tags: 
    - 设计模式
    - spring
    - 随笔
---







# 状态机



## 状态机

状态机是一种数学模型，用于描述系统在有限状态之间的转换和行为。





- 主要组成部分：



1. 状态：系统在某一时刻的条件或配置。
2. 事件：触发状态变化的条件或输入。
3. 动作：事件发生后执行的操作。执行动作后，状态可能保持不变或变成新的状态。
4. 转换：从一个状态到另一个状态的过程，基于特定的事件和条件触发。









- 两种不同类型的状态机

1. Moore机：输出仅依赖于当前状态，不受输入影响。（仅有当前值直接给出结果）
2. Mealy机：输出依赖于当前状态和输入状态，适合需要实时响应的系统，如某些硬件电路。（根据流水and原流水字段为空更新，查看能否更新成功，即从未上锁状态达到上锁状态）





## Spring中的状态机

> 基于[Spring State Machine](https://spring.io/projects/spring-statemachine)，下面引用一段spring官方对状态记得总结：
> 状态机之所以强大，是因为其行为始终能得到保证，保持一致，并且由于在启动机器时操作规则已被明确写定，所以相对容易调试。其理念在于，您的应用程序现在处于且可能存在于有限数量的状态中。然后，某些事情发生，使您的应用程序从一个状态转换到下一个状态。 状态机由触发器驱动，这些触发器基于事件或定时器。



Spring State Machine是Spring官方的状态机管理组件。

支持Moore机和Mealy机。它通过声明式配置定义状态、事件和转换。



特点：

1. 层次状态机：支持嵌套状态和区域，处理复杂业务逻辑。
2. 事件驱动：通过事件触发状态转换。
3. 持久化支持：可以将状态机保存到数据库或Redis，适合分布式项目。
4. 灵活：支持自定义动作、守卫（Guards）和监听器。





- 核心概念

1. 状态（states）：系统在某一时刻的状况，例如订单的“待支付”“已支付”“已发货”。
2. 事件（Events）：触发状态转换的信号，例如“支付成功”。
3. 转换（Tranitions）：从一个状态到另一个状态的规则，绑定事件和动作。
4. 动作（Actions）：状态转换或进入/退出状态时执行的操作，例如更新数据库，发送通知。
5. 守卫（Guards）：条件判断，确定是否允许状态转换，例如检查账户余额是否足够。
6. 上下文（Context）：保存状态机运行时的变量和扩展数据。
7. 监听器（Listeners）：监控状态变化，用于日志记录或触发回调。







- 实例代码

```java
@Configuration
@EnableStateMachine
public class OrderStateMachineConfig extends EnumStateMachineConfigurerAdapter<OrderStates,OrderEvents> {

    @Override
    public void configure(StateMachineStateConfigurer<OrderStates, OrderEvents> states) throws Exception {
        states.withStates()
                .initial(OrderStates.SUBMITTED)
                .states(EnumSet.allOf(OrderStates.class))
                .end(OrderStates.FULFILLED)
                .end(OrderStates.CANCELLED);
    }

    @Override
    public void configure(StateMachineTransitionConfigurer<OrderStates, OrderEvents> transitions) throws Exception {
        /*
         当订单处于 SUBMITTED 状态时，触发 PAY 事件会转移到 PAID 状态。
         当订单处于 PAID 状态时，触发 FULFILL 事件会转移到 FULFILLED 状态。
         在任何时候，触发 CANCEL 事件会转移到 CANCELLED 状态。
         */
        transitions.withExternal()
                .source(OrderStates.SUBMITTED).target(OrderStates.PAID).event(OrderEvents.PAY)
                .and()
                .withExternal()
                .source(OrderStates.SUBMITTED).target(OrderStates.FULFILLED).event(OrderEvents.FULFILL)
                .and()
                .withExternal()
                .source(OrderStates.SUBMITTED).target(OrderStates.CANCELLED).event(OrderEvents.CANCEL)
                .and()
                .withExternal()
                .source(OrderStates.PAID).target(OrderStates.CANCELLED).event(OrderEvents.CANCEL);
    }
    
}
```



### 什么样的项目适合用状态机



1. 可以将应用程序或其部分结构表示为状态
2. 想要将复杂的逻辑分解成更小的、易于管理的任务。
3. 该应用程序已经出现了并发问题，例如某些操作是异步进行的。



