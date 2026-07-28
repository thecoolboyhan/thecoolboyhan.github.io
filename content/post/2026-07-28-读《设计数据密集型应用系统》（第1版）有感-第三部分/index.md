---
title: 读《设计数据密集型应用系统》（第1版）有感-第三部分：派生数据
description: 数据领域的神书，拜读后希望可以总结。将多个不同数据系统整合至一致的应用程序体系结构中。具有不同数据模型，并针对不同访问模式进行过优化。批处理系统（MapReduce），流数据处理，软件的未来。
image: 1.png
date: 2026-07-28
categories:
  - 精选
  - 架构
  - 数据库
tags:
  - 数据库
  - 分布式
  - 数据

---



> 前言：神书是神书，可惜依然逃不过烂尾。从前一部分的分布式事务开始，明显感觉到质量有所下降。不是说后面的部分特别烂；只是说和前面的惊为天人，明显感觉不是一个层次。



## 第十章、批处理系统

目前市面上主要存在的三种服务：

1. **在线服务（在线系统）**
   客户请求指令到达服务器，服务尽快做出响应。响应时间是服务性能的主要考核指标，可用性也非常重要。

2. **批处理系统（离线系统）**
   接收大量的输入数据，运行一个作业来处理数据，并输出。作业需要执行一段时间（几分钟到几天），用户通常不会等待作业完成。批处理系统往往会定期运行，主要性能指标为：吞吐量（处理一定大小的输入数据需要的时间）。

3. **流处理系统（近实时系统）**
   介于在线与离线之间，处理输入并产生输出，但流式作业在事件发生后不久就对事件做处理，而批处理则是以一个固定的周期来工作。流处理系统比批处理系统具有更低的延迟。

### 使用 UNIX 工具进行批处理

#### UNIX 设计哲学

> 当需要以另一种方式处理数据时，我们应该有一些连接程序的方法，就像花园软管互相拧在一起。这就是计算机的 IO。

1. 每个程序只做好一件事。如果有新的工作，则建立一个全新的程序，而不是通过增加特征让旧程序变得复杂。
2. 尽量让一个程序的输出，变成另一个尚未确定的程序的输入。不要将输出与无关信息混在一起。避免使用严格的表格状或二进制输入格式。不要使用交互式的输入。
3. 尽早尝试设计和构建软件，甚至操作系统，最好几周内完成。需要扔掉那些笨拙的部份时不要犹豫，立即进行重建。
4. 优先使用工具来减轻编程任务，即使你不得不花费时间取构建工具，并在使用完成后，会将一部分工具丢掉。

> [!NOTE]
> 类似如今的敏捷开发、DevOps 运动。

- **接口统一**
  如果希望某个程序的输出，作为另一个程序的输入，也就意味着这些程序必须使用相同的数据格式，必须接口兼容。
  UNIX 是把操作系统中的所有东西，全部解析成文件描述符（也就是文件）来做到统一接口，但现实中，无法将所有的东西都统一成相同的接口。

- **逻辑与布线分离**
  UNIX 工具的另一个特点是使用标准输入和标准输出。管道允许将一个进程的 stdout 附加到另一个进程的 stdin 中。程序并不关心数据来自哪里或需要输出到哪里。（这就是松耦合、后期绑定或控制反转）
  但同样，这样设计也存在局限性：很难做到需要多个输入和输出的程序。用户不能将程序的输出传输给网络。（输出给网络，就很容易出现并发）

> [!NOTE]
> 所以 UNIX 工具的局限是只能在一台机器上运行。

### MapReduce 与分布式文件系统

> MapReduce 有点像分布在数千台机器上的 UNIX 工具。MapReduce 作业可以和 UNIX 进程相媲美，需要一个或多个输入，并产生一个或多个输出。

运行 MapReduce 作业通常不会修改输入，除了生成输出外没有任何副作用。（对原始数据而言，不会修改任何现有数据）

