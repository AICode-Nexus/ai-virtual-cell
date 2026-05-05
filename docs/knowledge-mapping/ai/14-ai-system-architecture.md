# AI系统架构 (AI System Architecture)

> 分布式训练、推理优化、资源调度、模型服务化、容错与可靠性、MLOps

## 1. 领域概述

AI系统架构关注如何高效、可靠地训练和部署大规模AI模型，核心挑战在于：

- **计算规模**：大模型训练需要数千GPU协同工作，通信和同步开销成为瓶颈。
- **推理延迟**：生产环境要求低延迟响应，需要模型压缩和推理优化。
- **资源效率**：GPU利用率、内存带宽、网络带宽的联合优化。
- **可靠性**：长时间训练中的故障恢复，生产推理的高可用性。

---

## 2. 核心架构/算法

### 2.1 分布式训练（Distributed Training）

- **数据并行（Data Parallelism）**：每个设备持有完整模型副本，处理不同数据批次，梯度同步后更新；AllReduce是核心通信原语。
- **张量并行（Tensor Parallelism）**：将单个层的权重矩阵分割到多个设备，适合超大矩阵运算（Megatron-LM）。
- **流水线并行（Pipeline Parallelism）**：将模型层分割到不同设备，通过微批次流水线减少气泡（GPipe、PipeDream）。
- **专家并行（Expert Parallelism）**：MoE模型中不同专家分布在不同设备，通过All-to-All路由。
- **3D并行**：数据+张量+流水线并行联合使用，是训练万亿参数模型的标准方案。
- **ZeRO优化**：将优化器状态、梯度、参数分片到不同设备，显著降低单设备内存需求（DeepSpeed）。

### 2.2 推理优化（Inference Optimization）

- **量化（Quantization）**：将浮点权重压缩为低比特整数（INT8、INT4），减少内存和计算；训练后量化（PTQ）和量化感知训练（QAT）。
- **剪枝（Pruning）**：移除不重要的权重或结构，减少模型大小和计算量；非结构化剪枝和结构化剪枝。
- **知识蒸馏（Knowledge Distillation）**：用大模型（教师）指导小模型（学生）训练，保留性能同时减小规模。
- **FlashAttention**：通过IO感知的注意力计算，减少HBM读写次数，显著提升注意力计算速度和内存效率。
- **KV Cache管理**：自回归推理中缓存历史键值，PagedAttention（vLLM）通过分页管理KV cache，提升吞吐量。
- **投机采样（Speculative Decoding）**：用小模型快速生成候选token，大模型并行验证，提升自回归生成速度。

### 2.3 资源调度（Resource Scheduling）

- **GPU集群调度**：Kubernetes+GPU插件、YARN、Slurm等调度框架，管理GPU资源分配和作业队列。
- **弹性训练**：支持训练过程中动态增减节点，提升集群利用率（Elastic Horovod、PyTorch Elastic）。
- **异构计算**：CPU+GPU+专用加速器（TPU、NPU）的协同调度，充分利用不同硬件特性。
- **内存管理**：梯度检查点（Gradient Checkpointing）以重计算换内存，激活重计算策略。
- **通信优化**：梯度压缩、重叠计算与通信、NCCL/RCCL通信库优化。

### 2.4 模型服务化（Model Serving）

- **推理服务框架**：TorchServe、Triton Inference Server、TensorFlow Serving，支持多模型管理和动态批处理。
- **动态批处理（Dynamic Batching）**：将多个请求合并为一个批次处理，提升GPU利用率。
- **模型版本管理**：支持多版本模型并行部署，A/B测试和灰度发布。
- **自动扩缩容**：基于请求量动态调整推理实例数，平衡成本和延迟。
- **边缘部署**：模型压缩后部署到移动设备或边缘服务器，需要考虑内存、算力和功耗约束。

### 2.5 容错与可靠性（Fault Tolerance and Reliability）

- **检查点保存**：定期保存训练状态，故障后从最近检查点恢复，减少重训成本。
- **弹性容错**：检测节点故障后自动重启或替换，训练继续进行（Torch Elastic）。
- **梯度累积**：在内存不足时通过多步累积梯度模拟大批量训练。
- **混合精度训练**：FP16/BF16计算+FP32主权重，平衡速度、内存和数值稳定性。
- **监控与告警**：训练损失、GPU利用率、内存使用、通信带宽的实时监控。

### 2.6 MLOps与生产化（MLOps）

- **实验追踪**：MLflow、Weights & Biases记录超参数、指标、模型版本，支持实验对比。
- **数据版本管理**：DVC管理数据集版本，确保实验可复现。
- **CI/CD for ML**：自动化模型训练、评估、部署流水线，确保模型质量。
- **特征存储（Feature Store）**：统一管理特征计算和存储，避免训练-服务特征不一致。
- **模型监控**：生产环境中监控数据漂移、模型性能退化，触发重训练。

---

## 3. 训练或优化机制

