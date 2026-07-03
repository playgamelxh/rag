## Loss Function 损失函数
### 一、基础定义
损失函数（Loss Function）：用来衡量模型预测值与真实标签之间差距的函数。
- 单个样本计算误差 → Loss
- 全部样本损失取平均 → Cost Function（代价函数）
- 训练目标：最小化损失

### 二、常用分类损失
1. **Cross Entropy Loss 交叉熵损失（最常用分类）**

   - 适用：多分类、二分类
   - 公式（二分类）：$L = -[y \log(\hat{y}) + (1 - y) \log(1 - \hat{y})]$
   - 特点：配合 sigmoid/softmax，梯度稳定，解决 MSE 梯度消失问题。

2. **Binary Cross Entropy (BCE) 二元交叉熵**

   - 仅二分类任务，输出层 sigmoid
   - 公式：$L = -\frac{1}{N} \sum_{i=1}^{N} [y_i \log(\hat{y}_i) + (1 - y_i) \log(1 - \hat{y}_i)]$

3. **Focal Loss 焦点损失**

   - 解决样本不均衡（正负样本差距大），降低易分样本权重
   - 公式：$L = -\alpha (1 - \hat{y})^\gamma \log(\hat{y})$

4. **Hinge Loss 合页损失**

   - SVM 专用，支持向量分类
   - 公式：$L = \max(0, 1 - y \cdot \hat{y})$

### 三、常用回归损失
1. **MSE 均方误差 L2 Loss**

   - 公式：$L = (y - \hat{y})^2$
   - 优点：梯度平滑；缺点：对异常值极其敏感。

2. **MAE 平均绝对误差 L1 Loss**

   - 公式：$L = |y - \hat{y}|$
   - 优点：鲁棒抗离群点；缺点：零点处梯度突变。

3. **Huber Loss**

   - 公式：$L_{\delta}(a) = \begin{cases} \frac{1}{2} a^2, & |a| \le \delta \\ \delta(|a| - \frac{1}{2} \delta), & |a| > \delta \end{cases}$，其中 $a = y - \hat{y}$
   - 结合 L1+L2：误差小时用 MSE，误差大时用 MAE，兼顾平滑与抗噪。超参数 $\delta$（阈值，人为设定，常用 1、1.345）

### 四、特殊场景损失
- **Dice Loss**：医学图像分割（样本不均衡分割），公式：$L = 1 - \frac{2 |X \cap Y|}{|X| + |Y|}$
- **IoU Loss**：目标检测分割，公式：$L = 1 - \frac{|X \cap Y|}{|X \cup Y|}$
- **Triplet Loss**：人脸识别 / 度量学习（拉近同类、拉远异类）
- **KL Divergence KL 散度**：分布对齐、知识蒸馏，公式：$D_{KL}(P \| Q) = \sum_i P(i) \log \frac{P(i)}{Q(i)}$

### 五、简单区分记忆
- 分类任务 → 交叉熵 CrossEntropyLoss
- 回归任务 → MSE / MAE / Huber
- 样本不平衡 → Focal / Dice
- 相似度对比 → Triplet Loss

## Cross Entropy Loss 交叉熵损失
### 一、前置知识：信息量、熵、交叉熵
#### 1. 自信息（信息量）
事件发生概率越小，信息量越大：

$I(x) = -\log P(x)$

$P=1$（必然发生）：$I=0$，无信息；

$P\to0$（极小概率）：$I\to+\infty$。
#### 2. 熵（Entropy）
真实分布 P 的平均信息量，衡量分布不确定性：

   $H(P) = -\sum_{i} P(x_i)\log P(x_i)$
   熵越大，数据越混乱。
#### 3. 交叉熵（Cross Entropy）
   用模型预测分布 Q 去编码真实分布 P，所需平均信息量：

   $CE(P,Q) = -\sum_{i} P(x_i)\log Q(x_i)$

   交叉熵 = 熵 + KL 散度（分布差异）

   $CE(P,Q) = H(P) + D_{KL}(P||Q)$

   训练时真实分布 P 固定（标签不变），最小化交叉熵等价于最小 KL 散度，即让预测分布贴近真实分布。

### 二、分两类场景：二分类 / 多分类场景 
### 1：二分类交叉熵 BCE (Binary Cross Entropy)
适用：只有两类，输出层激活 Sigmoid，输出 \([0,1]\) 概率。

