---
title:  NettyIO模型
description: 深入介绍NettyIO模型
image: 20205-05-29.png
date: 2025-07-02
categories: 
  - 精选
tags:
  - netty
  - java
  - io模型
---





# nettyIO模型



## BIO


先上代码：

``` java
//所有的操作都是阻塞的
public class SocketServer {
    public static void main(String[] args) throws IOException {
        ServerSocket serverSocket = new ServerSocket(9000);
        while(true){
            System.out.println("等待连接");
//            阻塞的
            Socket clientSocket = serverSocket.accept();
            System.out.println("有客户端连接了。。");
         		handler(clientSocket);
        }
    }

    private static void handler(Socket clientSocket) throws IOException {
        byte[] bytes = new byte[1024];
        System.out.println("准备read。。。");
//        接收客户端的数据，阻塞方法，没有数据可读时就阻塞
        int read = clientSocket.getInputStream().read(bytes);
        System.out.println("read完毕");
        if(read!=-1){
            System.out.println("接收到客户端的数据："+new String(bytes,0,read));
        }
        System.out.println("end");
    }
}
```



- 目前的缺陷

主程序采用单线程阻塞处理。同一时间只能处理一个连接，如果此连接没有处理结束，其他的客户端也无法连接。

- 如何优化？

在BIO的基础上，增加多线程操作，每次来一个线程就启动一个新的线程来处理。



```java
//所有的操作都是阻塞的
public class SocketServer {
    public static void main(String[] args) throws IOException {
        ServerSocket serverSocket = new ServerSocket(9000);
        while(true){
            System.out.println("等待连接");
//            阻塞的
            Socket clientSocket = serverSocket.accept();
            System.out.println("有客户端连接了。。");
//            在单线程上做优化，每接收的一个连接，就开启一个新的线程来处理
            Thread.ofPlatform().start(()->{
                try {
                    handler(clientSocket);
                } catch (IOException e) {
                    e.printStackTrace();
                }
            }).start();
        }
    }

    private static void handler(Socket clientSocket) throws IOException {
        byte[] bytes = new byte[1024];
        System.out.println("准备read。。。");
//        接收客户端的数据，阻塞方法，没有数据可读时就阻塞
        int read = clientSocket.getInputStream().read(bytes);
        System.out.println("read完毕");
        if(read!=-1){
            System.out.println("接收到客户端的数据："+new String(bytes,0,read));
        }
        System.out.println("end");
    }
}
```



### 问题

虽然可以同时处理多个请求了，但是当“C10K”时。会同时创建大量的线程，会占用大量的内存。

> C10K：同时有1万请求打到服务器
>
> C10M：同时有1千万请求打到服务器





### 使用池化技术来优化

如果使用线程池来处理请求，虽然可以同时处理部分请求，但是如果线程池的核心线程都被阻塞，就无法再处理其他请求了。（全部在阻塞队列中等待）



### 使用虚拟线程

其实上面所有的问题就可以在BIO的基础上直接使用虚拟线程技术来解决，但今天的重点不是这个下面只给出优化代码。

> 但虚拟线程不适合则长时间的处理，尽量处理小任务，如果存在大量复杂的处理。虚拟线程仍然有问题。

```java
Thread.ofVirtual().start(()->{
    try {
        handler(clientSocket);
    } catch (IOException e) {
        e.printStackTrace();
    }
}).start();
```



> 接下来就需要使用NIO了



## NIO

先上代码



```java
public class NioServer {
    
    static List<SocketChannel> channelList=new ArrayList<>();
    public static void main(String[] args) throws IOException {
//        Nio的服务channel，类似于BIO的ServerSocket
        try (ServerSocketChannel serverSocket = ServerSocketChannel.open()) {
//            将此ServerSocket绑定到9000端口
            serverSocket.socket().bind(new InetSocketAddress(9000));
//            将channel设置成非阻塞的
            serverSocket.configureBlocking(false);
            System.out.println("服务器启动成功");
            
            while (true) {
//                NIO的非阻塞操作由操作系统实现的，底层调用了linux的accept函数
                SocketChannel socketChannel = serverSocket.accept();
//                检测到连接
                if (socketChannel != null) {
                    System.out.println("连接成功");
//                    设置soocketChannel也是非阻塞
                    socketChannel.configureBlocking(false);
//                    把当前SocketChannel入队，方便后面轮询处理
                    channelList.add(socketChannel);
                }
                //            处理连接的请求
                Iterator<SocketChannel> iterator = channelList.iterator();
                while (iterator.hasNext()) {
                    SocketChannel sc = iterator.next();
//                    利用直接内存来处理请求
                    ByteBuffer byteBuffer = ByteBuffer.allocate(6);
                    int len = sc.read(byteBuffer);
                    if (len > 0) {
                        System.out.println("接收的消息："+new String(byteBuffer.array()));
                    }else if (len==-1){//如果断开连接，就出队
                        iterator.remove();
                        System.out.println("客户端断开了连接");
                    }
                }
            }
        }
    }
}
```



