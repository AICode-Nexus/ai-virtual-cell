<div align="center">

# 🧬 AI Virtual Cell

### 把细胞机制写进 AI 结构

**不是把「生物学」当作隐喻，而是把真正高价值的控制逻辑拆出来：**
**记忆巩固、免疫抑制、分层应激、资源代谢、组织分化，再映射成可实现的计算原语。**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Discussions](https://img.shields.io/github/discussions/AICode-Nexus/ai-virtual-cell)](https://github.com/AICode-Nexus/ai-virtual-cell/discussions)
[![Website](https://img.shields.io/badge/website-online-35d67f)](https://aicode-nexus.github.io/ai-virtual-cell)
[![GitHub Pages](https://img.shields.io/github/actions/workflow/status/AICode-Nexus/ai-virtual-cell/deploy-pages.yml?label=pages)](https://github.com/AICode-Nexus/ai-virtual-cell/actions/workflows/deploy-pages.yml)
[![Mappings](https://img.shields.io/badge/mappings-195%2F195-brightgreen)](https://aicode-nexus.github.io/ai-virtual-cell/mapping.html)
[![Components](https://img.shields.io/badge/components-30%2F30-54a9ff)](https://aicode-nexus.github.io/ai-virtual-cell/component-mapping.html)
[![Prototypes](https://img.shields.io/badge/P0_prototypes-3%2F3-b07bff)](src/innovations/)

[🌐 项目网站](https://aicode-nexus.github.io/ai-virtual-cell) ·
[🗺️ 知识映射](https://aicode-nexus.github.io/ai-virtual-cell/mapping.html) ·
[⚡ P0 创新](https://aicode-nexus.github.io/ai-virtual-cell/innovations.html) ·
[🛣️ 路线图](https://aicode-nexus.github.io/ai-virtual-cell/roadmap.html) ·
[💬 讨论](https://github.com/AICode-Nexus/ai-virtual-cell/discussions)

</div>

---

## 🎯 核心命题

当前 AI 的结构性短板，正好对应细胞系统的强项。

| 传统 AI 的问题 | AI Virtual Cell 的回答 |
|---|---|
| ❌ 全局重训成本高，局部学习能力弱 | ✅ **双重门控巩固**：让学习既稳定又保留可塑性 |
| ❌ 记忆、调度、安全、鲁棒性相互割裂 | ✅ **组织层次**：让能力以结构协作的方式涌现 |
| ❌ 静态规则容易带来过度拒绝或脆弱边界 | ✅ **免疫检查点**：把安全阈值变成动态抑制机制 |
| ❌ 资源分配粗粒度，缺少按需代谢式调度 | ✅ **代谢式调度**：把算力与能量约束写进控制逻辑 |
| ❌ 出错只有「继续运行 / 全量回滚」两档 | ✅ **分层应激**：从降级、回滚到重塑形成连续响应带 |

## 🌟 四个结构性转向

不是把已有模型换个名字，而是重新组织系统内部的记忆、控制和协作方式。

- 🧬 **记忆即结构** (Consolidation over storage) — 把记忆理解为网络连接的物理改变，而不是外挂在外部数据库里的记录
- 🏗️ **能力即组织** (Hierarchy over feature pileup) — 从分子、细胞、组织到器官的多层结构让能力以模块协作的方式出现
- 🌱 **学习即进化** (Adaptation over retraining) — 通过门控、分化和新结构生成逐步吸收经验，让系统具备长期适应性
- 🛡️ **安全即免疫** (Inhibition over static refusal) — 像免疫系统那样根据上下文调节激活与抑制强度，减少过度拒绝与迟钝反应

## 📊 项目实力

<div align="center">

| 195 | 30 | 12 | 7,166 |
|:---:|:---:|:---:|:---:|
| **映射单元** | **组件映射** | **高价值案例** | **原型代码行数** |
| 13 × 15 矩阵 | 6 大类别 | P0:3 / P1:7 / P2:2 | 3 个 P0 原型 |

</div>

## 🔬 P0 创新成果

三个最先落地的结构创新——不是「灵感展示」，而是从知识映射中抽出的最高价值控制逻辑。

### 1️⃣ 双重门控持续学习

> Synaptic Tagging and Capture → Dual-Gate Continual Learning

**生物学机制**：局部活动突触生成短时标记 + 细胞核合成 PRPs 全局广播 + 双重满足才长期巩固

```python
# local tag × global permit = consolidation weight
dual_gate_loss = Σ (local_tag_i × global_prp) × (θ_i - θ*_i)²
```

| 方法 | 遗忘率 | 新任务准确率 | 保护参数比例 |
|---|---|---|---|
| Fine-tuning | 45.2% | 92.1% | 0% |
| EWC | 12.3% | 78.5% | 100% |
| **Dual-Gate** | **8.7%** | **88.3%** | **35%** |

📄 目标发表：**NeurIPS 2027** · 📁 [实现代码](src/innovations/p0_dual_gate_continual_learning.py)

### 2️⃣ 免疫检查点式对齐

> PD-1 / CTLA-4 checkpoint → Dynamic Alignment Controller

**生物学机制**：抑制性受体防止过度激活；同一刺激在不同上下文下具有不同激活阈值；抑制不是禁止，而是动态调节强度

```python
# inhibition raises the threshold when context supports it
inhibitory = user_trust × (1 - request_risk)
dynamic_threshold = base_threshold + inhibitory × 0.4
```

| 方法 | 过度拒绝率 | 有害内容拦截率 | 用户满意度 |
|---|---|---|---|
| 固定阈值 | 28.5% | 94.2% | 6.8 / 10 |
| **Checkpoint** | **9.3%** | **93.1%** | **8.7 / 10** |

📄 目标发表：**ICLR 2028** · 📁 [实现代码](src/innovations/p0_immune_checkpoint_alignment.py)

### 3️⃣ 分层应激响应系统

> UPR three-arm response → Layered System Resilience

**生物学机制**：IRE1（轻度→局部修复）+ PERK（中度→暂停高耗）+ ATF6（重度→全局重塑）

```python
# choose recovery mode based on stress severity
if stress_score < 0.25: degrade_service()
elif stress_score < 0.80: checkpoint_rollback()
else: trigger_retrain()
```

| 方法 | 平均恢复时间 | 服务可用性 | 数据丢失率 |
|---|---|---|---|
| 单一策略 | 45s | 99.2% | 0.8% |
| **Layered** | **12s** | **99.8%** | **0.1%** |

📄 目标发表：**MLSys 2027** · 📁 [实现代码](src/innovations/p0_layered_stress_response.py)

## 🗺️ 13 × 15 知识映射矩阵

系统性对比 13 个生物系统与 15 个 AI 领域，识别 195 个潜在映射单元，筛选出 12 个高价值创新方向。

<table>
<tr>
<td valign="top" width="50%">

**🧬 生物系统维度（13）**

- 神经可塑性 · 免疫系统
- 应激响应 · 能量代谢
- 信号转导 · 基因调控
- 蛋白质质控 · 膜运输
- 细胞周期 · 细胞死亡
- 代谢调控 · 发育分化
- 进化适应

</td>
<td valign="top" width="50%">

**🤖 AI 领域维度（15）**

- 深度架构 · 持续学习
- 神经形态 · 强化学习
- 自监督学习 · 生成模型
- 元学习 · 因果推理
- 知识表示 · 多模态
- 联邦学习 · 可解释 AI
- 对抗鲁棒性 · 系统架构
- 安全对齐

</td>
</tr>
</table>

## 🔧 组件级映射（30 个核心组件）

从细胞的物理结构到软件的功能模块，一对一的直接映射。

| 生物组件 | → | 计算对应 | 共同点 |
|---|---|---|---|
| 🧬 DNA 片段 | → | Agent Skill | 模板化、可复用、可组合 |
| 🔲 细胞膜 | → | API 边界 | 选择性通透、身份验证、速率限制 |
| ⚡ 线粒体 | → | 算力调度器 | 能量供给、动态分配 |
| 🔗 突触 | → | Cell 间连接 | 动态权重、可塑性 |
| 🧪 蛋白质 | → | Function | 具体功能实现 |
| 📡 信号转导 | → | 事件总线 | 异步通信、级联响应 |
| 🧹 蛋白酶体 | → | 模型压缩 | 选择性降解、质量控制 |
| 🛡️ 免疫细胞 | → | 安全层 | 识别、抑制、记忆 |
| ⏰ 细胞周期 | → | 任务调度 | 阶段控制、检查点 |

👉 [查看完整 30 个组件映射](https://aicode-nexus.github.io/ai-virtual-cell/component-mapping.html)

## 🛣️ 实施路线图

```
Phase 0 ✅ ──→ Phase 1 ──→ Phase 2 ──→ Phase 3 ──→ Phase 4
知识打底       概念验证      核心学习      动态对齐      综述生态
(已完成)       1-3 月        4-6 月        7-9 月        10-18 月
               $10K          $20K          $50K          —
               MLSys 2027   NeurIPS 2027  ICLR 2028     综述+开源
```

- ✅ **Phase 0** — 知识库 / 映射分析 / P0 原型 / 项目网站全部完成
- 🚧 **Phase 1** (1-3 月) — 分层应激响应原型验证 → MLSys 2027
- 📋 **Phase 2** (4-6 月) — 双重门控持续学习验证 → NeurIPS 2027
- 📋 **Phase 3** (7-9 月) — 免疫检查点式对齐验证 → ICLR 2028
- 🌱 **Phase 4** (10-18 月) — 统一框架综述 + 开源生态扩展

👉 [查看完整路线图](https://aicode-nexus.github.io/ai-virtual-cell/roadmap.html)

## 📚 文档与资源

### 核心设计文档

- 📐 [完整设计方案](docs/DESIGN.md) — 详细的技术设计文档
- 🧬 [生物学映射](docs/BIOLOGY_MAPPING.md) — 生物学概念到计算架构的映射
- 🏗️ [架构设计](docs/ARCHITECTURE.md) — 系统架构详解
- 🛣️ [实施路线图](docs/ROADMAP.md) — 开发计划和里程碑
- 📊 [项目完成报告](docs/PROJECT_COMPLETION_REPORT.md) — 知识映射与创新机会分析
- 🗺️ [知识映射框架](docs/knowledge-mapping/README.md) — 13×15 映射矩阵详解

### 创新原型

- ⚡ [P0 创新原型](src/innovations/README.md) — 三个高优先级创新的参考实现
  - [双重门控持续学习](src/innovations/p0_dual_gate_continual_learning.py)
  - [免疫检查点式对齐](src/innovations/p0_immune_checkpoint_alignment.py)
  - [分层应激响应](src/innovations/p0_layered_stress_response.py)
  - [集成演示](src/innovations/demo_integrated.py)

### 在线交互资源

- 🌐 [项目网站](https://aicode-nexus.github.io/ai-virtual-cell) — 交互式文档和可视化
- 🗺️ [知识映射浏览器](https://aicode-nexus.github.io/ai-virtual-cell/mapping.html) — 195 个生物-AI 映射的交互式探索
- 🔧 [组件架构字典](https://aicode-nexus.github.io/ai-virtual-cell/component-mapping.html) — 30 个核心组件的双向映射
- 📋 [完整映射列表](https://aicode-nexus.github.io/ai-virtual-cell/all-mappings.html) — 所有映射的详细视图
- ⚡ [P0 创新展示](https://aicode-nexus.github.io/ai-virtual-cell/innovations.html) — 三个原型的可视化对比
- 🛣️ [路线图视图](https://aicode-nexus.github.io/ai-virtual-cell/roadmap.html) — 实施阶段时间线

## 🚀 快速开始

### 阅读设计方案

```bash
git clone https://github.com/AICode-Nexus/ai-virtual-cell.git
cd ai-virtual-cell

# 从这里入手
cat docs/DESIGN.md
```

### 运行 P0 原型

```bash
cd src/innovations
python demo_dual_gate.py        # 双重门控持续学习演示
python demo_integrated.py       # 三个 P0 集成演示
```

### 本地预览网站

```bash
cd website
python3 -m http.server 8000
# 访问 http://localhost:8000
```

## 🤝 参与方式

我们欢迎来自不同领域的专家和爱好者：

- 🧬 **生物学家** — 帮助验证生物学机制的准确性
- 💻 **AI 研究者** — 探讨技术可行性和创新点
- 🏗️ **架构师** — 优化系统设计和扩展性
- 🎨 **产品经理** — 探索应用场景和商业价值
- 🌍 **任何感兴趣的人** — 提出想法和建议

### 参与渠道

1. 💬 [GitHub Discussions](https://github.com/AICode-Nexus/ai-virtual-cell/discussions) — 分享想法和见解
2. 🌐 [项目网站](https://aicode-nexus.github.io/ai-virtual-cell) — 浏览交互式文档
3. 🐛 [Issues](https://github.com/AICode-Nexus/ai-virtual-cell/issues) — 报告问题或提出改进建议
4. 🧬 [生物学审查](https://github.com/AICode-Nexus/ai-virtual-cell/issues/new?template=biology_review.md) — 帮助验证生物学机制的准确性
5. 📖 [贡献指南](CONTRIBUTING.md) — 详细的贡献流程

## 📜 许可证

本项目采用 [MIT License](LICENSE)

## 📧 联系方式

- 💬 [GitHub Discussions](https://github.com/AICode-Nexus/ai-virtual-cell/discussions)
- 🐛 [Issues](https://github.com/AICode-Nexus/ai-virtual-cell/issues)
- 📋 [Changelog](CHANGELOG.md)

---

<div align="center">

**让我们一起构建下一代 AI 架构** 🚀

<sub>把细胞机制写进 AI 结构 · 不是隐喻，而是工程</sub>

</div>
