---
title:  算法-排序
description: 常见的排序汇总
image: 1.png
date: 2023-11-18
categories: 
  - 精选
  - 算法
tags:
  - 算法
  - 排序
  - 随笔
---

## OI WIKI
### 字符串
#### 字典树（Trie）

- 模版

```java
class Trie {
    //当前节点后面的节点
    private Trie[] children;
    //当前节点是否为结束
    private boolean isEnd;
    /** Initialize your data structure here. */
    public Trie() {
        children=new Trie[26];
        isEnd=false;
    }

    /** Inserts a word into the trie. */
    public void insert(String word) {
        Trie node =this;
        for(int i=0;i<word.length();i++){
            int t=word.charAt(i)-'a';
            if(node.children[t]==null){
                node.children[t]=new Trie();
            }
            node=node.children[t];
        }
        node.isEnd=true;
    }

    /** Returns if the word is in the trie. */
    public boolean search(String word) {
        Trie node=searchPrefix(word);
        return node!=null && node.isEnd;
    }

    /** Returns if there is any word in the trie that starts with the given prefix. */
    public boolean startsWith(String prefix) {
        return searchPrefix(prefix)!=null;
    }

    private Trie searchPrefix(String str){
        Trie node =this;
        for (int i = 0; i < str.length(); i++) {
            int t=str.charAt(i)-'a';
            if(node.children[t]==null) return null;
            node=node.children[t];
        }
        return node;
    }
}
```







> 记录算法书籍感悟，用心理解每一种套路
## 读《算法》有感


### 排序
#### 初级排序

- 排序算法的模版，后续所有排序遵守此模版

```java
private static class Example{
    //排序
    public static  void sort(Comparable[] a){

    }
    //判断a是否小于b
    private static  boolean less(Comparable a,Comparable b){
        return a.compareTo(b)<0;
    }

    //交换集合中i，j两个下标的元素
    private static void  exch(Comparable[] a,int i,int j){
        Comparable t = a[i];
        a[i]=a[j];
        a[j]=t;
    }

    //打印集合
    private static  void show(Comparable[] a){
        for (int i = 0; i < a.length; i++) {
            System.out.print(a[i]+" ");
            System.out.println();
        }
    }

    //验证a集合是否满足从小到大排序
    public static boolean isSorted(Comparable[] a){
        for (int i = 1; i < a.length; i++) {
            if(less(a[i],a[i-1]))
                return false;
        }
        return true;
    }
}
```


##### 选择排序

> 最简单的排序算法，首先，找到最小的那个元素，其次，将它和数组的第一个元素交换位置。再次，在剩下的元素中找到最小的元素。

算法的时间效率取决于比较的次数。

```java
public   void sort(Comparable[] a){
    for (int i = 0; i < a.length; i++) {
        int m=i;
        for (int j = i+1; j < a.length; j++) {
            if (less(a[j],a[m])) m=j;
            exch(a,i,m);
        }
    }
}
```


##### 插入排序

> 选择每一个数，把它放到正确的位置去 。保证当前指针左侧的数据一定是按照顺序排好的。

这种排序对于常见如果已知有一定顺序的东西排序效率更高，



```java
public   void sort(Comparable[] a){
   for(int i=1;i<a.length;i++){
       for(int j=i;j>=0&&less(a[j],a[j-1]);j--){
           exch(a,j,j-1);
       }
   }
}
```

