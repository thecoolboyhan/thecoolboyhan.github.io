---
title: 备战JDK25--并发
description: JDK25今年年底就要发布了，这次深入了解结构化并发和各种并发框架，争取一起搞清后面几年的并发。后记：用时一个多月终于完成了本文，对于并发比之前又更上了一层楼。
slug: JDK25-2
date: 2025-07-16 00:00:00+0000
image: 1.png
categories:
    - java
    - 精选
tags: 
    - java
    - 多线程
    - 结构化并发
    - 并发	
    - 虚拟线程
---





# JDK25 并发



[TOC]



## 并发集合



### Queue（七个默认的并发用队列）



1. **ArrayBlockingQueue**

- **实现原理**：   基于循环数组实现的有界阻塞队列。内部使用单一的 `ReentrantLock` 来保证线程安全，支持可选的公平（fair）策略。
- **特性**：
  - **有界性**：队列容量在创建时就确定好，不能动态扩充。
  - **FIFO 顺序**：遵循先进先出规则。
  - **阻塞策略**：当队列满时调用 `put()` 会阻塞；当队列空时调用 `take()` 会阻塞。
- **应用场景**：   在需要严格控制资源使用、限制任务数量的生产者—消费者场景中非常合适。例如线程池中，希望通过固定大小队列来防止任务积压导致内存溢出。



2. **LinkedBlockingQueue**

- **实现原理**：   基于链表实现的阻塞队列。在没有显式设置容量时，其默认容量为 `Integer.MAX_VALUE`（即近似无界），可以通过构造函数指定上限。内部采用两个锁——一个用于插入（putLock），另一个用于移除（takeLock），从而在高并发场景下能有效分离生产者和消费者的互斥操作。
- **特性**：
  - **可定界**：既可以指定队列大小，也可以使用默认无界。
  - **FIFO 顺序**：严格的先进先出。
  - **阻塞策略**：与 ArrayBlockingQueue 类似，队列满时插入阻塞，队列空时移除阻塞。
- **应用场景**：   常用于多生产者、多消费者的线程池任务队列，尤其是在任务生产与消费速度不一的场景中可帮助平衡负载。



3. **PriorityBlockingQueue**

- **实现原理**：   基于堆（通常是最小堆）实现的无界阻塞队列，队列中的元素需要实现 `Comparable` 接口或通过提供 `Comparator` 进行排序。
- **特性**：
  - **无界**：通常不设置容量上限，因此入队操作（`offer`/`put`）永远不会阻塞。
  - **排序策略**：队列中的元素顺序不是简单的 FIFO，而是按照优先级（自然顺序或比较器顺序）排序。
  - **阻塞策略**：当队列为空时，`take()` 操作会阻塞；但由于队列无界，入队操作不会因为容量问题而阻塞。
- **应用场景**：   当需要按照任务优先级而非提交顺序来处理任务时，例如任务调度系统、事件处理系统等场景。



4. **DelayQueue**

- **实现原理**：   是一个特殊的无界阻塞队列，队列中所有元素必须实现 `Delayed` 接口。内部同样基于堆结构来维护元素顺序，但只有当元素所关联的延迟时间到期后才能从队列中取出。
- **特性**：
  - **时间控制**：每个元素都带有一个延时，只有延时到期才能被消费。
  - **无界**：同 PriorityBlockingQueue，其入队操作不会阻塞。
  - **阻塞策略**：若队列头部元素延时未到，`take()` 将阻塞等待。
- **应用场景**：   非常适合实现定时任务调度、延时消息处理、缓存失效机制等需要时间延迟控制的场景。



5. **SynchronousQueue**

- **实现原理**：   与其他队列不同，SynchronousQueue 没有任何内部容量，每个插入操作都必须等待一个相对应的移除操作。它实际上充当一个手递手（handoff）的桥梁。
- **特性**：
  - **无容量**：不能存储元素，所有操作都是直接交互。
  - **阻塞策略**：无论是 `put()` 还是 `take()` 都会因为没有对方而阻塞，直到另一个操作到达。
  - **公平/非公平模式**：可以通过构造函数选择公平模式，从而影响线程获得等待权的顺序。
- **应用场景**：   通常用于线程池中作为工作线程直接传递任务的机制，减少任务在队列中积压，实现更低延迟的任务“交接”。



6. **LinkedTransferQueue**

- **实现原理**：   基于链表的无界队列，实现了 `TransferQueue` 接口，扩展了阻塞队列的功能。除了普通的入队/出队操作之外，它还提供了 `transfer()` 方法，允许生产者等待直到有消费者接收该元素。
- **特性**：
  - **无界**：不限制容量。
  - **直接交付选项**：通过 `transfer()` 或 `tryTransfer()` 方法，可实现任务的立即交付。
  - **高并发设计**：适合于需要低延迟和高吞吐量的任务传递场景。
- **应用场景**：   它适用于任务即交付（即若有消费者等待则直接传递，否则则存入队列等待）的场景，常见于高性能消息传递和任务调度系统中。



7. **ConcurrentLinkedQueue**

- **实现原理**：   虽然不属于阻塞队列，但它是一个基于非阻塞算法（CAS）的无界线程安全队列。内部使用链表数据结构，但不提供阻塞机制。
- **特性**：
  - **无界且非阻塞**：消费者需要主动轮询，没有内部锁或阻塞机制。
  - **高效**：在高并发场景下表现优异，但要求消费者能容忍轮询方式带来的延迟。
- **应用场景**：   当你只需要一个安全的队列而不希望引入因阻塞带来的额外开销时，用于日志缓冲、任务缓存等场景较为合适。



#### **总结**

| 队列类型                  | 是否有界 | 内部数据结构 | 顺序策略       | 阻塞行为                                               | 典型应用场景                           |
| ------------------------- | -------- | ------------ | -------------- | ------------------------------------------------------ | -------------------------------------- |
| **ArrayBlockingQueue**    | 有界     | 数组         | FIFO           | 队列满阻塞入队，空阻塞出队                             | 固定任务数量的生产者消费者模型         |
| **LinkedBlockingQueue**   | 可定界   | 链表         | FIFO           | 满时阻塞入队，空时阻塞出队                             | 线程池任务队列，多生产者多消费者       |
| **PriorityBlockingQueue** | 无界     | 堆           | 按优先级排序   | 空阻塞出队，不因容量问题阻塞入队                       | 优先级任务调度                         |
| **DelayQueue**            | 无界     | 堆           | 按延迟时间排序 | 头部未到期阻塞出队，入队不阻塞                         | 定时任务、延时消息、缓存失效机制       |
| **SynchronousQueue**      | 无容量   | 无内部存储   | 直接交接       | 生产者与消费者相互等待，双方都可能阻塞                 | 任务直接交付（如线程池任务传递）       |
| **LinkedTransferQueue**   | 无界     | 链表         | FIFO           | 支持通过 `transfer()` 进行直接交付，也支持常规阻塞操作 | 高性能、低延迟的任务传递               |
| **ConcurrentLinkedQueue** | 无界     | 链表         | 逻辑FIFO       | 非阻塞，需主动轮询消费                                 | 非阻塞场景，如日志消息队列、临时缓冲区 |



#### 如何选择



- **内存和容量控制**：如果希望严格限制内存或任务数量，选择有界的队列（如 ArrayBlockingQueue 或定界的 LinkedBlockingQueue）。
- **任务顺序**：需要按提交顺序处理任务时，FIFO 队列（ArrayBlockingQueue、LinkedBlockingQueue）较为理想；而需要基于状态优先级排序时，则应选 PriorityBlockingQueue。
- **时间调度**：如果任务需要延迟处理，则 DelayQueue 能够根据时间精确控制任务释放。
- **直接交接场景**：任务需要立即转交给消费者，避免积压则可以使用 SynchronousQueue 或 LinkedTransferQueue，它们能实现生产者和消费者之间的直接交付。
- **并发性能非阻塞场景**：当阻塞不是必需的，而仅需提供线程安全的队列操作时，ConcurrentLinkedQueue 是个好选择。



### Map

#### ConcurrentHashMap

传统拉链法hashMap结构，相比hashMap，线程安全采用hash格位上锁synchronized。内部put元素采用cas操作。多线程操作同一个元素，如果出现扩容，会多线程辅助扩容。扩容期间采用地址转发的方式来保证每个请求都能取到对象。



- 数据结构

**JDK7之前**

采用分段机制，每个段都是独立的HashMap。每个段采用独立的锁来保证线程安全。

**JDK8之后**

取消了分段机制，结构完全类似于hashMap，采用Node数组来存放hash头，每个node元素单独synchronized上锁





- 并发扩容

不再由单个线程来完成扩容操作。

而是多个线程共同参与。扩容过程中，如果有线程去原位置获取元素，会创建临时的地址转发保证正确的获取元素。



- 无锁get操作

get方法依赖于volatile来保证元素内存的可见性。能够在JVM层面不上锁的方式来读取对象











#### ConcurrentSkipListMap

并发有序MAP



- 数据结构（跳表）



主要有两层结构

1. 底层链表（Base List）：存储所有键值对节点，按顺序构成单向链表称为底层。
2. 索引层（Index Levels）：在底层之上，建立多级索引（塔），每一层索引节点通过指针连接，构成稀疏的链表，加快查找过程。



> 查找、插入、删除平均时间复杂度都为O(log n)



``` xml
 高层:     HeadIndex -> Index -> Index -> null
                 |          |
 中间层:     Index ------> Index ------> null
                 |          |
 底层:        Node  -->  Node  -->  Node  --> null

```



- 查

查询时从HeadIndex出发，向右查找，遇到比目标大的键就下一层，直到到达最底层。



- 插入

> 插入主要分两个部分，首先需要在底层链表中插入元素，其次就是有可能会提升出一个新的索引

1. 底层插入：利用CAS在底层链表插入新的节点，保证有序性。
2. 随机提升：利用随机判断，有几率让新插入的值向上升级，做索引键
3. 更新索引层：如果需要提升层数（层数可能不固定），在上层建立新的index节点，更新right、down指针。

时间复杂度：O(log n)



- **如何保证并发？**



1. **无锁并发读取**：大部分查找操作都是无锁的，内部节点通过volatile修饰来保证可见性
2. **小颗粒度的锁加CAS写操作**：插入、删除时，仅对局部结构上锁和利用CAS操作保证数据一致性（只存在较少的阻塞操作）
3. 弱一致性迭代器：通过迭代器遍历过程中允许并发更新，不会有并发修改异常。



### List

#### CopyOnWriteArrayList

> 写时复制，可以避免快速失败。

- 写时复制（同时只能有一个线程来修改数组）

添加、删除和更新操作，会先复制一份内部数组（Arrays.copyOf），对新复制的副本来进行修改。通过volatile来保证内部引用可见性。

- 无锁读取

写时产生的新数组会替换旧数组，每次读取时都只读取内部数组（内部数组被Volatile修饰），从而保证可见性和有序性







- 写操作上锁

写操作集合内部使用一个lock对象用synchronized（老版本是用ReentrantLock）来保证并发安全。



> 具体步骤：

1. 获取锁
2. 复制当前的数组（Arrays.copyOf）
3. 在新的数组中进行修改
4. 将新的数组值赋值给内部的volatile字段
5. 释放锁



``` java
public boolean add(E e) {
        synchronized (lock) {
            Object[] es = getArray();
            int len = es.length;
            es = Arrays.copyOf(es, len + 1);
            es[len] = e;
            setArray(es);
            return true;
        }
    }
```





#### Vector

> 老旧版List



所有方法都由synchronized修饰，效率低。虽然并发安全，但依然有ConcurrentModificationException。（内部依然使用modCount计数，发现变化时抛异常）快速失败。









## 原子类

> 线程安全的基本类。
>



下文以AtomicInteger为例：

- 无锁读取

内部由private volatile int value；存放值。利用volatile保证变量的可见性。





- 修改

内部修改使用无锁操作，利用unsafe类CASAPI实现修改。U.compareAndSetInt



```java
private static final Unsafe U = Unsafe.getUnsafe();
```









## synchronized



### 工作原理

基于监视器（monitor）机制，每个java对象都有一个关联的监视器，用于控制对同步代码的访问：



1. synchronized方法：线程调用synchronized方法时，它必须获取方法所属对象的监视器。如果方法是静态的，则获取类的监视器（Class对象）。
2. synchronized代码块：通过synchronized(obj){...}指定同步对象，线程获取obj对象的监视器。



### markword



> java同步的核心机制





