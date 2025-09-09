---
title:  读《重学java设计模式》有感
description:  小傅哥的金典书籍，对设计模式有个笼统的了解。目前还在攻读中。。
image: 1.png
date: 2025-09-09
slug: java-Ontwerp-patroon
categories: 
  - 精选
  - 设计模式
  - 架构
tags:
  - 设计模式
  - 读后感
  - 架构
---


> 设计模式的原则

## 第二章、6大设计原则

#### 1、单一职责原则

对于常需要修改的类，不应当维护两个以上的职责。如一个客户类，不应当维护普通客户，同时也维护VIP客户。



- 常见做法

构造客户功能的接口，不同的客户有不同客户的实现类。在实现客户功能时，每种客户都有不同的实现。客户之间相互独立，不会应为修改了普通客户的功能而影响到VIP客户的功能。



- 优点

避免了大量的if else

每种实现之间解耦，互不影响。

- 缺点

增加维护成本。

需要新建大量实现类和代码。



![1745222013194.png](https://fastly.jsdelivr.net/gh/thecoolboyhan/th_blogs@main/image/2025-04/1745222013194_1745222013217.png)

- bad

https://github.com/thecoolboyhan/personStudy/tree/c831c28ba2b994c38d066ef825c147e4353dff1f/design_patterns/src/%E9%87%8D%E5%AD%A6%E8%AE%BE%E8%AE%A1%E6%A8%A1%E5%BC%8F/Section2/%E5%8D%95%E4%B8%80%E8%81%8C%E8%B4%A3%E5%8E%9F%E5%88%99/bad



- good

https://github.com/thecoolboyhan/personStudy/tree/c831c28ba2b994c38d066ef825c147e4353dff1f/design_patterns/src/%E9%87%8D%E5%AD%A6%E8%AE%BE%E8%AE%A1%E6%A8%A1%E5%BC%8F/Section2/%E5%8D%95%E4%B8%80%E8%81%8C%E8%B4%A3%E5%8E%9F%E5%88%99/good

#### 2、开闭原则

> 面向抽象编程

应用只定义抽象结构，用实现来扩展细节。如应用自己的方法，和调用其他方法，因只调用其抽象类，具体的执行都由实现类来编写。



如果想添加或修改原有的功能，可以采用不同的实现类来编写。



- 问题

如果所有的方法都用实现类来实现，是否在修改时，还要修改调用时创建的实现类。如果代码运行时间常，是否会多出许多无用的实现类。



- 案例代码

https://github.com/thecoolboyhan/personStudy/tree/c831c28ba2b994c38d066ef825c147e4353dff1f/design_patterns/src/%E9%87%8D%E5%AD%A6%E8%AE%BE%E8%AE%A1%E6%A8%A1%E5%BC%8F/Section2/%E5%BC%80%E9%97%AD%E5%8E%9F%E5%88%99

#### 3、里氏替换原则

> 继承必须确保超类所拥有的性质在子类中仍然成立。
>
> “正方形不是长方形”



子类可以扩展父类的功能，但不能改变父类原有的功能。



1. 子类可以实现父类的抽象方法，但不能覆盖父类的非抽象方法
2. 子类可以增加父类特有的方法
3. 当子类的方法重载父类的方法时，方法的前置条件（入参）要比父类更宽松
4. 当子类的方法实现父类的方法（重写、重载、实现抽象方法），方法的返回值要比父类更严格或与父类相等。

##### 里氏替换的优点

1. 实现开闭原则的重要方式之一（主要方式）
2. 继承中重写父类造成的可复用性变差的问题。（解决了前面的疑问）
3. 为修改提供了正确性的保证，类的扩展不会给已有的系统引入新的错误，降低了代码出错的可能性。
4. 增加健壮性，同时变更时可以做到非常好的兼容性，降低风险。



- 案例代码

  https://github.com/thecoolboyhan/personStudy/tree/c831c28ba2b994c38d066ef825c147e4353dff1f/design_patterns/src/%E9%87%8D%E5%AD%A6%E8%AE%BE%E8%AE%A1%E6%A8%A1%E5%BC%8F/Section2/%E9%87%8C%E6%B0%8F%E6%9B%BF%E6%8D%A2%E5%8E%9F%E5%88%99

#### 4、迪米特法则原则

> 最少知道原则

两个类之间不要有过多的耦合关系，保持最少关联性。

每个层级的类都之和与自己直接关联的层级类来调用，不要出现跨级调用。（如：controller中调用repository）



#### 5、接口隔离原则

> 客户端不应该被迫依赖它不使用的方法。

一个类对另一个类的依赖应该建立在最小的接口上。



- bad



接口设计时，不应该让多数实现此接口的类要实现一些无用的接口。



- good

一个有多个方法的接口，应当拆成多个接口，需要使用对应功能时，才去实现对应的接口。



- 案例代码

  https://github.com/thecoolboyhan/personStudy/tree/c831c28ba2b994c38d066ef825c147e4353dff1f/design_patterns/src/%E9%87%8D%E5%AD%A6%E8%AE%BE%E8%AE%A1%E6%A8%A1%E5%BC%8F/Section2/%E6%8E%A5%E5%8F%A3%E9%9A%94%E7%A6%BB%E5%8E%9F%E5%88%99



#### 6、依赖倒置原则

高层模块不应该依赖于底层模块，二者都应该依赖于抽象。抽象不应该依赖于细节，细节应该依赖于抽象。


## 第四章、工厂模式


### 介绍

> 工厂模式是创建型设计模式的一种，提供了创建对象的最佳方式。

定义一个创建对象的接口，让其子类自己决定将哪一个工厂类实例化，工厂模式让创建过程延迟到子类中进行。

- 缺点

需要治理，如果实现的类比较多、难以维护、开发成本高。（需要结合不同的设计模式逐步优化）


### 模拟发放多种奖品

![1748401855514.png](https://fastly.jsdelivr.net/gh/thecoolboyhan/th_blogs@main/image/2025-05/1748401855514_1748401855529.png)

需要完成上面三种兑换方式：

发放优惠券需要防重，兑换卡需要卡ID，实物商品

需要发货位置（对象中含有）


#### 反例



``` java
public class PrizeController {

    private Logger logger = LoggerFactory.getLogger(PrizeController.class);

    public AwardRes awardToUser(AwardReq req) {
        String reqJson = JSON.toJSONString(req);
        AwardRes awardRes = null;
        try {
            logger.info("奖品发放开始{}。req:{}", req.getuId(), reqJson);
            // 按照不同类型方法商品[1优惠券、2实物商品、3第三方兑换卡(爱奇艺)]
            if (req.getAwardType() == 1) {
                CouponService couponService = new CouponService();
                CouponResult couponResult = couponService.sendCoupon(req.getuId(), req.getAwardNumber(), req.getBizId());
                if ("0000".equals(couponResult.getCode())) {
                    awardRes = new AwardRes("0000", "发放成功");
                } else {
                    awardRes = new AwardRes("0001", couponResult.getInfo());
                }
            } else if (req.getAwardType() == 2) {
                GoodsService goodsService = new GoodsService();
                DeliverReq deliverReq = new DeliverReq();
                deliverReq.setUserName(queryUserName(req.getuId()));
                deliverReq.setUserPhone(queryUserPhoneNumber(req.getuId()));
                deliverReq.setSku(req.getAwardNumber());
                deliverReq.setOrderId(req.getBizId());
                deliverReq.setConsigneeUserName(req.getExtMap().get("consigneeUserName"));
                deliverReq.setConsigneeUserPhone(req.getExtMap().get("consigneeUserPhone"));
                deliverReq.setConsigneeUserAddress(req.getExtMap().get("consigneeUserAddress"));
                Boolean isSuccess = goodsService.deliverGoods(deliverReq);
                if (isSuccess) {
                    awardRes = new AwardRes("0000", "发放成功");
                } else {
                    awardRes = new AwardRes("0001", "发放失败");
                }
            } else if (req.getAwardType() == 3) {
                String bindMobileNumber = queryUserPhoneNumber(req.getuId());
                IQiYiCardService iQiYiCardService = new IQiYiCardService();
                iQiYiCardService.grantToken(bindMobileNumber, req.getAwardNumber());
                awardRes = new AwardRes("0000", "发放成功");
            }
            logger.info("奖品发放完成{}。", req.getuId());
        } catch (Exception e) {
            logger.error("奖品发放失败{}。req:{}", req.getuId(), reqJson, e);
            awardRes = new AwardRes("0001", e.getMessage());
        }

        return awardRes;
    }

    private String queryUserName(String uId) {
        return "花花";
    }

    private String queryUserPhoneNumber(String uId) {
        return "15200101232";
    }

}
```



上面代码中一共有三种类型的营销方式，就通过三个if..else来实现功能。如果后续添加的新的模式，自然就是新的if..else


#### 正例

- 发奖品的接口

所有奖品发放，上方类只需要调用接口，接口的实现由工厂方法产生

```java
public interface ICommodity {
    void sendCommodity(String uId, String commodityId, String bizId, Map<String, String> extMap) throws Exception;
}
```



- 兑换卡

```java
public class CardCommodityService implements ICommodity {

    private Logger logger = LoggerFactory.getLogger(CardCommodityService.class);

    // 模拟注入
//    private IQiYiCardService iQiYiCardService = new IQiYiCardService();

    public void sendCommodity(String uId, String commodityId, String bizId, Map<String, String> extMap) throws Exception {
        
        String mobile = queryUserMobile(uId);
        iQiYiCardService.grantToken(mobile, bizId);
        logger.info("请求参数[爱奇艺兑换卡] => uId：{} commodityId：{} bizId：{} extMap：{}", uId, commodityId, bizId, JSON.toJSON(extMap));
        logger.info("测试结果[爱奇艺兑换卡]：success");
         
    }

    private String queryUserMobile(String uId) {
        return "15200101232";
    }

}
```



- 优惠券

```java
public class CouponCommodityService implements ICommodity {

    private Logger logger = LoggerFactory.getLogger(CouponCommodityService.class);

//    private CouponService couponService = new CouponService();

    public void sendCommodity(String uId, String commodityId, String bizId, Map<String, String> extMap) throws Exception {
        
        CouponResult couponResult = couponService.sendCoupon(uId, commodityId, bizId);
        logger.info("请求参数[优惠券] => uId：{} commodityId：{} bizId：{} extMap：{}", uId, commodityId, bizId, JSON.toJSON(extMap));
        logger.info("测试结果[优惠券]：{}", JSON.toJSON(couponResult));
        if (!"0000".equals(couponResult.getCode())) throw new RuntimeException(couponResult.getInfo());
         
    }

}
```



- 实物

```java
//实物商品
public class GoodsCommodityService implements ICommodity {

    private Logger logger = LoggerFactory.getLogger(GoodsCommodityService.class);

    private GoodsService goodsService = new GoodsService();

    public void sendCommodity(String uId, String commodityId, String bizId, Map<String, String> extMap) throws Exception {
        DeliverReq deliverReq = new DeliverReq();
        deliverReq.setUserName(queryUserName(uId));
        deliverReq.setUserPhone(queryUserPhoneNumber(uId));
        deliverReq.setSku(commodityId);
        deliverReq.setOrderId(bizId);
        deliverReq.setConsigneeUserName(extMap.get("consigneeUserName"));
        deliverReq.setConsigneeUserPhone(extMap.get("consigneeUserPhone"));
        deliverReq.setConsigneeUserAddress(extMap.get("consigneeUserAddress"));

        Boolean isSuccess = goodsService.deliverGoods(deliverReq);

        logger.info("请求参数[优惠券] => uId：{} commodityId：{} bizId：{} extMap：{}", uId, commodityId, bizId, JSON.toJSON(extMap));
        logger.info("测试结果[优惠券]：{}", isSuccess);

        if (!isSuccess) throw new RuntimeException("实物商品发放失败");
         
    }

    private String queryUserName(String uId) {
        return "花花";
    }

    private String queryUserPhoneNumber(String uId) {
        return "15200101232";
    }

}
```



- 商品工厂

```java
//商品工厂，得到不同类型的服务
public class StoreFactory {

    public ICommodity getCommodityService(Integer commodityType) {
        if (null == commodityType) return null;
        if (1 == commodityType) return new CouponCommodityService();
        if (2 == commodityType) return new GoodsCommodityService();
        if (3 == commodityType) return new CardCommodityService();
        throw new RuntimeException("不存在的商品服务类型");
    }
}
```



方法调用者只需要向工厂中输入服务类型，就可以得到不同的实现。后续想要扩展也只需要在工厂方法中添加，调用者不需要关心。


### 总结



- 优点

1. 避免创建者与具体的产品逻辑耦合
2. 满足单一职责，每个业务逻辑实现都在所属自己的类中完成
3. 满足开闭原则，无需修改调用方，就可以在程序中加入新的产品类型


## 抽象工厂模式



> 抽象工厂也称其他工厂的工厂，可以在抽象工厂中创建出其他工厂，与工厂模式一样，都是用来解决接口选择的问题，同样属于创建型模式。




### 案例1





1. 很多服务用到了Redis需要一起升级到集群。
2. 需要兼容集群A和集群B，便于后续的灾备。
3. 两套集群提供的接口和方法各有差异，需要做适配。
4. 不能影响到目前正常运行的系统。



目前有两个集群和一个单机redis现在需要做整合

- 项目结构：

``` diff
itstack-demo-design-2-00
└── src
    └── main
        └── java
            └── org.itstack.demo.design
                ├── matter
                │   ├── EGM.java
                │   └── IIR.java
                └── RedisUtils.java
```







- 原单机redis代码

![1753252779932.png](https://fastly.jsdelivr.net/gh/thecoolboyhan/th_blogs@main/image/2025-07/1753252779932_1753252779958.png)



- 集群EGM

![1753253037454.png](https://fastly.jsdelivr.net/gh/thecoolboyhan/th_blogs@main/image/2025-07/1753253037454_1753253037498.png)





- 集群IIR

![1753253072855.png](https://fastly.jsdelivr.net/gh/thecoolboyhan/th_blogs@main/image/2025-07/1753253072855_1753253072871.png)







- 传统if-else模式来实现调用

``` java
public class CacheServiceImpl implements CacheService {

    private RedisUtils redisUtils = new RedisUtils();

    private EGM egm = new EGM();

    private IIR iir = new IIR();

    public String get(String key, int redisType) {

        if (1 == redisType) {
            return egm.gain(key);
        }

        if (2 == redisType) {
            return iir.get(key);
        }

        return redisUtils.get(key);
    }

    public void set(String key, String value, int redisType) {

        if (1 == redisType) {
            egm.set(key, value);
            return;
        }

        if (2 == redisType) {
            iir.set(key, value);
            return;
        }

        redisUtils.set(key, value);
    }

    //... 同类不做太多展示，可以下载源码进行参考

}
```



> 按照上面模式修改，如果添加新集群，后续运维会非常困难。


### 利用抽象工厂来重构代码





![1753263026952.png](https://fastly.jsdelivr.net/gh/thecoolboyhan/th_blogs@main/image/2025-07/1753263026952_1753263026973.png)



利用代理类来实现抽象工厂的创建和获取，利用适配器来适配不同redis集群中的不同API。



- 结构图

``` xml
itstack-demo-design-2-02
└── src
    ├── main
    │   └── java
    │       └── org.itstack.demo.design
    │           ├── factory    
    │           │   ├── impl
    │           │   │   ├── EGMCacheAdapter.java 
    │           │   │   └── IIRCacheAdapter.java
    │           │   ├── ICacheAdapter.java
    │           │   ├── JDKInvocationHandler.java
    │           │   └── JDKProxy.java
    │           ├── impl
    │           │   └── CacheServiceImpl.java    
    │           └── CacheService.java 
    └── test
         └── java
             └── org.itstack.demo.design.test
                 └── ApiTest.java
```







1. ICacheAdapter:适配接口，分别包装两个集群中差异化的接口名称。EGMCacheAdapter`、`IIRCacheAdapter
2. `JDKProxy`、`JDKInvocationHandler`，是代理类的定义和实现，这部分也就是抽象工厂的另外一种实现方式。通过这样的方式可以很好的把原有操作Redis的方法进行代理操作，通过控制不同的入参对象，控制缓存的使用。





- 适配器接口

``` java
public interface ICacheAdapter {

    String get(String key);

    void set(String key, String value);

    void set(String key, String value, long timeout, TimeUnit timeUnit);

    void del(String key);

}
```





- 两个集群对于适配器的不同实现

``` java
public class EGMCacheAdapter implements ICacheAdapter {

    private EGM egm = new EGM();

    public String get(String key) {
        return egm.gain(key);
    }

    public void set(String key, String value) {
        egm.set(key, value);
    }

    public void set(String key, String value, long timeout, TimeUnit timeUnit) {
        egm.setEx(key, value, timeout, timeUnit);
    }

    public void del(String key) {
        egm.delete(key);
    }
}
```



``` java
public class IIRCacheAdapter implements ICacheAdapter {

    private IIR iir = new IIR();

    public String get(String key) {
        return iir.get(key);
    }

    public void set(String key, String value) {
        iir.set(key, value);
    }

    public void set(String key, String value, long timeout, TimeUnit timeUnit) {
        iir.setExpire(key, value, timeout, timeUnit);
    }

    public void del(String key) {
        iir.del(key);
    }

}
```



- 抽象工厂的代理类

JDK动态代理JDKProxy

``` java
public static <T> T getProxy(Class<T> interfaceClass, ICacheAdapter cacheAdapter) throws Exception {
    InvocationHandler handler = new JDKInvocationHandler(cacheAdapter);
    ClassLoader classLoader = Thread.currentThread().getContextClassLoader();
    Class<?>[] classes = interfaceClass.getInterfaces();
    return (T) Proxy.newProxyInstance(classLoader, new Class[]{classes[0]}, handler);
}
```



- **JDKInvocationHandler**详细invoke的方法，通过适配器来进行调用

``` java
public class JDKInvocationHandler implements InvocationHandler {

    private ICacheAdapter cacheAdapter;

    public JDKInvocationHandler(ICacheAdapter cacheAdapter) {
        this.cacheAdapter = cacheAdapter;
    }

    public Object invoke(Object proxy, Method method, Object[] args) throws Throwable {
        return ICacheAdapter.class.getMethod(method.getName(), ClassLoaderUtils.getClazzByArgs(args)).invoke(cacheAdapter, args);
    }

}
```





- 后续扩展

1. 添加新的适配器，实现ICacheAdapter接口，并实现相应的方法
2. 调用时通过JDKProxy动态代理创建类，创建1中实现的适配器
3. 后续调用只需利用之前的动态代理创建新的代理类，调用等API全部相同

JDKProxy.getProxy(CacheServiceImpl.class, new EGMCacheAdapter());

> 真正意义上对现有代码完全无侵入




### 总结

抽象工厂模式，解决的问题为在一个产品族中，存在多个不同类型的产品（redis集群，操作系统）情况下，接口选择问题。



本设计满足：单一职责、开闭原则、解耦等优点，但如果说随着业务的不断拓展，可能会造成类实现上的复杂度。但也可以说算不上缺点，因为可以随着其他设计方式的引入和代理类以及自动生成加载的方式降低此项缺点。

## 原型模式

> 原型模式主要解决的问题就是创建重复对象，而这部分对象内容比较复杂，生成过程可能从库或者RPC接口中获取数据的耗时比较长，因此采用克隆的方式节省时间。




### 上机考试案例



> 需要实现一个上级考试抽题的服务



``` xml
itstack-demo-design-4-00
└── src
    └── main
        └── java
            └── org.itstack.demo.design
                ├── AnswerQuestion.java
                └── ChoiceQuestion.java
```



- 选择题

``` java
public class ChoiceQuestion {

    private String name;                 // 题目
    private Map<String, String> option;  // 选项；A、B、C、D
    private String key;                  // 答案；B

    public ChoiceQuestion() {
    }

    public ChoiceQuestion(String name, Map<String, String> option, String key) {
        this.name = name;
        this.option = option;
        this.key = key;
    }

    // ...get/set
}
```





- 问答题

``` java
public class AnswerQuestion {

    private String name;  // 问题
    private String key;   // 答案

    public AnswerQuestion() {
    }

    public AnswerQuestion(String name, String key) {
        this.name = name;
        this.key = key;
    }

    // ...get/set
}
```


### bad

```xml
itstack-demo-design-4-01
└── src
    └── main
        └── java
            └── org.itstack.demo.design
                └── QuestionBankController.java
```





- 梭哈

``` java
public class QuestionBankController {

    public String createPaper(String candidate, String number) {

        List<ChoiceQuestion> choiceQuestionList = new ArrayList<ChoiceQuestion>();
        List<AnswerQuestion> answerQuestionList = new ArrayList<AnswerQuestion>();

        Map<String, String> map01 = new HashMap<String, String>();
        map01.put("A", "JAVA2 EE");
        map01.put("B", "JAVA2 Card");
        map01.put("C", "JAVA2 ME");
        map01.put("D", "JAVA2 HE");
        map01.put("E", "JAVA2 SE");

        Map<String, String> map02 = new HashMap<String, String>();
        map02.put("A", "JAVA程序的main方法必须写在类里面");
        map02.put("B", "JAVA程序中可以有多个main方法");
        map02.put("C", "JAVA程序中类名必须与文件名一样");
        map02.put("D", "JAVA程序的main方法中如果只有一条语句，可以不用{}(大括号)括起来");

        Map<String, String> map03 = new HashMap<String, String>();
        map03.put("A", "变量由字母、下划线、数字、$符号随意组成；");
        map03.put("B", "变量不能以数字作为开头；");
        map03.put("C", "A和a在java中是同一个变量；");
        map03.put("D", "不同类型的变量，可以起相同的名字；");

        Map<String, String> map04 = new HashMap<String, String>();
        map04.put("A", "STRING");
        map04.put("B", "x3x;");
        map04.put("C", "void");
        map04.put("D", "de$f");

        Map<String, String> map05 = new HashMap<String, String>();
        map05.put("A", "31");
        map05.put("B", "0");
        map05.put("C", "1");
        map05.put("D", "2");

        choiceQuestionList.add(new ChoiceQuestion("JAVA所定义的版本中不包括", map01, "D"));
        choiceQuestionList.add(new ChoiceQuestion("下列说法正确的是", map02, "A"));
        choiceQuestionList.add(new ChoiceQuestion("变量命名规范说法正确的是", map03, "B"));
        choiceQuestionList.add(new ChoiceQuestion("以下()不是合法的标识符", map04, "C"));
        choiceQuestionList.add(new ChoiceQuestion("表达式(11+3*8)/4%3的值是", map05, "D"));
        answerQuestionList.add(new AnswerQuestion("小红马和小黑马生的小马几条腿", "4条腿"));
        answerQuestionList.add(new AnswerQuestion("铁棒打头疼还是木棒打头疼", "头最疼"));
        answerQuestionList.add(new AnswerQuestion("什么床不能睡觉", "牙床"));
        answerQuestionList.add(new AnswerQuestion("为什么好马不吃回头草", "后面的草没了"));

        // 输出结果
        StringBuilder detail = new StringBuilder("考生：" + candidate + "\r\n" +
                "考号：" + number + "\r\n" +
                "--------------------------------------------\r\n" +
                "一、选择题" + "\r\n\n");

        for (int idx = 0; idx < choiceQuestionList.size(); idx++) {
            detail.append("第").append(idx + 1).append("题：").append(choiceQuestionList.get(idx).getName()).append("\r\n");
            Map<String, String> option = choiceQuestionList.get(idx).getOption();
            for (String key : option.keySet()) {
                detail.append(key).append("：").append(option.get(key)).append("\r\n");
                ;
            }
            detail.append("答案：").append(choiceQuestionList.get(idx).getKey()).append("\r\n\n");
        }

        detail.append("二、问答题" + "\r\n\n");

        for (int idx = 0; idx < answerQuestionList.size(); idx++) {
            detail.append("第").append(idx + 1).append("题：").append(answerQuestionList.get(idx).getName()).append("\r\n");
            detail.append("答案：").append(answerQuestionList.get(idx).getKey()).append("\r\n\n");
        }

        return detail.toString();
    }

}
```






### good



原型模式解决的问题为创建大量重复的类。

重复创建有时需要用到远程RPC调用，将消耗大量的时间。原型模式利用本地克隆的方式。



> 在需要用到克隆的类中都需要实现 `implements Cloneable` 接口。



``` xml
itstack-demo-design-4-02
└── src
    ├── main
    │   └── java
    │       └── org.itstack.demo.design
    │           ├── util
    │           │   ├── Topic.java
    │           │   └── TopicRandomUtil.java
    │           ├── QuestionBank.java
    │           └── QuestionBankController.java 
    └── test
         └── java
             └── org.itstack.demo.design.test
                 └── ApiTest.java
```





![1753345440048.png](https://fastly.jsdelivr.net/gh/thecoolboyhan/th_blogs@main/image/2025-07/1753345440048_1753345440072.png)



- 题目选项打乱

``` java
/**
 * 乱序Map元素，记录对应答案key
 * @param option 题目
 * @param key    答案
 * @return Topic 乱序后 {A=c., B=d., C=a., D=b.}
 */
static public Topic random(Map<String, String> option, String key) {
    Set<String> keySet = option.keySet();
    ArrayList<String> keyList = new ArrayList<String>(keySet);
    Collections.shuffle(keyList);
    HashMap<String, String> optionNew = new HashMap<String, String>();
    int idx = 0;
    String keyNew = "";
    for (String next : keySet) {
        String randomKey = keyList.get(idx++);
        if (key.equals(next)) {
            keyNew = randomKey;
        }
        optionNew.put(randomKey, option.get(next));
    }
    return new Topic(optionNew, keyNew);
}
```





- 克隆对象处理

``` java
public class QuestionBank implements Cloneable {

    private String candidate; // 考生
    private String number;    // 考号

    private ArrayList<ChoiceQuestion> choiceQuestionList = new ArrayList<ChoiceQuestion>();
    private ArrayList<AnswerQuestion> answerQuestionList = new ArrayList<AnswerQuestion>();

    public QuestionBank append(ChoiceQuestion choiceQuestion) {
        choiceQuestionList.add(choiceQuestion);
        return this;
    }

    public QuestionBank append(AnswerQuestion answerQuestion) {
        answerQuestionList.add(answerQuestion);
        return this;
    }

    @Override
    public Object clone() throws CloneNotSupportedException {
        QuestionBank questionBank = (QuestionBank) super.clone();
        questionBank.choiceQuestionList = (ArrayList<ChoiceQuestion>) choiceQuestionList.clone();
        questionBank.answerQuestionList = (ArrayList<AnswerQuestion>) answerQuestionList.clone();

        // 题目乱序
        Collections.shuffle(questionBank.choiceQuestionList);
        Collections.shuffle(questionBank.answerQuestionList);
        // 答案乱序
        ArrayList<ChoiceQuestion> choiceQuestionList = questionBank.choiceQuestionList;
        for (ChoiceQuestion question : choiceQuestionList) {
            Topic random = TopicRandomUtil.random(question.getOption(), question.getKey());
            question.setOption(random.getOption());
            question.setKey(random.getKey());
        }
        return questionBank;
    }

    public void setCandidate(String candidate) {
        this.candidate = candidate;
    }

    public void setNumber(String number) {
        this.number = number;
    }

    @Override
    public String toString() {

        StringBuilder detail = new StringBuilder("考生：" + candidate + "\r\n" +
                "考号：" + number + "\r\n" +
                "--------------------------------------------\r\n" +
                "一、选择题" + "\r\n\n");

        for (int idx = 0; idx < choiceQuestionList.size(); idx++) {
            detail.append("第").append(idx + 1).append("题：").append(choiceQuestionList.get(idx).getName()).append("\r\n");
            Map<String, String> option = choiceQuestionList.get(idx).getOption();
            for (String key : option.keySet()) {
                detail.append(key).append("：").append(option.get(key)).append("\r\n");;
            }
            detail.append("答案：").append(choiceQuestionList.get(idx).getKey()).append("\r\n\n");
        }

        detail.append("二、问答题" + "\r\n\n");

        for (int idx = 0; idx < answerQuestionList.size(); idx++) {
            detail.append("第").append(idx + 1).append("题：").append(answerQuestionList.get(idx).getName()).append("\r\n");
            detail.append("答案：").append(answerQuestionList.get(idx).getKey()).append("\r\n\n");
        }

        return detail.toString();
    }

}
```





- 初始化试卷

``` java
public class QuestionBankController {

    private QuestionBank questionBank = new QuestionBank();

    public QuestionBankController() {

        Map<String, String> map01 = new HashMap<String, String>();
        map01.put("A", "JAVA2 EE");
        map01.put("B", "JAVA2 Card");
        map01.put("C", "JAVA2 ME");
        map01.put("D", "JAVA2 HE");
        map01.put("E", "JAVA2 SE");

        Map<String, String> map02 = new HashMap<String, String>();
        map02.put("A", "JAVA程序的main方法必须写在类里面");
        map02.put("B", "JAVA程序中可以有多个main方法");
        map02.put("C", "JAVA程序中类名必须与文件名一样");
        map02.put("D", "JAVA程序的main方法中如果只有一条语句，可以不用{}(大括号)括起来");

        Map<String, String> map03 = new HashMap<String, String>();
        map03.put("A", "变量由字母、下划线、数字、$符号随意组成；");
        map03.put("B", "变量不能以数字作为开头；");
        map03.put("C", "A和a在java中是同一个变量；");
        map03.put("D", "不同类型的变量，可以起相同的名字；");

        Map<String, String> map04 = new HashMap<String, String>();
        map04.put("A", "STRING");
        map04.put("B", "x3x;");
        map04.put("C", "void");
        map04.put("D", "de$f");

        Map<String, String> map05 = new HashMap<String, String>();
        map05.put("A", "31");
        map05.put("B", "0");
        map05.put("C", "1");
        map05.put("D", "2");
        
        questionBank.append(new ChoiceQuestion("JAVA所定义的版本中不包括", map01, "D"))
                .append(new ChoiceQuestion("下列说法正确的是", map02, "A"))
                .append(new ChoiceQuestion("变量命名规范说法正确的是", map03, "B"))
                .append(new ChoiceQuestion("以下()不是合法的标识符",map04, "C"))
                .append(new ChoiceQuestion("表达式(11+3*8)/4%3的值是", map05, "D"))
                .append(new AnswerQuestion("小红马和小黑马生的小马几条腿", "4条腿"))
                .append(new AnswerQuestion("铁棒打头疼还是木棒打头疼", "头最疼"))
                .append(new AnswerQuestion("什么床不能睡觉", "牙床"))
                .append(new AnswerQuestion("为什么好马不吃回头草", "后面的草没了"));
    }

    public String createPaper(String candidate, String number) throws CloneNotSupportedException {
        QuestionBank questionBankClone = (QuestionBank) questionBank.clone();
        questionBankClone.setCandidate(candidate);
        questionBankClone.setNumber(number);
        return questionBankClone.toString();
    }

}
```




### 总结



> 原型模式使用的场景并不是很高。

- 优点

便于通过克隆方式创建复杂对象、也可以避免重复做初始化操作、不需要与类中所属的其他类耦合等

- 缺点

如果对象中包括了循环引用的克隆，以及类中深度使用对象的克隆，都会使此模式变得异常麻烦。
## 建造者模式



> 将多个简单对象通过一步步的组装构建出一个复杂对象的过程。



### 通过代码模拟一次装修

``` xml
itstack-demo-design-3-00
└── src
    └── main
        └── java
            └── org.itstack.demo.design
                ├── ceilling
                │   ├── LevelOneCeiling.java
                │   └── LevelTwoCeiling.java
                ├── coat
                │   ├── DuluxCoat.java
                │   └── LiBangCoat.java
                │   └── LevelTwoCeiling.java
                ├── floor
                │   ├── DerFloor.java
                │   └── ShengXiangFloor.java
                ├── tile
                │   ├── DongPengTile.java
                │   └── MarcoPoloTile.java
                └── Matter.java
```

在模拟工程中提供了装修中所需要的物料；`ceilling(吊顶)`、`coat(涂料)`、`floor(地板)`、`tile(地砖)`，这么四项内容。



- 物料接口

``` java
public interface Matter {

    String scene();      // 场景；地板、地砖、涂料、吊顶

    String brand();      // 品牌

    String model();      // 型号

    BigDecimal price();  // 价格

    String desc();       // 描述

}
```

每个单独的物料都具有的公共属性，保证所有的装修材料都可以按照统一标准进行获取。







- 吊顶

一级顶

``` java
public class LevelOneCeiling implements Matter {

    public String scene() {
        return "吊顶";
    }

    public String brand() {
        return "装修公司自带";
    }

    public String model() {
        return "一级顶";
    }

    public BigDecimal price() {
        return new BigDecimal(260);
    }

    public String desc() {
        return "造型只做低一级，只有一个层次的吊顶，一般离顶120-150mm";
    }

}
```





- 二级顶

``` java
public class LevelTwoCeiling  implements Matter {

    public String scene() {
        return "吊顶";
    }

    public String brand() {
        return "装修公司自带";
    }

    public String model() {
        return "二级顶";
    }

    public BigDecimal price() {
        return new BigDecimal(850);
    }

    public String desc() {
        return "两个层次的吊顶，二级吊顶高度一般就往下吊20cm，要是层高很高，也可增加每级的厚度";
    }
    
}
```





- 涂料(coat)

**多乐士**

```java
public class DuluxCoat  implements Matter {

    public String scene() {
        return "涂料";
    }

    public String brand() {
        return "多乐士(Dulux)";
    }

    public String model() {
        return "第二代";
    }

    public BigDecimal price() {
        return new BigDecimal(719);
    }

    public String desc() {
        return "多乐士是阿克苏诺贝尔旗下的著名建筑装饰油漆品牌，产品畅销于全球100个国家，每年全球有5000万户家庭使用多乐士油漆。";
    }
    
}
```

**立邦**

```java
public class LiBangCoat implements Matter {

    public String scene() {
        return "涂料";
    }

    public String brand() {
        return "立邦";
    }

    public String model() {
        return "默认级别";
    }

    public BigDecimal price() {
        return new BigDecimal(650);
    }

    public String desc() {
        return "立邦始终以开发绿色产品、注重高科技、高品质为目标，以技术力量不断推进科研和开发，满足消费者需求。";
    }

}
```

- 2.4 地板(floor)

**德尔**

```java
public class DerFloor implements Matter {

    public String scene() {
        return "地板";
    }

    public String brand() {
        return "德尔(Der)";
    }

    public String model() {
        return "A+";
    }

    public BigDecimal price() {
        return new BigDecimal(119);
    }

    public String desc() {
        return "DER德尔集团是全球领先的专业木地板制造商，北京2008年奥运会家装和公装地板供应商";
    }
    
}
```

**圣象**

```java
public class ShengXiangFloor implements Matter {

    public String scene() {
        return "地板";
    }

    public String brand() {
        return "圣象";
    }

    public String model() {
        return "一级";
    }

    public BigDecimal price() {
        return new BigDecimal(318);
    }

    public String desc() {
        return "圣象地板是中国地板行业著名品牌。圣象地板拥有中国驰名商标、中国名牌、国家免检、中国环境标志认证等多项荣誉。";
    }

}
```

- 2.5 地砖(tile)

**东鹏**

```java
public class DongPengTile implements Matter {

    public String scene() {
        return "地砖";
    }

    public String brand() {
        return "东鹏瓷砖";
    }

    public String model() {
        return "10001";
    }

    public BigDecimal price() {
        return new BigDecimal(102);
    }

    public String desc() {
        return "东鹏瓷砖以品质铸就品牌，科技推动品牌，口碑传播品牌为宗旨，2014年品牌价值132.35亿元，位列建陶行业榜首。";
    }

}
```

**马可波罗**

```java
public class MarcoPoloTile implements Matter {

    public String scene() {
        return "地砖";
    }

    public String brand() {
        return "马可波罗(MARCO POLO)";
    }

    public String model() {
        return "缺省";
    }

    public BigDecimal price() {
        return new BigDecimal(140);
    }

    public String desc() {
        return "“马可波罗”品牌诞生于1996年，作为国内最早品牌化的建陶品牌，以“文化陶瓷”占领市场，享有“仿古砖至尊”的美誉。";
    }

}
```








### bad

> 使用if-else来实现



``` xml
itstack-demo-design-3-01
└── src
    └── main
        └── java
            └── org.itstack.demo.design
                └── DecorationPackageController.java
```



``` java
public class DecorationPackageController {

    public String getMatterList(BigDecimal area, Integer level) {

        List<Matter> list = new ArrayList<Matter>(); // 装修清单
        BigDecimal price = BigDecimal.ZERO;          // 装修价格

        // 豪华欧式
        if (1 == level) {

            LevelTwoCeiling levelTwoCeiling = new LevelTwoCeiling(); // 吊顶，二级顶
            DuluxCoat duluxCoat = new DuluxCoat();                   // 涂料，多乐士
            ShengXiangFloor shengXiangFloor = new ShengXiangFloor(); // 地板，圣象

            list.add(levelTwoCeiling);
            list.add(duluxCoat);
            list.add(shengXiangFloor);

            price = price.add(area.multiply(new BigDecimal("0.2")).multiply(levelTwoCeiling.price()));
            price = price.add(area.multiply(new BigDecimal("1.4")).multiply(duluxCoat.price()));
            price = price.add(area.multiply(shengXiangFloor.price()));

        }

        // 轻奢田园
        if (2 == level) {

            LevelTwoCeiling levelTwoCeiling = new LevelTwoCeiling(); // 吊顶，二级顶
            LiBangCoat liBangCoat = new LiBangCoat();                // 涂料，立邦
            MarcoPoloTile marcoPoloTile = new MarcoPoloTile();       // 地砖，马可波罗

            list.add(levelTwoCeiling);
            list.add(liBangCoat);
            list.add(marcoPoloTile);

            price = price.add(area.multiply(new BigDecimal("0.2")).multiply(levelTwoCeiling.price()));
            price = price.add(area.multiply(new BigDecimal("1.4")).multiply(liBangCoat.price()));
            price = price.add(area.multiply(marcoPoloTile.price()));

        }

        // 现代简约
        if (3 == level) {

            LevelOneCeiling levelOneCeiling = new LevelOneCeiling();  // 吊顶，二级顶
            LiBangCoat liBangCoat = new LiBangCoat();                 // 涂料，立邦
            DongPengTile dongPengTile = new DongPengTile();           // 地砖，东鹏

            list.add(levelOneCeiling);
            list.add(liBangCoat);
            list.add(dongPengTile);

            price = price.add(area.multiply(new BigDecimal("0.2")).multiply(levelOneCeiling.price()));
            price = price.add(area.multiply(new BigDecimal("1.4")).multiply(liBangCoat.price()));
            price = price.add(area.multiply(dongPengTile.price()));
        }

        StringBuilder detail = new StringBuilder("\r\n-------------------------------------------------------\r\n" +
                "装修清单" + "\r\n" +
                "套餐等级：" + level + "\r\n" +
                "套餐价格：" + price.setScale(2, BigDecimal.ROUND_HALF_UP) + " 元\r\n" +
                "房屋面积：" + area.doubleValue() + " 平米\r\n" +
                "材料清单：\r\n");

        for (Matter matter: list) {
            detail.append(matter.scene()).append("：").append(matter.brand()).append("、").append(matter.model()).append("、平米价格：").append(matter.price()).append(" 元。\n");
        }

        return detail.toString();

    }

}
```


### good





``` xml
itstack-demo-design-3-02
└── src
    ├── main
    │   └── java
    │       └── org.itstack.demo.design
    │           ├── Builder.java    
    │           ├── DecorationPackageMenu.java
    │           └── IMenu.java 
    └── test
         └── java
             └── org.itstack.demo.design.test
                 └── ApiTest.java
```



![1753342260336.png](https://fastly.jsdelivr.net/gh/thecoolboyhan/th_blogs@main/image/2025-07/1753342260336_1753342260357.png)



- 装修包接口

``` java
public interface IMenu {

    IMenu appendCeiling(Matter matter); // 吊顶

    IMenu appendCoat(Matter matter);    // 涂料

    IMenu appendFloor(Matter matter);   // 地板

    IMenu appendTile(Matter matter);    // 地砖

    String getDetail();                 // 明细 

}
```



- 装修包实现

``` java
public class DecorationPackageMenu implements IMenu {

    private List<Matter> list = new ArrayList<Matter>();  // 装修清单
    private BigDecimal price = BigDecimal.ZERO;      // 装修价格

    private BigDecimal area;  // 面积
    private String grade;     // 装修等级；豪华欧式、轻奢田园、现代简约

    private DecorationPackageMenu() {
    }

    public DecorationPackageMenu(Double area, String grade) {
        this.area = new BigDecimal(area);
        this.grade = grade;
    }

    public IMenu appendCeiling(Matter matter) {
        list.add(matter);
        price = price.add(area.multiply(new BigDecimal("0.2")).multiply(matter.price()));
        return this;
    }

    public IMenu appendCoat(Matter matter) {
        list.add(matter);
        price = price.add(area.multiply(new BigDecimal("1.4")).multiply(matter.price()));
        return this;
    }

    public IMenu appendFloor(Matter matter) {
        list.add(matter);
        price = price.add(area.multiply(matter.price()));
        return this;
    }

    public IMenu appendTile(Matter matter) {
        list.add(matter);
        price = price.add(area.multiply(matter.price()));
        return this;
    }

    public String getDetail() {

        StringBuilder detail = new StringBuilder("\r\n-------------------------------------------------------\r\n" +
                "装修清单" + "\r\n" +
                "套餐等级：" + grade + "\r\n" +
                "套餐价格：" + price.setScale(2, BigDecimal.ROUND_HALF_UP) + " 元\r\n" +
                "房屋面积：" + area.doubleValue() + " 平米\r\n" +
                "材料清单：\r\n");

        for (Matter matter: list) {
            detail.append(matter.scene()).append("：").append(matter.brand()).append("、").append(matter.model()).append("、平米价格：").append(matter.price()).append(" 元。\n");
        }

        return detail.toString();
    }

}
```





- 调用方法

``` java
public class Builder {

    public IMenu levelOne(Double area) {
        return new DecorationPackageMenu(area, "豪华欧式")
                .appendCeiling(new LevelTwoCeiling())    // 吊顶，二级顶
                .appendCoat(new DuluxCoat())             // 涂料，多乐士
                .appendFloor(new ShengXiangFloor());     // 地板，圣象
    }

    public IMenu levelTwo(Double area){
        return new DecorationPackageMenu(area, "轻奢田园")
                .appendCeiling(new LevelTwoCeiling())   // 吊顶，二级顶
                .appendCoat(new LiBangCoat())           // 涂料，立邦
                .appendTile(new MarcoPoloTile());       // 地砖，马可波罗
    }

    public IMenu levelThree(Double area){
        return new DecorationPackageMenu(area, "现代简约")
                .appendCeiling(new LevelOneCeiling())   // 吊顶，二级顶
                .appendCoat(new LiBangCoat())           // 涂料，立邦
                .appendTile(new DongPengTile());        // 地砖，东鹏
    }

}
```




### 总结



- 什么时候适合建造者模式？

一些基本物料不会变，而其组合经常变化的时候。



- 此设计模式满足了单一职责原则以及可复用的技术、建造者独立、易扩展、便于控制细节风险。但同时当出现特别多的物料以及很多的组合后，类的不断扩展也会造成难以维护的问题。但这种设计结构模型可以把重复的内容抽象到数据库中，按照需要配置。这样就可以减少代码中大量的重复。



> 下面是小博哥的原话，太金典了



- 设计模式能带给你的是一些思想，但在平时的开发中怎么样清晰的提炼出符合此思路的建造模块，是比较难的。需要经过一些锻炼和不断承接更多的项目，从而获得这部分经验。有的时候你的代码写的好，往往是倒逼的，复杂的业务频繁的变化，不断的挑战！
## 单例模式
> 创建型设计模式
>
> 避免一个全局使用的类频繁的创建和消费，从而提升整体代码的性能。





七种不同的单例模式


### 0、静态类（非单例模式）

``` java
public class Singleton_00 {

    public static Map<String,String> cache = new ConcurrentHashMap<String, String>();
    
}
```

不需要维持状态，仅让全局访问，静态类的方式更加简单。

但如果需要被继承以及需要维持状态时，就需要使用到单例模式


### 懒汉模式（线程不安全）



``` java
public class Singleton_01 {

    private static Singleton_01 instance;

    private Singleton_01() {
    }

    public static Singleton_01 getInstance(){
        if (null != instance) return instance;
        instance = new Singleton_01();
        return instance;
    }

}
```



> 使构造函数为private，不允许直接创建对象，只能通过getInstance来创建

懒加载，只有在需要使用时才会创建对象。



- 为什么线程不安全？

当多个线程同时调用getInstance时，可能得到多个不同的对象。


### 懒汉模式（线程安全）



``` java
public class Singleton_02 {

    private static Singleton_02 instance;

    private Singleton_02() {
    }

    public static synchronized Singleton_02 getInstance(){
        if (null != instance) return instance;
        instance = new Singleton_02();
        return instance;
    }

}
```

利用synchronized保证同时只能有一个线程来创建对象



- 存在问题

所有线程在获取此单例类时，都会被synchronized锁定，导致资源浪费。


### 饿汉模式（线程安全）

``` java
public class Singleton_03 {

    private static Singleton_03 instance = new Singleton_03();

    private Singleton_03() {
    }

    public static Singleton_03 getInstance() {
        return instance;
    }

}
```



类似于最开始的静态类，当程序启动的时候，就直接运行加载，无论是否使用，直接创建对象。



- 为什么线程安全？

JVM在类加载的过程中
**加载**-->**验证**-->**准备**-->**解析**--><font color='red'>**初始化**</font>-->**使用**-->**卸载**

在初始化阶段就直接执行静态代码块，直接创建对象。后续其他类使用时就是已经创建好的对象。



- 存在的问题

程序启动，所有的单例类全部被创建，如果单例类特别多，会导致大量的资源占用。




### 类的内部类（线程安全）

``` java
public class Singleton_04 {

    private static class SingletonHolder {
        private static Singleton_04 instance = new Singleton_04();
    }

    private Singleton_04() {
    }

    public static Singleton_04 getInstance() {
        return SingletonHolder.instance;
    }

}
```



使用静态内部类，即保证了线程安全，也保证了懒加载，同时也没有锁来消耗性能。



- 如何被创建

初始时，并没有创建instance此内部类。

当有线程调用getInstance方法时，会返回SingletonHolder.instance对象。

有栈（线程）需要加载SingletonHolder.instance对象，JVM第一次把指向class的符号引用改成正常加载到JVM单例池中的直接引用。（此时相当于触发了类的饿汉式单例）



- 为什么线程安全？

> 《深入理解java虚拟机》中的原话：

虚拟机会保证一个类的()方法在多线程环境中被正确地加锁、同步，如果多个线程同时去初始化一个类，那么只会有一个线程去执行这个类的()方法，其他线程都需要阻塞等待，直到活动线程执行()方法完毕。如果在一个类的()方法中有耗时很长的操作，就可能造成多个进程阻塞(需要注意的是，其他线程虽然会被阻塞，但如果执行()方法后，其他线程唤醒之后不会再次进入()方法。同一个加载器下，一个类型只会初始化一次。)，在实际应用中，这种阻塞往往是很隐蔽的。





- 存在的问题

普通使用是非常推荐的。但是由于使用了静态内部类，无法从外部直接传递参数进去




### 双重锁校验（线程安全）DCL

``` java
public class Singleton_05 {

    private static volatile Singleton_05 instance;

    private Singleton_05() {
    }

    public static Singleton_05 getInstance(){
       if(null != instance) return instance;
       synchronized (Singleton_05.class){
           if (null == instance){
               instance = new Singleton_05();
           }
       }
       return instance;
    }

}
```



满足懒加载，会在初始化阶段上锁，后续操作无锁。


### CAS单例（线程安全）







``` java
public class Singleton_06 {

    private static final AtomicReference<Singleton_06> INSTANCE = new AtomicReference<Singleton_06>();

    private Singleton_06() {
    }

    public static final Singleton_06 getInstance() {
        for (; ; ) {
            Singleton_06 instance = INSTANCE.get();
            if (null != instance) return instance;
            INSTANCE.compareAndSet(null, new Singleton_06());
            return INSTANCE.get();
        }
    }

    public static void main(String[] args) {
        System.out.println(Singleton_06.getInstance()); // org.itstack.demo.design.Singleton_06@2b193f2d
        System.out.println(Singleton_06.getInstance()); // org.itstack.demo.design.Singleton_06@2b193f2d
    }

}
```



通过里用原子类中的CAS操作，实现CAS创建对象



- 存在的问题

CAS是一个忙等操作，会一直循环尝试，直到成功。但如果对象创建一直失败，就会无限重试。




### Effective Java作者推荐的枚举单例(线程安全)

``` java
public enum Singleton_07 {

    INSTANCE;
    public void test(){
        System.out.println("hi~");
    }

}
```



利用枚举类创建的单例对象，即使用过反射业务创建相同的对象。

*偿地提供了串行化机制，绝对防止对此实例化，即使是在面对复杂的串行化或者反射攻击的时候。*



## 适配器模式
> 结构型模式
>
> 把原本不兼容的接口，通过适配器修改做到统一。使得用户方便使用。

![场景模拟；接收多类型MQ消息](https://camo.githubusercontent.com/b83fc564cdb39695fd7527f0642bc8124749b9c8c32b1a093b41d4c0f88e775e/68747470733a2f2f627567737461636b2e636e2f6173736574732f696d616765732f323032302f6974737461636b2d64656d6f2d64657369676e2d362d30332e706e67)

多种差异化类型的接口做统一输出。

![适配器模型结构](https://camo.githubusercontent.com/8f0b35f2d77e5a64ae144303b79b4b519c0bfee796675b836bb558f2750463f3/68747470733a2f2f627567737461636b2e636e2f6173736574732f696d616765732f323032302f6974737461636b2d64656d6f2d64657369676e2d362d30342e706e67)

使用适配器模式就可以让代码，干净整洁易于维护、减少大量的重复判断，让代码更加易于维护和拓展。

> 统一适配器接口

``` java
public interface OrderAdapterService {

    boolean isFirst(String uId);

}
```



> 不同的两种实现

**内部商品接口**

```java
public class InsideOrderService implements OrderAdapterService {

    private OrderService orderService = new OrderService();

    public boolean isFirst(String uId) {
        return orderService.queryUserOrderCount(uId) <= 1;
    }

}
```

**第三方商品接口**

```
public class POPOrderAdapterServiceImpl implements OrderAdapterService {

    private POPOrderService popOrderService = new POPOrderService();

    public boolean isFirst(String uId) {
        return popOrderService.isFirstOrder(uId);
    }

}
```



在这两个接口中都实现了各自的判断方式，尤其像是提供订单数量的接口，需要自己判断当前接到mq时订单数量是否`<= 1`，以此判断是否为首单。

> 测试类

``` java
@Test
public void test_itfAdapter() {
    OrderAdapterService popOrderAdapterService = new POPOrderAdapterServiceImpl();
    System.out.println("判断首单，接口适配(POP)：" + popOrderAdapterService.isFirst("100001"));   

    OrderAdapterService insideOrderService = new InsideOrderService();
    System.out.println("判断首单，接口适配(自营)：" + insideOrderService.isFirst("100001"));
}
```

## 桥接模式

> 通过将抽象部分和实现部分分离，把多种可以匹配的使用进行组合。
>
> 在A类中含有B类的接口，通过构造函数传递B类的实现。

![场景模拟：多种支付和模式](https://camo.githubusercontent.com/1ce215061a2a6f355e046365659815e1126a172c3dfce827edee3ee3b9055945/68747470733a2f2f627567737461636b2e636e2f6173736574732f696d616765732f323032302f6974737461636b2d64656d6f2d64657369676e2d372d30322e706e67)


### 实现支付和支付模式的模式(反例)

``` java
public class PayController {

    private Logger logger = LoggerFactory.getLogger(PayController.class);

    public boolean doPay(String uId, String tradeId, BigDecimal amount, int channelType, int modeType) {
        // 微信支付
        if (1 == channelType) {
            logger.info("模拟微信渠道支付划账开始。uId：{} tradeId：{} amount：{}", uId, tradeId, amount);
            if (1 == modeType) {
                logger.info("密码支付，风控校验环境安全");
            } else if (2 == modeType) {
                logger.info("人脸支付，风控校验脸部识别");
            } else if (3 == modeType) {
                logger.info("指纹支付，风控校验指纹信息");
            }
        }
        // 支付宝支付
        else if (2 == channelType) {
            logger.info("模拟支付宝渠道支付划账开始。uId：{} tradeId：{} amount：{}", uId, tradeId, amount);
            if (1 == modeType) {
                logger.info("密码支付，风控校验环境安全");
            } else if (2 == modeType) {
                logger.info("人脸支付，风控校验脸部识别");
            } else if (3 == modeType) {
                logger.info("指纹支付，风控校验指纹信息");
            }
        }
        return true;
    }

}
```


### 使用桥接模式重构代码

> 把支付方式和支付模式进行分离，通过抽象类依赖实现类的方式进行桥接

![桥接模式模型结构](https://camo.githubusercontent.com/d38f1c25228b7adf4c647869f782d43c1758b5a6141457f3bdd545d816dba26f/68747470733a2f2f627567737461636b2e636e2f6173736574732f696d616765732f323032302f6974737461636b2d64656d6f2d64657369676e2d372d30332e706e67)

- 支付类型桥接抽象类

``` java
public abstract class Pay {

    protected Logger logger = LoggerFactory.getLogger(Pay.class);

    protected IPayMode payMode;

    public Pay(IPayMode payMode) {
        this.payMode = payMode;
    }

    public abstract String transfer(String uId, String tradeId, BigDecimal amount);

}
```



- 微信支付

``` java
public class WxPay extends Pay {

    public WxPay(IPayMode payMode) {
        super(payMode);
    }

    public String transfer(String uId, String tradeId, BigDecimal amount) {
        logger.info("模拟微信渠道支付划账开始。uId：{} tradeId：{} amount：{}", uId, tradeId, amount);
        boolean security = payMode.security(uId);
        logger.info("模拟微信渠道支付风控校验。uId：{} tradeId：{} security：{}", uId, tradeId, security);
        if (!security) {
            logger.info("模拟微信渠道支付划账拦截。uId：{} tradeId：{} amount：{}", uId, tradeId, amount);
            return "0001";
        }
        logger.info("模拟微信渠道支付划账成功。uId：{} tradeId：{} amount：{}", uId, tradeId, amount);
        return "0000";
    }

}
```

- 支付宝支付

``` java
public class ZfbPay extends Pay {

    public ZfbPay(IPayMode payMode) {
        super(payMode);
    }

    public String transfer(String uId, String tradeId, BigDecimal amount) {
        logger.info("模拟支付宝渠道支付划账开始。uId：{} tradeId：{} amount：{}", uId, tradeId, amount);
        boolean security = payMode.security(uId);
        logger.info("模拟支付宝渠道支付风控校验。uId：{} tradeId：{} security：{}", uId, tradeId, security);
        if (!security) {
            logger.info("模拟支付宝渠道支付划账拦截。uId：{} tradeId：{} amount：{}", uId, tradeId, amount);
            return "0001";
        }
        logger.info("模拟支付宝渠道支付划账成功。uId：{} tradeId：{} amount：{}", uId, tradeId, amount);
        return "0000";
    }

}
```

- 支付方式接口

``` java
public interface IPayMode {

    boolean security(String uId);

}
```

``` java
public class PayFaceMode implements IPayMode{

    protected Logger logger = LoggerFactory.getLogger(PayCypher.class);

    public boolean security(String uId) {
        logger.info("人脸支付，风控校验脸部识别");
        return true;
    }

}
```

指举例一个，其他大差不差



> 桥接模式满足单一职责和开闭原则，让每一部分的内容都很清晰易于维护和拓展。

## 组合模式

> 通过一堆的链接组织出一颗结构树，把相似对象组合成一组，可以被调用的结构树对象的设计思路。
>
> **经常在决策树中使用**

![场景模式；营销决策树](https://camo.githubusercontent.com/ffa8e4042a41740aa4c35fc65dbb90834b441a4856598998fc4c8787b117ac06/68747470733a2f2f627567737461636b2e636e2f6173736574732f696d616765732f323032302f6974737461636b2d64656d6f2d64657369676e2d382d30322e706e67)
### 组合模式反例

``` java
public class EngineController {

    private Logger logger = LoggerFactory.getLogger(EngineController.class);

    public String process(final String userId, final String userSex, final int userAge) {

        logger.info("ifelse实现方式判断用户结果。userId：{} userSex：{} userAge：{}", userId, userSex, userAge);

        if ("man".equals(userSex)) {
            if (userAge < 25) {
                return "果实A";
            }

            if (userAge >= 25) {
                return "果实B";
            }
        }

        if ("woman".equals(userSex)) {
            if (userAge < 25) {
                return "果实C";
            }

            if (userAge >= 25) {
                return "果实D";
            }
        }

        return null;

    }

}
```


### 利用组合模式重构代码

![组合模式模型结构](https://camo.githubusercontent.com/0b06bedfc851e25558bd6ae09aa7f20182487d26b43a188daf4a4b1cbe5646fc/68747470733a2f2f627567737461636b2e636e2f6173736574732f696d616765732f323032302f6974737461636b2d64656d6f2d64657369676e2d382d30332e706e67)

- 树节点逻辑过滤器接口

```java
public interface LogicFilter {

    /**
     * 逻辑决策器
     *
     * @param matterValue          决策值
     * @param treeNodeLineInfoList 决策节点
     * @return 下一个节点Id
     */
    Long filter(String matterValue, List<TreeNodeLink> treeNodeLineInfoList);

    /**
     * 获取决策值
     *
     * @param decisionMatter 决策物料
     * @return 决策值
     */
    String matterValue(Long treeId, String userId, Map<String, String> decisionMatter);

}
```

- 决策抽象类提供基础服务

``` java
public abstract class BaseLogic implements LogicFilter {

  //返回决策节点的下一个决策节点
    @Override
    public Long filter(String matterValue, List<TreeNodeLink> treeNodeLinkList) {
        for (TreeNodeLink nodeLine : treeNodeLinkList) {
            if (decisionLogic(matterValue, nodeLine)) return nodeLine.getNodeIdTo();
        }
        return 0L;
    }

  //获取决策值
    @Override
    public abstract String matterValue(Long treeId, String userId, Map<String, String> decisionMatter);

    private boolean decisionLogic(String matterValue, TreeNodeLink nodeLink) {
        switch (nodeLink.getRuleLimitType()) {
            case 1:
                return matterValue.equals(nodeLink.getRuleLimitValue());
            case 2:
                return Double.parseDouble(matterValue) > Double.parseDouble(nodeLink.getRuleLimitValue());
            case 3:
                return Double.parseDouble(matterValue) < Double.parseDouble(nodeLink.getRuleLimitValue());
            case 4:
                return Double.parseDouble(matterValue) <= Double.parseDouble(nodeLink.getRuleLimitValue());
            case 5:
                return Double.parseDouble(matterValue) >= Double.parseDouble(nodeLink.getRuleLimitValue());
            default:
                return false;
        }
    }

}
```

- 决策树的节点

> 需要决策的值或属性

**年龄节点**

``` java
public class UserAgeFilter extends BaseLogic {

    @Override
    public String matterValue(Long treeId, String userId, Map<String, String> decisionMatter) {
        return decisionMatter.get("age");
    }

}
```

**性别节点**

``` java
public class UserGenderFilter extends BaseLogic {

    @Override
    public String matterValue(Long treeId, String userId, Map<String, String> decisionMatter) {
        return decisionMatter.get("gender");
    }

}
```



- 决策引擎接口

``` java
public interface IEngine {

    EngineResult process(final Long treeId, final String userId, TreeRich treeRich, final Map<String, String> decisionMatter);

}
```



- 决策节点配置或管理

> 管理有哪些决策节点

``` java
public class EngineConfig {

    static Map<String, LogicFilter> logicFilterMap;

    static {
        logicFilterMap = new ConcurrentHashMap<>();
        logicFilterMap.put("userAge", new UserAgeFilter());
        logicFilterMap.put("userGender", new UserGenderFilter());
    }

    public Map<String, LogicFilter> getLogicFilterMap() {
        return logicFilterMap;
    }

    public void setLogicFilterMap(Map<String, LogicFilter> logicFilterMap) {
        this.logicFilterMap = logicFilterMap;
    }

}
```



- 决策引擎的功能抽象

``` java
public abstract class EngineBase extends EngineConfig implements IEngine {

    private Logger logger = LoggerFactory.getLogger(EngineBase.class);

    @Override
    public abstract EngineResult process(Long treeId, String userId, TreeRich treeRich, Map<String, String> decisionMatter);

    protected TreeNode engineDecisionMaker(TreeRich treeRich, Long treeId, String userId, Map<String, String> decisionMatter) {
        TreeRoot treeRoot = treeRich.getTreeRoot();
        Map<Long, TreeNode> treeNodeMap = treeRich.getTreeNodeMap();
        // 规则树根ID
        Long rootNodeId = treeRoot.getTreeRootNodeId();
        TreeNode treeNodeInfo = treeNodeMap.get(rootNodeId);
        //节点类型[NodeType]；1子叶、2果实
        while (treeNodeInfo.getNodeType().equals(1)) {
            String ruleKey = treeNodeInfo.getRuleKey();
            LogicFilter logicFilter = logicFilterMap.get(ruleKey);
            String matterValue = logicFilter.matterValue(treeId, userId, decisionMatter);
            Long nextNode = logicFilter.filter(matterValue, treeNodeInfo.getTreeNodeLinkList());
            treeNodeInfo = treeNodeMap.get(nextNode);
            logger.info("决策树引擎=>{} userId：{} treeId：{} treeNode：{} ruleKey：{} matterValue：{}", treeRoot.getTreeName(), userId, treeId, treeNodeInfo.getTreeNodeId(), ruleKey, matterValue);
        }
        return treeNodeInfo;
    }

}
```

- 决策引擎的实现

``` java
public class TreeEngineHandle extends EngineBase {

    @Override
    public EngineResult process(Long treeId, String userId, TreeRich treeRich, Map<String, String> decisionMatter) {
        // 决策流程
        TreeNode treeNode = engineDecisionMaker(treeRich, treeId, userId, decisionMatter);
        // 决策结果
        return new EngineResult(userId, treeId, treeNode.getTreeNodeId(), treeNode.getNodeValue());
    }

}
```



- 决策树建树

``` java
@Before
public void init() {
    // 节点：1
    TreeNode treeNode_01 = new TreeNode();
    treeNode_01.setTreeId(10001L);
    treeNode_01.setTreeNodeId(1L);
    treeNode_01.setNodeType(1);
    treeNode_01.setNodeValue(null);
    treeNode_01.setRuleKey("userGender");
    treeNode_01.setRuleDesc("用户性别[男/女]");
    // 链接：1->11
    TreeNodeLink treeNodeLink_11 = new TreeNodeLink();
    treeNodeLink_11.setNodeIdFrom(1L);
    treeNodeLink_11.setNodeIdTo(11L);
    treeNodeLink_11.setRuleLimitType(1);
    treeNodeLink_11.setRuleLimitValue("man");
    // 链接：1->12
    TreeNodeLink treeNodeLink_12 = new TreeNodeLink();
    treeNodeLink_12.setNodeIdTo(1L);
    treeNodeLink_12.setNodeIdTo(12L);
    treeNodeLink_12.setRuleLimitType(1);
    treeNodeLink_12.setRuleLimitValue("woman");
    List<TreeNodeLink> treeNodeLinkList_1 = new ArrayList<>();
    treeNodeLinkList_1.add(treeNodeLink_11);
    treeNodeLinkList_1.add(treeNodeLink_12);
    treeNode_01.setTreeNodeLinkList(treeNodeLinkList_1);
    // 节点：11
    TreeNode treeNode_11 = new TreeNode();
    treeNode_11.setTreeId(10001L);
    treeNode_11.setTreeNodeId(11L);
    treeNode_11.setNodeType(1);
    treeNode_11.setNodeValue(null);
    treeNode_11.setRuleKey("userAge");
    treeNode_11.setRuleDesc("用户年龄");
    // 链接：11->111
    TreeNodeLink treeNodeLink_111 = new TreeNodeLink();
    treeNodeLink_111.setNodeIdFrom(11L);
    treeNodeLink_111.setNodeIdTo(111L);
    treeNodeLink_111.setRuleLimitType(3);
    treeNodeLink_111.setRuleLimitValue("25");
    // 链接：11->112
    TreeNodeLink treeNodeLink_112 = new TreeNodeLink();
    treeNodeLink_112.setNodeIdFrom(11L);
    treeNodeLink_112.setNodeIdTo(112L);
    treeNodeLink_112.setRuleLimitType(5);
    treeNodeLink_112.setRuleLimitValue("25");
    List<TreeNodeLink> treeNodeLinkList_11 = new ArrayList<>();
    treeNodeLinkList_11.add(treeNodeLink_111);
    treeNodeLinkList_11.add(treeNodeLink_112);
    treeNode_11.setTreeNodeLinkList(treeNodeLinkList_11);
    // 节点：12
    TreeNode treeNode_12 = new TreeNode();
    treeNode_12.setTreeId(10001L);
    treeNode_12.setTreeNodeId(12L);
    treeNode_12.setNodeType(1);
    treeNode_12.setNodeValue(null);
    treeNode_12.setRuleKey("userAge");
    treeNode_12.setRuleDesc("用户年龄");
    // 链接：12->121
    TreeNodeLink treeNodeLink_121 = new TreeNodeLink();
    treeNodeLink_121.setNodeIdFrom(12L);
    treeNodeLink_121.setNodeIdTo(121L);
    treeNodeLink_121.setRuleLimitType(3);
    treeNodeLink_121.setRuleLimitValue("25");
    // 链接：12->122
    TreeNodeLink treeNodeLink_122 = new TreeNodeLink();
    treeNodeLink_122.setNodeIdFrom(12L);
    treeNodeLink_122.setNodeIdTo(122L);
    treeNodeLink_122.setRuleLimitType(5);
    treeNodeLink_122.setRuleLimitValue("25");
    List<TreeNodeLink> treeNodeLinkList_12 = new ArrayList<>();
    treeNodeLinkList_12.add(treeNodeLink_121);
    treeNodeLinkList_12.add(treeNodeLink_122);
    treeNode_12.setTreeNodeLinkList(treeNodeLinkList_12);
    // 节点：111
    TreeNode treeNode_111 = new TreeNode();
    treeNode_111.setTreeId(10001L);
    treeNode_111.setTreeNodeId(111L);
    treeNode_111.setNodeType(2);
    treeNode_111.setNodeValue("果实A");
    // 节点：112
    TreeNode treeNode_112 = new TreeNode();
    treeNode_112.setTreeId(10001L);
    treeNode_112.setTreeNodeId(112L);
    treeNode_112.setNodeType(2);
    treeNode_112.setNodeValue("果实B");
    // 节点：121
    TreeNode treeNode_121 = new TreeNode();
    treeNode_121.setTreeId(10001L);
    treeNode_121.setTreeNodeId(121L);
    treeNode_121.setNodeType(2);
    treeNode_121.setNodeValue("果实C");
    // 节点：122
    TreeNode treeNode_122 = new TreeNode();
    treeNode_122.setTreeId(10001L);
    treeNode_122.setTreeNodeId(122L);
    treeNode_122.setNodeType(2);
    treeNode_122.setNodeValue("果实D");
    // 树根
    TreeRoot treeRoot = new TreeRoot();
    treeRoot.setTreeId(10001L);
    treeRoot.setTreeRootNodeId(1L);
    treeRoot.setTreeName("规则决策树");
    Map<Long, TreeNode> treeNodeMap = new HashMap<>();
    treeNodeMap.put(1L, treeNode_01);
    treeNodeMap.put(11L, treeNode_11);
    treeNodeMap.put(12L, treeNode_12);
    treeNodeMap.put(111L, treeNode_111);
    treeNodeMap.put(112L, treeNode_112);
    treeNodeMap.put(121L, treeNode_121);
    treeNodeMap.put(122L, treeNode_122);
    treeRich = new TreeRich(treeRoot, treeNodeMap);
}
```




