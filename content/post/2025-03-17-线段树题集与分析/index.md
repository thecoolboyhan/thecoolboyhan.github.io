---
title: '线段树题集与分析'
date: 2025-03-17
permalink: /posts/17/线段树题集与分析/
image: 2025-03-17.png
categories: 
  - 精选
tags:
- 算法
- 力扣
- 线段树
---

> 线段树是算法竞赛中常用的用来维护 区间信息 的数据结构。
> 线段树可以在 O(\log N) 的时间复杂度内实现单点修改、区间修改、区间查询（区间求和，求区间最大值，求区间最小值）等操作。




## 线段树原理


### 建树



> 线段树将每个长度不为 ![1](data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7) 的区间划分成左右两个区间递归求解，把整个线段划分为一个树形结构，通过合并左右两区间信息来求得该区间的信息。这种数据结构可以方便的进行大部分的区间操作。



[![1742268138378.png](https://www.helloimg.com/i/2025/03/18/67d8e6d649a7c.png)](https://www.helloimg.com/i/2025/03/18/67d8e6d649a7c.png)



[![1742276497762.png](https://www.helloimg.com/i/2025/03/18/67d9077e920f0.png)](https://www.helloimg.com/i/2025/03/18/67d9077e920f0.png)

在实现时，我们考虑递归建树。设当前的根节点是p，如果根节点区间管辖的长度已经是1，则可以直接根据a数组上相应位置的值初始化该节点。否则我们将该区间从中点处分割为两个子区间，分别进入左右子节点递归建树，最后合并两个子节点的信息。



``` c++
void build(int s, int t, int p) {
  // 对 [s,t] 区间建立线段树,当前根的编号为 p
  if (s == t) {
    d[p] = a[s];
    return;
  }
  int m = s + ((t - s) >> 1);
  // 移位运算符的优先级小于加减法，所以加上括号
  // 如果写成 (s + t) >> 1 可能会超出 int 范围
  build(s, m, p * 2), build(m + 1, t, p * 2 + 1);
  // 递归对左右区间建树
  d[p] = d[p * 2] + d[(p * 2) + 1];
}
```



``` java
void build(int s, int t, int p) {
    // 对 [s,t] 区间建立线段树,当前根的编号为 p
    if (s == t) {
        d[p] = a[s];
        return;
    }
    int m = s + ((t - s) >> 1);
    // 移位运算符的优先级小于加减法，所以加上括号
    // 如果写成 (s + t) >> 1 可能会超出 int 范围
    build(s, m, p * 2);
    build(m + 1, t, p * 2 + 1);
    // 递归对左右区间建树
    d[p] = d[p * 2] + d[p * 2 + 1];
}

```




### 查询



如果要查询的区间为[3,5]，此时不能直接获取区间的值，但[3,5]可以拆成[3,3]和[4,5]，可以合并这两个区间的答案来求得这个区间的答案。

如果要查询的区间是[l,r]，则可以将其拆成最多为O(log n) 个极大的区间，合并这些区间即可求出[l,r]的答案。



- c++

``` c++
int getsum(int l, int r, int s, int t, int p) {
  // [l, r] 为查询区间, [s, t] 为当前节点包含的区间, p 为当前节点的编号
  if (l <= s && t <= r)
    return d[p];  // 当前区间为询问区间的子集时直接返回当前区间的和
  int m = s + ((t - s) >> 1), sum = 0;
  if (l <= m) sum += getsum(l, r, s, m, p * 2);
  // 如果左儿子代表的区间 [s, m] 与询问区间有交集, 则递归查询左儿子
  if (r > m) sum += getsum(l, r, m + 1, t, p * 2 + 1);
  // 如果右儿子代表的区间 [m + 1, t] 与询问区间有交集, 则递归查询右儿子
  return sum;
}
```



- java

``` java
int getSum(int l, int r, int s, int t, int p) {
    // [l, r] 为查询区间, [s, t] 为当前节点包含的区间, p 为当前节点的编号
    if (l <= s && t <= r) {
        return d[p];  // 当前区间为询问区间的子集时直接返回当前区间的和
    }
    int m = s + ((t - s) >> 1);
    int sum = 0;
    if (l <= m) {
        sum += getSum(l, r, s, m, p * 2);
    }
    // 如果左儿子代表的区间 [s, m] 与询问区间有交集, 则递归查询左儿子
    if (r > m) {
        sum += getSum(l, r, m + 1, t, p * 2 + 1);
    }
    // 如果右儿子代表的区间 [m + 1, t] 与询问区间有交集, 则递归查询右儿子
    return sum;
}

```


### 修改和懒惰标记

- 懒惰标记

> 通过延迟对节点信息的修改，从而减少不必要的操作次数。每次执行修改，通过打标记的方法表明该节点对应的区间在某一次操作中被修改，但不更新该节点的字节信息。实质性的修改在下次访问带有标记的节点时才进行。



- 修改

``` c++
// [l, r] 为修改区间, c 为被修改的元素的变化量, [s, t] 为当前节点包含的区间, p
// 为当前节点的编号
void update(int l, int r, int c, int s, int t, int p) {
  // 当前区间为修改区间的子集时直接修改当前节点的值,然后打标记,结束修改
  if (l <= s && t <= r) {
    d[p] += (t - s + 1) * c, b[p] += c;
    return;
  }
  int m = s + ((t - s) >> 1);
  if (b[p] && s != t) {
    // 如果当前节点的懒标记非空,则更新当前节点两个子节点的值和懒标记值
    d[p * 2] += b[p] * (m - s + 1), d[p * 2 + 1] += b[p] * (t - m);
    b[p * 2] += b[p], b[p * 2 + 1] += b[p];  // 将标记下传给子节点
    b[p] = 0;                                // 清空当前节点的标记
  }
  if (l <= m) update(l, r, c, s, m, p * 2);
  if (r > m) update(l, r, c, m + 1, t, p * 2 + 1);
  d[p] = d[p * 2] + d[p * 2 + 1];
}
```



``` java
void update(int l, int r, int c, int s, int t, int p) {
    // [l, r] 为修改区间, c 为被修改的元素的变化量, [s, t] 为当前节点包含的区间, p 为当前节点的编号
    if (l <= s && t <= r) {
        d[p] += (t - s + 1) * c;
        b[p] += c;
        return;
    }
    int m = s + ((t - s) >> 1);
    if (b[p] != 0 && s != t) {
        // 如果当前节点的懒标记非空, 则更新当前节点两个子节点的值和懒标记值
        d[p * 2] += b[p] * (m - s + 1);
        d[p * 2 + 1] += b[p] * (t - m);
        b[p * 2] += b[p];
        b[p * 2 + 1] += b[p];
        b[p] = 0;  // 清空当前节点的标记
    }
    if (l <= m) update(l, r, c, s, m, p * 2);
    if (r > m) update(l, r, c, m + 1, t, p * 2 + 1);
    d[p] = d[p * 2] + d[p * 2 + 1];
}

```



- 查询

``` c++
int getsum(int l, int r, int s, int t, int p) {
  // [l, r] 为查询区间, [s, t] 为当前节点包含的区间, p 为当前节点的编号
  if (l <= s && t <= r) return d[p];
  // 当前区间为询问区间的子集时直接返回当前区间的和
  int m = s + ((t - s) >> 1);
  if (b[p]) {
    // 如果当前节点的懒标记非空,则更新当前节点两个子节点的值和懒标记值
    d[p * 2] += b[p] * (m - s + 1), d[p * 2 + 1] += b[p] * (t - m);
    b[p * 2] += b[p], b[p * 2 + 1] += b[p];  // 将标记下传给子节点
    b[p] = 0;                                // 清空当前节点的标记
  }
  int sum = 0;
  if (l <= m) sum = getsum(l, r, s, m, p * 2);
  if (r > m) sum += getsum(l, r, m + 1, t, p * 2 + 1);
  return sum;
}
```



``` java
int getSum(int l, int r, int s, int t, int p) {
    // [l, r] 为查询区间, [s, t] 为当前节点包含的区间, p 为当前节点的编号
    if (l <= s && t <= r) {
        return d[p];  // 当前区间为询问区间的子集时直接返回当前区间的和
    }
    int m = s + ((t - s) >> 1);
    if (b[p] != 0) {
        // 如果当前节点的懒标记非空, 则更新当前节点两个子节点的值和懒标记值
        d[p * 2] += b[p] * (m - s + 1);
        d[p * 2 + 1] += b[p] * (t - m);
        b[p * 2] += b[p];
        b[p * 2 + 1] += b[p];
        b[p] = 0;  // 清空当前节点的标记
    }
    int sum = 0;
    if (l <= m) {
        sum = getSum(l, r, s, m, p * 2);
    }
    if (r > m) {
        sum += getSum(l, r, m + 1, t, p * 2 + 1);
    }
    return sum;
}

```



- 修改为某个值

``` c++
void update(int l, int r, int c, int s, int t, int p) {
  if (l <= s && t <= r) {
    d[p] = (t - s + 1) * c, b[p] = c, v[p] = 1;
    return;
  }
  int m = s + ((t - s) >> 1);
  // 额外数组储存是否修改值
  if (v[p]) {
    d[p * 2] = b[p] * (m - s + 1), d[p * 2 + 1] = b[p] * (t - m);
    b[p * 2] = b[p * 2 + 1] = b[p];
    v[p * 2] = v[p * 2 + 1] = 1;
    v[p] = 0;
  }
  if (l <= m) update(l, r, c, s, m, p * 2);
  if (r > m) update(l, r, c, m + 1, t, p * 2 + 1);
  d[p] = d[p * 2] + d[p * 2 + 1];
}

int getsum(int l, int r, int s, int t, int p) {
  if (l <= s && t <= r) return d[p];
  int m = s + ((t - s) >> 1);
  if (v[p]) {
    d[p * 2] = b[p] * (m - s + 1), d[p * 2 + 1] = b[p] * (t - m);
    b[p * 2] = b[p * 2 + 1] = b[p];
    v[p * 2] = v[p * 2 + 1] = 1;
    v[p] = 0;
  }
  int sum = 0;
  if (l <= m) sum = getsum(l, r, s, m, p * 2);
  if (r > m) sum += getsum(l, r, m + 1, t, p * 2 + 1);
  return sum;
}
```



``` java
void update(int l, int r, int c, int s, int t, int p) {
    if (l <= s && t <= r) {
        d[p] = (t - s + 1) * c;
        b[p] = c;
        v[p] = 1;
        return;
    }
    int m = s + ((t - s) >> 1);
    // 额外数组储存是否修改值
    if (v[p] != 0) {
        d[p * 2] = b[p] * (m - s + 1);
        d[p * 2 + 1] = b[p] * (t - m);
        b[p * 2] = b[p];
        b[p * 2 + 1] = b[p];
        v[p * 2] = 1;
        v[p * 2 + 1] = 1;
        v[p] = 0;
    }
    if (l <= m) update(l, r, c, s, m, p * 2);
    if (r > m) update(l, r, c, m + 1, t, p * 2 + 1);
    d[p] = d[p * 2] + d[p * 2 + 1];
}

int getSum(int l, int r, int s, int t, int p) {
    if (l <= s && t <= r) {
        return d[p];
    }
    int m = s + ((t - s) >> 1);
    if (v[p] != 0) {
        d[p * 2] = b[p] * (m - s + 1);
        d[p * 2 + 1] = b[p] * (t - m);
        b[p * 2] = b[p];
        b[p * 2 + 1] = b[p];
        v[p * 2] = 1;
        v[p * 2 + 1] = 1;
        v[p] = 0;
    }
    int sum = 0;
    if (l <= m) {
        sum = getSum(l, r, s, m, p * 2);
    }
    if (r > m) {
        sum += getSum(l, r, m + 1, t, p * 2 + 1);
    }
    return sum;
}

```


### 动态开点线段树

前面的堆式存储情况下，需要给线段树开4n大小的数组。为了节省空间，我们可以不一次性建好树，而是在最初只建立一个根节点代表整个区间。当我们需要访问某个子区间时，才建立代表这个区间的子节点。这样我们不再使用2p和2p+1代表p节点的儿子，而是使用ls和rs来记录儿子的编号。

**节点只有在有需要的时候才被创建**



> 单次操作的时间复杂度不变，为log(n)。由于每次创建操作都有可能创建并访问全新的一系列节点，因此m次单点操作后节点的数量规模是mlog(n)。最多只需要2n-1个节点，没有浪费。



- 修改

``` c++
// root 表示整棵线段树的根结点；cnt 表示当前结点个数
int n, cnt, root;
int sum[n * 2], ls[n * 2], rs[n * 2];

// 用法：update(root, 1, n, x, f); 其中 x 为待修改节点的编号
void update(int& p, int s, int t, int x, int f) {  // 引用传参
  if (!p) p = ++cnt;  // 当结点为空时，创建一个新的结点
  if (s == t) {
    sum[p] += f;
    return;
  }
  int m = s + ((t - s) >> 1);
  if (x <= m)
    update(ls[p], s, m, x, f);
  else
    update(rs[p], m + 1, t, x, f);
  sum[p] = sum[ls[p]] + sum[rs[p]];  // pushup
}
```



``` java
// root 表示整棵线段树的根节点；cnt 表示当前节点个数
int n, cnt, root = 0; // root 初始值为 0
int[] sum, ls, rs;

void initialize(int size) {
    // 初始化线段树的数组
    n = size;
    sum = new int[n * 2];
    ls = new int[n * 2];
    rs = new int[n * 2];
}

// 用法：update(root, 1, n, x, f); 其中 x 为待修改节点的编号
void update(int p, int s, int t, int x, int f) {
    if (p == 0) {
        p = ++cnt; // 当节点为空时，创建一个新的节点
    }
    if (s == t) {
        sum[p] += f;
        return;
    }
    int m = s + ((t - s) >> 1);
    if (x <= m) {
        if (ls[p] == 0) {
            ls[p] = ++cnt; // 创建左节点
        }
        update(ls[p], s, m, x, f);
    } else {
        if (rs[p] == 0) {
            rs[p] = ++cnt; // 创建右节点
        }
        update(rs[p], m + 1, t, x, f);
    }
    sum[p] = sum[ls[p]] + sum[rs[p]]; // pushup 操作
}

```



- 查询

``` c++
// 用法：query(root, 1, n, l, r);
int query(int p, int s, int t, int l, int r) {
  if (!p) return 0;  // 如果结点为空，返回 0
  if (s >= l && t <= r) return sum[p];
  int m = s + ((t - s) >> 1), ans = 0;
  if (l <= m) ans += query(ls[p], s, m, l, r);
  if (r > m) ans += query(rs[p], m + 1, t, l, r);
  return ans;
}

```



``` java
int query(int p, int s, int t, int l, int r) {
    if (p == 0) {
        return 0; // 如果节点为空，返回 0
    }
    if (s >= l && t <= r) {
        return sum[p]; // 如果当前区间是目标区间的子集，直接返回当前节点的值
    }
    int m = s + ((t - s) >> 1); // 计算当前区间的中点
    int ans = 0;
    if (l <= m) {
        ans += query(ls[p], s, m, l, r); // 查询左子区间
    }
    if (r > m) {
        ans += query(rs[p], m + 1, t, l, r); // 查询右子区间
    }
    return ans; // 返回查询结果
}

```


### 优化



1. 在叶子节点处无需放下懒惰标记，所以懒惰标记可以不下传到叶子节点。
2. 下放懒惰标记可以写一个专门的函数，从儿子节点更新当前节点也可以写一个专门的函数，降低代码编写难度。
3. 标记永久化：如果确定懒惰标记不会在中途加到溢出（超出该类型的最大范围），那么就可以将标记永久化。标记永久化可以避免下传懒惰标记，只需要在进行询问时把标记的影响加到答案当中，从而降低程序常数。


### 模板



- 区间加/求和

``` c++##include <bits/stdc++.h>
using namespace std;

template <typename T>
class SegTreeLazyRangeAdd {
  vector<T> tree, lazy;
  vector<T> *arr;
  int n, root, n4, end;

  void maintain(int cl, int cr, int p) {
    int cm = cl + (cr - cl) / 2;
    if (cl != cr && lazy[p]) {
      lazy[p * 2] += lazy[p];
      lazy[p * 2 + 1] += lazy[p];
      tree[p * 2] += lazy[p] * (cm - cl + 1);
      tree[p * 2 + 1] += lazy[p] * (cr - cm);
      lazy[p] = 0;
    }
  }

  T range_sum(int l, int r, int cl, int cr, int p) {
    if (l <= cl && cr <= r) return tree[p];
    int m = cl + (cr - cl) / 2;
    T sum = 0;
    maintain(cl, cr, p);
    if (l <= m) sum += range_sum(l, r, cl, m, p * 2);
    if (r > m) sum += range_sum(l, r, m + 1, cr, p * 2 + 1);
    return sum;
  }

  void range_add(int l, int r, T val, int cl, int cr, int p) {
    if (l <= cl && cr <= r) {
      lazy[p] += val;
      tree[p] += (cr - cl + 1) * val;
      return;
    }
    int m = cl + (cr - cl) / 2;
    maintain(cl, cr, p);
    if (l <= m) range_add(l, r, val, cl, m, p * 2);
    if (r > m) range_add(l, r, val, m + 1, cr, p * 2 + 1);
    tree[p] = tree[p * 2] + tree[p * 2 + 1];
  }

  void build(int s, int t, int p) {
    if (s == t) {
      tree[p] = (*arr)[s];
      return;
    }
    int m = s + (t - s) / 2;
    build(s, m, p * 2);
    build(m + 1, t, p * 2 + 1);
    tree[p] = tree[p * 2] + tree[p * 2 + 1];
  }

 public:
  explicit SegTreeLazyRangeAdd<T>(vector<T> v) {
    n = v.size();
    n4 = n * 4;
    tree = vector<T>(n4, 0);
    lazy = vector<T>(n4, 0);
    arr = &v;
    end = n - 1;
    root = 1;
    build(0, end, 1);
    arr = nullptr;
  }

  void show(int p, int depth = 0) {
    if (p > n4 || tree[p] == 0) return;
    show(p * 2, depth + 1);
    for (int i = 0; i < depth; ++i) putchar('\t');
    printf("%d:%d\n", tree[p], lazy[p]);
    show(p * 2 + 1, depth + 1);
  }

  T range_sum(int l, int r) { return range_sum(l, r, 0, end, root); }

  void range_add(int l, int r, T val) { range_add(l, r, val, 0, end, root); }
};
```



``` java
import java.util.*;

// 泛型类 SegTreeLazyRangeAdd，用于实现懒惰标记的线段树
class SegTreeLazyRangeAdd<T extends Number> {
    private T[] tree, lazy;  // tree 数组存储节点值，lazy 数组存储懒惰标记
    private T[] arr;         // 原数组
    private int n, root, n4, end; // n 是数组长度，root 是线段树根节点编号

    // 构造函数，初始化线段树
    public SegTreeLazyRangeAdd(T[] inputArray) {
        n = inputArray.length;
        n4 = n * 4; // 线段树的空间大小为 4n，足够存储所有节点
        tree = (T[]) new Number[n4]; // 初始化线段树的节点值
        lazy = (T[]) new Number[n4]; // 初始化线段树的懒惰标记
        arr = inputArray;
        Arrays.fill(tree, 0);  // 将 tree 数组的值设为 0
        Arrays.fill(lazy, 0);  // 将 lazy 数组的值设为 0
        end = n - 1;
        root = 1;
        build(0, end, 1); // 从根节点开始递归建树
        arr = null; // 建树完成后，释放原数组的引用
    }

    // 懒惰标记的下传逻辑
    private void maintain(int cl, int cr, int p) {
        int cm = cl + (cr - cl) / 2; // 计算中间点
        if (cl != cr && lazy[p] != 0) { // 只有非叶子节点才需要下传懒惰标记
            lazy[p * 2] += lazy[p]; // 将懒惰标记传递给左子节点
            lazy[p * 2 + 1] += lazy[p]; // 将懒惰标记传递给右子节点
            tree[p * 2] += lazy[p] * (cm - cl + 1); // 更新左子节点的值
            tree[p * 2 + 1] += lazy[p] * (cr - cm); // 更新右子节点的值
            lazy[p] = 0; // 清除当前节点的懒惰标记
        }
    }

    // 查询区间和的递归方法
    private T rangeSum(int l, int r, int cl, int cr, int p) {
        if (l <= cl && cr <= r) { // 当前节点完全覆盖目标区间
            return tree[p]; // 直接返回当前节点的值
        }
        int m = cl + (cr - cl) / 2; // 计算中点
        maintain(cl, cr, p); // 下传懒惰标记
        T sum = 0;
        if (l <= m) { // 左子区间与目标区间有交集
            sum += rangeSum(l, r, cl, m, p * 2);
        }
        if (r > m) { // 右子区间与目标区间有交集
            sum += rangeSum(l, r, m + 1, cr, p * 2 + 1);
        }
        return sum; // 返回左右子区间的和
    }

    // 区间加操作的递归方法
    private void rangeAdd(int l, int r, T val, int cl, int cr, int p) {
        if (l <= cl && cr <= r) { // 当前节点完全覆盖目标区间
            lazy[p] += val; // 更新懒惰标记
            tree[p] += (cr - cl + 1) * val; // 更新节点的值
            return;
        }
        int m = cl + (cr - cl) / 2; // 计算中点
        maintain(cl, cr, p); // 下传懒惰标记
        if (l <= m) { // 左子区间与目标区间有交集
            rangeAdd(l, r, val, cl, m, p * 2);
        }
        if (r > m) { // 右子区间与目标区间有交集
            rangeAdd(l, r, val, m + 1, cr, p * 2 + 1);
        }
        tree[p] = tree[p * 2] + tree[p * 2 + 1]; // 更新当前节点值
    }

    // 递归构建线段树
    private void build(int s, int t, int p) {
        if (s == t) { // 如果是叶子节点
            tree[p] = arr[s]; // 初始化叶子节点值
            return;
        }
        int m = s + (t - s) / 2; // 计算中点
        build(s, m, p * 2); // 递归构建左子树
        build(m + 1, t, p * 2 + 1); // 递归构建右子树
        tree[p] = tree[p * 2] + tree[p * 2 + 1]; // 初始化当前节点值
    }

    // 对外提供的区间加操作方法
    public void rangeAdd(int l, int r, T val) {
        rangeAdd(l, r, val, 0, end, root);
    }

    // 对外提供的区间和查询方法
    public T rangeSum(int l, int r) {
        return rangeSum(l, r, 0, end, root);
    }

    // 用于调试，显示线段树结构
    public void show(int p, int depth) {
        if (p > n4 || tree[p] == 0) return; // 如果节点超出范围或值为0，直接返回
        show(p * 2, depth + 1); // 显示左子树
        for (int i = 0; i < depth; ++i) System.out.print("\t");
        System.out.println(tree[p] + ":" + lazy[p]); // 显示当前节点
        show(p * 2 + 1, depth + 1); // 显示右子树
    }
}

```



- 区间修改/求和的线段树

``` c++##include <bits/stdc++.h>
using namespace std;

template <typename T>
class SegTreeLazyRangeSet {
  vector<T> tree, lazy;
  vector<T> *arr;
  vector<bool> ifLazy;
  int n, root, n4, end;

  void maintain(int cl, int cr, int p) {
    int cm = cl + (cr - cl) / 2;
    if (cl != cr && ifLazy[p]) {
      lazy[p * 2] = lazy[p],ifLazy[p*2] = 1;
      lazy[p * 2 + 1] = lazy[p],ifLazy[p*2+1] = 1;
      tree[p * 2] = lazy[p] * (cm - cl + 1);
      tree[p * 2 + 1] = lazy[p] * (cr - cm);
      lazy[p] = 0;
      ifLazy[p] = 0;
    }
  }

  T range_sum(int l, int r, int cl, int cr, int p) {
    if (l <= cl && cr <= r) return tree[p];
    int m = cl + (cr - cl) / 2;
    T sum = 0;
    maintain(cl, cr, p);
    if (l <= m) sum += range_sum(l, r, cl, m, p * 2);
    if (r > m) sum += range_sum(l, r, m + 1, cr, p * 2 + 1);
    return sum;
  }

  void range_set(int l, int r, T val, int cl, int cr, int p) {
    if (l <= cl && cr <= r) {
      lazy[p] = val;
      ifLazy[p] = 1;
      tree[p] = (cr - cl + 1) * val;
      return;
    }
    int m = cl + (cr - cl) / 2;
    maintain(cl, cr, p);
    if (l <= m) range_set(l, r, val, cl, m, p * 2);
    if (r > m) range_set(l, r, val, m + 1, cr, p * 2 + 1);
    tree[p] = tree[p * 2] + tree[p * 2 + 1];
  }

  void build(int s, int t, int p) {
    if (s == t) {
      tree[p] = (*arr)[s];
      return;
    }
    int m = s + (t - s) / 2;
    build(s, m, p * 2);
    build(m + 1, t, p * 2 + 1);
    tree[p] = tree[p * 2] + tree[p * 2 + 1];
  }

 public:
  explicit SegTreeLazyRangeSet<T>(vector<T> v) {
    n = v.size();
    n4 = n * 4;
    tree = vector<T>(n4, 0);
    lazy = vector<T>(n4, 0);
    ifLazy = vector<bool>(n4,0);
    arr = &v;
    end = n - 1;
    root = 1;
    build(0, end, 1);
    arr = nullptr;
  }

  void show(int p, int depth = 0) {
    if (p > n4 || tree[p] == 0) return;
    show(p * 2, depth + 1);
    for (int i = 0; i < depth; ++i) putchar('\t');
    printf("%d:%d\n", tree[p], lazy[p]);
    show(p * 2 + 1, depth + 1);
  }

  T range_sum(int l, int r) { return range_sum(l, r, 0, end, root); }

  void range_set(int l, int r, T val) { range_set(l, r, val, 0, end, root); }
};
```



``` java
import java.util.*;

// 泛型类 SegTreeLazyRangeSet，用于实现懒惰标记的线段树，支持区间修改（赋值）和区间求和
class SegTreeLazyRangeSet<T extends Number> {
    private T[] tree, lazy;          // tree 数组存储节点值，lazy 数组存储懒惰标记值
    private boolean[] ifLazy;        // ifLazy 数组标识懒惰标记是否有效
    private T[] arr;                 // 初始数组
    private int n, root, n4, end;    // n: 数组大小, root: 根节点编号, n4: 线段树大小, end: 数组末尾索引

    // 构造函数，接收一个数组用于初始化线段树
    public SegTreeLazyRangeSet(T[] inputArray) {
        n = inputArray.length;
        n4 = n * 4; // 根据线段树的性质，分配 4n 空间
        tree = (T[]) new Number[n4]; // 节点值数组
        lazy = (T[]) new Number[n4]; // 懒惰标记值数组
        ifLazy = new boolean[n4];    // 懒惰标记是否有效
        arr = inputArray;
        Arrays.fill(tree, 0);        // 初始化节点值为 0
        Arrays.fill(lazy, 0);        // 初始化懒惰标记值为 0
        Arrays.fill(ifLazy, false);  // 初始化懒惰标记无效
        end = n - 1;
        root = 1;                    // 根节点编号为 1
        build(0, end, 1);            // 递归构建线段树
        arr = null;                  // 构建完毕，释放初始数组引用
    }

    // 维护当前节点的懒惰标记并将标记下传到子节点
    private void maintain(int cl, int cr, int p) {
        int cm = cl + (cr - cl) / 2; // 计算当前区间的中点
        if (cl != cr && ifLazy[p]) { // 非叶子节点且懒惰标记有效时
            // 将懒惰标记传递给左子节点
            lazy[p * 2] = lazy[p];
            ifLazy[p * 2] = true;
            tree[p * 2] = lazy[p] * (cm - cl + 1); // 更新左子节点值
            // 将懒惰标记传递给右子节点
            lazy[p * 2 + 1] = lazy[p];
            ifLazy[p * 2 + 1] = true;
            tree[p * 2 + 1] = lazy[p] * (cr - cm); // 更新右子节点值
            lazy[p] = 0;  // 清空当前节点的懒惰标记值
            ifLazy[p] = false; // 标记当前节点的懒惰标记无效
        }
    }

    // 递归实现区间和查询
    private T rangeSum(int l, int r, int cl, int cr, int p) {
        if (l <= cl && cr <= r) { // 当前区间是目标区间的子集
            return tree[p];       // 直接返回当前节点的值
        }
        int m = cl + (cr - cl) / 2; // 计算中点
        maintain(cl, cr, p);        // 下传懒惰标记
        T sum = (T) (Integer) 0;    // 假设 T 为整型，初始化和为 0
        if (l <= m) {
            sum = add(sum, rangeSum(l, r, cl, m, p * 2)); // 查询左子区间
        }
        if (r > m) {
            sum = add(sum, rangeSum(l, r, m + 1, cr, p * 2 + 1)); // 查询右子区间
        }
        return sum; // 返回左右子区间的和
    }

    // 递归实现区间赋值操作
    private void rangeSet(int l, int r, T val, int cl, int cr, int p) {
        if (l <= cl && cr <= r) { // 当前区间是目标区间的子集
            lazy[p] = val;        // 设置懒惰标记
            ifLazy[p] = true;
            tree[p] = val * (cr - cl + 1); // 更新当前节点的值
            return;
        }
        int m = cl + (cr - cl) / 2; // 计算中点
        maintain(cl, cr, p);        // 下传懒惰标记
        if (l <= m) {
            rangeSet(l, r, val, cl, m, p * 2); // 更新左子区间
        }
        if (r > m) {
            rangeSet(l, r, val, m + 1, cr, p * 2 + 1); // 更新右子区间
        }
        tree[p] = add(tree[p * 2], tree[p * 2 + 1]); // 更新当前节点的值
    }

    // 递归构建线段树
    private void build(int s, int t, int p) {
        if (s == t) { // 如果是叶子节点
            tree[p] = arr[s]; // 将初始数组的值赋给节点
            return;
        }
        int m = s + (t - s) / 2; // 计算中点
        build(s, m, p * 2);      // 构建左子树
        build(m + 1, t, p * 2 + 1); // 构建右子树
        tree[p] = add(tree[p * 2], tree[p * 2 + 1]); // 初始化当前节点值
    }

    // 对外提供的区间和查询方法
    public T rangeSum(int l, int r) {
        return rangeSum(l, r, 0, end, root);
    }

    // 对外提供的区间赋值方法
    public void rangeSet(int l, int r, T val) {
        rangeSet(l, r, val, 0, end, root);
    }

    // 简单的调试方法，显示线段树结构
    public void show(int p, int depth) {
        if (p > n4 || tree[p] == 0) return; // 节点超出范围或无效
        show(p * 2, depth + 1);             // 显示左子树
        for (int i = 0; i < depth; ++i) System.out.print("\t");
        System.out.println(tree[p] + ":" + lazy[p]); // 显示当前节点
        show(p * 2 + 1, depth + 1);         // 显示右子树
    }

    // 辅助方法：两个数字相加（需要适配不同类型）
    private T add(T a, T b) {
        if (a instanceof Integer) {
            return (T) (Integer) (((Integer) a) + ((Integer) b));
        }
        if (a instanceof Long) {
            return (T) (Long) (((Long) a) + ((Long) b));
        }
        if (a instanceof Double) {
            return (T) (Double) (((Double) a) + ((Double) b));
        }
        // 可扩展支持其他类型
        throw new UnsupportedOperationException("Unsupported type: " + a.getClass());
    }
}

```




## 例题


### P3372 【模板】线段树 1
#### 题目描述

如题，已知一个数列 $\{a_i\}$，你需要进行下面两种操作：

1. 将某区间每一个数加上 $k$。
2. 求出某区间每一个数的和。
#### 输入格式

第一行包含两个整数 $n, m$，分别表示该数列数字的个数和操作的总个数。

第二行包含 $n$ 个用空格分隔的整数 $a_i$，其中第 $i$ 个数字表示数列第 $i$ 项的初始值。

接下来 $m$ 行每行包含 $3$ 或 $4$ 个整数，表示一个操作，具体如下：

1. `1 x y k`：将区间 $[x, y]$ 内每个数加上 $k$。
2. `2 x y`：输出区间 $[x, y]$ 内每个数的和。
#### 输出格式

输出包含若干行整数，即为所有操作 2 的结果。
#### 输入输出样例 #1
##### 输入 #1

```
5 5
1 5 4 2 3
2 2 4
1 2 3 2
2 3 4
1 1 5 1
2 1 4
```
##### 输出 #1

```
11
8
20
```
#### 说明/提示

对于 $15\%$ 的数据：$n \le 8$，$m \le 10$。  
对于 $35\%$ 的数据：$n \le {10}^3$，$m \le {10}^4$。    
对于 $100\%$ 的数据：$1 \le n, m \le {10}^5$，$a_i,k$ 为正数，且任意时刻数列的和不超过 $2\times 10^{18}$。

**【样例解释】**

![](https://cdn.luogu.com.cn/upload/pic/2251.png)





``` java
import java.util.*;
import java.io.*;

public class Main {
    static long[] a = new long[100005];//存储初始化的数组
    static long[] d = new long[270000];//存储线段树的区间和
    static long[] b = new long[270000];//存储懒惰标记

    static void build(int l, int r, int p) {
        // 是叶子节点
        if (l == r) {
            // 叶子节点值为编号本身
            d[p] = a[l];
            return;
        }
        // 不是叶子节点
        // 二分查找
        int m = l + ((r - l) >> 1);
        // 构造m左边的树
        build(l, m, p << 1);
        // 构造m右边的树，右边树坐标为当前坐标*2+1
        build(m + 1, r, (p << 1) | 1);
        // 当前节点值等于左右两边的和
        d[p] = d[p << 1] + d[(p << 1) | 1];
    }

    // 更新
    static void update(int l, int r, long c, int s, int t, int p) {
        // l:从l开始更新，r:右端点，c：需要更新成的值
        // 当前节点p代表的左端点，右端点，当前节点的编号
        if (l <= s && t <= r) {
            // 如果p点代表的端点在需要更新的范围内（l,r)
            // 将当前节点的值更新成节点数量*c
            d[p] += (t - s + 1) * c;
            // 懒标记当前节点值增加了c
            b[p] += c;
            return;
        }

        // 中点
        int m = s + ((t - s) >> 1);

        // 如果存在懒惰值，上面的赋值的b[p]
        if (b[p] != 0) {
            // p节点的左子树值=中点-左节点+1
            d[p << 1] += b[p] * (m - s + 1);
            // p右子树等于=右节点-中点
            d[(p << 1) | 1] += b[p] * (t - m);
            // 继续懒惰标记
            b[p << 1] += b[p];
            b[(p << 1) | 1] += b[p];
            // 当前节点的懒惰标记已被操作，取消懒惰
            b[p] = 0;
        }
        // 更新左子树
        if (l <= m) update(l, r, c, s, m, p << 1);
        // 更新右子树
        if (r > m) update(l, r, c, m + 1, t, (p << 1) | 1);

        //更新当前节点的值
        d[p] = d[p << 1] + d[(p << 1) | 1];
    }

    static long getsum(int l, int r, int s, int t, int p) {
        // l查询的左端点，r查询的右端点
        // s当前节点表示的左端点，当前节点表示的右端点，p当前节点的编号
        // 如果当前节点在需要查询的范围内
        if (l <= s && t <= r) {
            return d[p];
        }
        // 继续二分查找
        int m = s + ((t - s) >> 1);
        // 存在需要懒惰更新的值
        if (b[p] != 0) {
            d[p << 1] += b[p] * (m - s + 1);
            d[(p << 1) | 1] += b[p] * (t - m);
            b[p << 1] += b[p];
            b[(p << 1) | 1] += b[p];
            b[p] = 0;
        }

        long sum = 0;
        if (l <= m) sum += getsum(l, r, s, m, p << 1);
        if (r > m) sum += getsum(l, r, m + 1, t, (p << 1) | 1);
        return sum;
    }

    public static void main(String... arg) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        var in = new StreamTokenizer(br);
        in.nextToken();
        int n = (int) in.nval;
        in.nextToken();
        int q = (int) in.nval;
        for (int i = 1; i <= n; i++) {
            in.nextToken();
            a[i] = (long) in.nval;
        }
        // 初始化线段树
        build(1, n, 1);

        // q>=0
        while (q-- > 0) {
            in.nextToken();
            int i1 = (int) in.nval;
            in.nextToken();
            int i2 = (int) in.nval;
            in.nextToken();
            int i3 = (int) in.nval;
            if (i1 == 2) {
                System.out.println(getsum(i2, i3, 1, n, 1));
            } else {
                in.nextToken();
                long i4 = (long) in.nval;
                update(i2, i3, i4, 1, n, 1);
            }
        }
        br.close();
    }
}
```




### P3373 【模板】线段树 2
#### 题目描述

如题，已知一个数列，你需要进行下面三种操作：

- 将某区间每一个数乘上 $x$；
- 将某区间每一个数加上 $x$；
- 求出某区间每一个数的和。
#### 输入格式

第一行包含三个整数 $n,q,m$，分别表示该数列数字的个数、操作的总个数和模数。

第二行包含 $n$ 个用空格分隔的整数，其中第 $i$ 个数字表示数列第 $i$ 项的初始值。

接下来 $q$ 行每行包含若干个整数，表示一个操作，具体如下：

操作 $1$： 格式：`1 x y k`  含义：将区间 $[x,y]$ 内每个数乘上 $k$

操作 $2$： 格式：`2 x y k`  含义：将区间 $[x,y]$ 内每个数加上 $k$

操作 $3$： 格式：`3 x y`  含义：输出区间 $[x,y]$ 内每个数的和对 $m$ 取模所得的结果
#### 输出格式

输出包含若干行整数，即为所有操作 $3$ 的结果。
#### 输入输出样例 #1
##### 输入 #1

```
5 5 38
1 5 4 2 3
2 1 4 1
3 2 5
1 2 4 2
2 3 5 5
3 1 4
```
##### 输出 #1

```
17
2
```
#### 说明/提示

【数据范围】

对于 $30\%$ 的数据：$n \le 8$，$q \le 10$。  
对于 $70\%$ 的数据：$n \le 10^3 $，$q \le 10^4$。  
对于 $100\%$ 的数据：$1 \le n \le 10^5$，$1 \le q \le 10^5$。

除样例外，$m = 571373$。

（数据已经过加强 ^\_^）

样例说明：

 ![](https://cdn.luogu.com.cn/upload/pic/2255.png) 

故输出应为 $17$、$2$（$40 \bmod 38 = 2$）。





```java
import java.util.Scanner;

public class SegmentTree {
    // 定义变量：数组长度、操作次数、取模值
    static int n, m;
    static long mod;
    // 定义数组：原数组、区间和数组、乘法懒标记数组、加法懒标记数组
    static long[] a = new long[100005];
    static long[] sum = new long[400005];
    static long[] mul = new long[400005];
    static long[] laz = new long[400005];

    // 更新节点信息，合并左右子节点的区间和
    public static void up(int i) {
        sum[i] = (sum[i << 1] + sum[(i << 1) | 1]) % mod;
    }

    // 处理懒标记：将当前节点的懒标记下放到子节点
    public static void pd(int i, int s, int t) {
        int l = i << 1, r = (i << 1) | 1, mid = (s + t) >> 1;
        // 如果存在乘法懒标记，更新左右子节点
        if (mul[i] != 1) {
            mul[l] = (mul[l] * mul[i]) % mod;
            mul[r] = (mul[r] * mul[i]) % mod;
            laz[l] = (laz[l] * mul[i]) % mod;
            laz[r] = (laz[r] * mul[i]) % mod;
            sum[l] = (sum[l] * mul[i]) % mod;
            sum[r] = (sum[r] * mul[i]) % mod;
            mul[i] = 1; // 清空当前节点的乘法懒标记
        }
        // 如果存在加法懒标记，更新左右子节点
        if (laz[i] != 0) {
            sum[l] = (sum[l] + laz[i] * (mid - s + 1)) % mod;
            sum[r] = (sum[r] + laz[i] * (t - mid)) % mod;
            laz[l] = (laz[l] + laz[i]) % mod;
            laz[r] = (laz[r] + laz[i]) % mod;
            laz[i] = 0; // 清空当前节点的加法懒标记
        }
    }

    // 构建线段树
    public static void build(int s, int t, int i) {
        mul[i] = 1; // 初始化乘法懒标记
        if (s == t) { // 如果是叶子节点
            sum[i] = a[s]; // 将原数组的值赋给叶子节点
            return;
        }
        int mid = (s + t) >> 1; // 计算中点
        build(s, mid, i << 1); // 构建左子树
        build(mid + 1, t, (i << 1) | 1); // 构建右子树
        up(i); // 更新当前节点的信息
    }

    // 区间乘法操作：将区间内的值全部乘以某个数
    public static void chen(int l, int r, int s, int t, int i, long z) {
        int mid = (s + t) >> 1;
        if (l <= s && t <= r) { // 当前区间完全包含在目标区间内
            mul[i] = (mul[i] * z) % mod; // 更新乘法懒标记
            laz[i] = (laz[i] * z) % mod; // 更新加法懒标记
            sum[i] = (sum[i] * z) % mod; // 更新区间和
            return;
        }
        pd(i, s, t); // 下放懒标记
        if (mid >= l) chen(l, r, s, mid, i << 1, z); // 左子树递归
        if (mid + 1 <= r) chen(l, r, mid + 1, t, (i << 1) | 1, z); // 右子树递归
        up(i); // 更新当前节点的信息
    }

    // 区间加法操作：将区间内的值全部加上某个数
    public static void add(int l, int r, int s, int t, int i, long z) {
        int mid = (s + t) >> 1;
        if (l <= s && t <= r) { // 当前区间完全包含在目标区间内
            sum[i] = (sum[i] + z * (t - s + 1)) % mod; // 更新区间和
            laz[i] = (laz[i] + z) % mod; // 更新加法懒标记
            return;
        }
        pd(i, s, t); // 下放懒标记
        if (mid >= l) add(l, r, s, mid, i << 1, z); // 左子树递归
        if (mid + 1 <= r) add(l, r, mid + 1, t, (i << 1) | 1, z); // 右子树递归
        up(i); // 更新当前节点的信息
    }

    // 区间查询：查询区间内的和
    public static long getAns(int l, int r, int s, int t, int i) {
        int mid = (s + t) >> 1;
        long tot = 0;
        if (l <= s && t <= r) return sum[i]; // 当前区间完全包含在目标区间内
        pd(i, s, t); // 下放懒标记
        if (mid >= l) tot = (tot + getAns(l, r, s, mid, i << 1)) % mod; // 左子树递归查询
        if (mid + 1 <= r) tot = (tot + getAns(l, r, mid + 1, t, (i << 1) | 1)) % mod; // 右子树递归查询
        return tot % mod; // 返回结果取模
    }

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        n = sc.nextInt(); // 输入数组长度
        m = sc.nextInt(); // 输入操作次数
        mod = sc.nextLong(); // 输入取模值
        for (int i = 1; i <= n; i++) {
            a[i] = sc.nextLong(); // 输入原数组
        }
        build(1, n, 1); // 构建线段树
        for (int i = 1; i <= m; i++) {
            int bh = sc.nextInt(); // 输入操作类型
            if (bh == 1) {
                int x = sc.nextInt(), y = sc.nextInt();
                long z = sc.nextLong();
                chen(x, y, 1, n, 1, z); // 区间乘法操作
            } else if (bh == 2) {
                int x = sc.nextInt(), y = sc.nextInt();
                long z = sc.nextLong();
                add(x, y, 1, n, 1, z); // 区间加法操作
            } else if (bh == 3) {
                int x = sc.nextInt(), y = sc.nextInt();
                System.out.println(getAns(x, y, 1, n, 1)); // 区间查询操作
            }
        }
        sc.close(); // 关闭输入流
    }
}

```