![250708094129439.png](https://fastly.jsdelivr.net/gh/thecoolboyhan/th_blogs@main/image/2025-07/250708094129439_1751938889451.png)





- 线程安全：锁状态位，控制JVM对共享资源的访问。
- 高效（锁升级）：（偏向锁→轻量级锁→重量级锁），JVM减少了同步的性能开销。
- GC友好：存放GC相关的元数据，对象的年龄，用于辅助垃圾回收







![1751938945966.png](https://fastly.jsdelivr.net/gh/thecoolboyhan/th_blogs@main/image/2025-07/1751938945966_1751938946010.png)

synchronized的不同markword

| 锁状态   | markword末尾3位 | 描述                                      |
| -------- | --------------- | ----------------------------------------- |
| 无锁     | 01              | 存放哈希码                                |
| 偏向锁   | 100             | 存储偏向线程的指针（JDK15之后被弃用）     |
| 轻量级锁 | 00              | 存放指向线程栈锁记录的指针（JDK21默认锁） |
| 重量级锁 | 10              | 存放指向监视器的指针                      |
| 可被回收 | 11              | 表示当前对象可被回收                      |

![1751939000120.png](https://fastly.jsdelivr.net/gh/thecoolboyhan/th_blogs@main/image/2025-07/1751939000120_1751939000151.png)





- JDK15为什么弃用自旋锁和偏向锁？



偏向锁：

当线程首次获取锁，markword中记录线程偏向线程的指针。被记录的线程后续对上锁对象进行操作时是无锁的。（效率高）

如果另一个线程尝试获取该锁时，偏向锁会被撤销，需要**Safepoint**操作，此操作会停止所有的线程。





废弃原因：



1. **复杂且维护成本高**：JVM偏向锁存在大量代码，且会影响其他的hotspot组件，如垃圾回收等。
2. **性能收益减少**：偏向锁只在单线程时能体现出收益，现代cpu在锁竞争等场景成本以足够低。使得偏向锁价值降低。









### 轻量级锁和重量级锁



- 锁为什么要升级？

不同竞争场景，不同的锁有不同考虑。



**低竞争场景着重效率**

在单线或低竞争的情况下，轻量级锁开销小，几乎接近于无锁状态。



**高竞争场景着重正确性**

重量级锁通过监视器（monitor对象）来实现，有操作系统调度，确保线程安全，避免数据竞争。



**两种共用从而达到动态适应**



确保性能和正确性的平衡。







- 锁升级有什么好处？

1. 性能优化：轻量级锁同步开销少。避免了操作系统调用的开销。
2. 减少内存分配：轻量级锁在对象头中存锁信息，重量级锁需要额外分配一个监视器（monitor）对象。
3. 动态的调节锁，可以达到部分场景的“既要又要”。





| 特点     | 轻量级                                   | 重量级                              |
| -------- | ---------------------------------------- | ----------------------------------- |
| 定义     | 优化机制，减少低竞争场景的同步开销       | 传统锁机制，处理高竞争场景          |
| 使用场景 | 低竞争                                   | 高竞争                              |
| 实现机制 | 使用CAS操作，存储在对象头MarkWord中      | 依赖操作系统Mutex Lock，创建Monitor |
| 等待方式 | 自旋等待，循环检测锁可用                 | 阻塞等待，进入阻塞队列              |
| 性能     | 低竞争高效，避免上下文切换               | 高竞争时高效，涉及上下文切换开销    |
| 内存占用 | 直接使用对象头，几乎不占用内存           | 需要Monitor对象，增加内存使用       |
| 锁位     | 00                                       | 10                                  |
| 升级条件 | 自旋10次或有第三个线程竞争锁升级重量级锁 | 默认状态，锁竞争激烈时升级          |







- 原理

| 操作   | 轻量级                                                       | 重量级                                                       |
| ------ | ------------------------------------------------------------ | ------------------------------------------------------------ |
| 获取锁 | 1、检测对象头是否为无锁（01）<br />2、如果无锁，线程使用CAS操作将MarkWord更新为指向线程栈中的锁记录<br />3、如果失败，进入自旋状态，循环尝试获取锁 | 1、线程检测对象MarkWord是否为重量级锁（10）<br />2、如果是，调用操作系统互斥锁接口尝试获取Monitor<br />3、如果Monitor已被其他线程持有，当前线程阻塞，进入EntrySet等待 |
| 解锁   | 1、检测markwor是否指向自己的<br />2、如果是：线程使用CAS操作将MarkWord恢复为无锁状态（01）<br />3、如果CAS失败，表示锁已升级为重量级锁，调用重量级锁的解锁机制 | 1、检测MarkWord是否指向自己的Monitor<br />2、如果是：线程调用操作系统互斥锁接口，释放Monitor<br />3、操作系统唤醒EntrySet中的一个线程，继续竞争锁 |

 







## volatile



> 保证多线程间的可见性，防止指令重排序



**注意**：volatile不能保证原子性，如果想要原子性，需要synchronized或原子类配合







### 可见性





![250708132014757.png](https://fastly.jsdelivr.net/gh/thecoolboyhan/th_blogs@main/image/2025-07/250708132014757_1751952014821.png)



读操作：直接与主内存交互，而不是与线程本地缓存交互。

写操作：立刻刷新到主内存，读操作直接从主内存读取。





> 实现方式：在cpu的三级缓存中，每个核心有自己独有的本地缓存。cpu间的共享变量由L3存放。volatile通过给CPU上锁，实现可见性。



老CPU：老CPU通过给CPU总线上锁，实现共同修改的变量同时只会有一个核心能够读取到。（这样锁粒度太大，效率低）

新CPU：采用给L3的共享变量的内存地址上锁，保证同时只会有一个线程能够修改共享的变量。而且每次修改，都会强制回写到主内存中。

- 缺点

虽然现在volatile锁定的内存区域很小，但如果是修改特别频繁的变量。由于每次都会锁定主内存中的地址，修改后再释放。修改频繁，导致效率低下。





### 有序性

> 由于不同的操作可能使用到计算器不同的部件，于是CPU为了增快运行效率，程序并不会严格按照代码的顺序执行。<font color='red'>CPU会在**单线程不影响结果**的情况下，随机分配创建对象和对象操作的顺序。</font>

但并发场景，我们想让对象按照我们想要的顺序执行，就需要保证有序性。volatile采用的方式是通过内存屏障（读写屏障）





- 写操作

通过store barrier，确保之前的写操作都完成，并将写缓冲区的数据刷新到主内存中。

新CPU采用Lock add指令，起到full barrier作用。（lock add效率更高）



- 读操作

读操作前加入load barrier，确保之后的读操作都能看到最新的数据。

**X86 新CPU自带禁止指令重排序，不需要额外指令。**



### 举例



- 单例模式创建对象，使用DCL

> 防止半初始化问题



``` java
public class Singleton {
    private static volatile Singleton instance;

    public static Singleton getInstance() {
        if (instance == null) {
            synchronized (Singleton.class) {
                if (instance == null) {
                    instance = new Singleton();
                }
            }
        }
        return instance;
    }
}
```



- 线程之间共享变量

当通讯标志



``` java
public class FlagExample {
    private volatile boolean running = true;

    public void start() {
        new Thread(() -> {
            while (running) {
                // do something
            }
        }).start();
    }
  //可以从外部停止线程
    public void stop() {
        running = false;
    }
}
```











## Lock接口及其相关同步器



> LockSupport、AQS、ReentrantLock、[Semaphore](https://docs.oracle.com/javase/8/docs/api/java/util/concurrent/Semaphore.html), [CyclicBarrier](https://docs.oracle.com/javase/8/docs/api/java/util/concurrent/CyclicBarrier.html), [CountdownLatch](https://docs.oracle.com/javase/8/docs/api/java/util/concurrent/CountDownLatch.html), [Phaser](https://docs.oracle.com/javase/8/docs/api/java/util/concurrent/Phaser.html), 和 [Exchanger](https://docs.oracle.com/javase/8/docs/api/java/util/concurrent/Exchanger.html)

### LockSupport

> 让线程阻塞，和解除阻塞的工具，是锁实现的核心功能之一。



性能优于传统的 wait/notify方法。





- API

| 方法                     | 描述                                                         |
| ------------------------ | ------------------------------------------------------------ |
| park()                   | 阻塞当前线程，直到获得继续运行的许可。如果一直没有许可，线程进入阻塞状态，直到被unpark或中断 |
| unpark(Thread thread)    | 为指定线程提供许可。如果线程被park阻塞，许可会解除其阻塞状态；否则，许可保留供后续park使用。<font color='red'>（**也就是说，解锁可以在上锁之前**）</font> |
| parkNanos(long nanos)    | 阻塞当前线程，最多等待纳秒数，除非获得许可。（锁超时）       |
| parkUntil(long deadline) | 阻塞当前线程，直到指定截止实现，除非获得许可。锁超时）       |
| getBlocker(Thread t)     | 返回线程的阻塞对象，用来检测线程阻塞的原因。如果线程未阻塞，返回null |





- 许可机制

每个线程最多持有一个许可。unpark增加许可，park消耗许可或阻塞线程。









每个线程都有一个许可计数器，初始为0，最大为1。

unpark会计数器设为1，park检查并消耗许可或阻塞线程。



>  Park和unpark是操作系统原生方法，通过JNI调用操作系统的线程管理功能实现。





- 中断支持

当线程被park时如果被中断，park会立刻返回，并设置成中断状态。

> 所以写park代码时，要考虑Thread.interrupted()





- java内部使用场景

**Reentrantlock**：通过LockSupport阻塞等待锁的线程，unpark唤醒等待队列中的下一个线程。

**Semaphore**：park和unpark管理许可的分配和等待。





- 用于线程间协调

生产消费者模式，生产者调用unpark唤醒消费者线程。







> LockSupport解锁虚拟线程时，有特殊的方式，放到虚拟线程那里统一讲。





### AQS（AbstractQueuedSynchronizer）

> 并发包核心框架，抽象类，实现了同步器。
>
> 多种锁、线程池都是通过AQS来实现唤醒和竞争的。
>
> 这是一种典型的<font color='red'>模板方法</font>，它提供了一个基本的同步框架，子类实现特定抽象方法，即可构建不同的同步器。



**主要组成部份**



- 同步状态（state）:一个用volatile修饰的整数，表示同步器的当前状态。0表示未被锁定，大于0表示被锁定。用volatile修饰后保证所有线程可见。
- 等待队列（Queue）：一个FIFO（先进先出）双向链表，用于存储等待获取同步状态的线程。当同步状态不可用（state大于0时），线程会被加入等待队列，按顺序等待。
- 条件变量（condition）：AQS支持通过条件变量，让线程等待特定的条件变为真。每个条件变量有自己的等待队列，可以通过条件变量实现复杂的同步逻辑。



- **为什么等待队列要使用双向链表**？

当某个线程被中断，或者需要退出锁竞争时，可以直接让需要退出队列的线程，修改自己的前后节点的指针，实现快速删除。





![250708201041259.png](https://fastly.jsdelivr.net/gh/thecoolboyhan/th_blogs@main/image/2025-07/250708201041259_1751976641270.png)

- API

| 方法                  | 描述                                           |
| --------------------- | ---------------------------------------------- |
| acquire(int arg)      | 尝试获取同步状态，如果不可用则阻塞等待         |
| release（int arg）    | 释放同步状态                                   |
| tryAcquire（int arg） | 尝试获取同步状态，不会阻塞，子类需要实现此方法 |
| tryRelease(int arg)   | 尝试释放同步状态，子类实现此方法               |
| isHeldExclusively（） | 检查当前线程是否独占持有同步状态               |
| getQueueLength()      | 返回等待队列中的线程数                         |
| hasQueuedThreads()    | 检查是否用线程在等待队列中                     |



> AQS为抽象类，子类实现AQS时，需要重写tryAcquire和tryRelease，定义具体的获取和释放逻辑。
>
> ReentrantLock会检查当前线程是否持有锁（可重入）
>
> Semaphore会检查剩余的许可数量









- 线程阻塞和唤醒
  AQS使用AbstractOwnableSynchronizer管理线程的所有权，通过LockSupport来阻塞和唤醒线程。阻塞的线程会暂停执行，等待被唤醒后重新尝试获取锁。





- AQS的使用场景

1. ReentrantLock：可重入锁
2. Semaphore：信号量，控制同时访问资源的线程数。（限流）
3. CountDownLatch：倒数器，协调多线程执行。
4. CyclicBarrier：阶段锁：多个线程相互等待，直到所有线程到达某个点。
5. ReadWriteLock：读写锁。多读一写





- 自定义锁



``` java
public class MyLock extends AbstractQueuedSynchronizer {
    @Override
    protected boolean tryAcquire(int acquires) {
        return compareAndSetState(0, 1);
    }
//解锁是一个非常复杂的操作，这里演示就直接让锁释放成功
    @Override
    protected boolean tryRelease(int releases) {
        setState(0);
        return true;
    }

    public void lock() {
        acquire(1);
    }

    public void unlock() {
        release(1);
    }
}
```





> condition没有单独讲解，其实这才是线程唤醒条件的关键，上面提到的各种AQS实现，其实都是对condition的一些不同的运用。





### ReentrantLock（可重入锁）

> 基于AQS的可重入锁，最常用的自定义锁，比synchronized更灵活。



- 实现原理

基于AQS实现，通过等待队列管理竞争线程，支持公平和非公平模式。公平模式，线程先来先获取锁；非公平模式，可能出现插队情况。



> 公平模式，严格按照等待队列顺序来修改state对象
>
> 非公平模式，新来的线程会先尝试修改state对象，若修改成功直接获取锁，如果没有在进入等待队列获取锁。（已经进入等待队列的线程要按顺序来获取锁）





- 主要API

**获取锁**：lock获取锁，阻塞直到成功。trylock尝试获取锁，不阻塞。

**释放锁**：unlock释放锁，必须在持有锁时调用。

**条件变量**：newCondition创建条件变量（之前提到的Condition），用于等待和通知。

**监控**：getHoldCount查看当前线程的锁持有次数。



> 可重入：通过holdCount锁被获取的次数，每获取一次+1





> **为了避免死锁，lock必须在finally代码中有unlock**



- 与synchronized对比

| 特性     | ReentrantLock                | synchronized                |
| -------- | ---------------------------- | --------------------------- |
| 可重入性 | 支持，基于hold count         | 支持，基于监视器（Monitor） |
| 公平性   | 可选                         | 非公平                      |
| 超时获取 | 支持（trylock with timeout） | 不支持                      |
| 可中断   | 支持（lockInterruptibly）    | 部分支持（可通过中断处理）  |
| 条件变量 | 支持（newCondition）         | 支持（手动wait/notify)      |
| 监控     | 支持（getHoldCount）         | 不提供对外api               |









- 如何自定义 Condition

``` java
Lock lock = new ReentrantLock();
Condition notEmpty = lock.newCondition();
lock.lock();
try {
    while (queue.isEmpty()) {
        notEmpty.await(); // 消费者等待
    }
    // 处理队列中的元素
} finally {
    lock.unlock();
}
```





### Semaphore（信号量）

> java的计数信号量，用来控制同时访问共享资源的线程数，基于AQS实现。



- 实现原理

通过AQS的同步状态（state）表示可用许可数量。



初始设置的state值，就是最大同时可以访问资源的数量。



获取锁：acquire ，通过CAS减少state值，若state小于0，则线程进入等待队列。



释放锁：release，增加state值，并唤醒等待队列中的线程



> state对象可以被减少到负值，当state对象为负数时，表示有过多的线程来竞争锁。同时也可以提现出目前共有多少个线程需要竞争锁。









- 使用场景

1. 限流：控制访问资源的线程数，限制API请求的并发量。
2. 资源池管理：管理固定数量的资源，如数据库连接池或线程池。
   1. 用Semaphore管理连接池，确保连接数量不超过上限
3. 线程协调：实现类似栅栏的效果，控制多线程的执行顺序。
4. 互斥锁：当state设置为1时，可以做互斥锁（但是不可重入）



- 限流

``` java
Semaphore semaphore = new Semaphore(3); // 允许 3 个线程并发访问
try {
    semaphore.acquire(); // 获取许可
    // 访问共享资源
} finally {
    semaphore.release(); // 释放许可
}
```





### CyclicBarrier（阶段锁）

> 基于AQS，让一组线程在某个点同步等待，当全部到达时，在一起行动。（可以重复使用）





- 主要方法

await()：让线程等待，直到所有线程到达屏障点。

reset()：重置屏障，供下次使用。





- 工作原理

1. 屏障点：当一组线程都调用await方法到达屏障点时，屏障被触发，所有线程被释放继续执行。
2. 屏障动作：当所有线程到达屏障点后，由最后一个线程执行Runnable任务（barrier action）。
3. 重用：CyclicBarrier可以被重用（与他类似的CountDownLatch不可以），所有线程通过屏障后，可以通过reset方法重置屏障，供下次使用。
4. 异常处理：如果一个线程在等待屏障时因中断、超时或者其他原因离开屏障点，所有等待的线程都会抛出BrokenBarrierException，表示屏障已经被破坏。





- 对比

| 特性     | CyclicBarrier          | CountDownLatch                 | Semaphore    |
| -------- | ---------------------- | ------------------------------ | ------------ |
| 重用     | 支持（reset）          | 不支持                         | 支持         |
| 线程等待 | 所有线程相互等待       | 一个或多个线程等待其他线程完成 | 控制并发访问 |
| 屏障动作 | 支持（可选的Runnable） | 不支持                         | 不支持       |
| 场景     | 并行计算、数据处理     | 启动/完成信号                  | 限流、资源池 |







- 使用场景

1. 并行计算：多个线程各自完成一部分任务，需要同步执行下一步操作。

   多个线程各自执行任务，在所有线程完成后再合并结果。

2. 数据处理：分块处理数据，每个线程处理一个数据块，所有线程完成后再进行下一步处理。

3. 游戏开发：多个玩家需要在游戏开始前都做好准备。

4. 线程协调：当一组线程需要在某个点上同步执行时。





``` java
import java.util.concurrent.BrokenBarrierException;
import java.util.concurrent.CyclicBarrier;

public class CyclicBarrierExample {
    private static final CyclicBarrier BARRIER = new CyclicBarrier(4);

    public static void main(String[] args) {
        for (int i = 0; i < 4; i++) {
            new Thread(() -> {
                try {
                    System.out.println(Thread.currentThread().getName() + " is waiting at barrier");
                    BARRIER.await(); // 等待所有线程到达屏障点
                    System.out.println(Thread.currentThread().getName() + " has crossed the barrier");
                } catch (InterruptedException | BrokenBarrierException e) {
                    e.printStackTrace();
                }
            }).start();
        }
    }
}
```



> 四个线程在屏障点等待，等全部都完成时，再继续执行。







### CountdownLatch（倒数器）





> 基于AQS的同步工具，允许一个或多个线程等待直到其他线程完成一组操作。





- 工作原理

1. 初始化，规定需要等待几个操作完成。
2. 等待：需要等待的线程调用await方法阻塞，直到等待计数器归零。如果计数器大于零，线程会被加入AQS的等待队列，并通过LockSupport.park阻塞。
3. 计数：线程调用countDown方法将计数器减一。每调用一次，计数器减少1，如果计数器到达零，上方等待的线程会被释放。
4. **不可重用**：countDownLatch是一次性的，计数器不能重置。如果想要重用，可以使用CyclicBarrier。





- 实现原理

如何实现等待的数量：利用AQS的state对象



如何等待：需要等待的线程在AQS的等待队列中，当state对象变成0时，立刻返回。



内存可见：开发遵守happens-before规范，如果通过volatile变量保证可见性。





- 使用场景

1. 待定多个线程初始化完成：每次初始化完成后，调用countDown
2. 启动多个线程后等待它们完成：规定好需要运行的次数，然后倒数。
3. 分阶段执行：某个阶段需要等待所有线程都完成后再执行。（一次性）



### Phaser（"强大的多段锁"）



> 基于AQS，比CyclicBarrier更灵活的同步机制。允许多个线程在不同阶段同步等待。支持动态注册和解注册线程，适合线程数量会变化的场景。（**可以伸缩**）



- 阶段（Phase）：支持多个同步阶段，每个阶段都有自己的编号。从0开始，到达同步点后，阶段号递增。
- 注册：通过register方法，动态的把线程注册到Phaser中。
- 到达：arrive或arriveAndAwaitAdvance表示到达同步点。arriveAndAwaitAdvance会阻塞当前线程
- 等待：没有满足到达的线程数量时，线程会等待。注册数量的线程到达时，所有等待线程会被释放。
- 解注册（解绑）：arriveAndDeregister方法，在<font color='red'>**到达同步点时**</font>解注册
- onAdvance(钩子函数)：运行重写onAdvance方法自定义阶段结束时的行为，例如执行更新操作。







#### 底层实现

虽然是基于AQS的共享模式，但实现更加复杂。内部主要包括



1. 阶段计数器：每个阶段都有唯一的编号，阶段结束时递增。通过getPhase查询当前所处的阶段。
2. 注册计数器：动态管理当前注册的线程数。通过getRegisteredParties查询数量。
3. 等待队列：使用AQS的等待队列管理等待线程，当线程调用arriveAndAwaitAdvance时，如果有线程未到达同步点，当前线程会被加入队列并阻塞。
4. onAdvance机制：当所有线程到达同步点时，Phaser会调用onAdvance方法。



- 使用场景

1. 动态线程池：线程数可以变化的场景，例如并行计算任务。线程可以运行时动态加入或离开。
2. 多阶段计算：每个阶段需要同步的计算任务，例如数据处理管道。每个阶段可以有不同的线程数。
3. 递归算法：任务数变化的递归策略，例如快排，Phaser可以处理任务分治过程中线程数的动态变化。





- 多阶段计算

``` java
import java.util.concurrent.Phaser;

public class PhaserExample {
    public static void main(String[] args) {
        int threads = 3;
      //初始规定三个线程
        Phaser phaser = new Phaser(threads);

        for (int i = 0; i < threads; i++) {
            final int threadNum = i;
            new Thread(() -> {
                System.out.println("Thread " + threadNum + " starting phase " + phaser.getPhase());
                // 模拟工作
                try {
                    Thread.sleep(1000);
                } catch (InterruptedException e) {
                    e.printStackTrace();
                }
                System.out.println("Thread " + threadNum + " arriving at phase " + phaser.getPhase());
                phaser.arriveAndAwaitAdvance(); // 到达同步点并等待

                System.out.println("Thread " + threadNum + " starting phase " + phaser.getPhase());
                // 模拟下一阶段工作
                try {
                    Thread.sleep(1000);
                } catch (InterruptedException e) {
                    e.printStackTrace();
                }
                System.out.println("Thread " + threadNum + " arriving at phase " + phaser.getPhase());
                phaser.arriveAndDeregister(); // 到达同步点并解注册
            }).start();
        }
    }
}
```







#### 动态线程池





- 动态线程池

> 利用Phaser实现，线程可以在运行时，动态的加入或离开。





```java
class DynamicThreadPoolWithPhaser {
    public static void main(String[] args) throws InterruptedException {
        // 创建 Phaser
        Phaser phaser = new Phaser() {
            @Override
            protected boolean onAdvance(int phase, int registeredParties) {
                System.out.println("Advancing to phase " + (phase + 1) + " with " + registeredParties + " parties remaining");
                return registeredParties == 0; // 当没有注册线程时终止
            }
        };

        // 阶段 1：启动 4 个线程
        Thread[] threads = new Thread[6]; // 预分配最大线程数
        System.out.println("Starting Phase 1 with 4 threads");
        for (int i = 0; i < 4; i++) {
            phaser.register(); // 为每个线程注册
            threads[i] = new Thread(new Worker(phaser, i, i < 2 ? 2 : 3), "Worker-" + i);
            threads[i].start();
        }
        phaser.arriveAndAwaitAdvance(); // 主线程等待 Phase 1 完成

        // 阶段 2：增加到 6 个线程
        System.out.println("Starting Phase 2 with 6 threads");
        for (int i = 4; i < 6; i++) {
            phaser.register(); // 为新线程注册
            threads[i] = new Thread(new Worker(phaser, i, 3), "Worker-" + i);
            threads[i].start();
        }
        phaser.arriveAndAwaitAdvance(); // 主线程等待 Phase 2 完成

        // 阶段 3：减少到 2 个线程（由 Worker 内部逻辑控制）
        System.out.println("Starting Phase 3 with 2 threads");
        phaser.arriveAndAwaitAdvance(); // 主线程等待 Phase 3 完成

        // 等待所有线程结束
        for (Thread t : threads) {
            if (t != null) {
                t.join();
            }
        }
        System.out.println("All phases completed. Final phase: " + phaser.getPhase() + ", terminated: " + phaser.isTerminated());
    }
}

class Worker implements Runnable {
    private final Phaser phaser;
    private final int id;
    private final int maxPhase; // 最大参与阶段

    public Worker(Phaser phaser, int id, int maxPhase) {
        this.phaser = phaser;
        this.id = id;
        this.maxPhase = maxPhase;
    }

    @Override
    public void run() {
        try {
            for (int p = 0; p <= maxPhase; p++) {
                if (phaser.isTerminated()) {
                    System.out.println("Worker-" + id + " stopped: Phaser terminated");
                    return;
                }
                System.out.println("Worker-" + id + " starting phase " + p);
                Thread.sleep(ThreadLocalRandom.current().nextInt(1000, 2000)); // 模拟工作
                System.out.println("Worker-" + id + " completed phase " + p);
                if (p == maxPhase) {
                    phaser.arriveAndDeregister(); // 到达最大阶段后解注册
                } else {
                    phaser.arriveAndAwaitAdvance(); // 等待其他线程
                }
            }
        } catch (InterruptedException e) {
            System.out.println("Worker-" + id + " interrupted: " + e.getMessage());
            Thread.currentThread().interrupt();
        }
    }
}
```

> 初始化Phaser时，可以不指定最大阶段数。（为了方便自己复用）。可以给使用的运行的线程规定不同的最大阶段数。当固定的线程到达最大阶段数时，就让他退出。其他最大阶段数较大的，继续运行。











- 动态核心线程数的线程池（与Phaser无关）

```java
class DynamicThreadPool {
    public static void main(String[] args) throws InterruptedException {
        // 创建 ThreadPoolExecutor，初始核心线程数为 5，最大线程数为 10
        ThreadPoolExecutor executor = new ThreadPoolExecutor(
                5, // 核心线程数
                10, // 最大线程数
                60L, // 空闲线程存活时间
                TimeUnit.SECONDS,
                new LinkedBlockingQueue<Runnable>() // 任务队列
        );

        // 打印初始线程池状态
        System.out.println("初始核心线程数: " + executor.getCorePoolSize());
        System.out.println("初始线程池大小: " + executor.getPoolSize());

        // 提交 10 个任务
        for (int i = 0; i < 10; i++) {
            final int taskId = i;
            executor.execute(() -> {
                System.out.println("任务 " + taskId + " 开始执行，线程: " + Thread.currentThread().getName());
                try {
                    Thread.sleep(2000); // 模拟工作
                } catch (InterruptedException e) {
                    Thread.currentThread().interrupt();
                }
                System.out.println("任务 " + taskId + " 完成，线程: " + Thread.currentThread().getName());
            });
        }

        // 等待 3 秒，让部分任务运行并排队
        Thread.sleep(3000);

        // 打印当前线程池状态
        System.out.println("3 秒后，线程池大小: " + executor.getPoolSize());
        System.out.println("活跃线程数: " + executor.getActiveCount());
        System.out.println("已完成任务数: " + executor.getCompletedTaskCount());
        System.out.println("排队任务数: " + executor.getQueue().size());

        // 将核心线程数动态调整为 10
        executor.setCorePoolSize(10);
        System.out.println("核心线程数调整为: " + executor.getCorePoolSize());

        // 等待 2 秒，让新线程启动
        Thread.sleep(2000);

        // 打印调整后的线程池状态
        System.out.println("调整核心线程数后，线程池大小: " + executor.getPoolSize());
        System.out.println("活跃线程数: " + executor.getActiveCount());
        System.out.println("已完成任务数: " + executor.getCompletedTaskCount());
        System.out.println("排队任务数: " + executor.getQueue().size());

        // 提交另外 5 个任务
        for (int i = 10; i < 15; i++) {
            final int taskId = i;
            executor.execute(() -> {
                System.out.println("任务 " + taskId + " 开始执行，线程: " + Thread.currentThread().getName());
                try {
                    Thread.sleep(2000); // 模拟工作
                } catch (InterruptedException e) {
                    Thread.currentThread().interrupt();
                }
                System.out.println("任务 " + taskId + " 完成，线程: " + Thread.currentThread().getName());
            });
        }

        // 关闭线程池
        executor.shutdown();
        System.out.println("线程池关闭已启动");

        // 等待所有任务完成
        executor.awaitTermination(1, TimeUnit.HOURS);
        System.out.println("所有任务完成");
    }
}
```











- 总结

其他同步工具理论上也可以实现类似的阶段功能，但像Phaser这种动态注册的只有Phaser





| 特性     | Phaser                 | CyclicBarrier          | CountDownLatch           | Semaphore    |
| -------- | ---------------------- | ---------------------- | ------------------------ | ------------ |
| 重用     | 支持                   | 支持                   | 不支持                   | 支持         |
| 动态注册 | 支持                   | 不支持                 | 不支持                   | 不支持       |
| 多阶段   | 支持                   | 支持（固定线程数）     | 不支持                   | 不支持       |
| 使用场景 | 动态线程池、多阶段计算 | 固定线程数的多阶段同步 | 等待初始化完成、任务结束 | 限流、资源池 |









### Exchanger（交换器，线程间沟通工具）

> 并不基于AQS，只基于LockSupport实现的交换器。在两个线程之前交换数据，一个线程使用exchange方法就阻塞，直到另一个线程也调用exchange方法。两个线程交换各自的结果，然后运行。





- API

| 方法名                                       | 描述                               |
| -------------------------------------------- | ---------------------------------- |
| Exchanger                                    | 构造方法                           |
| V exchange(V x)                              | 等待另一个线程到达汇合点并交换对象 |
| V exchange(V x, long timeout, TimeUnit unit) | 等待交换的对象，可能超时           |





- 实现原理

1. 阻塞唤醒：利用LockSupport.park 和LockSupport.unpark实现线程阻塞和唤醒。
2. 超时机制：利用LockSupport.parkNanos
3. 被交换的对象存储的位置：被交换的对象存储在ThreadLocal中







- 使用场景



1. 生产者消费者：两个线程交换缓冲区
2. 遗传算法：两个线程可能需要交换种群或部分计算结果。
3. 管道设计：在多个阶段中，阶段间的数据传递可以通过Exchanger实现
4. 两个线程同步数据





- 生产者消费者代码



``` java
import java.util.concurrent.Exchanger;

public class ProducerConsumerExample {
    public static void main(String[] args) {
        Exchanger<String> exchanger = new Exchanger<>();
        new Thread(() -> {
            try {
                for (int i = 0; i < 5; i++) {
                    String data = "Data " + i;
                    System.out.println("Producer sending: " + data);
                    String received = exchanger.exchange(data);
                    System.out.println("Producer received: " + received);
                    Thread.sleep(1000); // 模拟生产时间
                }
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
            }
        }).start();
        new Thread(() -> {
            try {
                for (int i = 0; i < 5; i++) {
                    String ack = "Ack " + i;
                    System.out.println("Consumer sending: " + ack);
                    String received = exchanger.exchange(ack);
                    System.out.println("Consumer received: " + received);
                    Thread.sleep(1200); // 模拟消费时间
                }
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
            }
        }).start();
    }
}
```









## 线程池（重点）

> 这部分来自于权威的[javaguide](https://javaguide.cn/java/concurrent/java-thread-pool-summary.html#%E7%BA%BF%E7%A8%8B%E6%B1%A0%E4%BB%8B%E7%BB%8D)



- 线程池的好处

1. **降低资源消耗**：通过重复利用已创建的线程降低线程创建和销毁造成的消耗
2. **提高响应速度**：当任务到达时，任务可以不需要等到线程创建就能立即执行。
3. **提高线程的可管理性**：线程（平台线程）是稀缺资源，如果无限制的创建（虚拟线程就是可以近乎无限制的创建:-)），不仅会消耗系统资源，还会降低系统的稳定性。

> 这些都只平台线程，永远不要试图池化虚拟线程



### Executor框架



通过Excutor来启动线程要比使用Thread的start方法更好，效率更高（用线程池实现，节约开销）。<font color='red'>有助于避免this逃逸问题</font>



- this逃逸问题：在构造函数返回之前，其他线程就持有该对象的引用，调用尚未构造完全的对象的方法可能引发错误。







Executor主要分三大部分：







1、**任务**（Runnable/callable)



被执行的任务需要实现Runnable和Callable接口。





2、 **任务的执行**（Executor）

类关系图

![250710164606221.png](https://fastly.jsdelivr.net/gh/thecoolboyhan/th_blogs@main/image/2025-07/250710164606221_1752137166268.png)



ThreadPoolExecutor和ScheduledThreadPoolExecutor两个类都可以执行任务。

ThreadPoolExecutor使用频率更高





3、 **异步计算的结果**(Future)

> 存储异步计算的结果



![1752137379630.png](https://fastly.jsdelivr.net/gh/thecoolboyhan/th_blogs@main/image/2025-07/1752137379630_1752137379657.png)





- 执行流程

1. 主线程首先要创建实现 `Runnable` 或者 `Callable` 接口的任务对象。
2. 把创建完成的实现 `Runnable`/`Callable`接口的 对象直接交给 `ExecutorService` 执行: `ExecutorService.execute（Runnable command）`）或者也可以把 `Runnable` 对象或`Callable` 对象提交给 `ExecutorService` 执行（`ExecutorService.submit（Runnable task）`或 `ExecutorService.submit（Callable <T> task）`）。
3. 如果执行 `ExecutorService.submit（…）`，`ExecutorService` 将返回一个实现`Future`接口的对象（我们刚刚也提到过了执行 `execute()`方法和 `submit()`方法的区别，`submit()`会返回一个 `FutureTask 对象）。由于 FutureTask` 实现了 `Runnable`，我们也可以创建 `FutureTask`，然后直接交给 `ExecutorService` 执行。
4. 最后，主线程可以执行 `FutureTask.get()`方法来等待任务执行完成。主线程也可以执行 `FutureTask.cancel（boolean mayInterruptIfRunning）`来取消此任务的执行。





### ThreadPoolExecutor类（重点）



``` java
    /**
     * 用给定的初始参数创建一个新的ThreadPoolExecutor。
     */
    public ThreadPoolExecutor(int corePoolSize,//线程池的核心线程数量
                              int maximumPoolSize,//线程池的最大线程数
                              long keepAliveTime,//当线程数大于核心线程数时，多余的空闲线程存活的最长时间
                              TimeUnit unit,//时间单位
                              BlockingQueue<Runnable> workQueue,//任务队列，用来储存等待执行任务的队列
                              ThreadFactory threadFactory,//线程工厂，用来创建线程，一般默认即可
                              RejectedExecutionHandler handler//拒绝策略，当提交的任务过多而不能及时处理时，我们可以定制策略来处理任务
                               ) {
        if (corePoolSize < 0 ||
            maximumPoolSize <= 0 ||
            maximumPoolSize < corePoolSize ||
            keepAliveTime < 0)
            throw new IllegalArgumentException();
        if (workQueue == null || threadFactory == null || handler == null)
            throw new NullPointerException();
        this.corePoolSize = corePoolSize;
        this.maximumPoolSize = maximumPoolSize;
        this.workQueue = workQueue;
        this.keepAliveTime = unit.toNanos(keepAliveTime);
        this.threadFactory = threadFactory;
        this.handler = handler;
    }
```



- 核心参数：



1. corePoolSize：核心线程数
2. maximumPoolSize：最大线程数
3. long keepAliveTime：**核心线程外的线程**的存活实现
4. TimeUnit unit：时间单位
5. BlockingQueue<Runnable> workQueue：等待队列
6. ThreadFactory threadFactory：创建线程的工厂
7. RejectedExecutionHandler handler：拒绝策略



![1752137770223.png](https://fastly.jsdelivr.net/gh/thecoolboyhan/th_blogs@main/image/2025-07/1752137770223_1752137770241.png)





- 拒绝策略



1. `ThreadPoolExecutor.AbortPolicy`：抛出 `RejectedExecutionException`来拒绝新任务的处理。
2. `ThreadPoolExecutor.CallerRunsPolicy`：调用执行自己的线程运行任务，也就是直接在调用`execute`方法的线程中运行(`run`)被拒绝的任务，如果执行程序已关闭，则会丢弃该任务。因此这种策略会降低对于新任务提交速度，影响程序的整体性能。如果您的应用程序可以承受此延迟并且你要求任何一个任务请求都要被执行的话，你可以选择这个策略。
3. `ThreadPoolExecutor.DiscardPolicy`：不处理新任务，直接丢弃掉。
4. `ThreadPoolExecutor.DiscardOldestPolicy`：此策略将丢弃最早的未处理的任务请求。

> 阻塞队列可以参考并发集合中的7种等待队列



### **线程池的原理（重点）**





- 使用Executor.execute(worker)提交一个线程



``` java
   // 存放线程池的运行状态 (runState) 和线程池内有效线程的数量 (workerCount)
   private final AtomicInteger ctl = new AtomicInteger(ctlOf(RUNNING, 0));

    private static int workerCountOf(int c) {
        return c & CAPACITY;
    }
    //任务队列
    private final BlockingQueue<Runnable> workQueue;

    public void execute(Runnable command) {
        // 如果任务为null，则抛出异常。
        if (command == null)
            throw new NullPointerException();
        // ctl 中保存的线程池当前的一些状态信息
        int c = ctl.get();

        //  下面会涉及到 3 步 操作
        // 1.首先判断当前线程池中执行的任务数量是否小于 corePoolSize
        // 如果小于的话，通过addWorker(command, true)新建一个线程，并将任务(command)添加到该线程中；然后，启动该线程从而执行任务。
        if (workerCountOf(c) < corePoolSize) {
            if (addWorker(command, true))
                return;
            c = ctl.get();
        }
        // 2.如果当前执行的任务数量大于等于 corePoolSize 的时候就会走到这里，表明创建新的线程失败。
        // 通过 isRunning 方法判断线程池状态，线程池处于 RUNNING 状态并且队列可以加入任务，该任务才会被加入进去
        if (isRunning(c) && workQueue.offer(command)) {
            int recheck = ctl.get();
            // 再次获取线程池状态，如果线程池状态不是 RUNNING 状态就需要从任务队列中移除任务，并尝试判断线程是否全部执行完毕。同时执行拒绝策略。
            if (!isRunning(recheck) && remove(command))
                reject(command);
                // 如果当前工作线程数量为0，新创建一个线程并执行。
            else if (workerCountOf(recheck) == 0)
                addWorker(null, false);
        }
        //3. 通过addWorker(command, false)新建一个线程，并将任务(command)添加到该线程中；然后，启动该线程从而执行任务。
        // 传入 false 代表增加线程时判断当前线程数是否少于 maxPoolSize
        //如果addWorker(command, false)执行失败，则通过reject()执行相应的拒绝策略的内容。
        else if (!addWorker(command, false))
            reject(command);
    }
```



1. 如果当前运行的线程数小于核心线程数，那么就会新建一个线程来执行任务
2. 如果当前运行的线程数等于或大于核心线程数，但是小于最大线程数，那么就把该任务放入到任务队列里等待执行。
3. 如果向任务队列投放任务失败（任务队列已经满了），但是当前运行的线程数是小于最大线程数的，就新建一个线程来执行任务。
4. 如果当前运行的线程数已经等同于最大线程数了，新建线程将会使当前运行的线程超出最大线程数，那么当前任务会被拒绝，拒绝策略会调用`RejectedExecutionHandler.rejectedExecution()`方法。



![1752138126645.png](https://fastly.jsdelivr.net/gh/thecoolboyhan/th_blogs@main/image/2025-07/1752138126645_1752138126692.png)



``` java
    // 全局锁，并发操作必备
    private final ReentrantLock mainLock = new ReentrantLock();
    // 跟踪线程池的最大大小，只有在持有全局锁mainLock的前提下才能访问此集合
    private int largestPoolSize;
    // 工作线程集合，存放线程池中所有的（活跃的）工作线程，只有在持有全局锁mainLock的前提下才能访问此集合
    private final HashSet<Worker> workers = new HashSet<>();
    //获取线程池状态
    private static int runStateOf(int c)     { return c & ~CAPACITY; }
    //判断线程池的状态是否为 Running
    private static boolean isRunning(int c) {
        return c < SHUTDOWN;
    }


    /**
     * 添加新的工作线程到线程池
     * @param firstTask 要执行
     * @param core参数为true的话表示使用线程池的基本大小，为false使用线程池最大大小
     * @return 添加成功就返回true否则返回false
     */
   private boolean addWorker(Runnable firstTask, boolean core) {
        retry:
        for (;;) {
            //这两句用来获取线程池的状态
            int c = ctl.get();
            int rs = runStateOf(c);

            // Check if queue empty only if necessary.
            if (rs >= SHUTDOWN &&
                ! (rs == SHUTDOWN &&
                   firstTask == null &&
                   ! workQueue.isEmpty()))
                return false;

            for (;;) {
               //获取线程池中工作的线程的数量
                int wc = workerCountOf(c);
                // core参数为false的话表明队列也满了，线程池大小变为 maximumPoolSize
                if (wc >= CAPACITY ||
                    wc >= (core ? corePoolSize : maximumPoolSize))
                    return false;
               //原子操作将workcount的数量加1
                if (compareAndIncrementWorkerCount(c))
                    break retry;
                // 如果线程的状态改变了就再次执行上述操作
                c = ctl.get();
                if (runStateOf(c) != rs)
                    continue retry;
                // else CAS failed due to workerCount change; retry inner loop
            }
        }
        // 标记工作线程是否启动成功
        boolean workerStarted = false;
        // 标记工作线程是否创建成功
        boolean workerAdded = false;
        Worker w = null;
        try {

            w = new Worker(firstTask);
            final Thread t = w.thread;
            if (t != null) {
              // 加锁
                final ReentrantLock mainLock = this.mainLock;
                mainLock.lock();
                try {
                   //获取线程池状态
                    int rs = runStateOf(ctl.get());
                   //rs < SHUTDOWN 如果线程池状态依然为RUNNING,并且线程的状态是存活的话，就会将工作线程添加到工作线程集合中
                  //(rs=SHUTDOWN && firstTask == null)如果线程池状态小于STOP，也就是RUNNING或者SHUTDOWN状态下，同时传入的任务实例firstTask为null，则需要添加到工作线程集合和启动新的Worker
                   // firstTask == null证明只新建线程而不执行任务
                    if (rs < SHUTDOWN ||
                        (rs == SHUTDOWN && firstTask == null)) {
                        if (t.isAlive()) // precheck that t is startable
                            throw new IllegalThreadStateException();
                        workers.add(w);
                       //更新当前工作线程的最大容量
                        int s = workers.size();
                        if (s > largestPoolSize)
                            largestPoolSize = s;
                      // 工作线程是否启动成功
                        workerAdded = true;
                    }
                } finally {
                    // 释放锁
                    mainLock.unlock();
                }
                //// 如果成功添加工作线程，则调用Worker内部的线程实例t的Thread#start()方法启动真实的线程实例
                if (workerAdded) {
                    t.start();
                  /// 标记线程启动成功
                    workerStarted = true;
                }
            }
        } finally {
           // 线程启动失败，需要从工作线程中移除对应的Worker
            if (! workerStarted)
                addWorkerFailed(w);
        }
        return workerStarted;
    }
```





![1752216397588.png](https://fastly.jsdelivr.net/gh/thecoolboyhan/th_blogs@main/image/2025-07/1752216397588_1752216397606.png)







- ThreadPoolExecutor的运行状态

| 运行状态       | 状态描述                                                     |
| -------------- | ------------------------------------------------------------ |
| RUNNING运行    | 能接收新提交的任务，也能处理阻塞队列中的任务                 |
| shutdown关闭   | 关闭状态，不再接受新提交的任务，但可以继续处理阻塞队列中的任务 |
| stop停止       | 不能接收新的任务，也不处理队列中的任务，会中断正在处理任务的线程 |
| tidying整理    | 所有任务都已终止了，workerCount（有效线程）为0               |
| terminated终止 | 在terminated方法执行后进入该状态，终止                       |

### 对比



- Runnable和Callable

run没有返回值，call有返回值，run可以被execute也可以被submit，call只能被submit













- execute和submit



1. 返回值：

   **execute**：用来提交不需要返回值的任务。无法判断任务是否被成功执行。

   **submit**：会返回一个Future对象，通过Future判断是否执行成功，并获取任务的返回值。（get()方法会阻塞当前线程直到任务完成）
   
1. 异常处理：

   1. 使用submit提交时，可用Future也可以得到子线程抛出的异常。
2. 使用execute时，需要手动自定义ThreadFactory或者ThreadPoolExecutor的afterExcute方法（afterExcute方法现在受保护方法，无法直接调用，需要通过ThreadPool调用）

> <font color='red'>**异常是否会中断线程**</font>:线程池核心线程，会在线程池第一次被调用时创建。后续如果核心线程运行过程中出现异常，会视情况来决定是否会结束线程。
> execute提交的线程：出现异常会中断。
> submit提交的线程：出现异常也不中断。
> **原因**：核心线程运行run或call结束后，会将核心线程归还。但如果中途检测到异常，execute外层并没有用try处理这种情况，会导致线程应异常被抛出。而没有归还操作。导致核心线程异常中止。submit由于会接收返回值，外层有用try包裹核心线程的执行，即使出现异常，也可以正常的归还核心线程。







- Shutdown和shutdownnow

1. shutdown：关闭线程池，线程池的状态变为shutdown，线程池不再接收新的任务，但队列里的任务要执行完毕。
2. shutdownNow：关闭线程池，线程池状态变为stop，会终止现在正在运行的任务，并把等待队列中的任务以list的形式返回。





### 最佳实践（重点）

> 同样来自[javaguide](https://javaguide.cn/java/concurrent/java-thread-pool-best-practices.html)



- **创建线程池**

> 不要用**`Executors`**创建线程池



1. **`FixedThreadPool`**和**`SingleThreadExecutor`**使用的是无界等待队列，当任务过多时，会有内存溢出风险。
2. **`CachedThreadPool`**：使用的是同步队列SynchronousQueue（没有空间大小），允许创建的线程池数量是Integer.MAX_VALUE，为了快速处理任务，会不断创建最大线程。
3. **`ScheduledThreadPool`**和**`SingleThreadScheduledExecutor`**：使用的是DelayedWorkQueue无界延迟阻塞队列，队列中的任务需要等延迟到了才能运行。有可能OOM





- **监控线程池运行状态**



> Springboot自带的Actuator组件可以监控线程池的状态。
> 下面都是ThreadPoolExecutor自带的API



![1752215769875.png](https://fastly.jsdelivr.net/gh/thecoolboyhan/th_blogs@main/image/2025-07/1752215769875_1752215769888.png)





- 不同业务使用的不同的线程池

> 当线程池中的任务需要启动子线程运行任务时，切记不要使用相同的线程池提交任务。否则会发生死锁





相同线程池产生死锁的情况：父线程在等待子线程执行完成。子线程在等待父线程让出核心线程才能执行任务。







- **该如何设置核心线程数**



常规：



CPU密集型CPU：N

IO密集型CPU：M*N（M:整数，如2）







**严谨方式**

```
最佳线程数 = N（CPU 核心数）∗（1+WT（线程等待时间）/ST（线程计算时间））`，其中 `WT（线程等待时间）=线程运行总时间 - ST（线程计算时间）
```









[**美团技术团队的操作**](https://tech.meituan.com/2020/04/02/java-pooling-pratice-in-meituan.html)



来自于美团技术团队，点上方文字跳转源文



> 美团为了最大程度的利用CPU的多核性能，并行能力，总结了两个场景的线程管理方法。





- 快速响应客户请求

> 用户发起的实时请求，服务追求响应时间。比如用户查看一个商品的信息，需要将商品的价格、优惠、库存、图片等聚合起来展示



不设置队列去缓冲并发任务，调高corePoolSize和maxPoolSize去尽可能创造多的线程快速执行任务。





- 批处理任务

> 大量的报表，批量核算等任务。同时也想让任务加快，则更需要从吞吐量角度考虑。





应调整合适的核心线程数，最好不要让机器出现额外的未知的线程（不要使用最大线程数，不要把批处理服务器和正常接收的请求的服务放到同一台服务器）



利用固定的线程数，可以有效避免上下文的频繁切换。









- IO密集型和CPU密集型任务运行起来的情况差异非常大

IO密集型任务，CPU消耗小，适合把运行中的线程调多。

CPU密集型的任务，CPU消耗大，如果核心线程多。容易产生OOM，但如果线程少，响应慢。



> 最好可以动态化的调整线程

![1752283049617.png](https://fastly.jsdelivr.net/gh/thecoolboyhan/th_blogs@main/image/2025-07/1752283049617_1752283307154.png)



### 动态化线程池



- **简化线程池配置**：

线程池构造函数有7个参数，但最核心的是3个：核心线程数、最大线程数、等待队列。

简化方式：



1. **并行执行子任务，提高响应速度**：应该使用同步队列，所有子任务都不应该被缓存下来，应该立刻执行。
2. **并行执行大批次任务，提高吞吐量**：应该使用有界队列，使用队列去缓冲大批量的任务，队列容量必须固定，防止任务无限堆积。





- **参数可动态配置**

美团为了解决参数不好配，修改参数成本高等问题。在java线程池留有高扩展性的基础上，封装线程池，**允许线程池监听同步外部的消息，根据消息修改配置**。



- **增加线程池的监控**

在线程池的生命周期添加监控能力，时刻了解线程池的状态。



![1752284028374.png](https://fastly.jsdelivr.net/gh/thecoolboyhan/th_blogs@main/image/2025-07/1752284028374_1752284028396.png)





- 功能架构

![1752284156569.png](https://fastly.jsdelivr.net/gh/thecoolboyhan/th_blogs@main/image/2025-07/1752284156569_1752284156599.png)



- 实现方式

利用ThreadPoolExecutor提供的setter方法，设置核心线程数。最大线程数等。

![1752284432146.png](https://fastly.jsdelivr.net/gh/thecoolboyhan/th_blogs@main/image/2025-07/1752284432146_1752284432171.png)

用核心线程举例



1. 当前值小于原始值：中断多余的线程。
2. 当前值大于原始值：尝试消费队列中的任务。





- 队列如何控制？

美团自定义了一个ResizableCapacityLinkedBlockIngQueue队列，让他变为可变的。





- 线程池避坑

1. 不要重复创建线程池。特别不要在每次请求中创建线程池。
2. 线程池和ThreadLocal公用：由于核心线程是复用的，新的任务可能会从ThreadLocal中读取到老数据。如果没有显示的remove变量。变量依旧会保存在上下文中。这种情况会导致类加载器泄露，因为线程池中线程被重用，旧的ThreadLocal变量无法被回收。







### tomcat线程池（重点）



> tomcat重写了ThreadPool，新版本tomcat已支持使用虚拟线程来执行任务。
>
> tomcat在传统线程池调用逻辑上进行了修改，打破了传统线程池的任务处理方式。

- 参数列表

1. maxThreads:线程池中最大的活动线程数，默认为200.控制同时处理请求的最大线程数。当有新的HTTP请求到达时，如果当前有空闲线程（即当前活跃线程数小于maxThreads），Tomcat会直接使用这些空闲线程来处理请求。等maxThreads用尽后，才会让请求入队等待。
2. minSpareThreads：始终保持存活的线程数（线程池的核心线程数）默认为25，确保可以快速响应请求，避免创建线程的延迟。
3. maxIdleTime：空闲线程等待任务的最大时间，默认1分钟，超过此时间线程会被关闭。
4. threadPriority：线程优先级，默认为5（普通优先级）。影响操作系统对线程的调度。
5. daemon：是否为守护线程，默认为True。守护线程不会阻止JVM退出。（让JVM不会由于有请求在处理而无法关闭）
6. namePreFix：线程名称的前缀，默认`tomcat-exec-`
7. 任务队列的最大长度，默认为Integer.MAX_VALUE。所有线程都忙时，超出此长度的任务会被拒绝。
8. threadRenewalDelay：上下文停止后线程更新的延迟时间，默认为1秒。防止线程泄露。



- 不是线程池的参数，但依然会影响到线程池

acceptCount：当所有线程忙时，最大排队连接数。默认值为 100，超过则拒绝新连接。

maxConnections：服务器同时接受和处理的连接数上限，与线程池的 maxThreads 配合使用。（默认使用无界队列，但通过此参数可以控制队列中任务的数量）









- <font color='red'>**tomcat线程池源码中的运行逻辑**</font>

> tomcat重写了ThreadPool，重新设计了任务提交等方法。这也算是双亲委派机制的一种破坏



1. 通过addWorker(Runnable firstTask, boolean core)方法来接收任务，先尝试使用核心线程来运行任务。
2. 如果核心线程不能启动，则判断数量是否超过maxThreads
3. 如果没有超过maxThreads，则启动新线程处理
4. 如果超过maxThreads，则尝试让任务入队，如果队列中任务超过maximumPoolSize，则直接给客户端返回异常。









- **<font color='red'> 什么是线程泄露？为什么threadRenewalDelay可以防止线程泄露？</font>**

线程泄露指在多线程环境中，线程被创建但未能被正确终止或释放，导致这些线程一直占用系统资源（内存、CPU）。

tomcat中的内存泄露：

1. 未终止的线程：Web应用在运行时，可能通过new Thread（）或其他方式创建线程，但当应用停止（如Tomcat关闭或应用卸载），这些线程没有被正确终止。
2. ThreadLocal变量没有被清理：ThreadLocal中的变量无法被回收。



- 如何利用threadRenewalDelay防止上面的情况？

threadRenewalDelay的主要功能：

1. 定期更新线程：当一个Web应用上下文停止后，Tomcat会等待指定的延迟时间，然后更新线程池中的线程。这意味着旧的线程会被终止，新的线程会被创建。
2. 清理ThreadLocal变量：更新线程的过程中，Tomcat会确保旧线程上的ThreadLocal变量被清理，从而避免这些变量持有的引用导致的类加载器泄露。

> 所以后面提到的ThreadLocal中的内存泄露情况，在普通web调用中使用ThreadLocal，即使没有清理，也不会导致内存泄露。







## ThreadLocal



> Thread类有一个类型为ThreadLocal.ThreadLocalMap的变量threadLocals，每个线程都一个自己的ThreadLocalMap。

![1752286327130.png](https://fastly.jsdelivr.net/gh/thecoolboyhan/th_blogs@main/image/2025-07/1752286327130_1752286327153.png)

每个线程在往ThreadLocal里放值时，都会往自己的ThreadLocalMap里存。读也是在自己的map里找对应的key，从而达到线程隔离。



### 各种引用



- java的四种引用：

1. 强：普通new出的对象，垃圾回收器永远不会回收强引用的对象，哪怕内存不足
2. 软：使用softReference修饰的对象，软引用会在内存要溢出的时候被回收
3. 弱：使用WeakReference修饰的对象，只要发生垃圾回收，弱引用就会被回收
4. 虚：使用PhantomReference进行定义。



> ThreadLocal的key为弱引用。



- 内存泄露问题

ThreadLocal的key在GC后会被回收，但Thread对map的强引用还在，map中的value也同样存在。

![1752286993099.png](https://fastly.jsdelivr.net/gh/thecoolboyhan/th_blogs@main/image/2025-07/1752286993099_1752286993129.png)

> 上面的情况会出现value的值永远存在，导致内存泄露。



> TIPS：ThreadLocalMap使用的是开放寻址法，没有链表结构。



### 子线程如何获取父线程的数据

> 利用JDK的InheritableThreadLocal类获取父线程变量

``` java
public class InheritableThreadLocalDemo {
    public static void main(String[] args) {
        ThreadLocal<String> ThreadLocal = new ThreadLocal<>();
        ThreadLocal<String> inheritableThreadLocal = new InheritableThreadLocal<>();
        ThreadLocal.set("父类数据:threadLocal");
        inheritableThreadLocal.set("父类数据:inheritableThreadLocal");

        new Thread(new Runnable() {
            @Override
            public void run() {
                System.out.println("子线程获取父类ThreadLocal数据：" + ThreadLocal.get());
                System.out.println("子线程获取父类inheritableThreadLocal数据：" + inheritableThreadLocal.get());
            }
        }).start();
    }
}
```

结果：

> 子线程获取父类ThreadLocal数据：null
> 子线程获取父类inheritableThreadLocal数据：父类数据:inheritableThreadLocal



- 实现原理

父线程在创建子线程时，Thread#Init方法在构造方法中被调用，会将inheritableThreadLocal中的数据拷贝给子线程：

``` java
private void init(ThreadGroup g, Runnable target, String name,
                      long stackSize, AccessControlContext acc,
                      boolean inheritThreadLocals) {
    if (name == null) {
        throw new NullPointerException("name cannot be null");
    }

    if (inheritThreadLocals && parent.inheritableThreadLocals != null)
        this.inheritableThreadLocals =
            ThreadLocal.createInheritedMap(parent.inheritableThreadLocals);
    this.stackSize = stackSize;
    tid = nextThreadID();
}
```



## ForkJoinPool





### why ForkJoinPool

> 计算从1到10000的累加

- 传统方式

> 利用两个线程，分别拆分然后计算。

``` java
public class ExecutorTest {
    public static void main(String[] args) throws ExecutionException, InterruptedException {
//        用线程池计算从1到10000的累加
        ThreadPoolExecutor threadPoolExecutor= new ThreadPoolExecutor(10,100,1000, TimeUnit.MILLISECONDS,new LinkedBlockingDeque<>());
//        分两个线程计算，计算速度应对是单线程的两倍
        Future<Integer> future1 = threadPoolExecutor.submit(() -> {
            int sum = 0;
            for (int i = 0; i < 5000; i++) {
                sum += i;
            }
            return sum;
        });
        Future<Integer> future2 = threadPoolExecutor.submit(() -> {
            int sum = 0;
            for (int i = 5000; i <= 10000; i++) {
                sum += i;
            }
            return sum;
        });
        Integer s1 = future1.get();
        Integer s2 = future2.get();
        threadPoolExecutor.shutdown();
        System.out.println(s1+s2);
    }
}
```





## ForkJoinPool

> 利用forkJoin来拆分任务，首先定义：
>
> 如果增加数字的数量小于100，就不需要再拆分。
>
> 如果大于100个，任务会被二分。



任务拆分的代码：

``` java
public class SumTask extends RecursiveTask<Long> {

    private final int l;
    private final int r;

    public SumTask(int l, int r) {
        this.l = l;
        this.r = r;
    }
    @Override
    protected Long compute() {
        long res=0;
//        判断任务是否拆封
        if(r-l<100){
            for (int i = l; i <=r; i++) {
                res+=i;
            }
            return res;
        }
//        需要被拆封的情况：经典二分查找
        int mid=(l+r)/2;
        SumTask leftTask=new SumTask(l,mid);
        SumTask rightTask=new SumTask(mid+1,r);
        leftTask.fork();
        rightTask.fork();
        long left=leftTask.join();
        long right=rightTask.join();
        return left+right;
    }
}
```





任务执行的代码：

```java
public class ForkJoinExecutorTest1 {
    public static void main(String[] args) {
//        拆封核心线程来运行任务，共拆封10个
        try(ForkJoinPool forkJoinPool = new ForkJoinPool(10)){
            SumTask sumTask = new SumTask(1, 10000);
            ForkJoinTask<Long> future = forkJoinPool.submit(sumTask);
//            如果检测到错误，输出错误信息
            if (future.isCompletedAbnormally()) System.out.println(future.getException());
//            Thread.sleep(5000);
            System.out.println(future.get());
        } catch (InterruptedException | ExecutionException e) {
            throw new RuntimeException(e);
        }
    }
}
```



> 自由的拆分任务，合理的利用核心线程，对CPU有更强的利用率。



### 运行过程





1. 工作窃取算法

   每个工作线程（ForkJoinWorkerThread）都有自己的双端队列Deque，用于存储任务。

   当一个线程运行完自己的任务队列后，它可以从其他忙碌线程的队列头部获取任务，从而达到平衡负载。

2. 并行度

   并行度：只有多少个线程同时运行，默认为CPU可用的核心数，可以通过构造函数自定义。

3. 任务执行

   任务必须是ForkJoinTask的子类，支持fork（异步启动任务）和join（等待子任务完成）操作。

4. 内存可见

   每个任务中的status字段为volatile修饰的，保证状态的变化是可见的。



- 使用场景

1. 分治算法：归并排序、快速排序等。
2. 并行流：java8的并行流（parallelStream）底层基于ForkJoinPool
3. 异步任务：异步任务可以使用
4. 虚拟线程：虚拟线程内部也是ForkJoinPool实现的，不过是系统单独的pool，与commonPool公共池不相干。



### 坑





1. 公共池的滥用：commonPool公共池是整个JVM中共享的，很多公共组件也会使用公共池中资源，如果自定义的任务过长，会影响系统其他组件的运行。

   > 可以自定义创建独立的ForkJoinPool，但是使用起来需要特别小心

2. 任务分解不合理：实例中的拆封方式采取二分查找，且规定一个任务的最小单位为100，如果将单位设的过小，会特别浪费资源。

3. 异常处理：异常处理不会传播，每次拆封时都需要考虑异常情况。

   > 在拆分过程中，运行过程中，最好都用try-catch处理异常

4. 工作窃取：ForkJoin适合CPU密集型的任务，对于IO密集型任务（网络请求或文件读取等），其效率可能不如正常使用线程池，因为IO操作会阻塞线程， 影响工作窃取算法的效率。

5. **把ForkJoin与虚拟线程搞混**：虚拟线程虽然基于ForkJoin，但和ForkJoinpool不是一回事。ForkJoin更适合CPU密集型任务，不适合长任务或IO密集型任务。如果线程阻塞，ForkJoin就会被阻塞。虚拟线程适合IO密集型任务，如果CPU利用率高的任务，反而使用虚拟线程并不会带来什么好处。







- 如果任务拆分的不好会怎样？

ForkJoinTask任务是轻量级任务，任务内部包含拆分和运行两部分，如果代码开发不当，导致任务无限拆分，无限被提交。会导致堆内存溢出。



> 需要合理的拆分任务、设置任务的颗粒度。
> 同时也可以考虑是否采用一些别的框架：如powerJob等带MapReduce功能的框架。（但使用powerjob调度复杂，反而降低了效率）。





<font color='red'>**一定要做好getQueuedTaskCount队列大小监控，检测是否存在异常增长**</font>









## 虚拟线程

我[这篇关于虚拟线程](https://thecoolboyhan.github.io/p/java21%E6%A0%B8%E5%BF%83%E5%BA%93--%E5%B9%B6%E5%8F%91/)的文章，放到现在依然非常经典。













![1752329052241.png](https://fastly.jsdelivr.net/gh/thecoolboyhan/th_blogs@main/image/2025-07/1752329052241_1752329052265.png)







虚拟线程是轻量级线程，可减少编写、维护和调试高吞吐量并发应用程序的工作量。



> 从JDK19开始提供，JDK21中完成。



线程是可以调度的最小单元。它们彼此之间独立。

线程主要分两种：平台线程和虚拟线程。



### 简介

- 什么是平台线程？



平台线程被是操作系统的包装实现。平台线程在底层的操作系统线程上运行java代码，并且平台线程整个生命周期都是由操作系统线程完成的。因此，可用的平台线程数量受限于操作系统线程数量。



平台线程通常具有较大的线程栈和其他由操作系统维护的资源。它们适合执行各种任务，但是可能是一种有限的资源。（操作系统的线程数有限）





- 什么是虚拟线程？





像平台线程一样，虚拟线程也是java.lang.Thread类的一个实例。然而虚拟线程并不绑定特定的操作系统线程上。虚拟线程仍然在操作系统线程上运行。然而，当在虚拟线程中运行的代码调用阻塞I/O操作时，java会暂停该虚拟线程，知道它可以恢复。与被暂停的虚拟线程相关联的操作系统线程可以自由的为其他虚拟线程执行操作。







虚拟线程的实现方式类似于虚拟内存。为了模拟大量内存，操作系统将一个大的虚拟空间映射到有限的RAM上。同样，为了模拟大量线程，java将大量虚拟线程映射到少量的操作系统线程上。







与平台线程不同，虚拟线程通常具有较浅的调用栈，只执行少量操作，例如：单个HTTP客户端调用或单个JDBC查询。虽然虚拟线程支持线程局部变量和可继承线程局部变量，但需要谨慎使用，因为单个JVM可能支持数百万个虚拟线程。







> 虚拟线程适合运行大部分时间被阻塞的任务，这些任务通常在等待i/o操作完成。虚拟线程不适合运行长时间的CPU密集型操作。





- 为什么使用虚拟线程？





在高吞吐量的并发应用程序中使用虚拟线程，特别是那些由大量并发任务组成的应用程序，这些任务大部分时间都在等待。服务器应用程序就是高吞吐量应用程序的例子，因为它们通常执行许多阻塞I/O操作的客户端请求。







> 虚拟线程并不是更快的线程：它的运行速度和平台线程没有区别。虚拟线程存在的目的是为了提供规模（更高的吞吐量），而不是速度（更低的延迟）。





### 创建和使用虚拟线程



> 以下项目代码可以我的另一个项目(personStudy)中找到

#### 使用Thread类和使用Thread.Builder 接口来创建虚拟线程







- 使用Thread类创建虚拟线程



```java

private static void createByThread() throws InterruptedException {

    Thread thread = Thread.ofVirtual().start(() -> System.out.println("Hello"));

//    join是为了让虚拟线程插队到主线程之前，保证在主线程结束之前可以看到虚拟线程的打印

    thread.join();

  }

```







- 通过Thread.Builder创建







```java
//创建一个线程
**private static void createByThreadBuilder1() throws InterruptedException {
    Thread.Builder builder = Thread.ofVirtual().name("virtualThread");
//    同样可以用来创建平台线程,所有其他API都兼容
//    Thread.Builder builder = Thread.ofPlatform().name("PlatformThread");
    Runnable task= () -> {
      System.out.println("Running thread");
    };
    Thread t = builder.start(task);
    System.out.println("Thread t name"+t.getName());
    t.join();
}
```







- 通过builder快速创建两个虚拟线程并启动

```java
private static void createByThreadBuilder2() throws InterruptedException {
    Thread.Builder builder=Thread.ofVirtual().name("worker-",0);
    Runnable task=()->{
     System.out.println("Thread ID:"+Thread.currentThread().threadId());
    };
//启动后会总动给start+1.
    Thread t1 = builder.start(task);
    t1.join();
    System.out.println(t1.getName()+" terminated");
    Thread t2 = builder.start(task);
    t2.join();
    System.out.println(t2.getName()+" terminated");
}
```





#### 使用Executors创建虚拟线程



> Future.get()会自动上锁等待任务返回，所以不需要join方法



```java
private static void createByExecutors(){
  try(ExecutorService myExecutor = Executors.newVirtualThreadPerTaskExecutor()){
    Future<?> future = myExecutor.submit(() -> System.out.println("Running thread"));
    future.get();

    System.out.println("task completed");
  } catch (ExecutionException | InterruptedException e) {
    throw new RuntimeException(e);
  }
}

```





#### 实例



> 客户端向服务器发送消息，服务器将每个请求都用一个虚拟线程来处理。



- 服务端



```java
public class EchoServer {
		public static void main(String[] args) {

//    if(args.length != 1){
//      System.out.println("usage: java EchoServer <port>");
//      System.exit(0);
//    }

    int port = 8080;

//    传入端口号
//    int port = Integer.parseInt(args[0]);

    try(

        ServerSocket serverSocket = new ServerSocket(port)
   ){

      while(true){
//      不知道hostname
//        System.out.println(serverSocket.getInetAddress().getHostName());
//       获取到连接请求，创建一个虚拟线程来处理
        Socket clientSocket = serverSocket.accept();

//        创建虚拟线程的方式为Thread类
        Thread.ofVirtual().start(()->{
          try(
//            输入输出流
             PrintWriter out = new PrintWriter(clientSocket.getOutputStream(),true);
             BufferedReader in = new BufferedReader(new InputStreamReader(clientSocket.getInputStream()))
         ) {
//            获取客户端发送来的请求
            String inputLine;
            while((inputLine=in.readLine())!=null){
              System.out.println(inputLine);
              out.println(inputLine);
            }
          } catch (IOException e) {
            e.printStackTrace();
          }
        });
      }
    } catch (IOException e) {
      System.out.println(e.getMessage());
    }
  }
}
```





- 客户端

```java
public class EchoClient {
  public static void main(String[] args) throws IOException {
    if(args.length!=2){
      System.out.println(args.length);
      for (String arg : args) {
        System.out.println(arg);
      }
      System.out.println("Usage: EchoClient <host> <port>");
      System.exit(1);
    }
    String hostName=args[0];
    int port=Integer.parseInt(args[1]);
    try(
        Socket echoSocket = new Socket(hostName,port);
        PrintWriter out = new PrintWriter(echoSocket.getOutputStream(),true);
        BufferedReader in = new BufferedReader(new InputStreamReader(echoSocket.getInputStream()))
    ){
      BufferedReader bufferedReader = new BufferedReader(new InputStreamReader(System.in));
      String userInput;
      while((userInput=bufferedReader.readLine())!=null){
        out.println(userInput);
        System.out.println("echo:"+in.readLine());
        if (userInput.equals("bye")) break;
      }
    }
  }
}
```

### 调度虚拟线程和固定虚拟线程

当虚拟线程开始运行时，java runtime会将虚拟线程分配或挂载到平台线程上，然后操作系统会像往常一样调度该平台线程。虚拟线程运行一段代码后，java runtime可以将该虚拟线程从平台线程上卸载。（在虚拟线程发生IO操作阻塞时）空闲的平台线程可以被java运行时重新挂载一个新的虚拟线程。

#### 虚拟线程无法被卸载的情况

在虚拟线程执行以下阻塞操作时，无法被java runtime卸载：

- 当执行被synchronized修饰的同步代码块（被上锁的代码）
- 运行本地方法或外部函数时

#### 虚拟线程使用指南





- 非阻塞风格开发的代码，即使使用虚拟线程，也不会有多大提升

```java
CompletableFuture.supplyAsync(info::getUrl, pool)
  .thenCompose(url -> getBodyAsync(url, HttpResponse.BodyHandlers.ofString()))
  .thenApply(info::findImage)
  .thenCompose(url -> getBodyAsync(url, HttpResponse.BodyHandlers.ofByteArray()))
  .thenApply(info::setImageData)
  .thenAccept(this::process)
  .exceptionally(t -> { t.printStackTrace(); return null; });
```









- 以同步风格开发的代码，使用虚拟线程将带来极大的提升

```java
try {
  String page = getBody(info.getUrl(), HttpResponse.BodyHandlers.ofString());
  String imageUrl = info.findImage(page);
  byte[] data = getBody(imageUrl, HttpResponse.BodyHandlers.ofByteArray());  
  info.setImageData(data);
  process(info);
} catch (Exception ex) {
  t.printStackTrace();
}
```

- 将每个并发任务表示为一个虚拟线程；永远不用对虚拟线程进行池化



> 尽管虚拟线程的行为与平台线程相同，但不是相同的程序概念。



平台线程稀缺，所以需要使用线程池来管理。（线程池中的平台线程数始终小于等于最大线程数）



虚拟线程众多，每个线程都不应该代表某种共享的、池化的资源，而应代表一个任务。虚拟线程的数量始终等于程序中的并发任务数量。





> 应该将每个任务表示为一个虚拟线程

```java
try (var executor = Executors.newVirtualThreadPerTaskExecutor()) {
  Future<ResultA> f1 = executor.submit(task1);
  Future<ResultB> f2 = executor.submit(task2);
  // ... use futures
}
```



Executors.newVirtualThreadPerTaskExecutor()不会返回线程池，它为每个提交的任务都创建一个新的虚拟线程。





- 同时向多个服务器发起注销操作

```java
void handle(Request request, Response response) {
  var url1 = ...
  var url2 = ...

  try (var executor = Executors.newVirtualThreadPerTaskExecutor()) {
    var future1 = executor.submit(() -> fetchURL(url1));
    var future2 = executor.submit(() -> fetchURL(url2));
    response.send(future1.get() + future2.get());
  } catch (ExecutionException | InterruptedException e) {
    response.fail(e);
  }
}

String fetchURL(URL url) throws IOException {
  try (var in = url.openStream()) {
    return new String(in.readAllBytes(), StandardCharsets.UTF_8);
  }
}
```

#### 使用信号量限制并发

- 平台线程使用池化技术来限制并发

```java
ExecutorService es = Executors.newFixedThreadPool(10);
...
Result foo() {
  try {
    var fut = es.submit(() -> callLimitedService());
    return f.get();
  } catch (...) { ... }
}
```





> 线程池限制并发数量只是附带效果，线程池主旨在于共享稀缺资源，而虚拟线程不是稀缺资源，因此永远不应被池化。





- 使用semaphore来限制虚拟线程的并发数量

```java
Semaphore sem = new Semaphore(10);
...
Result foo() {
  sem.acquire();
  try {
    return callLimitedService();
  } finally {
    sem.release();
  }
}
```






![67bc238255790.png](https://fastly.jsdelivr.net/gh/thecoolboyhan/th_blogs@main/image/2025-05/67bc238255790_1747189632774.png)




- 不要在虚拟线程中创建复杂的线程独享变量
- 在虚拟线程内部使用synchronized代码块，会阻塞OS线程。可以试着把synchronized放到虚拟线程外面或者使用ReentrantLock



```java
synchronized(lockObj) {
  frequentIO();
}
```



替换后：

```java
lock.lock();
try {
  frequentIO();
} finally {
  lock.unlock();
}
```









### 原理



- 虚拟线程的Thread类和平台线程的Thread并不相同，虚拟线程使用的是VirtualThread，继承自平台Thread。整个VirtualThread都是重新设计的。



> 虚拟线程统一由JVM调度，当遇到阻塞时，JVM暂停该虚拟线程并调度其他虚拟线程。





- 创建和调度

JVM会创建一个拥有固定核心数的ForkJoinPool，此ForkJoinPool的核心池由虚拟线程独有，与JVM自带的公共池不冲突。每次虚拟线程运行是，会绑定到ForkJoinPool中的平台线程运行，并且遇到阻塞时，会让出平台线程，给其他虚拟线程使用。





- 续体和切换

续体：虚拟线程会保存当前运行状态（堆栈和局部变量）。

切换：ForkJoinPool继续消费队列中的其他虚拟线程，相当于虚拟线程遇到阻塞时，会自动调用forkJoin中的join方法，切换到其他子任务运行。







- mount和unmount

挂载当前到平台线程、从平台线程中解绑当前虚拟线程





### ThreadContainers

> JDK的内部类，用来管理虚拟线程和平台线程的层次结构。



用树形结构来存储，每次提交或者运行数据时，通过ThreadContainers.root()来启动和遍历虚拟线程与平台线程，然后运行。





有了ThreadContainers，可以管理上百万个虚拟线程。

### Thread常用API和虚拟线程API实现对比





| API                                  | 平台线程                                                     | 虚拟线程                                                     |
| ------------------------------------ | ------------------------------------------------------------ | ------------------------------------------------------------ |
| 创建                                 | 继承Thread类，重写run方法<br />实现Runnable接口并传递给Thread | Thread.ofVirtual().start(Runnable)<br />Thread.Builder.virtual() |
| start                                | 用synchronized锁定当前线程对象(为了保证一线程只能被启动一次)，使用start0方法调用操作系统启动线程。 | 使用start(ThreadContainers.root())方法，从根开始调用虚拟线程，并不会固定的启动某个虚拟线程。尝试安排此虚拟线程启动，最后还是会交给ForkJoinPool来实现调度。 |
| join                                 | synchronized锁住当前线程，然后无限wait（0）                  | 利用CountDownLatch来实现await操作，直到超时或者CountDownLatch被归零 |
| wait                                 | 利用操作系统wait0方法，来实现等待监听Monitor对象             | 同平台线程，只是在被打断时，会清理走虚拟线程独有的打断方法   |
| interrupt                            | synchronized锁住当前线程，调用interrupt0方法，打断操作系统线程。 | 锁住线程的interruptLock，调用unpark方法解除当前虚拟线程的锁（unsafe操作） |
| sleep                                | 创建一个event实现，调用sleep0方法，让操作系统执行睡眠。睡眠结束后，提交sleepevent事件 | 调用虚拟线程类中的ScheduledExecutorService定时任务线程池，创建一个睡眠时间的定时任务。等到固定时间，会unpark当前虚拟线程。<font color='red'>（就是利用定时任务线程池，使得多个虚拟线程同时sleep，且同时被唤醒）</font> |
| notify                               | 唤醒等待此对象的监视器（monitor）中的线程，是synchronized的原理，与线程本身无关 | 与虚拟线程无关                                               |
| yield                                | 调用yield0方法，让操作系统调度当前线程退出CPU                | 尝试修改当前虚拟线程的运行状态为YIELDING，让平台线程重新竞争一次虚拟线程。 |
| LockSupport工具类                    | 通过每个平台线程都有的许可变量，调用操作系统park方法，park让许可变为0，unpark 让许可变为1。实现高效的加锁解锁 | 利用JavaLangAccess对当前虚拟线程实现续体操作，让出绑定的平台线程给其他虚拟线程调度。 |
| 利用BufferedReader等实现的IO读写操作 | 也是利用LockSupport.park实现上锁操作，等读取到数据后再解锁   | 由于利用LockSupport故而不会阻塞平台线程                      |



注：ReentrantLock等lock工具类，都是使用LockSupport或AQS上锁工具与框架实现。均不会阻塞虚拟线程。

> <font color='red'>综上所述，其实平台线程中的所有阻塞方法，在虚拟线程中都是非阻塞的。</font>所以虚拟线程可是实现真正意义上的“虚拟概念”，如果需要进入传统的阻塞方法，都是由JVM平台自己来实现的。不会调用操作系统的方法来真正的阻塞线程。



但是，如果虚拟线成的平台线程，因为锁等情况被阻塞了，就还是会正常的走平台线程的阻塞方法，让虚拟线程也暂停运行。







### 注意事项



- 虚拟线程在什么情况下会阻塞（老黄历了，pinning问题在JDK24被解决）？

从上面得知，虚拟线程在传统java实现的阻塞方法中，都不会被阻塞。就是无论是IO阻塞还是LockSupport实现的java自定义锁都不会阻塞虚拟线程。但如果调用synchronized同步工具，会调用操作系统wait方法，阻塞平台线程，故而阻塞虚拟线程。（虚拟线程被阻塞是由于synchronized的上锁方式，由操作系统实现，操作系统不会感知虚拟线程故而阻塞虚拟线程绑定的平台线程）。





- 不要池化虚拟线程

java官方说明虚拟线程大小只有几kb，并非稀缺资源，所以不应当也不能被池化。Executors.newVirtualThreadPerTaskExecutor只是提供了一个使用虚拟线程的API（为了和平台线程统一API，方便使用）。并不会真正的创建虚拟线程池。





- pinning问题解决

传统synchronized会调用操作系统wait方法，通过轻量级线程或Monitor对象阻塞平台线程，导致绑定在平台线程上的虚拟线程也被阻塞。现在当平台线程被wat阻塞后，卸载虚拟线程，通知后重新调度，可能使用新载体。





- ThreadLocal内存

每个虚拟线程都有自己的ThreadLocal，但虚拟线程理论上是无限的资源，因此要谨慎使用虚拟线程的ThreadLocal。



- 虽然使用了ForkJoinPool但只合适IO密集型任务

ForkJoinPool可以分解任务，窃取其他线程任务，增加CPU的利用率。非常适合CPU密集型任务。

但同样使用了ForkJoinPool实现的虚拟线程，却更适用于IO密集型任务。因为ForkJoinpool只是虚拟线程的载体， 虚拟线程真正优秀的是他几乎所有的阻塞场景，都开发了虚拟线程非阻塞的应对方式。当虚拟线程阻塞时，就取消挂载当前虚拟线程，转让其他虚拟线程挂载到载体线程上。









## 结构化并发(扩展)





> 将运行在不同线程中的相关任务组视为一个工作单元，从而简化错误处理和取消操作，提高可靠性，增强可观察性。



- StructuredTaskScope

可以将每个子任务分叉，让它们在各自独立线程中运行。StructuredTaskScope可以确保在主任务继续之前完成所有子任务。或者可以指定某个子任务成功时程序继续运行。


### StructuredTaskScope的用法

1. 创建一个StructuredTaskScope，使用“try-with-resources”语法一起（自动关闭）
2. 将子任务定义为callable实例。
3. 使用“StructuredTaskScope::fork”语法在各自线程中为每个子任务创建分支。
4. 调用StructuredTaskScope::join 
5. 处理子任务的结果
6. 关闭StructuredTaskScope



![67bd253b95065.png](https://fastly.jsdelivr.net/gh/thecoolboyhan/th_blogs@main/image/2025-05/67bd253b95065_1747189902643.png)

``` java
    Callable<String> task1 = ...
    Callable<Integer> task2 = ...

    try (var scope = new StructuredTaskScope<Object>()) {

        Subtask<String> subtask1 = scope.fork(task1);
        Subtask<Integer> subtask2 = scope.fork(task2);

        scope.join();

        ... process results/exceptions ...

    } // close
```


### ShutdownOnSuccess和ShutdownOnFailure

- ShutdownOnFailure

其中一个子任务失败，就取消所有子任务。



- ShutdownOnSuccess

其中一个子任务成功，就取消剩余所有的子任务。



``` java
public class SCRandomTasks {

    class TooSlowException extends Exception {
        TooSlowException(String s){
            super(s);
        }
    }

    /**
     分别启动5个任务，调用成功关闭和失败关闭。
     */
    public static void main(String[] args) {
        var myApp = new SCRandomTasks();
        try{
            System.out.println("Running handleShutdownOnFailure...");
            myApp.handleShutdownOnFailure();
        } catch (ExecutionException | InterruptedException e) {
            System.out.println(e.getMessage());
        }
        try{
            System.out.println("Running handleShutdownOnSuccess...");
            myApp.handleShutdownOnSuccess();
        } catch (ExecutionException | InterruptedException e) {
            System.out.println(e.getMessage());
        }
    }

    public Integer randomTask(int max,int threshold) throws TooSlowException, InterruptedException {
        int t = new Random().nextInt(max);
        System.out.println("Duration:"+t);
        if(t>threshold) throw new TooSlowException(STR."Duration \{t} greater than threshold \{threshold}");
        Thread.sleep(t);
        return t;
    }

    void handleShutdownOnSuccess() throws InterruptedException, ExecutionException {
        try(var scope=new StructuredTaskScope.ShutdownOnSuccess()){
            IntStream.range(0,5)
                    .mapToObj(i->scope.fork(()->randomTask(1000,850)))
                    .toList();
            scope.join();
//            捕获第一个完成的子任务，并返回其结果。
            System.out.println(STR."First task to finish: \{scope.result()}");
        }
    }

    void handleShutdownOnFailure() throws InterruptedException, ExecutionException {
        try(var scope=new StructuredTaskScope.ShutdownOnFailure()){
//            var t= new SCRandomTasks();
            var subtasks= IntStream.range(0,5)
                    .mapToObj(i->scope.fork(new Callable<Integer>() {
                        @Override
                        public Integer call() throws Exception {
                            return randomTask(1000,850);
                        }
                    }))
                    .toList();
//            捕获子任务抛出的第一个异常，然后调用该方法:中断所有新的子任务启动，中断所有正在运行的其他子任务线程，并让主程序继续执行。
            scope.join()
                    .throwIfFailed();
            var totalDuration=subtasks.stream()
                    .map(StructuredTaskScope.Subtask::get)
                    .reduce(0,Integer::sum);
            System.out.println(STR."Total Duration:\{totalDuration}");
        }

    }
}
```


### 自定义结构化任务策略

```java
public class CollectingScope<T> extends StructuredTaskScope<T> {
    private final Queue<Subtask<?extends T>> successSubtasks=new LinkedTransferQueue<>();
    private final Queue<Subtask<?extends T>> failedSubtasks=new LinkedTransferQueue<>();

    @Override
    protected void handleComplete(Subtask<? extends T> subtask) {
        if(subtask.state()==Subtask.State.SUCCESS) successSubtasks.add(subtask);
        else if (subtask.state()==Subtask.State.FAILED) failedSubtasks.add(subtask);
    }

    @Override
    public StructuredTaskScope<T> join() throws InterruptedException {
        super.join();
        return this;
    }
    public Stream<Subtask<? extends T>> successfulTasks(){
        super.ensureOwnerAndJoined();
        return successSubtasks.stream();
    }
    
    public Stream<Subtask<? extends T>> failedTasks(){
        super.ensureOwnerAndJoined();
        return failedSubtasks.stream();
    }
}
```









``` java
import java.util.concurrent.StructuredTaskScope;
import java.util.concurrent.Callable;
import java.util.stream.Stream;

record Response(String user, int order) {}

class StructuredConcurrencyExample {
    Response handle() throws InterruptedException {
        try (var scope = StructuredTaskScope.open()) { // 默认 Joiner，等待所有子任务完成
            var userTask = scope.fork(() -> findUser()); // 子任务1：获取用户
            var orderTask = scope.fork(() -> fetchOrder()); // 子任务2：获取订单
            scope.join(); // 等待所有子任务完成
            return new Response(userTask.get(), orderTask.get()); // 提取结果
        } catch (Exception e) {
            throw new RuntimeException("Task failed", e);
        }
    }

    String findUser() throws InterruptedException {
        Thread.sleep(1000); // 模拟 I/O 操作
        return "User123";
    }

    int fetchOrder() throws InterruptedException {
        Thread.sleep(1500); // 模拟 I/O 操作
        return 456;
    }

    public static void main(String[] args) throws InterruptedException {
        var example = new StructuredConcurrencyExample();
        System.out.println(example.handle());
    }
}
```











> 用时一个多月终于完成了本文。