虽然是一个线程来处理了所有的请求，且请求的处理理论没有数量限制。

但依然存在一些问题

### 问题

1. while（true）一直占用CPU，CPU的一个核心被占用了。
2. 存在过多无用处理：如果暂存集合中数量特别多，且真正需要处理的请求可能只有一两个。但如果想要处理仍然需要遍历整个集合。



- 优化剪枝



## IO多路复用

直接上代码

```java
public class NioSelectorServer {
    public static void main(String[] args) throws IOException {
        try (ServerSocketChannel serverSocketChannel = ServerSocketChannel.open();
//            打开系统Selector处理Channel，创建epoll
             Selector selector = Selector.open();) {
            serverSocketChannel.socket().bind(new InetSocketAddress(9000));
            serverSocketChannel.configureBlocking(false);
//            把Channel注册到Selector上，并让Selector选择连接事件
            serverSocketChannel.register(selector, SelectionKey.OP_ACCEPT);
            System.out.println("服务器启动成功");
            while (true){
//                阻塞等待需要处理的事件
                selector.select();
//                返回有事件的key
                Set<SelectionKey> selectionKeys = selector.selectedKeys();
                Iterator<SelectionKey> iterator = selectionKeys.iterator();
//                遍历处理有事件的请求
                while(iterator.hasNext()){
                    SelectionKey key = iterator.next();
//                    如果是连接事件
                    if(key.isAcceptable()){
                        try (ServerSocketChannel server = (ServerSocketChannel) key.channel()) {
                            SocketChannel socketChannel = server.accept();
                            socketChannel.configureBlocking(false);
//                            给当前连接注册读取时间
                            socketChannel.register(selector, SelectionKey.OP_READ);
                            System.out.println("客户端连接成功了");
                        }
//                        如果是读事件
                    }else if(key.isReadable()){
                        try (SocketChannel server = (SocketChannel) key.channel()) {
                            ByteBuffer byteBuffer = ByteBuffer.allocate(6);
                            int len = server.read(byteBuffer);
                            if(len >0){
                                System.out.println("接收的请求:"+new String(byteBuffer.array()));
                            }else if (len == -1){
                                System.out.println("客户端连接断开");
                                server.close();
                            }
                        }
//                        当前事件已经被处理，删除当前数据
                        iterator.remove();
                    }
                }
            }
        }
        
    }
}
```



通过上面的方式，可以完美解决普通NIO中的问题



如果selector检测不到事件，就处于阻塞状态。不会占用CPU



不会存在多余处理，只有有事件的请求才会被程序处理。没有事件的连接都处于挂起状态。



### Selector

> 允许一个线程同时管理多个Channel，选择器可以在非阻塞的模式下高效处理多个连接，减少线程切换的开销。



- 选择器的核心作用

1. 监控多个通道的状态（监听事件）
2. 减少线程数量，一个线程可以管理多个IO连接
3. 提高性能，避免传统阻塞IO为每个连接创建线程的开销



- 工作原理

1. **注册通道**：将 `SelectableChannel`（如 `SocketChannel`）注册到 `Selector`，并指定感兴趣的事件（如 `OP_READ`、`OP_WRITE`）。

2. **监听事件**：调用 `select()` 方法，阻塞直到至少有一个通道就绪。

3. **处理事件**：遍历 `SelectionKey` 集合，执行相应的 I/O 操作。



- 事件