- **混合精度训练**：FP16前向/反向传播+FP32主权重，损失缩放防止梯度下溢。
- **梯度检查点**：只保存部分激活值，反向传播时重计算，以时间换空间。
- **梯度累积**：多步小批量梯度累积后更新，模拟大批量训练效果。
- **学习率预热**：训练初期小学习率避免不稳定，逐步增大到目标学习率。
- **通信-计算重叠**：在反向传播计算的同时异步传输已完成层的梯度，隐藏通信延迟。

---

## 4. 优点、边界与常见失败模式

### 4.1 主要优点

- **规模扩展**：分布式训练使训练万亿参数模型成为可能。
- **推理效率**：量化、蒸馏等技术使大模型在资源受限环境部署成为可能。
- **生产可靠性**：容错机制和MLOps流程保障生产环境的稳定性。

### 4.2 共性边界

- **通信瓶颈**：大规模分布式训练中通信开销可能超过计算开销。
- **工程复杂度**：分布式系统调试困难，故障定位复杂。
- **硬件依赖**：高性能训练依赖特定硬件（A100/H100），成本高昂。

### 4.3 典型失败模式

- **通信死锁**：分布式训练中不当的同步操作导致死锁。
- **内存溢出**：批量大小或模型规模超出GPU内存，需要调整并行策略。
- **数值不稳定**：混合精度训练中梯度下溢或上溢，需要损失缩放。
- **训练-服务不一致**：特征处理或预处理逻辑在训练和服务时不一致。
- **模型退化**：生产环境数据漂移导致模型性能下降，需要监控和重训练。

---

## 5. 与其他AI领域的交叉关系

- **与深度神经网络架构**：架构设计影响并行策略选择，MoE需要专家并行。
- **与联邦学习**：联邦学习是分布式训练的隐私保护变体，共享通信优化技术。
- **与神经形态计算**：神经形态硬件需要专门的系统软件栈和调度策略。
- **与安全对齐**：模型服务化需要考虑安全过滤和内容审核的系统集成。

---

## 6. 代表性系统或论文方向

- **分布式训练框架**：PyTorch DDP、DeepSpeed、Megatron-LM、Horovod。
- **推理优化**：FlashAttention（Dao 2022）、vLLM（Kwon 2023）、TensorRT。
- **调度系统**：Kubernetes、YARN、Slurm、Volcano（GPU调度）。
- **MLOps工具**：MLflow、Weights & Biases、Kubeflow、Airflow。
- **模型服务**：Triton Inference Server、TorchServe、Ray Serve。

---

## 7. 技术要点速览（机制级）

1. 数据并行通过AllReduce同步梯度，是最常用的分布式训练方式。
2. 张量并行将权重矩阵分割到多设备，适合超大矩阵运算。
3. 流水线并行通过微批次减少气泡，提升设备利用率。
4. ZeRO将优化器状态分片，显著降低单设备内存需求。
5. 3D并行联合使用三种并行方式，是训练超大模型的标准方案。
6. 量化将浮点权重压缩为低比特，减少内存和计算。
7. FlashAttention通过IO感知计算显著提升注意力效率。
8. KV Cache管理是自回归推理吞吐量的关键。
9. 投机采样通过小模型预测+大模型验证加速生成。
10. 动态批处理将多请求合并，提升GPU利用率。
11. 梯度检查点以重计算换内存，支持更大批量训练。
12. 混合精度训练平衡速度、内存和数值稳定性。
13. 通信-计算重叠隐藏分布式训练的通信延迟。
14. 弹性训练支持动态增减节点，提升集群利用率。
15. 检查点保存是长时间训练容错的基础。
16. 特征存储避免训练-服务特征不一致。
17. 模型监控检测生产环境数据漂移和性能退化。
18. CI/CD for ML自动化模型训练和部署流水线。
19. 边缘部署需要模型压缩和专用推理引擎。
20. 通信瓶颈是大规模分布式训练的主要性能限制。

---

## 8. 参考来源

### A类证据（权威综述/教材/官方）

- Shoeybi, M., et al. (2019). Megatron-LM: Training Multi-Billion Parameter Language Models Using Model Parallelism. *arXiv:1909.08053*.
- Rajbhandari, S., et al. (2020). ZeRO: Memory Optimizations Toward Training Trillion Parameter Models (DeepSpeed). *SC 2020*.
- NVIDIA. *Triton Inference Server Documentation*. https://docs.nvidia.com/deeplearning/triton-inference-server/

### B类证据（代表性论文）

- Dao, T., et al. (2022). FlashAttention: Fast and Memory-Efficient Exact Attention with IO-Awareness. *NeurIPS 2022*.
- Kwon, W., et al. (2023). Efficient Memory Management for Large Language Model Serving with PagedAttention (vLLM). *SOSP 2023*.
- Huang, Y., et al. (2019). GPipe: Efficient Training of Giant Neural Networks using Pipeline Parallelism. *NeurIPS 2019*.

### 官方技术文档

- PyTorch Distributed: https://pytorch.org/docs/stable/distributed.html
- DeepSpeed: https://www.deepspeed.ai/
- Ray: https://docs.ray.io/