设：

真实标签 \(y \in \{0,1\}\)

模型预测概率 \(\hat{y} = \sigma(z) \in (0,1)\)

单样本损失：
$L = -\big[y\log\hat{y} + (1-y)\log(1-\hat{y})\big]$

批量总损失（N 个样本取平均）：
$\mathcal{L} = -\frac{1}{N}\sum_{n=1}^N \big[y_n\log\hat{y}_n + (1-y_n)\log(1-\hat{y}_n)\big]$

直观理解

真实标签 $y=1$：只保留第一项 $-\log\hat{y}$，预测越接近 1 损失越小；

真实标签 $y=0$：只保留第二项 $-\log(1-\hat{y})$，预测越接近 0 损失越小。

带权重 BCE（处理样本不均衡）正负样本数量差距大时，增加权重 $\alpha$：
$L = -\big[\alpha\cdot y\log\hat{y} + (1-y)\log(1-\hat{y})\big]$
### 2：多分类交叉熵 CE / CrossEntropyLoss
适用：C 个类别，输出层 Softmax，输出各类别概率和为 1。

独热标签：真实分布 $y_i$，只有正确类别为 1，其余为 0。

模型输出每个类概率 $\hat{y}_i$，$\sum_{i=1}^C \hat{y}_i=1$。

单样本损失：
$L = -\sum_{i=1}^C y_i \log \hat{y}_i$
因为标签是独热，仅正确类别项保留，简化为：

$L = -\log(\hat{y}_{\text{正确类别}})$

批量损失：

$\mathcal{L} = -\frac{1}{N}\sum_{n=1}^N \sum_{i=1}^C y_{n,i}\log\hat{y}_{n,i}$

举例子 

3 分类，真实标签第 2 类 $y=[0,1,0]$，模型预测概率 $[0.1,0.7,0.2]$

$L = -(0\cdot\log0.1 + 1\cdot\log0.7 + 0\cdot\log0.2) = -\log0.7$

预测正确类别概率越高，损失越小。

### 三、为什么分类不用 MSE，要用交叉熵？
#### 1. MSE 梯度会饱和，训练极慢
以二分类 sigmoid 举例，MSE 损失：

$L=(y-\hat{y})^2$

当预测极度偏离标签（$\hat{y}\approx0,y=1$），sigmoid 梯度接近 0，梯度消失，参数几乎不更新。
#### 2. 交叉熵梯度无饱和，收敛更快
BCE 对网络输出 logit z 的梯度化简后：
$\frac{\partial L}{\partial z} = \hat{y} - y$

梯度仅等于预测与标签差值，和 sigmoid 导数无关，误差大时梯度依然很大，快速修正模型。
#### 3. 概率分布匹配天然适配分类任务
Softmax 输出合法概率分布，交叉熵直接衡量两个分布差距，数学上匹配分类建模目标。

### 四、PyTorch 两种接口区分（极易混淆）
#### 1. nn.BCELoss
   输入要求：已经经过 sigmoid 的概率值
   ```
   loss_fn = nn.BCELoss()
   z = torch.tensor([2.1, -1.3])
   y_pred = torch.sigmoid(z)  # 手动sigmoid
   y_true = torch.tensor([1., 0.])
   loss = loss_fn(y_pred, y_true)
   ```
#### 2. nn.BCEWithLogitsLoss（推荐，数值更稳定）
   内部自带 sigmoid，直接输入网络原始 logit，避免单独 sigmoid 造成数值溢出
   ```
   loss_fn = nn.BCEWithLogitsLoss()
   z = torch.tensor([2.1, -1.3]) # 原始输出，不用sigmoid
   y_true = torch.tensor([1., 0.])
   loss = loss_fn(z, y_true)
   ```
#### 3. nn.CrossEntropyLoss（多分类标准）
   内部自动做 Softmax，输入原始 logit；标签不用独热，直接传类别索引
   ```
   loss_fn = nn.CrossEntropyLoss()
   logits = torch.tensor([[1.2,3.5,0.4], [2.1,0.5,1.1]]) # [batch, num_class]
   labels = torch.tensor([1,0]) # 类别下标
   loss = loss_fn(logits, labels)
   ```
   
