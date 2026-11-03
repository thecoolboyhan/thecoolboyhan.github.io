---
title: 读《设计机器学习应用系统》有感-神经网络与机器学习
description: AI Coding 时代，程序员等工程人员应该何去何从，第二部分，机器学习的前置知识。如何表示数据，如何计算和构建树等。如何建模和如何训练。
本部分通过如何建模，训练模型，到模型的分类，进化历程来详细讲解。说实话，有些部份晦涩难懂，阅读起来很吃力。
image: 1.png
date: 2026-11-03
categories:
  - 精选
  - AI
  - 数学
  - 统计
tags:
  - AI
  - 数学

---

## 神经网络结构

**如何建模**

### 神经网络基础原理

#### 生物神经元结构与启发

![神经元结构示意图](https://ai.icyfenix.cn/assets/neuron-structure-Bl2p45q2.png)

> 生物神经元结构

- Hebb 学习规则

1. **无监督学习**：Hebb 规则不需要外部标签指导，只需根据神经元自身的活动调整连接。这是无监督学习思想的源头。
2. **联想记忆**：Hebb 规则天然适合构建联想记忆网络。当两个概念（如"苹果"和"红色"）反复同时出现时，网络中对应的神经元连接增强，形成联想。之后看到苹果，自然会联想到红色。
3. **竞争学习**：<span class="text-blue">Hebb 规则的延伸，引入竞争机制，最强的神经元获得权重更新，弱者被抑制。</span>这发展出了自组织映射（SOM）等方法。

### 线性感知机

能够自动调整权重，从而实现模式识别和分类任务。

- **感知机模型**：<span class="text-gray">一个单层神经网络，由输入层和输出层组成，没有隐藏层。</span>
1. 线性组合：计算输入的加权总和，加上偏置。
2. 激活函数：通过阈值函数（简单的正负号函数）将线性输出转换为二值输出

![感知机结构](https://ai.icyfenix.cn/assets/perceptron-structure-0JjdhmdM.png)

![线性可分与 XOR 问题](https://ai.icyfenix.cn/assets/linear-separability-CFL3uBki.png)

### 多层感知机（MLP）

> 多层感知机在输入和输出层之间增加了隐藏层，隐藏层对输入施加了非线性变换，将原始空间映射到新的空间。

![多层感知机结构示意图](https://ai.icyfenix.cn/assets/mlp-structure-CUEzM44g.png)

![XOR问题特征空间变换](https://ai.icyfenix.cn/assets/mlp-xor-space-transformation-DgF3eACu.png)

重新组织数据的空间分布，原本在空间中交错的XOR数据，变成了在（h1，h2）空间后变的有序，正类聚在一起，负类被分离到两侧，可以轻松的完成线性分类。

- 万能逼近定理

![1789961464372.png](https://fastly.jsdelivr.net/gh/thecoolboyhan/th_blogs@main/image/2026-09/1789961464372_1789961464383.png)

<span class="text-blue">只要隐藏层神经元足够多，单隐藏层 MLP 可以逼近任意连续函数，误差可以任意小。</span>

- 多层感知机和单层感知机的对比

![代码运行结果](https://ai.icyfenix.cn/assets/moon_dataset_mlp-DOmPKDBH.png)

1. 左图是感知机决策边界，绿色直线代表感知机学到的决策边界，是一条僵硬的直线（由于随机数据，不一定每次都会在有限的坐标区域中看到），试图切分两个交叠的月牙。<span class="text-red">**无论这条直线如何调整，都无法分隔蓝色和红色数据点，大量样本落在错误的一侧。这是感知机线性约束的局限。**</span>

2. 中图是 MLP 的决策边界，绿色的曲线边界蜿蜒而行，优雅地包裹住蓝色月牙，同时避开红色月牙。这条弯曲的边界正是隐藏层非线性变换的结果，MLP 将原始空间"扭曲"，使得弯曲边界在原空间中呈现为优雅的弧线。数据点被正确分类，准确率显著提升。

3. 右图是训练过程的损失函数变化情况，交叉熵损失随迭代次数稳步下降，展示了 MLP 学习过程的收敛特性。初期损失快速下降，网络迅速掌握数据的主要规律，后期损失平稳收敛，表明网络已接近最优解。

### 前向传播

> <span class="text-gray">神经网络中信号从输入层经各层神经元逐层传递至输出层的过程。</span>

- **信号流动过程**："**输入 → 加权求和 → 激活变换**"
![1789962131456.png](https://fastly.jsdelivr.net/gh/thecoolboyhan/th_blogs@main/image/2026-09/1789962131456_1789962131474.png)

信号流动是一个接力传递的过程，输入信号进入第一层，经过线性组合和激活变换后，输出作为第二层的输入，以此类推，制造输出最终预测。网络每层都在加工上一层传递来的信号。

数与变量表达的计算过程表述为矩阵乘法和非线性变换的组合，<span class="text-green">**既便于推导反向传播公式，也便于利用 GPU 等硬件的矩阵运算优化能力**</span>，现代深度学习框架（TensorFlow、PyTorch）的底层实现都是基于矩阵运算的。

- 计算图

> 深度学习架构如何管理复杂的计算流程

表示计算过程的图形化方法，节点表示运算（加减乘除），边表示数据流动，将复杂的计算过程分解为基本运算的组合。

![1791445562176.png](https://fastly.jsdelivr.net/gh/thecoolboyhan/th_blogs@main/image/2026-10/1791445562176_1791445562190.png)

![1791445605450.png](https://fastly.jsdelivr.net/gh/thecoolboyhan/th_blogs@main/image/2026-10/1791445605450_1791445605466.png)

> 计算图让计算过程变得可视且透明。调试神经网络时可以直接顺着图的拓扑结构定位计算错误或理解中间结果。它为自动微分提供了数据结构层面的支撑。

- 批量计算与效率优化

批量处理最直接的价值在于计算效率。现代 GPU 拥有数千到上万个计算核心，这些核心的设计初衷就是高效执行矩阵运算。



|          批量大小范围           | 特点                                                   | 适用场景                             |
| :-----------------------------: | :----------------------------------------------------- | :----------------------------------- |
|    小批量（B=16*B*=16-6464）    | 梯度噪声大，训练波动，但有利于跳出局部最优；内存占用低 | 内存受限场景、研究实验、追求泛化性能 |
| 中等批量（B=128*B*=128-512512） | 平衡效率和稳定性，梯度噪声适中                         | 常用选择，多数训练场景               |
|    大批量（B=1024*B*=1024+）    | 计算效率高，梯度稳定，但可能陷入局部最优；内存占用高   | 大规模训练、GPU/TPU 高性能硬件       |

> 并不是在内存允许的情况下，批量越大越好。小批量梯度噪音大并不全是坏事，噪音相当于在梯度上添加了随机干扰，这种干扰可以帮助跳出局部最优。



### 反向传播

> 如何确定神经网络的参数（权重和偏置），深度学习领域最重要的算法之一。

当网络输出错误时，如何确定数百甚至数千个参数中哪些应该调整，以及调整多少。反向传播通过计算损失函数对各层参数的梯度，将输出端的误差信号精确地反向传递到每一层，每一个参数，告诉网络谁的贡献大，谁该调整多少。



#### 反向传播的数学基础

<font color='red'>神经网络实际上是一个层层嵌套的复合函数，数据从输入层开始，依次经过每一层的线性变换和激活函数，最终到达输出层。</font>如果我们想调整某个参数来降低预测误差，计算这个参数应该调整多少，实际上就是要从这个复合函数的输出值，反推他的参数变化。



接下来，把单层网络的情况扩展到多层网络，观察损失对输入 x**x** 变化的导数，以一个三层网络为例，信息前向传递路径如下：

<svg id="mermaid-1792746204259" width="100%" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" class="flowchart" style="max-width: 1226px; display: inline-block; margin: 0px auto; width: 919.5px; height: 77.6953px;" viewBox="0 6.5 1226 103.59375" role="graphics-document document" aria-roledescription="flowchart-v2"><g><marker id="mermaid-1792746204259_flowchart-v2-pointEnd" class="marker flowchart-v2" viewBox="0 0 10 10" refX="5" refY="5" markerUnits="userSpaceOnUse" markerWidth="8" markerHeight="8" orient="auto"><path d="M 0 0 L 10 5 L 0 10 z" class="arrowMarkerPath" style="stroke-width: 1; stroke-dasharray: 1, 0;"></path></marker><marker id="mermaid-1792746204259_flowchart-v2-pointStart" class="marker flowchart-v2" viewBox="0 0 10 10" refX="4.5" refY="5" markerUnits="userSpaceOnUse" markerWidth="8" markerHeight="8" orient="auto"><path d="M 0 5 L 10 10 L 10 0 z" class="arrowMarkerPath" style="stroke-width: 1; stroke-dasharray: 1, 0;"></path></marker><marker id="mermaid-1792746204259_flowchart-v2-pointEnd-margin" class="marker flowchart-v2" viewBox="0 0 11.5 14" refX="11.5" refY="7" markerUnits="userSpaceOnUse" markerWidth="10.5" markerHeight="14" orient="auto"><path d="M 0 0 L 11.5 7 L 0 14 z" class="arrowMarkerPath" style="stroke-width: 0; stroke-dasharray: 1, 0;"></path></marker><marker id="mermaid-1792746204259_flowchart-v2-pointStart-margin" class="marker flowchart-v2" viewBox="0 0 11.5 14" refX="1" refY="7" markerUnits="userSpaceOnUse" markerWidth="11.5" markerHeight="14" orient="auto"><polygon points="0,7 11.5,14 11.5,0" class="arrowMarkerPath" style="stroke-width: 0; stroke-dasharray: 1, 0;"></polygon></marker><marker id="mermaid-1792746204259_flowchart-v2-circleEnd" class="marker flowchart-v2" viewBox="0 0 10 10" refX="11" refY="5" markerUnits="userSpaceOnUse" markerWidth="11" markerHeight="11" orient="auto"><circle cx="5" cy="5" r="5" class="arrowMarkerPath" style="stroke-width: 1; stroke-dasharray: 1, 0;"></circle></marker><marker id="mermaid-1792746204259_flowchart-v2-circleStart" class="marker flowchart-v2" viewBox="0 0 10 10" refX="-1" refY="5" markerUnits="userSpaceOnUse" markerWidth="11" markerHeight="11" orient="auto"><circle cx="5" cy="5" r="5" class="arrowMarkerPath" style="stroke-width: 1; stroke-dasharray: 1, 0;"></circle></marker><marker id="mermaid-1792746204259_flowchart-v2-circleEnd-margin" class="marker flowchart-v2" viewBox="0 0 10 10" refY="5" refX="12.25" markerUnits="userSpaceOnUse" markerWidth="14" markerHeight="14" orient="auto"><circle cx="5" cy="5" r="5" class="arrowMarkerPath" style="stroke-width: 0; stroke-dasharray: 1, 0;"></circle></marker><marker id="mermaid-1792746204259_flowchart-v2-circleStart-margin" class="marker flowchart-v2" viewBox="0 0 10 10" refX="-2" refY="5" markerUnits="userSpaceOnUse" markerWidth="14" markerHeight="14" orient="auto"><circle cx="5" cy="5" r="5" class="arrowMarkerPath" style="stroke-width: 0; stroke-dasharray: 1, 0;"></circle></marker><marker id="mermaid-1792746204259_flowchart-v2-crossEnd" class="marker cross flowchart-v2" viewBox="0 0 11 11" refX="12" refY="5.2" markerUnits="userSpaceOnUse" markerWidth="11" markerHeight="11" orient="auto"><path d="M 1,1 l 9,9 M 10,1 l -9,9" class="arrowMarkerPath" style="stroke-width: 2; stroke-dasharray: 1, 0;"></path></marker><marker id="mermaid-1792746204259_flowchart-v2-crossStart" class="marker cross flowchart-v2" viewBox="0 0 11 11" refX="-1" refY="5.2" markerUnits="userSpaceOnUse" markerWidth="11" markerHeight="11" orient="auto"><path d="M 1,1 l 9,9 M 10,1 l -9,9" class="arrowMarkerPath" style="stroke-width: 2; stroke-dasharray: 1, 0;"></path></marker><marker id="mermaid-1792746204259_flowchart-v2-crossEnd-margin" class="marker cross flowchart-v2" viewBox="0 0 15 15" refX="17.7" refY="7.5" markerUnits="userSpaceOnUse" markerWidth="12" markerHeight="12" orient="auto"><path d="M 1,1 L 14,14 M 1,14 L 14,1" class="arrowMarkerPath" style="stroke-width: 2.5;"></path></marker><marker id="mermaid-1792746204259_flowchart-v2-crossStart-margin" class="marker cross flowchart-v2" viewBox="0 0 15 15" refX="-3.5" refY="7.5" markerUnits="userSpaceOnUse" markerWidth="12" markerHeight="12" orient="auto"><path d="M 1,1 L 14,14 M 1,14 L 14,1" class="arrowMarkerPath" style="stroke-width: 2.5; stroke-dasharray: 1, 0;"></path></marker><g class="root"><g class="clusters"></g><g class="edgePaths"><path d="M132,58.297L134.083,58.297C136.167,58.297,140.333,58.297,143.833,58.297C147.333,58.297,150.167,58.297,151.583,58.297L153,58.297" id="mermaid-1792746204259-L_x_z1_0" class=" edge-thickness-normal edge-pattern-solid edge-thickness-normal edge-pattern-solid flowchart-link" style=";" data-edge="true" data-et="edge" data-id="L_x_z1_0" data-points="W3sieCI6MTMyLCJ5Ijo1OC4yOTY4NzV9LHsieCI6MTQ0LjUsInkiOjU4LjI5Njg3NX0seyJ4IjoxNTcsInkiOjU4LjI5Njg3NX1d" data-look="classic" marker-end="url(#mermaid-1792746204259_flowchart-v2-pointEnd)"></path><path d="M313,58.297L315.083,58.297C317.167,58.297,321.333,58.297,324.833,58.297C328.333,58.297,331.167,58.297,332.583,58.297L334,58.297" id="mermaid-1792746204259-L_z1_a1_0" class=" edge-thickness-normal edge-pattern-solid edge-thickness-normal edge-pattern-solid flowchart-link" style=";" data-edge="true" data-et="edge" data-id="L_z1_a1_0" data-points="W3sieCI6MzEzLCJ5Ijo1OC4yOTY4NzV9LHsieCI6MzI1LjUsInkiOjU4LjI5Njg3NX0seyJ4IjozMzgsInkiOjU4LjI5Njg3NX1d" data-look="classic" marker-end="url(#mermaid-1792746204259_flowchart-v2-pointEnd)"></path><path d="M494,58.297L496.083,58.297C498.167,58.297,502.333,58.297,505.833,58.297C509.333,58.297,512.167,58.297,513.583,58.297L515,58.297" id="mermaid-1792746204259-L_a1_z2_0" class=" edge-thickness-normal edge-pattern-solid edge-thickness-normal edge-pattern-solid flowchart-link" style=";" data-edge="true" data-et="edge" data-id="L_a1_z2_0" data-points="W3sieCI6NDk0LCJ5Ijo1OC4yOTY4NzV9LHsieCI6NTA2LjUsInkiOjU4LjI5Njg3NX0seyJ4Ijo1MTksInkiOjU4LjI5Njg3NX1d" data-look="classic" marker-end="url(#mermaid-1792746204259_flowchart-v2-pointEnd)"></path><path d="M675,58.297L677.083,58.297C679.167,58.297,683.333,58.297,686.833,58.297C690.333,58.297,693.167,58.297,694.583,58.297L696,58.297" id="mermaid-1792746204259-L_z2_a2_0" class=" edge-thickness-normal edge-pattern-solid edge-thickness-normal edge-pattern-solid flowchart-link" style=";" data-edge="true" data-et="edge" data-id="L_z2_a2_0" data-points="W3sieCI6Njc1LCJ5Ijo1OC4yOTY4NzV9LHsieCI6Njg3LjUsInkiOjU4LjI5Njg3NX0seyJ4Ijo3MDAsInkiOjU4LjI5Njg3NX1d" data-look="classic" marker-end="url(#mermaid-1792746204259_flowchart-v2-pointEnd)"></path><path d="M856,58.297L858.083,58.297C860.167,58.297,864.333,58.297,867.833,58.297C871.333,58.297,874.167,58.297,875.583,58.297L877,58.297" id="mermaid-1792746204259-L_a2_z3_0" class=" edge-thickness-normal edge-pattern-solid edge-thickness-normal edge-pattern-solid flowchart-link" style=";" data-edge="true" data-et="edge" data-id="L_a2_z3_0" data-points="W3sieCI6ODU2LCJ5Ijo1OC4yOTY4NzV9LHsieCI6ODY4LjUsInkiOjU4LjI5Njg3NX0seyJ4Ijo4ODEsInkiOjU4LjI5Njg3NX1d" data-look="classic" marker-end="url(#mermaid-1792746204259_flowchart-v2-pointEnd)"></path><path d="M1037,58.297L1039.083,58.297C1041.167,58.297,1045.333,58.297,1048.833,58.297C1052.333,58.297,1055.167,58.297,1056.583,58.297L1058,58.297" id="mermaid-1792746204259-L_z3_a3_0" class=" edge-thickness-normal edge-pattern-solid edge-thickness-normal edge-pattern-solid flowchart-link" style=";" data-edge="true" data-et="edge" data-id="L_z3_a3_0" data-points="W3sieCI6MTAzNywieSI6NTguMjk2ODc1fSx7IngiOjEwNDkuNSwieSI6NTguMjk2ODc1fSx7IngiOjEwNjIsInkiOjU4LjI5Njg3NX1d" data-look="classic" marker-end="url(#mermaid-1792746204259_flowchart-v2-pointEnd)"></path></g><g class="edgeLabels"><g class="edgeLabel"><g class="label" data-id="L_x_z1_0" transform="translate(0, 0)"><foreignObject width="0" height="0"><div xmlns="http://www.w3.org/1999/xhtml" class="labelBkg" style="color: rgb(51, 51, 51) !important; background-color: rgba(255, 255, 255, 0.5); display: table-cell; white-space: nowrap; line-height: 1.5; max-width: 200px; text-align: center;"><span class="edgeLabel " style="color: rgb(51, 51, 51); fill: rgb(51, 51, 51); background-color: rgb(255, 255, 255); text-align: center;"></span></div></foreignObject></g></g><g class="edgeLabel"><g class="label" data-id="L_z1_a1_0" transform="translate(0, 0)"><foreignObject width="0" height="0"><div xmlns="http://www.w3.org/1999/xhtml" class="labelBkg" style="color: rgb(51, 51, 51) !important; background-color: rgba(255, 255, 255, 0.5); display: table-cell; white-space: nowrap; line-height: 1.5; max-width: 200px; text-align: center;"><span class="edgeLabel " style="color: rgb(51, 51, 51); fill: rgb(51, 51, 51); background-color: rgb(255, 255, 255); text-align: center;"></span></div></foreignObject></g></g><g class="edgeLabel"><g class="label" data-id="L_a1_z2_0" transform="translate(0, 0)"><foreignObject width="0" height="0"><div xmlns="http://www.w3.org/1999/xhtml" class="labelBkg" style="color: rgb(51, 51, 51) !important; background-color: rgba(255, 255, 255, 0.5); display: table-cell; white-space: nowrap; line-height: 1.5; max-width: 200px; text-align: center;"><span class="edgeLabel " style="color: rgb(51, 51, 51); fill: rgb(51, 51, 51); background-color: rgb(255, 255, 255); text-align: center;"></span></div></foreignObject></g></g><g class="edgeLabel"><g class="label" data-id="L_z2_a2_0" transform="translate(0, 0)"><foreignObject width="0" height="0"><div xmlns="http://www.w3.org/1999/xhtml" class="labelBkg" style="color: rgb(51, 51, 51) !important; background-color: rgba(255, 255, 255, 0.5); display: table-cell; white-space: nowrap; line-height: 1.5; max-width: 200px; text-align: center;"><span class="edgeLabel " style="color: rgb(51, 51, 51); fill: rgb(51, 51, 51); background-color: rgb(255, 255, 255); text-align: center;"></span></div></foreignObject></g></g><g class="edgeLabel"><g class="label" data-id="L_a2_z3_0" transform="translate(0, 0)"><foreignObject width="0" height="0"><div xmlns="http://www.w3.org/1999/xhtml" class="labelBkg" style="color: rgb(51, 51, 51) !important; background-color: rgba(255, 255, 255, 0.5); display: table-cell; white-space: nowrap; line-height: 1.5; max-width: 200px; text-align: center;"><span class="edgeLabel " style="color: rgb(51, 51, 51); fill: rgb(51, 51, 51); background-color: rgb(255, 255, 255); text-align: center;"></span></div></foreignObject></g></g><g class="edgeLabel"><g class="label" data-id="L_z3_a3_0" transform="translate(0, 0)"><foreignObject width="0" height="0"><div xmlns="http://www.w3.org/1999/xhtml" class="labelBkg" style="color: rgb(51, 51, 51) !important; background-color: rgba(255, 255, 255, 0.5); display: table-cell; white-space: nowrap; line-height: 1.5; max-width: 200px; text-align: center;"><span class="edgeLabel " style="color: rgb(51, 51, 51); fill: rgb(51, 51, 51); background-color: rgb(255, 255, 255); text-align: center;"></span></div></foreignObject></g></g></g><g class="nodes"><g class="node default  " id="mermaid-1792746204259-flowchart-x-0" data-look="classic" transform="translate(70, 58.296875)"><rect class="basic label-container" style="" x="-62" y="-43.796875" width="124" height="87.59375"></rect><g class="label" style="" transform="translate(-32, -28.796875)"><rect></rect><foreignObject width="64" height="57.59375"><div xmlns="http://www.w3.org/1999/xhtml" style="color: rgb(51, 51, 51) !important; display: table-cell; white-space: nowrap; line-height: 1.5; max-width: 200px; text-align: center;"><span class="nodeLabel " style="color: rgb(51, 51, 51); fill: rgb(51, 51, 51);"><p style="line-height: 1.8; overflow-wrap: break-word; margin: 0px; font-size: inherit !important; color: rgb(24, 24, 27);">输入 x<br>（向量）</p></span></div></foreignObject></g></g><g class="node default" id="mermaid-1792746204259-flowchart-z1-1" data-look="classic" transform="translate(235, 58.296875)"><rect class="basic label-container" style="" x="-78" y="-43.796875" width="156" height="87.59375"></rect><g class="label" style="" transform="translate(-48, -28.796875)"><rect></rect><foreignObject width="96" height="57.59375"><div xmlns="http://www.w3.org/1999/xhtml" style="color: rgb(51, 51, 51) !important; display: table-cell; white-space: nowrap; line-height: 1.5; max-width: 200px; text-align: center;"><span class="nodeLabel " style="color: rgb(51, 51, 51); fill: rgb(51, 51, 51);"><p style="line-height: 1.8; overflow-wrap: break-word; margin: 0px; font-size: inherit !important; color: rgb(24, 24, 27);">隐藏层 z¹<br>（线性变换）</p></span></div></foreignObject></g></g><g class="node default" id="mermaid-1792746204259-flowchart-a1-3" data-look="classic" transform="translate(416, 58.296875)"><rect class="basic label-container" style="" x="-78" y="-43.796875" width="156" height="87.59375"></rect><g class="label" style="" transform="translate(-48, -28.796875)"><rect></rect><foreignObject width="96" height="57.59375"><div xmlns="http://www.w3.org/1999/xhtml" style="color: rgb(51, 51, 51) !important; display: table-cell; white-space: nowrap; line-height: 1.5; max-width: 200px; text-align: center;"><span class="nodeLabel " style="color: rgb(51, 51, 51); fill: rgb(51, 51, 51);"><p style="line-height: 1.8; overflow-wrap: break-word; margin: 0px; font-size: inherit !important; color: rgb(24, 24, 27);">隐藏层 a¹<br>（激活函数）</p></span></div></foreignObject></g></g><g class="node default" id="mermaid-1792746204259-flowchart-z2-5" data-look="classic" transform="translate(597, 58.296875)"><rect class="basic label-container" style="" x="-78" y="-43.796875" width="156" height="87.59375"></rect><g class="label" style="" transform="translate(-48, -28.796875)"><rect></rect><foreignObject width="96" height="57.59375"><div xmlns="http://www.w3.org/1999/xhtml" style="color: rgb(51, 51, 51) !important; display: table-cell; white-space: nowrap; line-height: 1.5; max-width: 200px; text-align: center;"><span class="nodeLabel " style="color: rgb(51, 51, 51); fill: rgb(51, 51, 51);"><p style="line-height: 1.8; overflow-wrap: break-word; margin: 0px; font-size: inherit !important; color: rgb(24, 24, 27);">隐藏层 z²<br>（线性变换）</p></span></div></foreignObject></g></g><g class="node default" id="mermaid-1792746204259-flowchart-a2-7" data-look="classic" transform="translate(778, 58.296875)"><rect class="basic label-container" style="" x="-78" y="-43.796875" width="156" height="87.59375"></rect><g class="label" style="" transform="translate(-48, -28.796875)"><rect></rect><foreignObject width="96" height="57.59375"><div xmlns="http://www.w3.org/1999/xhtml" style="color: rgb(51, 51, 51) !important; display: table-cell; white-space: nowrap; line-height: 1.5; max-width: 200px; text-align: center;"><span class="nodeLabel " style="color: rgb(51, 51, 51); fill: rgb(51, 51, 51);"><p style="line-height: 1.8; overflow-wrap: break-word; margin: 0px; font-size: inherit !important; color: rgb(24, 24, 27);">隐藏层 a²<br>（激活函数）</p></span></div></foreignObject></g></g><g class="node default  " id="mermaid-1792746204259-flowchart-z3-9" data-look="classic" transform="translate(959, 58.296875)"><rect class="basic label-container" style="" x="-78" y="-43.796875" width="156" height="87.59375"></rect><g class="label" style="" transform="translate(-48, -28.796875)"><rect></rect><foreignObject width="96" height="57.59375"><div xmlns="http://www.w3.org/1999/xhtml" style="color: rgb(51, 51, 51) !important; display: table-cell; white-space: nowrap; line-height: 1.5; max-width: 200px; text-align: center;"><span class="nodeLabel " style="color: rgb(51, 51, 51); fill: rgb(51, 51, 51);"><p style="line-height: 1.8; overflow-wrap: break-word; margin: 0px; font-size: inherit !important; color: rgb(24, 24, 27);">输出 z³<br>（线性变换）</p></span></div></foreignObject></g></g><g class="node default  " id="mermaid-1792746204259-flowchart-a3-11" data-look="classic" transform="translate(1140, 58.296875)"><rect class="basic label-container" style="" x="-78" y="-43.796875" width="156" height="87.59375"></rect><g class="label" style="" transform="translate(-48, -28.796875)"><rect></rect><foreignObject width="96" height="57.59375"><div xmlns="http://www.w3.org/1999/xhtml" style="color: rgb(51, 51, 51) !important; display: table-cell; white-space: nowrap; line-height: 1.5; max-width: 200px; text-align: center;"><span class="nodeLabel " style="color: rgb(51, 51, 51); fill: rgb(51, 51, 51);"><p style="line-height: 1.8; overflow-wrap: break-word; margin: 0px; font-size: inherit !important; color: rgb(24, 24, 27);">输出 a³<br>（激活函数）</p></span></div></foreignObject></g></g></g></g></g><defs><filter id="mermaid-1792746204259-drop-shadow" height="130%" width="130%"><feDropShadow dx="4" dy="4" stdDeviation="0" flood-opacity="0.06" flood-color="#000000"></feDropShadow></filter></defs><defs><filter id="mermaid-1792746204259-drop-shadow-small" height="150%" width="150%"><feDropShadow dx="2" dy="2" stdDeviation="0" flood-opacity="0.06" flood-color="#000000"></feDropShadow></filter></defs></svg>

*图：三层神经网络前向传播信号流动*

一个参数x，会一层层影响后面的所有层。最终影响函数l。

> 传递到第一层输入的梯度，等于所有后续各层导数的连乘积，这就是反向传播的核心，梯度沿着计算链路从输出层反向传递到输入层，每经过一层，梯度乘以该层激活函数的导数和线性变化的导数。这个过程和前向传播的过程刚好相反。

如下游数据有问题，现在需要找到在哪一环出现了故障，需要从下至上每层检测，这个过程与反向传播类似。



#### 计算图视角下的反向传播

计算图将神经网络的前向传播过程分解为一系列基本运算节点，每个节点只负责一个简单的操作（如矩阵乘法、激活函数、加法），数据沿着边从输入流向输出，在处理反向传播时，就将信息流动的方向反转。

![1793171701324.png](https://fastly.jsdelivr.net/gh/thecoolboyhan/th_blogs@main/image/2026-10/1793171701324_1793171701337.png)

反向传播利用程序，自动将前向传播的数据反向流转



#### 计算复杂度分析

- 时间复杂度

方向传播的时间复杂度和前向传播的在同一个量级，意味着训练一次迭代（一次前向传播和一次后向传播）的计算量大概就是前向传播的计算量的两倍，也是同一量级的。



- 空间复杂度

反向传播需要存储前向传播的中间结果用于计算梯度，这需要有一定的内存开销。总和得出，内存占用等于批量大小乘以各层神经元数的两倍。



> 对于大型网络和批量训练，内存开销可能成为瓶颈。譬如，一个 10 层网络，每层 1000 个神经元，批量大小 1000，内存占用约为1000×10×1000×2=21000×10×1000×2=2 千万个浮点数，按 FP32 计算，约需 80 MB 内存。这还只是训练中间结果的存储开销，并未计算模型参数本身占用的内存。

- 减少内存占用的一些常用方式

1. 梯度检查点：只存储分层的中间结果，需要时重新计算。（用时间换空间）内存受限，但计算资源充足
2. 内存复用：计算完梯度后，立刻释放中间结果内存，减少峰值内存占用。（手动回收内存）
3. 混合精度：使用低精度存储中间结果，减少一半内存占用。（精简数据）



### 激活函数和损失函数



#### 梯度消失和梯度爆炸

**梯度消失**是指反向传播中梯度逐层衰减，传递到网络前面几层时已经十分接近0，参数几乎不在更新。**梯度消失是由于连续与一个小于 1 的导数相乘而导致的**



> 一旦出现梯度消失，权重变化就变得极小，深层网络的前面几层参数几乎不更新，训练过程收敛极慢或停滞。同时由于前面几层没有学到有效特征，测试集的表现通常也不好。

- 梯度爆炸

反向传播中梯度逐层放大，前面几层梯度极大，参数更新幅度过大，训练变得极不稳定。**激活函数导数长期大于 1**



> 梯度消失和梯度爆炸是模型训练中的两种问题，下面主要说明如何减少两种问题出现的机率

#### 激活函数

如果网络全部使用线性变换，无论叠加多少层，最终仍然是线性模型。



- 双曲正切函数

是Sigmoid的改进版本。放大输入

![Sigmoid 与 tanh 函数对比](https://ai.icyfenix.cn/assets/sigmoid-tanh-comparison-D5cBz144.png)

*图：Sigmoid 与 tanh 函数和导数图像对比*

> 假设调整房间中的空调温度，目标温度25，当空调只能在30-40内调节，你能传递给网络训练的信息就只能一直是“天气太热”，网络不知道应该具体降温多少。如果把可调节范围扩大到-10到50，空调自然可以精确给出当前温度和目标温度的差距。

| 特性       | Sigmoid                | tanh                   |
| :--------- | :--------------------- | :--------------------- |
| 输出范围   | (0,1)(0,1)             | (−1,1)(−1,1)           |
| 输出中心   | 非零中心（恒正）       | 零中心（正负平衡）     |
| 导数最大值 | 0.250.25               | 11                     |
| 梯度消失   | 严重（两端导数趋近 0） | 存在（两端导数趋近 0） |
| 适用位置   | 输出层（二分类）       | 隐藏层（浅层网络）     |



- ReLU及其变体

正数就保持不变，负数就置零，在零点的左右导数甚至都不相等。

通过只保留正数，让计算变成线性的，但同时带来了大量的数据死亡（小于0的数据将永久归零）。所以需要大量的调整，让死亡的神经元占比降低。



- GELU与Swish

在ReLU的基础上，用微小斜率和指数平滑来修补负数区域，一定程度上缓解神经元死亡的风险。



**GELU函数**：在ReLU的基础上加权，来决定输出的是z还是0。相当于可以动态的调整负数为零的范围，极限值等于ReLU所有负数都为0。

![GELU / Swish / ReLU 曲线对比](https://ai.icyfenix.cn/assets/gelu-swish-relu-comparison-CwbscJWB.png)

*图：左为 GELU、Swish 和 ReLU 曲线对比，右为 GELU 精确形式与 tanh 近似的对比*

**Swish函数**：用自动搜索技术发现更好的激活函数。

- 激活函数的选择策略

| 场景                               | 推荐激活函数         | 原因                                             |
| :--------------------------------- | :------------------- | :----------------------------------------------- |
| 隐藏层（CNN / 传统深度网络）       | ReLU / Leaky ReLU    | 缓解梯度消失，计算高效，配合批归一化效果稳定     |
| 隐藏层（Transformer 编码器）       | GELU                 | 平滑梯度流，无神经元死亡，匹配残差连接和层归一化 |
| 隐藏层（Transformer 解码器 / LLM） | Swish（SwiGLU 门控） | 门控机制选择性抑制无关特征，困惑度更低           |
| 隐藏层（浅层网络）                 | tanh / ReLU          | 浅层网络梯度消失问题不严重                       |
| 输出层（二分类）                   | Sigmoid              | 输出概率，符合二分类语义                         |
| 输出层（多分类）                   | Softmax              | 输出概率分布，符合多分类语义                     |
| 输出层（回归）                     | Linear（无激活）     | 输出无范围限制                                   |



#### 损失函数

> 激活函数决定网络的非线性表达能力，损失函数决定网络的优化目标。

损失函数衡量预测值与真实值之间的差距、引导参数更新方向。

- 回归损失

回归问题的目标是预测连续值，房价预测、温度预测、销量预测等。度量连续值损失方式是：计算预测值与真实值之间的差距，差距越大惩罚越重。



**三种常见的回归损失函数**：

| 特性         | MSE          | MAE              | Huber                  |
| :----------- | :----------- | :--------------- | :--------------------- |
| 惩罚方式     | 二次（平方） | 纯线性           | 小误差二次，大误差线性 |
| 异常值敏感度 | 高（敏感）   | 低（鲁棒）       | 中（平衡）             |
| 梯度变化     | 与误差成正比 | 恒定 ±1±1        | 小误差递减，大误差恒定 |
| 优化难度     | 易（凸函数） | 中（零点不可导） | 易（处处可导）         |



- 分类损失

类别是离散的信息（猫、狗、鸟），需要专门的损失函数 **交叉熵损失**。以信息中概率越小的事件发生时信息量越大的观点为基础，度量两个概率分布之间的差距。



- Hinge损失

支持向量机的损失函数，体现了最大间隙原则的优化思想。寻找最大间隙分类边界，不仅需要分类正确，还要求分类边界与两类样本保持足够的距离，提高泛化能力。



| 任务类型         | 推荐损失函数                 | 输出层激活 | 选择原因                   |
| :--------------- | :--------------------------- | :--------- | :------------------------- |
| 回归（无异常值） | MSE                          | Linear     | 数据干净，MSE 收敛快       |
| 回归（有异常值） | MAE / Huber                  | Linear     | 异常值鲁棒，不过度迁就     |
| 二分类           | Binary Cross-Entropy         | Sigmoid    | 梯度计算高效，避免消失     |
| 多分类           | Categorical Cross-Entropy    | Softmax    | 梯度计算高效，概率语义清晰 |
| 多标签分类       | Binary Cross-Entropy（每类） | Sigmoid    | 每个标签独立二分类         |



## 优化神经网络

**如何训练**

### 梯度下降

> 梯度下降是最经典、应用最广泛的优化算法之一。就是沿着梯度的反方向（损失下降最快的方向）更新参数。



#### 梯度下降的基本原理

反向传播部分我们推导出了[计算梯度的公式](https://ai.icyfenix.cn/deep-learning/neural-network-structure/backpropagation.html#参数梯度计算)，有了梯度之后，该如何更新参数，这个场景就仿佛登山者在四周雾气弥漫，看不清位置的山上，凭脚下的感知，能判断出坡度，接下来要决定的是朝哪个方向走、走多远。



![梯度下降的几何直观示意图](https://ai.icyfenix.cn/assets/gradient-descent-geometric-intuition-B55BzlFa.png)

*图：梯度下降的几何直观*



接下来的问题是每一步该走多远。如果每一步走得太小，可能需要走几千步才能到达山谷。如果每一步走得太大，可能直接跳过山谷，跑到另一边的山坡上，甚至越跑越远。

| 特性             | 批量梯度下降       | 随机梯度下降       | 小批量梯度下降       |
| :--------------- | :----------------- | :----------------- | :------------------- |
| 每步使用样本数   | 全部样本 m*m*      | 单个样本           | 小批量 b*b*          |
| 梯度精度         | 精确（真实梯度）   | 噪声大（近似梯度） | 适中（噪声可控）     |
| 计算效率         | 低（遍历全部数据） | 高（每样本更新）   | 较高（每小批量更新） |
| 收敛稳定性       | 稳定（平滑路径）   | 震荡（波动路径）   | 较稳定（适度噪声）   |
| 跳出局部最优能力 | 弱（无噪声）       | 强（噪声帮助探索） | 适中                 |



#### 动量法

![椭圆损失曲面示意图](https://ai.icyfenix.cn/assets/elliptical-loss-surface-JiRPzJj0.png)

*图：椭圆损失曲面 L=W12+100W22\*L*=\*W*12+100\*W*22 的三维可视化*



SGD每一步完全依赖当前位置的梯度，完全不考虑历史信息。当梯度在不同方向上差异很大时，参数更新方向在各个方向之间剧烈摆动，无法沿着一条平滑的路径收敛。



**动量法**：引入历史梯度信息，平滑参数更新方向，就像物理学中的动量概念，一个有质量的物体在运动时会保持惯性，不会因为单次受力而剧烈改变方向。



> 动量法的核心机制是梯度累积。当梯度方向一致，历史梯度累积放大当前梯度，加速前进；当梯度方向摆动，历史梯度正负抵消，削弱当前梯度，抑制震荡，整体收敛更平稳高效。



#### Nesterov加速梯度



- NAG原理

NAG 相对于动量法的改进是在预测位置计算梯度，而不是在当前位置。



> 新速度 = 惯性保留 + 预测位置的推力
>
> 新位置 = 当前位置 − 速度

NAG可以避免冲过头的情况，当发现梯度反转（过了山谷），提前减速，可以更平稳的到底山谷底部。



### 自适应优化器

根据参数的历史梯度自动调整学习率，为每个参数分配独立的更新步长。



**下面是自适应优化器的迭代过程**：越来越好

- AdaGrad

既然频繁更新的参数已经学到了很多信息，就应该放慢脚步，反之，稀疏更新的参数还有大量信息待学，就应该大步前进。

> 参数每更新一步，学习率就变小一点。训练后期，学习率可能变得极小，参数几乎不再更新，训练停滞。

- RMSprop

滑动平均是一种加权平均，新数据权重大、旧数据权重逐渐衰减，就像一个窗口在数据链中滑动，让历史信息有进有出，因此 RMSprop 能做到只保留最近若干步的梯度信息。

**优点**：

窗口效应，只保留最近的梯度信息，避免了梯度累计只进不出，让学习率不再单调递减。

能走更快适应梯度变化，当梯度变化剧烈时，E也快速调整，学习率响应更加灵敏。

**缺陷**：

它只使用梯度平方调整学习率，没有累积历史梯度方向，相当于放弃了[动量法](https://ai.icyfenix.cn/deep-learning/neural-network-optimization/gradient-descent.html#动量法)的平滑效果。



- Adam（目前广泛使用的自适应优化器）

同时估计梯度的[一阶矩](https://en.wikipedia.org/wiki/Moment_(mathematics))和二阶矩，将动量法与自适应学习率融于一身。



- AdamW（权重修正版）

将权重衰减从梯度更新中分离，让梯度更新负责学习数据规律，权重衰减负责控制模型复杂度，两者应该独立运作、互不干扰。

现在一般在所有场景中都可以使用 AdamW 替代 Adam，尤其在需要强正则化的任务上，譬如大规模语言模型训练，AdamW 如今已成为许多 Transformer 架构模型，如 BERT、GPT 的默认优化器。



- Muon（优化器的未来）

1. 第一步，动量累积。Muon 像动量法一样，维护一个历史梯度的加权平均（动量缓冲区），新梯度加入时保留大部分旧方向、融入小部分新方向，以此平滑更新路径、抑制震荡。
2. 第二步，正交化。这是 Muon 与所有前述优化器不同的地方。可以把一个矩阵想象成多个独立方向及其强度的组合。譬如，一个权重矩阵可能在某些方向上推动得很猛（强度大），在另一些方向上只是轻轻触碰（强度小）。正交化做的事情就是只保留这些方向本身，而把它们的强度全部拉平到相同的水平。就像一个团队里有嗓门大的成员和沉默寡言的成员，正交化相当于给每个人装上同样音量的麦克风，让所有声音都能被平等地听到。

#### 如何选择优化器



| 优化器   | 核心机制                    | 优势                 | 缺陷                           | 适用场景                       |
| :------- | :-------------------------- | :------------------- | :----------------------------- | :----------------------------- |
| SGD      | 基础梯度下降                | 简单、稳定           | 震荡、慢                       | 简单任务、精调                 |
| Momentum | 动量平滑                    | 加速、抑制震荡       | 需调学习率                     | 通用                           |
| NAG      | 预测位置梯度                | 提前响应拐点         | 稍复杂                         | 追求精度                       |
| AdaGrad  | 累积梯度平方                | 稀疏梯度友好         | 学习率衰减                     | 稀疏数据、短期训练             |
| RMSprop  | 滑动平均梯度平方            | 学习率稳定           | 无动量                         | 长期训练、RNN                  |
| Adam     | 动量 + 自适应               | 鲁棒、快速           | 权重衰减问题                   | 通用、默认选择                 |
| AdamW    | Adam+解耦权重衰减           | 正则化稳定           | SGD 相比有额外的二阶矩内存开销 | 默认选择                       |
| Muon     | 动量 + Newton-Schulz 正交化 | 利用矩阵结构、内存省 | 仅适用于二维矩阵参数           | Transformer 隐藏层、大规模训练 |



- | 任务类型             | 推荐优化器      | 理由                                 |
  | :------------------- | :-------------- | :----------------------------------- |
  | 通用深度学习         | AdamW           | 鲁棒性强，默认选择                   |
  | 计算机视觉           | SGD + Momentum  | 实验表明泛化能力更好                 |
  | 自然语言处理         | AdamW           | 稀疏梯度，自适应优势明显             |
  | RNN/LSTM             | RMSprop / AdamW | 适应梯度尺度差异                     |
  | 精调预训练模型       | SGD + Momentum  | 小学习率精调，防止破坏预训练特征     |
  | 稀疏数据（推荐系统） | AdamW           | 稀疏参数获得大学习率                 |
  | 大规模语言模型训练   | Muon + AdamW    | 隐藏层用 Muon 提速，其余参数用 AdamW |



## 深层网络稳定性

### 权重初始化

一个好的初始化能让训练快速、稳定地收敛。



- Xavier初始化

通过分析信号在网络中的传播过程，推导出保持信号稳定所需的权重方差，精确计算出最佳的初始化参数。



一方面当输入远离 0 时，激活函数非线性特征显现，Xavier 初始化只能尽量让激活值落在线性区域，但无法完全避免饱和。另一方面更为严重，Xavier 初始化不适配 [ReLU 激活函数](https://ai.icyfenix.cn/deep-learning/neural-network-structure/activation-loss-functions.html#relu-及其变体) ，ReLU 的特性与 Sigmoid 和 tanh 完全不同。ReLU 只保留正值，负值全部置零，这意味着约一半的激活值被杀死，信号强度减半。Xavier 的线性假设在 ReLU 上完全失效，如果用 Xavier 初始化 ReLU 网络，激活值会逐层衰减，深层网络的梯度几乎为零。



- He初始化

ReLU 的稀疏性问题主要发生在前向传播阶段，反向传播时梯度只通过正值神经元传递，同样存在信号减半的问题，但 He 初始化优先保证前向传播的信号稳定性，因此仅对前向方向进行补偿。当 nin≈nout*n**in*≈*n**o**u**t* 时，He 初始化方差约为 Xavier 的两倍。



### Dropout正则化

训练时随机丢弃一部分神经元，让每个神经元学会独立工作，不能依赖其他神经元的存在。



- Dropout原理

训练时随机关闭一部分神经元，让剩下的神经元独立完成任务。

被丢弃的神经元（ri=0*r**i*=0）不参与前向传播和反向传播，其梯度为零，相当于从网络中暂时消失。这种暂时消失是关键，神经元只是本轮训练被丢弃，下一轮可能又被保留，所有神经元在整个训练过程中都会被反复使用。

**Dropout 实际上在训练时隐式地构建了海量的子网络，推理时相当于对这些子网络的预测进行平均。这种训练一个模型，获得多个模型效果的特性，才是 Dropout 的精髓所在。**



### 批归一化

>  随着网络深度增加，各层输入分布不断变化，导致梯度传播不稳定。这种现象称为**内部协变量偏移**，它使得深层网络难以训练、收敛缓慢、对初始化高度敏感。



- BN算法原则

既然各层输入分布的变化是训练困难的根源，就要想办法在每一层引入一种机制，强制将输入分布标准化，使其保持稳定。



## 卷积神经网络

卷积层通过小型滤波器在图像上滑动提取局部特征，池化层降采样扩大感受野，多层堆叠后实现从局部到全局的特征抽象。

> 如何抽象一个复杂的对象



### CNN基础原理

> 视觉模型

- 卷积原理

卷积操作在用一个探针在图像上逐位置探测。针头（卷积核）是一个小型矩阵，譬如 3×33×3 的方格，每个格子里有个数值，将探针放在图像某个位置，探针的数值和图像对应位置的像素值相乘后求和，得到一个输出值。



![卷积运算数值示例：5×5 输入图像、3×3 卷积核和 3×3 输出特征图](https://ai.icyfenix.cn/assets/conv-3x3-input-kernel-Cj1lEzQv.png)

CNN 的关键突破在于它不再需要人工卷积核设计，卷积核参数并不是预先定义的，而是通过反向传播训练学习。



- AlexNet架构设计

深度学习在视觉领域的崛起

![1793602228270.png](https://fastly.jsdelivr.net/gh/thecoolboyhan/th_blogs@main/image/2026-11/1793602228270_1793602228289.png)



## 生成式模型

机器学习的主要应用是做预测（图像分类）或者做决策（量化投资），用于这些任务场景的模型被称为**判别式模型**（Discriminative Model）。还有一种是根据已有数据或给出已知特征，让机器生成具有特定特征的数据，完成这类任务的模型就被称为**生成式模型**（Generative Model）。

### 变分自编码器

> 如何让神经网络学习概率分布，而非单纯的点估计。



- 自编码器原理

一种无监督学习模型，设计目标是学习数据的压缩表示，并不是生成新样本。

> 将数据从高维度压缩到低维空间，再从低维表示重建原始数据。

![1793604554591.png](https://fastly.jsdelivr.net/gh/thecoolboyhan/th_blogs@main/image/2026-11/1793604554591_1793604554617.png)

编码器负责将高维输入压缩为低维潜在编码，解码器则将低维编码展开为高维重建输出。



- 变分自编码器

<svg id="mermaid-1793603885446" width="100%" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" class="flowchart" style="max-width: 1254.41px; display: inline-block; margin: 0px auto; width: 940.811px; height: 56.0977px;" viewBox="0 6.5 1254.4140625 74.796875" role="graphics-document document" aria-roledescription="flowchart-v2"><g><g class="root"><g class="nodes"><g class="node default" id="mermaid-1793603885446-flowchart-B1-0" data-look="classic" transform="translate(108.41796875, 43.8984375)"><g class="label" style="" transform="translate(-70.41796875, -14.3984375)"><foreignObject width="140.8359375" height="28.796875"><div xmlns="http://www.w3.org/1999/xhtml" style="color: rgb(51, 51, 51) !important; display: table-cell; white-space: nowrap; line-height: 1.5; max-width: 200px; text-align: center;"><span class="nodeLabel " style="color: rgb(51, 51, 51); fill: rgb(51, 51, 51);"><p style="line-height: 1.8; overflow-wrap: break-word; margin: 0px; font-size: inherit !important; color: rgb(24, 24, 27);">输入 x（高维数据）</p></span></div></foreignObject></g></g><g class="node default" id="mermaid-1793603885446-flowchart-B2-1" data-look="classic" transform="translate(319.0859375, 43.8984375)"><rect class="basic label-container" style="" x="-85.25" y="-29.3984375" width="170.5" height="58.796875"></rect><g class="label" style="" transform="translate(-55.25, -14.3984375)"><rect></rect><foreignObject width="110.5" height="28.796875"><div xmlns="http://www.w3.org/1999/xhtml" style="color: rgb(51, 51, 51) !important; display: table-cell; white-space: nowrap; line-height: 1.5; max-width: 200px; text-align: center;"><span class="nodeLabel " style="color: rgb(51, 51, 51); fill: rgb(51, 51, 51);"><p style="line-height: 1.8; overflow-wrap: break-word; margin: 0px; font-size: inherit !important; color: rgb(24, 24, 27);">编码器 Encoder</p></span></div></foreignObject></g></g><g class="node default" id="mermaid-1793603885446-flowchart-B3-3" data-look="classic" transform="translate(513.8984375, 43.8984375)"><rect class="basic label-container" style="fill:#c8e6c9 !important" x="-84.5625" y="-29.3984375" width="169.125" height="58.796875"></rect><g class="label" style="" transform="translate(-54.5625, -14.3984375)"><rect></rect><foreignObject width="109.125" height="28.796875"><div xmlns="http://www.w3.org/1999/xhtml" style="color: rgb(51, 51, 51) !important; display: table-cell; white-space: nowrap; line-height: 1.5; max-width: 200px; text-align: center;"><span class="nodeLabel " style="color: rgb(51, 51, 51); fill: rgb(51, 51, 51);"><p style="line-height: 1.8; overflow-wrap: break-word; margin: 0px; font-size: inherit !important; color: rgb(24, 24, 27);">分布参数 (μ, σ)</p></span></div></foreignObject></g></g><g class="node default  " id="mermaid-1793603885446-flowchart-B4-5" data-look="classic" transform="translate(713.55078125, 43.8984375)"><rect class="basic label-container" style="fill:#fff9c4 !important" x="-90.08984375" y="-29.3984375" width="180.1796875" height="58.796875"></rect><g class="label" style="" transform="translate(-60.08984375, -14.3984375)"><rect></rect><foreignObject width="120.1796875" height="28.796875"><div xmlns="http://www.w3.org/1999/xhtml" style="color: rgb(51, 51, 51) !important; display: table-cell; white-space: nowrap; line-height: 1.5; max-width: 200px; text-align: center;"><span class="nodeLabel " style="color: rgb(51, 51, 51); fill: rgb(51, 51, 51);"><p style="line-height: 1.8; overflow-wrap: break-word; margin: 0px; font-size: inherit !important; color: rgb(24, 24, 27);">采样 z ~ N(μ, σ²)</p></span></div></foreignObject></g></g><g class="node default" id="mermaid-1793603885446-flowchart-B5-7" data-look="classic" transform="translate(914.50390625, 43.8984375)"><rect class="basic label-container" style="" x="-85.86328125" y="-29.3984375" width="171.7265625" height="58.796875"></rect><g class="label" style="" transform="translate(-55.86328125, -14.3984375)"><rect></rect><foreignObject width="111.7265625" height="28.796875"><div xmlns="http://www.w3.org/1999/xhtml" style="color: rgb(51, 51, 51) !important; display: table-cell; white-space: nowrap; line-height: 1.5; max-width: 200px; text-align: center;"><span class="nodeLabel " style="color: rgb(51, 51, 51); fill: rgb(51, 51, 51);"><p style="line-height: 1.8; overflow-wrap: break-word; margin: 0px; font-size: inherit !important; color: rgb(24, 24, 27);">解码器 Decoder</p></span></div></foreignObject></g></g><g class="node default" id="mermaid-1793603885446-flowchart-B6-9" data-look="classic" transform="translate(1135.890625, 43.8984375)"><rect class="basic label-container" style="" x="-110.5234375" y="-29.3984375" width="221.046875" height="58.796875"></rect><g class="label" style="" transform="translate(-80.5234375, -14.3984375)"><rect></rect><foreignObject width="161.046875" height="28.796875"><div xmlns="http://www.w3.org/1999/xhtml" style="color: rgb(51, 51, 51) !important; display: table-cell; white-space: nowrap; line-height: 1.5; max-width: 200px; text-align: center;"><span class="nodeLabel " style="color: rgb(51, 51, 51); fill: rgb(51, 51, 51);"><p style="line-height: 1.8; overflow-wrap: break-word; margin: 0px; font-size: inherit !important; color: rgb(24, 24, 27);">重建输出 x' （近似 x）</p></span></div></foreignObject></g></g></g></g></g><defs><filter id="mermaid-1793603885446-drop-shadow" height="130%" width="130%"><feDropShadow dx="4" dy="4" stdDeviation="0" flood-opacity="0.06" flood-color="#000000"></feDropShadow></filter></defs><defs><filter id="mermaid-1793603885446-drop-shadow-small" height="150%" width="150%"><feDropShadow dx="2" dy="2" stdDeviation="0" flood-opacity="0.06" flood-color="#000000"></feDropShadow></filter></defs></svg>

*图：VAE 工作流程*

![1793604781463.png](https://fastly.jsdelivr.net/gh/thecoolboyhan/th_blogs@main/image/2026-11/1793604781463_1793604781487.png)



### 生成式对抗网络



- GAN架构设计

![1793605291694.png](https://fastly.jsdelivr.net/gh/thecoolboyhan/th_blogs@main/image/2026-11/1793605291694_1793605291717.png)

同一个训练，让生成器和判别器做对抗，生成器负责欺骗判别器，判别器负责鉴别生成器。一方的成功往往代表另一方的失败。在对抗中来训练模型。



- 纳什均衡

<font color='red'>GAN的理想训练终点是生成器和判别器达到纳什均衡</font>，每个玩家的策略在给定其他玩家策略的前提下是最优的，任何玩家单独改变策略都不会获益。两个人在博弈中各自找到了最佳策略，谁先改变策略谁就会吃亏，达到一种势均力敌的稳定状态。



**GAN达到纳什均衡的两个条件**：

1. 生成器学到了真实数据的全部特征，生成的样本和统计的样本统计上无法区分。
2. 判别器无法区分真实样本和生成样本，对任何输入，判别器输出的概率都是0.5。

![1793605979796.png](https://fastly.jsdelivr.net/gh/thecoolboyhan/th_blogs@main/image/2026-11/1793605979796_1793605979820.png)



- GAN与VAE对比

**VEA**：学习分布再采样，编码器将数据映射到潜在空间的概率分布，解码器从分布采样重建数据。训练的目标是保证损失最小。<font color='red'>重建的损失具有像素级准确的倾向，会导致生成样本模糊，VAE总是学到数据的平均表示，而非细节特征。</font>



**GAN**：对抗博弈，学习造假。生成器不需要显示学习分布，只需要欺骗判别器。判别器学习鉴别真假的过程中，间接刻画真实数据的特征。<font color='red'>GAN没有显式的空间结构，很难像VAE那样通过调整编维度控制生成特征（变体一定程度克服了这个缺点）</font>

| 特性       | VAE                        | GAN                     |
| :--------- | :------------------------- | :---------------------- |
| 生成原理   | 学习数据分布，从分布采样   | 对抗训练，无显式分布    |
| 训练目标   | 重建损失 + KL 散度（ELBO） | 对抗博弈损失（Minimax） |
| 生成质量   | 通常模糊，但稳定           | 通常清晰，但不稳定      |
| 潜在空间   | 有结构，可解释，可编辑     | 无显式结构，难以控制    |
| 训练稳定性 | 稳定，容易收敛             | 不稳定，可能崩溃        |
| 计算开销   | 较低（单网络训练）         | 较高（两网络交替训练）  |



## 序列模型

目前为止，所有的模型每次输入的处理都是独立的，本次处理与上一次输入没有关系。（无状态的）

现实中存在一类数据，数据之间存在时间依赖关系。处理序列数据，需要一种具有状态的、能够记住过去信息、根据历史做出当前决策的模型架构。



### RNN基础原理

> 循环神经网络通过引入循环连接在时间维度上传递信息，让网络拥有记忆的能力，当前时刻的输出不仅取决于当前输入，还取决于之前所有时刻的输入。



- 序列建模

![1793611975363.png](https://fastly.jsdelivr.net/gh/thecoolboyhan/th_blogs@main/image/2026-11/1793611975363_1793611975399.png)

> 网络在时刻t的输出，不仅传递给下一层，还传递回网络自身，作为时刻t+1的额外输入。



- 梯度传递与局限

RNN的训练算法被称为时间反向传播。



### LSTM与GRU门控制

