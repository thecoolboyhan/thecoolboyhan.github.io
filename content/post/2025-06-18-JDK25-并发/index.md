---
title: 备战JDK25--并发
description: JDK25今年年底就要发布了，这次深入了解结构化并发和各种并发框架，争取一起搞清后面几年的并发
slug: JDK25-2
date: 2025-06-18 00:00:00+0000
image: 1.png
categories:
    - java
    - 精选
tags: 
    - java
    - 多线程
    - 结构化并发
    - 并发
---





# JDK25 并发



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



### Phaser（"分段锁"）



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





- 动态线程池

