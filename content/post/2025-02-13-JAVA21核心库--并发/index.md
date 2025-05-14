---
title: JAVA21核心库--并发
date: 2025-02-13
description: 根据21版本的JDK，重新认识java的并发 
image: java21c.png
categories: 
  - 精选
tags:
  - java
  - 并发
  - 调研
  - 多线程
  - 虚拟线程
---

> 根据21版本的JDK，重新认识java的并发

https://docs.oracle.com/en/java/javase/21/core/concurrency.html
## Concurrency(并发)

> Java SE 的并发 API 提供了一个强大的可扩展框架高性能线程实用程序，例如线程池和阻塞队列。此软件包使程序员无需手动编写这些实用程序，其方式与集合框架对数据结构所做的方式大致相同。此外，这些软件包还提供用于高级并发编程的低级基元。


### 并发包组成

-  高性能、灵活的线程池

>  a high-performance, flexible thread pool;



- 异步执行任务框架

> a framework for asynchronous execution of tasks



- 针对大量并发访问优化的集合类

> a host of collection classes optimized for concurrent access;



- 实时同步器（信号量）

> synchronization utilities such as counting semaphores



- 原子类

> atomic variables



- 锁

> locks

- condition


### 常用API

| API                      | 备注                                                         |
| ------------------------ | ------------------------------------------------------------ |
| 虚拟线程Virtual threads  | 虚拟线程是轻量级线程的一种，可以减少编写、维护和调试高吞吐量并发量的应用程序。 |
| 结构化并发               | 将不同线程中运行的相关任务组视为同一个工作单元，从而简化异常处理和取消，提高可靠性和增强可观察性。 |
| 异步任务调度框架         | Executor接口根据一组执行策略，标准化了异步任务的调用、调度、执行和控制等。使任务可以在线程池中执行，或单个线程中执行，开发人员可以创建任意执行策略的自定义实现。内置实现了可配置的策略，如：队列长度限制，拒绝策略，这些策略可以防止资源失控，提高了程序的稳定性。 |
| Fork/join 框架           | 使线程池高效运行大量任务。基于“工作窃取”（workstealing）技术使所有工作线程保持繁忙，以充分利用多个处理器。 |
| 并发集合                 | [`Queue`](https://docs.oracle.com/javase/8/docs/api/java/util/Queue.html)、[`BlockingQueue`](https://docs.oracle.com/javase/8/docs/api/java/util/concurrent/BlockingQueue.html) 和 [`BlockingDeque`](https://docs.oracle.com/javase/8/docs/api/java/util/concurrent/BlockingDeque.html) |
| 原子类                   | 已原子方式创建的变量类，提供高性能原子计算、比较和使用。可以实现高性能并发算法、计数器、序列号生成等。 |
| 同步器（Synchronizers）  | 通用的同步类，促进线程之间的协调。主要包括：[Semaphore](https://docs.oracle.com/javase/8/docs/api/java/util/concurrent/Semaphore.html), [CyclicBarrier](https://docs.oracle.com/javase/8/docs/api/java/util/concurrent/CyclicBarrier.html), [CountdownLatch](https://docs.oracle.com/javase/8/docs/api/java/util/concurrent/CountDownLatch.html), [Phaser](https://docs.oracle.com/javase/8/docs/api/java/util/concurrent/Phaser.html), 和 [Exchanger](https://docs.oracle.com/javase/8/docs/api/java/util/concurrent/Exchanger.html). |
| 锁                       | 虽然锁是通过synchronized关键字内置到java中的，但内置的monitor锁存在许多限制。<br />lock包下提供与synchronized同效的高性能锁实现，且还支持指定超时时间，不同的锁、同时持有多个锁，以及锁的打断、等待、获取等操作。 |
| 纳秒级计时器（nanoTime） | [`System.nanoTime`](https://docs.oracle.com/javase/8/docs/api/java/lang/System.html#nanoTime--) 允许访问纳秒级时间源，用来操作各种锁时间。实现精度主要取决于操作系统平台。 |
| 线程局部变量             | 与常规变量不同，每个访问线程局部变量的线程，都有自己独立初始化的变量副本。 |


## 虚拟线程（Virtual threads）

虚拟线程是轻量级线程，可减少编写、维护和调试高吞吐量并发应用程序的工作量。

> 从JDK19开始提供，JDK21中完成。

线程是可以调度的最小单元。它们彼此之间独立。线程主要分两种：平台线程和虚拟线程。


### 什么是平台线程？

平台线程被是操作系统的包装实现。平台线程在底层的操作系统线程上运行java代码，并且平台线程整个生命周期都是由操作系统线程完成的。因此，可用的平台线程数量受限于操作系统线程数量。

平台线程通常具有较大的线程栈和其他由操作系统维护的资源。它们适合执行各种任务，但是可能是一种有限的资源。（操作系统的线程数有限）


### 什么是虚拟线程？



像平台线程一样，虚拟线程也是java.lang.Thread类的一个实例。然而虚拟线程并不绑定特定的操作系统线程上。虚拟线程仍然在操作系统线程上运行。然而，当在虚拟线程中运行的代码调用阻塞I/O操作时，java会暂停该虚拟线程，知道它可以恢复。与被暂停的虚拟线程相关联的操作系统线程可以自由的为其他虚拟线程执行操作。



虚拟线程的实现方式类似于虚拟内存。为了模拟大量内存，操作系统将一个大的虚拟空间映射到有限的RAM上。同样，为了模拟大量线程，java将大量虚拟线程映射到少量的操作系统线程上。



与平台线程不同，虚拟线程通常具有较浅的调用栈，只执行少量操作，例如：单个HTTP客户端调用或单个JDBC查询。虽然虚拟线程支持线程局部变量和可继承线程局部变量，但需要谨慎使用，因为单个JVM可能支持数百万个虚拟线程。



> 虚拟线程适合运行大部分时间被阻塞的任务，这些任务通常在等待i/o操作完成。虚拟线程不适合运行长时间的CPU密集型操作。


### 为什么使用虚拟线程？



在高吞吐量的并发应用程序中使用虚拟线程，特别是那些由大量并发任务组成的应用程序，这些任务大部分时间都在等待。服务器应用程序就是高吞吐量应用程序的例子，因为它们通常执行许多阻塞I/O操作的客户端请求。



> 虚拟线程并不是更快的线程：它的运行速度和平台线程没有区别。虚拟线程存在的目的是为了提供规模（更高的吞吐量），而不是速度（更低的延迟）。


### 创建和使用虚拟线程

> 以下项目代码可以我的另一个项目(personStudy)中找到
#### 使用Thread类和使用Thread.Builder 接口来创建虚拟线程



- 使用Thread类创建虚拟线程

```java
private static void createByThread() throws InterruptedException {
        Thread thread = Thread.ofVirtual().start(() -> System.out.println("Hello"));
//        join是为了让虚拟线程插队到主线程之前，保证在主线程结束之前可以看到虚拟线程的打印
        thread.join();
    }
```



- 通过Thread.Builder创建



```java
//创建一个线程
private static void createByThreadBuilder1() throws InterruptedException {
        Thread.Builder builder = Thread.ofVirtual().name("virtualThread");
//        同样可以用来创建平台线程,所有其他API都兼容
//        Thread.Builder builder = Thread.ofPlatform().name("PlatformThread");
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
//        启动后会总动给start+1.
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
//        if(args.length != 1){
//            System.out.println("usage: java EchoServer <port>");
//            System.exit(0);
//        }
        int port = 8080;
//        传入端口号
//        int port = Integer.parseInt(args[0]);
        try(
                ServerSocket serverSocket = new ServerSocket(port)
        ){
            while(true){
//                不知道hostname
//                System.out.println(serverSocket.getInetAddress().getHostName());
//                获取到连接请求，创建一个虚拟线程来处理
                Socket clientSocket = serverSocket.accept();
//                创建虚拟线程的方式为Thread类
                Thread.ofVirtual().start(()->{
                   try(
//                           输入输出流
                           PrintWriter out = new PrintWriter(clientSocket.getOutputStream(),true);
                           BufferedReader in = new BufferedReader(new InputStreamReader(clientSocket.getInputStream()))
                   ) {
//                       获取客户端发送来的请求
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


### 虚拟线程使用指南



- 非阻塞风格开发的代码，即使使用虚拟线程，也不会有多大提升

``` java
CompletableFuture.supplyAsync(info::getUrl, pool)
   .thenCompose(url -> getBodyAsync(url, HttpResponse.BodyHandlers.ofString()))
   .thenApply(info::findImage)
   .thenCompose(url -> getBodyAsync(url, HttpResponse.BodyHandlers.ofByteArray()))
   .thenApply(info::setImageData)
   .thenAccept(this::process)
   .exceptionally(t -> { t.printStackTrace(); return null; });
```



- 以同步风格开发的代码，使用虚拟线程将带来极大的提升

``` java
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



- 将每个并发任务表示为一个虚拟线程；<font color='red'>永远不用对虚拟线程进行池化</font>

> 尽管虚拟线程的行为与平台线程相同，但不是相同的程序概念。

平台线程稀缺，所以需要使用线程池来管理。（线程池中的平台线程数始终小于等于最大线程数）

虚拟线程众多，每个线程都不应该代表某种共享的、池化的资源，而应代表一个任务。虚拟线程的数量始终等于程序中的并发任务数量。

> 应该将每个任务表示为一个虚拟线程

``` java
try (var executor = Executors.newVirtualThreadPerTaskExecutor()) {
   Future<ResultA> f1 = executor.submit(task1);
   Future<ResultB> f2 = executor.submit(task2);
   // ... use futures
}
```



Executors.newVirtualThreadPerTaskExecutor()不会返回线程池，它为每个提交的任务都创建一个新的虚拟线程。



- 同时向多个服务器发起注销操作

``` java
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

``` java
ExecutorService es = Executors.newFixedThreadPool(10);
...
Result foo() {
    try {
        var fut = es.submit(() -> callLimitedService());
        return f.get();
    } catch (...) { ... }
}
```

> <font color='red'>线程池限制并发数量只是附带效果，线程池主旨在于共享稀缺资源，而虚拟线程不是稀缺资源，因此永远不应被池化。</font>

- 使用semaphore来限制虚拟线程的并发数量

``` java
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

``` java
synchronized(lockObj) {
    frequentIO();
}
```

替换后：

``` java
lock.lock();
try {
    frequentIO();
} finally {
    lock.unlock();
}
```


## 结构化并发

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


## Task scheduling framework