**下文中主要以 HDFS 分布式文件系统举例说明 MapReduce。**

与网络链接存储（NAS）和存储区域网络（SAN）架构的共享磁盘方法相比，HDFS 基于无共享原则。共享磁盘由集中存储设备实现，而无共享方法则不需要特殊硬件，只需要通过网络连接的计算机。

HDFS 在每台机器上运行一个守护进程，并开放一个节点，允许其他节点访问存储在该机器上的文件。名为 NameNode 的中央服务器会跟踪哪个文件存储在哪台机器上（相当于索引）。HDFS 创建了一个庞大的文件系统，来充分利用每台机器上的磁盘资源。

#### MapReduce 的执行流程

1. 读取一组输入文件，并将其分解成记录。
2. 调用 mapper 函数从每个输入记录中提取一个键值对。
3. 按关键字将所有的键值对排序。
4. 调用 reducer 函数遍历排序后的键值对。

> 第二步的 map 提取键值对和第四步的 reduce 对键值对进行操作是由用户自定义编写的代码。



**mapper**

每个输入都会调用一次mapper，mapper从记录中提取出任意数量的键值对（可能为0个）。它不会保留输入和输出的任何状态，因此每条记录都是相互独立的。

**Reducer**

处理由mapper生成的键值对，收集属于同一个关键字的所有值，并使用迭代器调用reducer以处理该值的集合。生成输出的记录





- MapReduce的分布式执行

MapReduce和UNIX工具包的区别主要在于MapReduce可以跨多台机器执行，且不用编写代码来指定如何并行化。mapper和reducer一次只能处理一条记录，它们不需要直到输入来自哪里输出到什么地方，所以框架可以处理复杂的跨机器移动数据的情景。



