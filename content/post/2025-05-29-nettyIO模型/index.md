---
title:  NettyIO模型
description: 深入介绍NettyIO模型
#image: 1.png
date: 2025-05-29
categories: 
  - 精选
tags:
  - netty
  - java
  - io模型
---

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



## NIO多路复用

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



### 源码



- selector

由java.nio.channels.spi类中创建







