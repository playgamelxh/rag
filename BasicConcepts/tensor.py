import torch
import numpy as np

if __name__ == '__main__':
    # 1. 创建 Tensor
    # # 1.1 从列表创建
    # t1 = torch.tensor([1,2,3])
    # t2 = torch.tensor([[1,2],[3,4]])
    # # 1.2 特殊矩阵
    # zeros = torch.zeros(3,4)       # 3行4列全0
    # ones = torch.ones(2,5)         # 全1
    # rand = torch.rand(3,3)         # [0,1)均匀随机
    # randn = torch.randn(2,2)       # 标准正态分布 N(0,1)
    # eye = torch.eye(4)             # 单位方阵
    # arange = torch.arange(0,10,2)  # 0,2,4,6,8
    # # 1.3 从 numpy 互转
    # arr = np.array([1,2,3])
    # t = torch.from_numpy(arr)
    # arr2 = t.numpy()
    # # 1.4 指定设备
    # t_gpu = torch.tensor([1,2], device="cuda")
    # t_cpu = torch.tensor([1,2]).cpu()
    # # 1.5 指定数据类型
    # t_float = torch.tensor([1,2], dtype=torch.float32)
    # t_long = torch.tensor([1,2], dtype=torch.long)

    # # 2. 形状 / 维度操作（最常用）
    # # 2.1 查看维度信息
    # t = torch.rand(3,4, 3)
    # print(t.shape)
    # print(t.size())
    # print(t.dim())
    # print(t.numel())
    # # 2.2 变形reshape/view
    # t = torch.rand(2,6)    
    # print(t)
    # print(t.view(3, 4))
    # print(t.reshape(4, -1)) # -1 自动适配
    # # 2.3 维度交换、转置
    # t = torch.rand(2,3)
    # print(t)
    # t_t = t.t()
    # print(t_t)
    # t1 = torch.rand(2,3,4)
    # print(t1)
    # t2 = t1.permute(2,0,1) # 2,3,4 -> 4,2,3; 2,0,1 代表了维度的交换顺序
    # print(t2)
    # # 2.4 4 增减维度 squeeze /unsqueeze
    # t = torch.rand(3)
    # print("t:",t)
    # t1 = t.unsqueeze(0)   # 增加第0维 (1,3)
    # print("t1:",t1)
    # t2 = t.unsqueeze(1)   # (3,1)
    # print("t2:",t2)
    # t3 = torch.rand(1,3,1)
    # print("t3:",t3)
    # t4 = t3.squeeze()     # 删掉所有长度为1的维度 → (3)
    # print("t4:", t4)
    # t5 = t3.squeeze(0)    # 只删第0维
    # print("t5:", t5)
    # # 2.5. 复制、拼接、拆分
    # # 拼接 cat（维度不变）
    # a = torch.rand(2,3)
    # b = torch.rand(2,3)
    # c = torch.cat([a,b], dim=0) # 按行拼 (4,3)
    # d = torch.cat([a,b], dim=1) # 按列拼 (2,6)
    # # 堆叠 stack（新增维度）
    # e = torch.stack([a,b], dim=0) # (2,2,3)
    # # 拆分 chunk / split
    # t = torch.rand(6,3)
    # parts = t.chunk(3, dim=0) # 均分3份

    # # 3. 索引与切片（和 numpy 几乎一致）
    # t = torch.rand(4,5)
    # print(t[0])                # 第0行
    # print(t[:,0])              # 所有行第0列
    # print(t[1:3, 2:4])         # 行1~2，列2~3
    # t[t>0.5]                   # 布尔索引，取出大于0.5的所有元素
    # t[[0,2],[1,3]]             # 高级索引：(0,1)、(2,3)两个点

    # # 4. 数学运算
    # # 4.1 逐元素四则运算
    # a = torch.tensor([1,2,3])
    # b = torch.tensor([4,5,6])
    # print(a + b)
    # print(a - b)
    # print(a * b) # 逐元素乘 Hadamard
    # print(a / b)
    # print(a ** 2)# 平方
    # print(a % 2) # 取余
    # # 4.2 矩阵乘法（重点区分）
    # A = torch.rand(2,3)
    # B = torch.rand(3,4)
    # C = A @ B               # 矩阵相乘 等价 torch.mm(A,B)
    # D = torch.matmul(A,B)   # 逐元素乘：A * B
    # # 4.3 常用数学函数
    # t = torch.tensor([-1, 0, 1.5])
    # torch.abs(t)       # 绝对值
    # torch.exp(t)       # e^x
    # torch.log(torch.abs(t)+1e-6) # 对数
    # torch.sqrt(torch.abs(t))
    # torch.sin(t), torch.cos(t)
    # torch.clamp(t, min=0, max=1) # 限制区间 [0,1]
    # # 4.4 聚合运算（求和、均值、最大最小）
    # t = torch.rand(2,3)
    # t.sum()         # 全部元素求和
    # t.sum(dim=0)    # 按列求和
    # t.sum(dim=1)    # 按行求和
    # t.mean(dim=0)   # 均值
    # print(t)
    # print(t.max(dim=1))    # 每行最大值 + 索引
    # print(t.min())         # 最小值
    # print(t.argmax(dim=1)) # 返回最大值索引
    # print(t.argmin())      # 返回最小值索引

    # # 5. 设备与梯度相关（深度学习核心）
    # # 5.1 设备切换 cpu /cuda
    # t = torch.rand(3,3)
    # t_gpu = t.cuda()    # 移到GPU
    # t_cpu = t_gpu.cpu() # 移回CPU
    # t2 = t.to("cuda")
    # 5.2 梯度 requires_grad
    # # 开启梯度跟踪
    # x = torch.tensor([1.0,2.0], requires_grad=True)
    # print(x)
    # y = x.sum()
    # print(y)
    # y.backward()        # 反向求梯度
    # print(x.grad)       # 输出梯度
    # # 关闭梯度（推理常用）
    # with torch.no_grad():
    #     out = x * 2
    #     print(out)
    # # 5.3 分离梯度、复制
    # x.detach()      # 断开计算图，无梯度
    # x.clone()       # 深拷贝，独立内存
    # x.data          # 旧写法取数值，推荐detach()

    # # 6. 布尔、比较操作
    # t = torch.tensor([1,2,3])
    # print(t)
    # mask = t > 2        # tensor([False, False, True])
    # print(mask)
    # print(t[mask])             # 筛选满足条件元素
    # print(torch.where(mask, torch.ones_like(t), t)) # 条件赋值
    # print(torch.eq(t, 2))      # ==
    # print(torch.ne(t, 2))      # !=
    # print(torch.lt(t, 2))      # <
    # print(torch.gt(t, 2))      # >

    # # 7. 内存与原地操作
    # t = torch.tensor([1,2])
    # print(t)
    # print(t.add_(5)) # t +=5
    # print(t.mul_(2)) # t *=2

    # 8. 高频易错点总结
    # 8.1 * 是逐元素乘；@ / matmul 才是矩阵乘法；
    # 8.2 view 需要连续内存，不连续用 reshape()；
    # 8.3 梯度计算仅对 float 有效，long/int 无法求导；
    # 8.4 CPU Tensor 和 CUDA Tensor 不能直接运算，必须统一设备；
    # 8.5 squeeze() 只会删掉维度长度 = 1 的轴，不会删正常维度；
    # 8.6 cat 不新增维度，stack 一定会新增一维。