![1784618620495.png](https://fastly.jsdelivr.net/gh/thecoolboyhan/th_blogs@main/image/2026-07/1784618620495_1784618620506.png)



键值对必须经过排序，如果数据集太大无法在一台机器上使用常规排序算法。MapReduce的排序是分阶段进行的。每个map任务会基于关键字哈希值，按照reduce对输出进行分块。每个分区都会被写入mapper程序所在的本地磁盘上的已排序文件。（可以使用SStable或LSM-tree）



当mapper读取完输入数据并写入排序后的输出文件，MapReduce调度器就会通知reducer开始从mapper中获取输出文件。reducer和每个mapper相连接，并按照自己的分区从mapper中下载排序后的键值对文件。



reduce任务从mapper中获取文件并将它们合并在一起，同时保持数据的排序。如果多个不同的mapper使用相同的关键字生成记录，这些记录会在reduce的输入文件中相邻。



reduce通过关键字和迭代器进行调用，而迭代器逐步扫描所有具有相同关键字的记录。reducer会通过自定义逻辑来处理这些数据，并生成任意数量的输出记录。这些输出数据被写入分布式文件系统的文件中。



- MapReduce的工作流

单个MapReduce可以解决的文件范围有限。将mapReduce链接到工作流中，一个作业的输出将作业下一个作业的输入。



>  MapReduce作业更像是一系列命令，每个命令的输出被写入临时文件，下一个命令从临时文件中读取。(写入临时文件的目的是方便续跑)

只有当作业完成输出时，整个批处理的输出才能被视为有效的。



#### Reduce端的join与分组

mapper的目的是从每个输入记录中提取关键字和值。对于一个活动时间日志与用户数据库关联的场景。一组mapper负责扫描活动事件（提取用户ID作为关键字，用户事件作为值），另一组mapper负责遍历用户数据库（提取用户ID作为关键字，用户出生日期作为值）。

![1784622391951.png](https://fastly.jsdelivr.net/gh/thecoolboyhan/th_blogs@main/image/2026-07/1784622391951_1784622391980.png)

MapReduce对数据进行排序后，相同的用户ID会在reduce的输入中相邻。然后通过Reduce对相同ID的数据进行真正的join操作。



由于reducer每次只处理一个特定用户ID的所有记录，因此只需要将用户记录在内存中保存一次，且不需要向网络发送任何请求。reduce会将来自join两侧的记录合并在一起。



- 处理数据倾斜

> 如果单个关键字相关的数据量特别大，那么会破坏将相同关键字的数据放在一起的模式。如某个少数名人有数百万的追随者。在单个reducer中收集与名人相关的所有活动，可能会导致严重的数据倾斜。

处理这种热键，通常需要一个任务来先扫描出热键（或手动指定哪些是热键），将热键尽可能随机的分散到不同的reduce中（而不是按照原有的通过顺序确定reducer），甚至可以先把热键拆分成更多更小的任务，通过多次reduce操作来进行join。这样可以更好的利用分布式的并行处理能力。



#### map端的join操作

mapper负责准备输入数据，从每个输入中提取关键字和值，将键值对分配给reducer分区，并按关键字排序。



在reducer端执行join，可能需要多次文件的复制。如果可以在map端对数据join，将极大的提高性能。



- 广播哈希join

> 适合大数据集与小数据集join，尤其是小数据集可以加载到mapper的内存中。

每个mapper的内存中维护一个表，每个mapper负责将自己的数据都加载到内存中。这样可以将相同的数据在map端就join。

> 这里更像每条记录被广播到不同的mapper中。

- 分区哈希join

将map端join的数据进行分区，将所有要join的记录整理到相同的分区中，每个mapper只需要从输入中读取一个分区就够了。





> MapReduce虽然性能缓慢（尤其多次mr后，将产生大量的文件），但可以做到随时停止，续跑。必要时可以给需要的任务让出资源。



### MapReduce示例（java版）



#### 实现的功能

把一个文本“文档”当成分布式输入，交给 MapReduce 框架统计每个单词出现的次数（WordCount），最后把结果打印出来。

统计一篇文章中，各个关键字出现的次数。（非常符合谷歌搜索设计之初的需求）



#### 实现代码

首先MapReduce框架应该和实现分离开来。利用UNIX工具包的思想，我们构建好一套规则后，用户完全可以自定义其中的组件。



``` java
/**
 * 极简 MapReduce 框架（纯 JDK 25，使用虚拟线程、record、Stream 等现代特性）。
 *
 * 泛型说明：
 *   K1/V1 —— Map 阶段输入键值类型（通常 K1 为行偏移量，V1 为文本行）
 *   K2/V2 —— Map 输出 / Reduce 输入的中间键值类型
 *   K3/V3 —— Reduce 输出的最终键值类型
 */
public class MapReduce<K1, V1, K2, V2, K3, V3> {

    /**
     * 不可变的键值对。
     * JDK 16+ 的 record：编译器自动生成构造器、访问器 key()/value()、equals/hashCode/toString，
     * 比手写 class 更简洁，适合作为纯数据载体。
     */
    public record Pair<K, V>(K key, V value) {}

    /** Mapper 接口：处理一条输入记录。@FunctionalInterface 允许用 lambda 实现。 */
    @FunctionalInterface
    public interface Mapper<K1, V1, K2, V2> {
        void map(K1 key, V1 value, Context<K2, V2> context);
    }

    /** Reducer 接口：处理同一个 key 的一组 value。@FunctionalInterface 允许用 lambda 实现。 */
    @FunctionalInterface
    public interface Reducer<K2, V2, K3, V3> {
        void reduce(K2 key, Iterable<V2> values, Context<K3, V3> context);
    }

    /** 收集器：Map/Reduce 通过它输出 <key, value>。 */
    public static class Context<K, V> {
        // synchronizedList 保证虚拟线程并发写入时的安全
        private final List<Pair<K, V>> output = Collections.synchronizedList(new ArrayList<>());

        public void write(K key, V value) {
            output.add(new Pair<>(key, value));
        }

        public List<Pair<K, V>> getOutput() {
            return output;
        }
    }

    private final Mapper<K1, V1, K2, V2> mapper;
    private final Reducer<K2, V2, K3, V3> reducer;

    public MapReduce(Mapper<K1, V1, K2, V2> mapper, Reducer<K2, V2, K3, V3> reducer) {
        this.mapper = mapper;
        this.reducer = reducer;
    }

    /**
     * 提交一个 Job 并执行，返回最终结果列表。
     * splits：已经切分好的多个输入分片（模拟不同节点的输入）。
     */
    public List<Pair<K3, V3>> run(List<List<Pair<K1, V1>>> splits) throws InterruptedException {
        var mapped = parallelMap(splits);     // 1) 并行 Map 阶段
        var grouped = shuffleAndSort(mapped); // 2) Shuffle & Sort：按 key 分组并排序
        return parallelReduce(grouped);       // 3) 并行 Reduce 阶段
    }

    /**
     * 并行 Map 阶段：为每个分片提交一个任务。
     * JDK 21+ 虚拟线程（Project Loom）：newVirtualThreadPerTaskExecutor 为每个任务创建一个轻量级虚拟线程，
     * 由 JVM 调度到平台线程上，能轻松支撑百万级并发，避免了传统线程池的容量规划。
     * ExecutorService 是 AutoCloseable，try-with-resources 会在结束时等待所有任务完成。
     */
    private List<Pair<K2, V2>> parallelMap(List<List<Pair<K1, V1>>> splits) throws InterruptedException {
        try (var executor = Executors.newVirtualThreadPerTaskExecutor()) {
            // var + Stream：把每个分片映射为一个异步任务
            var futures = splits.stream()
                    .map(split -> executor.submit(() -> {
                        var ctx = new Context<K2, V2>();
                        for (var record : split) {
                            mapper.map(record.key(), record.value(), ctx);
                        }
                        return new ArrayList<>(ctx.getOutput());
                    }))
                    .toList();

            var result = new ArrayList<Pair<K2, V2>>();
            for (var f : futures) {
                result.addAll(unsafeGet(f));
            }
            return result;
        }
    }

    /**
     * Shuffle & Sort：把相同 key 的中间结果汇聚到一起。
     * JDK 8+ Stream 的 groupingBy 三步式：
     *   - 分类函数 Pair::key         ：按 key 分组（shuffle）
     *   - () -> new TreeMap<>()       ：下游 Map 用 TreeMap，保证 key 有序（sort）
     *   - mapping(Pair::value, toList)：把分组后的 value 收集成 List
     */
    private Map<K2, List<V2>> shuffleAndSort(List<Pair<K2, V2>> mapped) {
        return mapped.stream()
                .collect(Collectors.groupingBy(
                        Pair::key,
                        TreeMap::new,
                        Collectors.mapping(Pair::value, Collectors.toList())));
    }

    /** 并行 Reduce 阶段：同样使用虚拟线程执行器，每个 key 一组交给一个 reduce 调用。 */
    private List<Pair<K3, V3>> parallelReduce(Map<K2, List<V2>> grouped) throws InterruptedException {
        try (var executor = Executors.newVirtualThreadPerTaskExecutor()) {
            var futures = grouped.entrySet().stream()
                    .map(entry -> executor.submit(() -> {
                        var ctx = new Context<K3, V3>();
                        reducer.reduce(entry.getKey(), entry.getValue(), ctx);
                        return new ArrayList<>(ctx.getOutput());
                    }))
                    .toList();

            var result = new ArrayList<Pair<K3, V3>>();
            for (var f : futures) {
                result.addAll(unsafeGet(f));
            }
            return result;
        }
    }

    /**
     * 安全获取 Future 结果：把受检异常（ExecutionException / InterruptedException）包装为运行时异常，
     * 避免在每个调用点都写 throws，保持外层代码简洁。
     */
    private static <T> T unsafeGet(Future<T> future) {
        try {
            return future.get();
        } catch (ExecutionException e) {
            throw new RuntimeException("任务执行失败", e.getCause());
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
            throw new RuntimeException("任务被中断", e);
        }
    }
}
```



- 用户自定义实现mapper和Reducer

> 当前需求中的mapper作用是将文章中的有效字符提取出来。提取出来后，value应该为当前有效字符的数量。一次map操作可能提取出多组关键字，但每组关键字之间相互独立。

> Reducer需要将按顺序遍历mapper输出的关键字，然后把相同的关键字汇总和。这里reduce前数据已经通过框架join过了，相同的key已经全部到了一个KV内部，但是V并没有做处理。reduce的作用是对这些V做处理。



``` java
/**
 * 经典示例：单词计数 WordCount。
 *
 * 输入：若干文本行（key = 行号，value = 一行文本）
 * Map：把每行按空白拆成单词，输出 <单词, 1>
 * Reduce：把同一单词的 1 累加，输出 <单词, 出现总次数>
 */
public class WordCount {

    /** Map 阶段：把一行文本拆成单词并输出 <单词, 1>。 */
    public static class WordCountMapper implements MapReduce.Mapper<Long, String, String, Integer> {
        @Override
        public void map(Long ignoredLineNo, String value, MapReduce.Context<String, Integer> context) {
            // 转小写 -> 按空白拆分 -> 过滤掉标点等非单词字符 -> 丢弃空白 -> 写出
            // 全程使用 Stream，配合 var 与 lambda，风格更现代
            Arrays.stream(value.toLowerCase().split("\\s+"))
                  .map(w -> w.replaceAll("[^a-z0-9\\u4e00-\\u9fa5]", ""))
                  .filter(w -> !w.isBlank())                  // JDK 11+ String.isBlank()：判断是否为空或仅含空白
                  .forEach(w -> context.write(w, 1));
        }
    }

    /** Reduce 阶段：把同一单词的一组计数累加。 */
    public static class WordCountReducer implements MapReduce.Reducer<String, Integer, String, Integer> {
        @Override
        public void reduce(String key, Iterable<Integer> values, MapReduce.Context<String, Integer> context) {
            // StreamSupport 把 Iterable 转为 Stream，再用 mapToInt + sum 完成聚合
            int sum = StreamSupport.stream(values.spliterator(), false)
                                   .mapToInt(Integer::intValue)
                                   .sum();
            context.write(key, sum);
        }
    }
}
```



用于测试的Main方法：



``` java
/**
 * 入口：准备输入分片、提交 MapReduce Job、打印结果。
 */
public class Main {
    public static void main(String[] args) throws Exception {
        // 文本块（Text Blocks，JDK 15+ 稳定）：多行字符串更直观，适合表示一篇“文档”
        String document = """
                hello world hello mapreduce
                mapreduce is a distributed computing model
                hello distributed world
                mapreduce mapreduce mapreduce
                分布式 计算 mapreduce 分布式 系统
                world hello world
                """;

        // 把文档按行切成 3 个分片（split），模拟分布式输入被切分的过程
        var lines = document.lines().toList();           // JDK 16+ Stream.toList()：返回不可变列表
        var splits = new ArrayList<List<MapReduce.Pair<Long, String>>>();
        for (int i = 0; i < lines.size(); i += 2) {
            var split = new ArrayList<MapReduce.Pair<Long, String>>();
            for (int j = i; j < Math.min(i + 2, lines.size()); j++) {
                split.add(new MapReduce.Pair<>((long) j, lines.get(j)));
            }
            splits.add(split);
        }

        // 构造 Job 并提交运行（框架内部使用虚拟线程并行执行 Map/Reduce）
        var job = new MapReduce<>(new WordCount.WordCountMapper(), new WordCount.WordCountReducer());
        var result = job.run(splits);

        // record 的访问器为 key() / value()；forEach + lambda 打印结果
        System.out.println("====== WordCount 结果 ======");
        result.forEach(p -> System.out.println(p.key() + " : " + p.value()));
    }
}
```







#### 思想总结



这里全程使用虚拟线程模拟分布式调用，实际生产中，每次虚拟线程提交可以看作一次网络分布式调用。通过map拆分key，通过框架聚合数据，然后每个key交给不同的reduce来并行处理。



- 中心思想

这里只展示了一个操作，如果在复杂的工作流中，完全可以用多个MapReduce连接起来。

总体流程：把原始数据提交给mapper，经过mapper分割后，交给框架来分组排序，之后将相同组的数据交给Reducer来执行操作。













## 第十一章、流处理系统

前面的批处理任务，往往需要读取完全部数据后，才会开始处理数据。MapReduce在读取完数据后，对记录排序，然后处理。然而，很多数据是无限的，而且会随着时间的推移而到达。

批处理系统对于上面的场景，往往按天来拆分数据，今天的数据明天才会被处理。

> 为了减少这种延迟，可以更频繁的运行处理，完全放弃了固定的时间片，每当有事件就开始处理。这就是流处理的思想



### 发送事件流



传统批处理系统，往往是消费者定期扫描某个公共资源（可能有多个消费者消费同一个资源），但当需要扫描的资源特别多，这将形成一个性能瓶颈。而且会有大量的性能浪费。

> 如果资源很可贵，当生产者数据就绪后，主动通知消费者，将是一个很好的方式。（事件驱动）



#### 消息系统

- 发送者维护（不推荐）

讲需要发送的消息和发送的目标统一维护在生产者，生产者要考虑生产速度，被压，消费者目标等问题。



- 消息代理（大部分做法）

使用一个专门为生产消费模型设计的中间数据库来维护消息，生产者发送消息后，数据被写入中间数据库。后续所有操作状态由中间数据库代理维护。可以控制多个不同消费者的消费进度，消息数量，消费速率等。由于数据库可多级部署，甚至可以通过代理实现分布式事务。（XA和JTA等）

![1785143908280.png](https://fastly.jsdelivr.net/gh/thecoolboyhan/th_blogs@main/image/2026-07/1785143908280_1785143908289.png)





#### 分区日志

>  普通消息在传递给消费者后就会删除。消息代理是基于瞬时的消息传递思维而构建的。而然，批处理系统的一个关键特征是可以反复运行。

如果将一个新的消费者添加到消息系统，通常只会接受之后的新消息，任何之前的消息都会消失，无法恢复。

日志消息为了解决以上问题，将数据库的持久化方式和消息传递相结合。



- 基于日志的消息存储（kafka）

日志是磁盘上一个仅支持追加式修改记录的序列。可以使用相同的结构来实现消息代理：生产者通过在日志尾部追加来实现发送消息，生产者通过读取日志来接收消息。如果读取到消息的末尾，则等待新的消息通知。

> 类似与UNIX工具的tail -f命令

在不同的节点处理不同的分区，使每个分区变成不同的日志，并且可以独立于其他分区读取和写入。

![1785153160205.png](https://fastly.jsdelivr.net/gh/thecoolboyhan/th_blogs@main/image/2026-07/1785153160205_1785153160236.png)



- 对比传统的消息系统

传统消息系统往往可能会出现多线程消费，但每个消息的处理速度又不相同，则可能出现早接收的消息被晚处理完。

**传统消息系统**：适合消息顺序不重要，且单个消息处理速度慢的情况。

日志消息系统往往单个线程处理单个分区的消息，且消息是一个接一个处理的。

**日志消息系统**：适合吞吐量大，且需严格限制扇出，且单个消息处理速度快的场景。（如何某个消息处理速度慢，则可能会影响后续的所有消息）