| 事件类型事件类型 | 描述描述                                          |
| ---------------- | ------------------------------------------------- |
| `OP_ACCEPT`      | 服务器端 `ServerSocketChannel` 接收到新的连接请求 |
| `OP_CONNECT`     | 客户端 `SocketChannel` 连接成功                   |
| `OP_READ`        | 通道中有数据可读                                  |
| `OP_WRITE`       | 通道可以写入数据                                  |



由java.nio.channels.spi类中创建，取系统默认的java.nio.channels.spi.SelectorProvider。



### linux：epoll



- 工作原理

`epoll_create()`：创建 `epoll` 实例，返回一个文件描述符（FD）。

`epoll_ctl()`：向 `epoll` 实例中添加、修改或删除文件描述符（FD）。

`epoll_wait()`：等待事件发生，并返回就绪的文件描述符。



- 相比传统的优点

1. 事件驱动：相比 `select` 和 `poll`，`epoll` 采用 **事件驱动** 机制，避免了轮询所有文件描述符的开销。
2. 就绪列表：`epoll` 维护一个 **就绪列表**，只返回发生事件的文件描述符，而不是遍历整个 FD 集合。
3. **支持大规模连接**：`epoll` 可以处理 **百万级别** 的连接，而不会因为 FD 数量增加而导致性能下降。



### macOS和BSD：kqueue



- 工作原理：

`kqueue()`：创建一个事件队列。

`kevent()`：用于注册、修改或删除事件，并等待事件发生。



- 优点：

1. **低开销**：`kqueue` 采用 **事件驱动** 机制，减少了 CPU 轮询开销。
2. **支持多种事件类型**：不仅支持 **I/O 事件**，还支持 **进程、信号、定时器** 等事件。



### Windows：IOCP



- 工作原理：

`CreateIoCompletionPort()`：创建一个完成端口（Completion Port）。

`PostQueuedCompletionStatus()`：用于提交 I/O 任务。

`GetQueuedCompletionStatus()`：用于获取完成的 I/O 任务。



- 优点：

1. **异步 I/O**：IOCP 采用 **异步事件驱动** 机制，减少了线程切换开销。
2. **高吞吐量**：IOCP 适用于 **高并发服务器**，如 Windows Server 上的 Web 服务器。



### 其他系统：select或poll

- 工作原理

`select()`：遍历所有文件描述符，检查哪些是可读、可写或有异常。

`poll()`：采用类似 `select` 的方式，但使用 **动态数组** 代替固定大小的 FD 集合。



- 缺点：

1. **性能较低**：`select` 需要遍历整个 FD 集合，导致 **O(n)** 级别的时间复杂度。
2. **FD 限制**：`select` 只能处理 **1024** 个文件描述符，而 `poll` 没有这个限制。



### 总结



Java NIO 选择器的实现位于 `sun.nio.ch` 包中，不同操作系统会加载不同的 SelectorProvider：

- **Linux**：`sun.nio.ch.EPollSelectorImpl`
- **macOS / BSD**：`sun.nio.ch.KQueueSelectorImpl`
- **Windows**：`sun.nio.ch.WindowsSelectorImpl`
- **其他系统**：`sun.nio.ch.PollSelectorImpl`

当 Java 程序调用 `Selector.open()` 时，JVM 会根据操作系统自动选择合适的实现。



- 性能对比

| 操作系统        | 底层实现          | 主要特点                       |
| --------------- | ----------------- | ------------------------------ |
| **Linux**       | `epoll`           | 高效事件驱动，适用于大规模连接 |
| **macOS / BSD** | `kqueue`          | 低开销，支持多种事件类型       |
| **Windows**     | `IOCP`            | 异步 I/O，适用于高吞吐量服务器 |
| **其他系统**    | `select` / `poll` | 适用于较旧系统，但性能较低     |



> 10万级别的请求IO多路可以勉强处理

### 依然有缺点

当连接数量建立的比较多，且每个连接收发都相当频繁时，一次selectkey操作可能就会出现上万个事件需要处理。大部分请求处理慢，造成用户体验极差，且可能导致服务器暂时无法处理，







## 反应器模式（Reactor）





> 用于处理并发请求的事件设计模式。通过一个中央事件处理器（Reactor）来监听资源上的事件，在事件发生时将这些事件分派到注册的事件处理器，从而实现高效的并发处理。能够在单线程中管理大量连接，提高系统的吞吐量和响应性。