![2023-11-1116:18:12-1699690691965.png](https://gitee.com/grsswh/drawing-bed/raw/master/image/2023-11-1116:18:12-1699690691965.png)


##### 希尔排序

> 让数组中任意间隔为h的元素都是有序的。依次减少h的大小，来实现全部有序。

可以减少数组元素交换的次数。



```java
public   void sort(Comparable[] a){
   int n=a.length;
   int h=1;
   //把数组分成三份
   while(h<n/3) h=3*h+1;
   //只要每份的数量大于1
   while(h>=1){
       for (int i = h; i < n; i++) {
           //保证，对于所有的份数来说，每个间隔为h元素都是按照从小到大的顺序排序
           for(int j=i;j>=h&&less(a[j],a[j-h]);j-=h)
               exch(a,j,j-h);
       }
       //减小份数，继续排
       h=h/3;
   }
}
```



![2023-11-1116:36:02-1699691761837.png](https://gitee.com/grsswh/drawing-bed/raw/master/image/2023-11-1116:36:02-1699691761837.png)


#### 归并排序（分治）

> 将两个有序数组，归并成一个更大的有序数组。

时间复杂度：NlogN

空间复杂度：N

![2023-11-1116:54:30-1699692869952.png](https://gitee.com/grsswh/drawing-bed/raw/master/image/2023-11-1116:54:30-1699692869952.png)
##### 原地归并

> 把两个数组中的元素直接归并到第三个数组里

已知两个需要归并的数组都是排好序的，直接从这两个数组里依次取最小值，加入到结果里。



```java
public void merge(Comparable[] a,int lo,int mid, int hi){
    //放最后排序的结果
    Comparable[] res=new Comparable[a.length];
    //将数组的lo到mid，和mid+1到hi部分归并
    int i=lo,j=mid+1;
    for(int k=lo;k<=hi;k++)
        res[k]=a[k];

    for(int k=lo;k<=hi;k++)
        //如果左边界大于中点，表示左边元素已经被取完，从右边取
        if (i>mid)
            a[k]=res[j++];
    //如果右边大于边界，右边取完，取左边
        else if (j>hi)
            a[k]=res[i++];
        //如果右边小于左边，取右边
        else if(less(res[j],res[i]))
            a[k]=res[j++];
        else
            //否则取左边
            a[k]=res[i++];
}
```

![2023-11-1117:11:19-1699693878701.png](https://gitee.com/grsswh/drawing-bed/raw/master/image/2023-11-1117:11:19-1699693878701.png)


##### 自顶向下的归并排序

> 把数组不断地拆成两个数组，最后通过归并两个数组来组合所有数组



```java
public void sort(Comparable[] a){
    sort(a,0,a.length-1);
}
public   void sort(Comparable[] a,int lo,int hi){
    if(hi<=lo) return;
    int mid=lo+((hi-lo)>>1);
    sort(a,lo,mid);
    sort(a,mid+1,hi);
    merge(a,lo,mid,hi);
}
```

![2023-11-1117:24:44-1699694684157.png](https://gitee.com/grsswh/drawing-bed/raw/master/image/2023-11-1117:24:44-1699694684157.png)


##### 自低向上的归并排序

> 先排列小的两个数组，可以有效的减少代码量



```java
//辅助数组
private Comparable[] aux;
public void sort(Comparable[] a){
    int n = a.length;
    aux=new Comparable[n];
    //每次对sz个元素来排序
    for(int sz=1;sz<n;sz+=sz)
        //左边界从0开始，每段左边界都是上一次+sz
        for(int lo=0;lo<n-sz;lo+=sz+sz)
            //对于每次需要归并的两个数组，左边边界已经确认，中点为小数组+sz-1，右边边界为中点+sz和数组长度-1取较小值
            merge(a,lo,lo+sz-1,Math.min(lo+sz+sz+-1,n-1));
}
```

![2023-11-1117:35:09-1699695308672.png](https://gitee.com/grsswh/drawing-bed/raw/master/image/2023-11-1117:35:09-1699695308672.png)
####   快速排序

> 应用最广泛的排序算法，只需要很小的辅助空间就可以在原地实现排序。

只需要O1的空间就可以在NlogN的时间内完成排序

![2023-11-1210:14:21-1699755261111.png](https://gitee.com/grsswh/drawing-bed/raw/master/image/2023-11-1210:14:21-1699755261111.png)



- 快排基类

```java
public void sort(Comparable[] a){
   sort(a,0,a.length-1);
}
private void sort(Comparable[] a, int lo, int hi) {
    //终止条件
    if(hi<=lo)  return ;
    //拆封数组
    int j =partition(a,lo,hi);
    //排前面
    sort(a,lo,j-1);
    //后面
    sort(a,j+1,hi);
}
```
##### 原地切分

选出要切分范围的第一个数字，把它放到合适的位置。

```java
//把目标数字放到合适的位置
private int partition(Comparable[] a, int lo, int hi) {
    //i表示当前遍历到第几个数，j表示上线边界
    int i=lo,j=hi+1;
    //选第一个数出来放到合适的位置，用第一个数来切割
    Comparable v=a[lo];
    while(true){
        //找到从左到右第一个大于目标数组的数
        while(less(a[++i],v))   if(i==hi)   break;
        //从右到左，第一个小于目标数字的数
        while(less(v,a[--j]))   if(j==lo)   break;
        //跳出条件，当i==j时，表示i左边的数字都小于目标数，右边的数字都大于目标数
        if(i>=j)    break;
        //把小于目标的数字放到左边，大于目标的数字放到右边
        exch(a,i,j);
    }
    //由于左边界为选出的数字，上方循环到跳出条件时，j最后一个指向小于目前的数字，交换这两个数字
    exch(a,lo,j);
  	//j为已经放好的位置，j作为新的中点
    return j;
}
```


##### 三向切分的快速排序

> 上世纪90年代，两位大佬证实，三向切分的快速排序比归并排序和其他排序方法包括重复元素很多的实际应用中更快。

几乎可以理解成最快的排序，这种算法可以有效的把所有相同的元素全部都不需要反复排序。可以有效的避免重复计算。

```java
private void sort(Comparable[] a, int lo, int hi) {
    //跳出条件
    if(hi<=lo) return ;
    //lt：要排序的文件，i：遍历起始位置，gt：右边界
    int lt=lo,i=lo+1,gt=hi;
    //目标元素
    Comparable v = a[lo];
    while(i<=gt){
        //目标元素和当前元素比较
        int cmp = a[i].compareTo(v);
        //如果当前元素小于目标元素，交换当前元素位置，让指针后移一位，目标指针也后移一位。此时目标指针还是指向了目标元素本身，因为对于所有大于当前元素的元素，都会被下面的if排除到数组之外。所有小于目标元素的，都会被替换到目标元素之前，目标指针，一定指向所有等于当前元素的第一个元素。
        if(cmp<0) exch(a,lt++,i++);
        //如果目标元素大于当前元素，右边界减一，直接把大于当前元素的数字换到要比较的数组范围之外， 留给下次给其他元素排序时来比较。
        else if(cmp>0) exch(a,i,gt--);
        //如果相同，直接跳过当前元素比较
        else i++;
    }
    //拆分后，排小于目标元素的元素
    sort(a,lo,lt-1);
    //排大于
    sort(a,gt+1,hi);
}
```

![2023-11-1420:33:11-1699965191109.png](https://gitee.com/grsswh/drawing-bed/raw/master/image/2023-11-1420:33:11-1699965191109.png)


#### 优先队列


##### 堆实现

> 所有元素都存的pg【1.。。n】中，pg【0】没有被使用。

```java
class MaxPQ<Key extends  Comparable<Key>>{
    //用数组存放当前队列中的元素
    private Key[] pq;
    //当前队列中的元素数量
    private int N=0;
    public MaxPQ(int maxN){
        //初始化一个大小为n+1的元素数组
        pq=(Key[]) new Comparable[maxN+1];
    }
    //判空
    public boolean isEmpty(){
        return N==0;
    }
    //当前队列大小
    public int size(){
        return N;
    }
    //插入一个元素
    public void insert(Key v){
        //当前队列数量+1，把当前key放进去
        pq[++N]=v;
        //把当前元素换到正确的位置
        swim(N);
    }
    //出队最大的元素
    public Key delMax(){
        //pq[1]为当前队列中最大的元素
        Key max=pq[1];
        //让选出的元素和最小的元素交换，减少当前元素的数量
        exch(1,N--);
        //把第N个元素（也就是刚刚选出的元素）归零
        pq[N+1]=null;
        //把上面换到堆顶的元素放到正确的位置
        sink(1);
        //返回取出的最大元素
        return max;
    }
    //由上至下的堆有序化实现
    private void sink (int k){
        //2*k表示当前节点的子节点，如果当前节点存的子节点
        while(2*k<=N){
            //取出当前节点的子节点
            int j=2*k;
            //小于N表示存在子节点，因为存在两个子节点，取出较大的那个字节节点
            if(j<N&&less(j,j+1))    j++;
            //让当前节点和较大的子节点进行交换
            exch(k,j);
            //把当前节点指向子节点
            k=j;
        }
    }
    //由下至上的堆有序化实现
    private void swim(int k){
        //大于1，表示可以上浮，如果为1表示已经是最大节点，不需要参与上浮，k/2表示当前节点的父节点，如果父节点小于当前节点
        while(k>1&&less(k/2,k)){
            //交换当前节点和父节点，
            exch(k/2,k);
            //把指针指向已经被交换到父节点的值
            k=k/2;
        }
    }
    private boolean less(int i,int j){
        return pq[i].compareTo(pq[j])<0;
    }
    //交换两个节点
    private void exch(int i,int j){
        Key t=pq[i];
        pq[i]=pq[j];
        pq[j]=t;
    }
}
```
#### 各种排序总结



| 算法         | 是否稳定 | 是否原地排序 | 时间复杂度       | 空间复杂度 | 备注                                               |
| ------------ | -------- | ------------ | ---------------- | ---------- | -------------------------------------------------- |
| 选择排序     | 否       | 是           | N*N              | 1          | 取决于插入元素的排列情况                           |
| 插入排序     | 是       | 是           | 介于N到N*N之间   | 1          | 取决于插入元素的排列情况                           |
| 希尔排序     | 否       | 是           | NlogN到N*N       | 1          | 取决于插入元素的排列情况                           |
| 快速排序     | 否       | 是           | NlogN            | logN       | 运行效率由概率提供保证                             |
| 三向快速排序 | 否       | 是           | 介于N和NlogN之间 | logN       | 运行效率由概率保证，同时也取决于输入元素的分布情况 |
| 归并排序     | 是       | 否           | NlogN            | N          |                                                    |
| 堆排序       | 否       | 是           | NlogN            | 1          |                                                    |


### 查找


#### 顺序查找

> 依次遍历，最简单的查找

```java
//顺序查找
class SequentialSearchST<Key,Value>{
    //基于链表的实现
    private Node first;
    //节点
    private class Node {
        Key key;
        Value val;
        Node next;
        public Node(Key key,Value val,Node next){
            this.key=key;
            this.val=val;
            this.next=next;
        }
    }
    //查找一个key的val
    public Value get(Key key){
        //从头节点开始遍历，向后递归
        for(Node x=first;x!=null;x=x.next)
            if(key.equals(x.key))
                return x.val;
        //如果找不到返回空
        return null;
    }
    //放入一对key-val
    public void put(Key key,Value val){
        //先之前是否已经存在当前key
        for(Node x=first;x!=null;x=x.next)
            //如果找到
            if(key.equals(x.key)) {
                //把旧val改成当前val
                x.val = val;
                return;
            }
        //如果没有找到，新建一个节点，新节点的next指针指向老头节点，新节点做为链表新的头节点
        first=new Node(key,val,first);
    } 
}
```
#### 有序数组中的二分查找



```java
 //二分查找（基于有序数组）
    class BinarySearchST<Key extends Comparable<Key>,Value>{
        //基于数组的实现
        private Key[] keys;
        private Value[] vals;
        private int N;
        public BinarySearchST(int capacity){
            keys=(Key[]) new Comparable[capacity];
            vals=(Value[]) new Object[capacity];
        }
        public int size(){
            return N;
        }
        //获取一个元素
        public Value get(Key key){
            //如果堆为空，直接返回null
            if(isEmpty()) return null;
            //找到当前key在数组中的位置
            int i=rank(key);
//            如果找到当前元素，返回val
            if(i<N&&keys[i].compareTo(key)==0) return vals[i];
//            否则返回null
            else return null;
        }
//        放入一对key-val
        public void put(Key key,Value val){
//            找到当前元素所在的位置
            int i=rank(key);
//            如果存在当前元素
            if(i<N&&keys[i].compareTo(key)==0){
//                把val改成新val
                vals[i]=val;
                return;
            }
//            没有找到key，让之之前rank查找到的左边界之后的所有元素全部向后移动一格
            for(int j=N;j>i;j--){
                keys[j]=keys[j-1];
                vals[j]=vals[j-1];
            }
            //找到的i设置一对新key-val
            keys[i]=key;
            vals[i]=val;
//            当前元素数量++
            N++;
        }
        public void delete(Key key){
            put(key,null);
        }
        //找到key在数组中的位置
        private int rank(Key key){
            //lo下边界，hi上边界
            int lo=0,hi=N-1;
            //二分查找模版
            while(lo<=hi){
                //中点
                int mid=lo+(hi-lo)/2;
//                要选择元素和当前中点所指元素来比较
                int cmp=key.compareTo(keys[mid]);
                //小
                if(cmp<0) hi=mid-1;
                //大
                else if(cmp>0) lo=mid+1;
//                bingo
                else return mid;
            }
//            如果没有找到，返回当前左边界下标，此下标指向如果需要插入当前key合适的位置
            return lo;
        }
        public boolean isEmpty(){
            return size()==0;
        }
        public boolean contains(Key key){
            return get(key)!=null;
        }
    }
```


#### 两种查找的总结



| 算法                 | 最坏查找 | 最坏插入 | 平均查找 | 平均插入 | 是否支持有序性相关的操作 |
| -------------------- | -------- | -------- | -------- | -------- | ------------------------ |
| 顺序查找（无序链表） | N        | N        | N/2      | N        | 否                       |
| 二分查找（有序数组） | logN     | 2*N      | logN     | N        | 是                       |
|                      |          |          |          |          |                          |
#### 符号表查找（key-val）的各种实现的优缺点

| 使用的数据结构       | 优点                                               | 缺点                                                         |
| -------------------- | -------------------------------------------------- | ------------------------------------------------------------ |
| 链表（顺序查找）     | 适用于小型问题                                     | 对于大型符号表很慢                                           |
| 有序数组（二分查找） | 最优的查找效率和空间需求，能够进行有序性相关的操作 | 插入操作很慢                                                 |
| 二叉查找树           | 实现简单，能够进行有序性相关的操作                 | 没有性能上界的保证，连接需要额外的空间                       |
| 平衡二叉查找树       | 最优的查找和插入效率，能够进行有序性相关的操作     | 连接需要额外的空间                                           |
| 散列表               | 能够快速的查找和插入常见类型的数据                 | 需要计算每种类型的数据的散列，无法进行有序性相关的操作，链接和空节点需要额外的空间 |


#### 二分查找树

