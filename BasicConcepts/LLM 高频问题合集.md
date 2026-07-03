# 算法 + ML/DL/LLM 高频面试题合集（分模块，含名词解释 + 核心问答）
## 一、数据结构与算法高频（笔试 / 一面必考）
### 名词解释
* 时间复杂度 Time Complexity：衡量算法运行耗时随输入规模增长的变化趋势，忽略常数、低阶项，用 O 标记。
* 空间复杂度 Space Complexity：算法执行占用内存大小的增长量级，分额外空间、输入空间。
* 动态规划 Dynamic Programming (DP)：拆分重复子问题，存储子问题解避免重复计算，核心：最优子结构、重叠子问题。
* 贪心算法 Greedy：每一步取局部最优，期望全局最优，仅适用于具备贪心选择性质的场景。
* 二分查找 Binary Search：有序数组中不断折半缩小搜索区间，时间复杂度 O (logn)。
* 哈希表 Hash Table：通过哈希函数映射键值，平均增删查 O (1)，存在哈希碰撞。
* 栈 Stack：后进先出 LIFO；队列 Queue：先进先出 FIFO。
* 二叉树 Binary Tree：每个节点最多两个子节点；二叉搜索树 BST：左 < 根 < 右；堆 Heap：完全二叉树，分大顶堆 / 小顶堆，用于 TopK、排序。
* 无向图 Undirected Graph：节点 + 边，分为有向 / 无向、加权 / 无权；BFS 广度优先、DFS 深度优先。
* 滑动窗口 Sliding Window：双指针维护区间，解决连续子数组最值、求和类问题。
### 高频问答
* 快速排序、归并排序、堆排序原理、复杂度、稳定性对比？
* 哈希碰撞如何解决？拉链法 / 开放寻址法优劣？
* TopK 问题三种解法：快排分区、堆、计数排序适用场景？
* 二叉树层序、前中后序遍历（递归 + 迭代实现）？
* DP 经典题型：背包、最长递增子序列、编辑距离、打家劫舍思路？
* LRU 缓存实现原理，双向链表 + 哈希表？
* 如何判断链表有环，找环入口？快慢指针法。
## 二、机器学习 ML 基础高频
### 名词解释
* 张量 Tensor：0 阶标量、1 阶向量、2 阶矩阵、高维多维数组；深度学习计算基础单元，支持自动微分、GPU 加速。
* 损失函数 Loss Function：衡量模型预测值与真实标签差距，指导参数更新。
* 梯度下降 Gradient Descent：沿损失函数梯度反方向迭代更新权重，最小化损失。
* 过拟合 Overfitting：模型记住训练集噪声，泛化能力差；欠拟合 Underfitting：模型复杂度不足，训练集效果差。
* 正则化 Regularization：约束权重降低过拟合，L1（产生稀疏权重）、L2（权重衰减）。
* 偏差 Bias / 方差 Variance：偏差代表拟合能力，方差代表数据扰动带来波动；权衡 Bias-Variance Tradeoff。
* 梯度消失 / 爆炸 Vanishing/Exploding Gradient：深层网络反向传播梯度极小 / 极大，参数无法有效更新。
* 归一化 Normalization / 标准化 Standardization：缩放特征消除量纲，加速梯度收敛。
* 交叉验证 Cross Validation：划分多组训练 / 验证集，客观评估模型泛化能力。
* 混淆矩阵 Confusion Matrix：TP/TN/FP/FN，计算精确率 Precision、召回率 Recall、F1、准确率 Accuracy。
### 高频问答
* 逻辑回归损失为什么用交叉熵，不用 MSE？
* 随机森林、XGBoost、LightGBM 核心区别、优缺点？
* 如何处理类别不平衡样本？上采样、下采样、加权损失、Focal loss。
* 特征筛选方法：方差筛选、皮尔逊相关、树模型特征重要性？
* K-means 聚类流程、K 值选择方法、优缺点？
* PCA 主成分分析作用、计算流程，PCA 与 LDA 区别？
* 梯度下降变体：SGD、Mini-batch、Adam、RMSprop 原理与适用场景？
* 如何判断模型过拟合，对应解决手段？
## 三、深度学习 DL 核心高频
### 名词解释
* 神经网络激活函数 Activation：引入非线性，Sigmoid、Tanh、ReLU、LeakyReLU、GELU。
* 卷积层 Conv2d：滑动卷积核提取局部空间特征，权重共享减少参数量。
* 池化层 Pooling：下采样降维度，最大池化 MaxPool、平均池化 AvgPool。
* BatchNorm 批量归一化：每层输入标准化，缓解梯度消失、加速训练、轻微正则。
* Dropout：训练随机丢弃神经元，防止神经元共适应，抑制过拟合。
* 感受野 Receptive Field：输出特征图单个像素映射回原图的区域。
* 残差连接 Residual Connection：ResNet 核心，跨层直连解决深层网络梯度消失。
* 多头注意力 Multi-Head Attention：拆分多组注意力并行捕捉不同维度依赖。
* 反向传播 Backpropagation：链式求导逐层计算梯度，更新网络全部参数。
* Epoch/Batch/Iteration：Epoch 全部数据集遍历一轮；Batch 单次输入样本数；Iteration 一轮批次迭代。
### 高频问答
* ReLU 相比 Sigmoid 优势，ReLU 存在什么问题，如何解决？
* 卷积神经网络 CNN 相比全连接网络优势？
* ResNet 残差结构为什么能解决深层网络难训练问题？
* BatchNorm 放在卷积前还是后，推理时如何使用？
* 转置卷积、空洞卷积作用，各自适用场景？
* 池化层缺点，有哪些无池化替代方案？
* 训练 loss 下降、验证 loss 上升是什么问题，怎么处理？
## 四、大模型 LLM 专项高频（算法岗必考）
### 名词解释
* Transformer：基于自注意力机制的基础架构，所有 LLM 统一底座，编码器 Encoder、解码器 Decoder。
* 自注意力 Self-Attention：序列内部元素互相计算相似度，捕捉长距离依赖。
* 位置编码 Positional Encoding：为序列注入时序位置信息，区分词语先后顺序。
* 上下文窗口 Context Window：模型单次可处理的最大输入 + 输出 token 长度。
* Tokenizer 分词器 Tokenizer：文本转模型可计算的 token ID，分为 BPE、WordPiece、SentencePiece。
* 预训练 Pre-training：海量无标注文本学习通用语言知识；微调 Fine-tune：下游任务有标注数据适配。
* SFT 有监督微调：使用高质量人工对话数据微调基座模型，对齐人类指令。
* RLHF 基于人类反馈强化学习：奖励模型 RM 打分，PPO 优化模型输出贴合人类偏好。
* 上下文学习 ICL：仅输入少量示例，不更新权重即可完成任务，大模型涌现能力。
* KV 缓存 KV Cache：缓存历史注意力 key/value，推理时重复利用，大幅降低生成显存开销、提速。
### 高频问答
* Transformer 相比 RNN/LSTM 优势，RNN 无法并行计算根源？
* 自注意力计算复杂度，如何通过稀疏注意力、滑动窗口优化？
* 预训练目标：MLM 掩码语言模型、CLM 自回归语言模型区别，BERT/GPT 架构差异？
* LLM 训练三阶段：预训练、SFT、RLHF 完整流程，每阶段作用？
* 模型推理加速手段：KV 缓存、量化、张量并行、流水线并行原理？
* 大模型常见问题：幻觉、上下文丢失、重复生成，成因与缓解方案？
* 微调方案对比：全量微调、LoRA、QLoRA、Prefix-Tuning 优缺点、显存开销？
* 涌现能力 Emergent Ability：模型规模突破阈值后出现小模型不具备的复杂推理能力。
* 温度系数 Temperature、TopP、TopK 采样参数作用，如何控制生成随机性？
* 多轮对话历史如何拼接输入，长文本窗口膨胀如何优化？
## 五、通用基础概念英文对照表（面试写作直接用）
* 基础概念：fundamental concepts
* 名词解释：term definition
* 张量：Tensor
* 梯度下降：Gradient Descent
* 过拟合：Overfitting
* 残差连接：Residual Connection
* 自注意力：Self-Attention
* 上下文学习：In-Context Learning
* 分词器：Tokenizer
* 批量归一化：Batch Normalization
* 反向传播：Backpropagation