1. 资源（Resources）
   - 资源是生成事件的实体，如网络连接（Socket Handle）或文件描述符。
   - 例如，在网络服务器中，资源可能是客户端的 TCP 连接。
2. 同步事件解多路器（Synchronous Event Demultiplexer）
   - 使用事件循环（event loop）来阻塞等待所有资源的事件。
   - 当资源准备好进行同步操作且不会阻塞时，解多路器将资源发送到分发器。
   - CSDN 文章（web:3）提到，这部分通常通过 select、poll 或 epoll 等系统调用实现。
3. 分发器（Dispatcher）
   - 负责处理请求处理器的注册和注销。
   - 将资源分发到相关的请求处理器，确保事件被正确处理。
   - 例如，分发器可能根据事件类型（如读、写、关闭）调用不同的处理器。
4. 请求处理器（Request Handlers）
   - 应用程序定义的请求处理程序，负责处理与资源相关联的请求。
   - 处理器通常是同步调用的，处理业务逻辑，如读取数据或发送响应。

### 工作原理

反应器模式的工作流程如下：

- 事件循环持续监听资源上的事件（如连接建立、数据到达）。
- 当事件发生时，同步事件解多路器通知分发器。
- 分发器根据事件类型调用注册的请求处理器。
- 请求处理器同步地处理事件，例如读取数据或执行业务逻辑。
- 整个过程通常在单线程中完成，但可以结合线程池处理复杂任务。





### 优势

**模块化和可重用性**：将程序特定代码分离为模块化、可重用的组件，便于维护和扩展。

**简化并发**：通过同步调用处理器，避免了多线程系统的复杂性，减少了线程创建、销毁和切换的开销。

**高效处理高并发**：单个线程可以处理大量连接，适合高吞吐量场景，如 Web 服务器。

例如，博客园文章（web:9）提到，反应器模式代替多线程处理方式，节省系统资源，提高吞吐量。





### 缺点



**调试困难**：由于控制流的反转（好莱坞原则：不要打电话给我们，我们会打电话给你），调试可能更复杂。

**并发限制**：同步调用处理器可能限制最大并发性，尤其在对称多处理（SMP）硬件上。

**可扩展性**：受同步调用和解多路器的限制，扩展到大规模并发可能需要额外的优化。









## Netty IO模型（单机处理百万级并发）



> 主从Reactor模式，在反应器单线程的基础上提供并发能力。



### 主要组件



1. **BossGroup**

- 负责接收客户端的连接请求，相当于主Reactor。
- 有新连接时，创建NioSocketChannel并将其注册到WorkerGroup的某个NioEventLoop上。
- 常规默认为单线程（可配置）

2. **WorkerGroup**

   - 负责处理已建立连接的IO事件，如读写操作，相当于从Reactor。
   - 可以有多个线程，默认为CPU核心数的两倍。
   - 每个WorkerGroup中的NioEventLoop轮询其selector，处理注册的Channel事件

3. **NioEventLoop**

   - 每个NioEventLoop包含一个Selector，用于监听绑定在其上的SocketChannel的网络通讯。
     - 轮询read/write事件
     - 处理IO事件和业务逻辑
     - 执行任务队列（runAllTasks），处理耗时的任务。

4. **ChannelPipeline**

   - 抽象数据管道，包含双向链表的ChannelHandler，用于拦截和处理IO事件。
   - 支持添加、删除handler，处理入站和出站事件。

   > 入站事件从头到尾走handler，出站事件从尾到头走handler



### 工作原理



1. BossGroup监听accept事件，当有新连接时，生成NioSocketChannel，并将其注册到WorkerGroup的某个NioEventLoop的Selector上。
2. WorkerGroup的NioEventLoop轮询Selector，处理注册的Channel上的读写事件。
3. 当有IO事件发生时，通过ChannelPipline中的handler链处理数据，确保数据流的连续性和高效性。



### 优点



- **非阻塞IO**：IO操作不会阻塞线程，线程可以在等待IO完成时处理其他任务。（读写操作异步通知业务线程，无需阻塞）
- **高并发**：通过少量线程管理大量并发，减少线程创建和上下文切换的开销。（支持百万级并发）
- **可扩展(伸缩性)**：主从Reactor模式允许配置“多主多从”，通过启动参数调整线程池大小。
