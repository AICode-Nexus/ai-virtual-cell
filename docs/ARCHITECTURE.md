# AI Virtual Cell：系统架构详解

## 1. 架构总览

### 1.1 七层架构模型

```
┌─────────────────────────────────────────────────────────┐
│  Layer 7: Ecosystem (生态系统)                           │
│  多个 Organism 的群落，竞争与协作，共同进化               │
├─────────────────────────────────────────────────────────┤
│  Layer 6: Organism (生命体)                              │
│  完整智能体，含神经系统、内分泌系统、免疫系统             │
├─────────────────────────────────────────────────────────┤
│  Layer 5: Organ (器官)                                   │
│  多组织协同，实现复杂功能（大脑、感觉器官等）             │
├─────────────────────────────────────────────────────────┤
│  Layer 4: Tissue (组织)                                  │
│  同类细胞集合，专业化功能（感知、推理、记忆等）           │
├─────────────────────────────────────────────────────────┤
│  Layer 3: Cell Network (细胞网络)                        │
│  细胞间连接（突触），信号传递，网络拓扑                   │
├─────────────────────────────────────────────────────────┤
│  Layer 2: Cell (细胞)                                    │
│  基础计算单元，含基因组 + 细胞器 + 状态 + 生命周期       │
├─────────────────────────────────────────────────────────┤
│  Layer 1: Molecular (分子)                               │
│  Skill(基因), Agent(RNA), Function(蛋白质), MCP Tool(酶) │
└─────────────────────────────────────────────────────────┘
```

### 1.2 设计原则

- **去中心化**：无全局控制器，通过局部交互产生全局行为
- **自组织**：细胞自主决定分裂、分化、凋亡
- **异步通讯**：细胞间通过信号分子异步通讯
- **动态拓扑**：网络结构随学习和适应持续变化

---

## 2. Cell 内部架构

### 2.1 组件关系图

```
                    ┌──────────────┐
                    │   Membrane   │ ← 输入/输出控制
                    │ (API Gateway)│
                    └──────┬───────┘
                           │
              ┌────────────┼────────────┐
              │            │            │
    ┌─────────▼──┐  ┌──────▼─────┐  ┌──▼──────────┐
    │  Receptors │  │  Nucleus   │  │  Secretion  │
    │ (消息接收) │  │ (基因调控) │  │  (信号分泌) │
    └─────────┬──┘  └──────┬─────┘  └─────────────┘
              │            │
              │     ┌──────▼─────┐
              │     │  Ribosome  │ ← Skill → Agent 实例化
              │     │ (Agent工厂)│
              │     └──────┬─────┘
              │            │
              │     ┌──────▼──────────┐
              └────►│  Endoplasmic    │ ← 内部消息路由
                    │  Reticulum (ER) │
                    └──────┬──────────┘
                           │
                    ┌──────▼─────┐
                    │Mitochondria│ ← 算力分配
                    │ (算力管理) │
                    └────────────┘
```

### 2.2 生命周期状态机

```
                    ┌─────────┐
                    │  Birth  │
                    └────┬────┘
                         │
                    ┌────▼────┐
              ┌────►│  Active │◄────┐
              │     └────┬────┘     │
              │          │          │
         ┌────┴───┐ ┌───▼────┐ ┌───┴─────┐
         │Dividing│ │Learning│ │Signaling│
         └────┬───┘ └───┬────┘ └───┬─────┘
              │         │          │
              └────►┌───▼──┐◄─────┘
                    │Active│
                    └───┬──┘
                        │ (health < threshold)
                    ┌───▼──────┐
                    │ Apoptosis│
                    └───┬──────┘
                        │
                    ┌───▼──┐
                    │ Dead │
                    └──────┘
```

### 2.3 核心接口定义

```typescript
// Cell 公共接口
interface IAICell {
  // 生命周期
  live(): Promise<void>;
  mitosis(): Promise<IAICell>;
  differentiate(type: string): Promise<IAICell>;
  apoptosis(): Promise<void>;

  // 信号处理
  receiveSignal(signal: Signal): void;
  secreteSignal(signal: Signal): void;

  // 学习
  learn(experience: Experience): Promise<void>;
  consolidateMemory(): Promise<void>;

  // 状态查询
  getState(): CellState;
  getHealth(): number;
  getEnergy(): number;
}

// 细胞器接口
interface IMitochondria {
  produceATP(): Promise<number>;
  allocate(task: Task): ComputeBudget;
  getEnergyLevel(): number;
}

interface IRibosome {
  translate(skill: Skill): Agent;
  getActiveAgents(): Agent[];
}

interface IMembrane {
  receive(input: any): Signal;
  secrete(output: any): void;
  filter(signal: Signal): boolean;
}
```

---

## 3. Synapse 架构

### 3.1 突触可塑性模型

```
信号传递流程：

Pre-synaptic Cell                Post-synaptic Cell
      │                                │
      │  ──── Signal ────►             │
      │       × weight                 │
      │       × (1 - delay)            │
      │                                │
      │  ◄─── Feedback ───            │
      │                                │

可塑性规则：

1. 短期增强 (STP)
   - 触发条件：两次激活间隔 < 1s
   - 效果：weight 临时增加
   - 持续时间：秒级

2. 长时程增强 (LTP)
   - 触发条件：累计激活 > 100 次
   - 效果：weight 永久增加
   - 伴随结构变化：髓鞘化、受体密度增加

3. 长时程抑制 (LTD)
   - 触发条件：长时间未激活 (> 60s)
   - 效果：weight 逐渐降低
   - 最终可能触发突触修剪

4. 突触修剪
   - 触发条件：weight < 0.1
   - 效果：连接被删除
   - 释放资源
```

### 3.2 突触接口

```typescript
interface ISynapse {
  transmit(signal: Signal): Promise<void>;
  getWeight(): number;
  getDelay(): number;
  getMyelination(): number;

  // 可塑性
  potentiate(amount: number): void;   // 增强
  depress(amount: number): void;      // 抑制
  consolidate(): Promise<void>;       // 巩固
  prune(): Promise<void>;             // 修剪
}
```

---

## 4. Tissue 架构

### 4.1 组织类型

```
┌──────────────────────────────────────────────────┐
│                  Tissue Types                    │
├──────────────┬───────────────────────────────────┤
│ Perception   │ 感知组织：处理输入（文本/图像/音频）│
│ Reasoning    │ 推理组织：逻辑推理、规划、决策      │
│ Memory       │ 记忆组织：信息存储和检索            │
│ Motor        │ 运动组织：生成输出（文本/代码/动作） │
│ Immune       │ 免疫组织：错误检测、异常处理、修复   │
└──────────────┴───────────────────────────────────┘
```

### 4.2 组织内部结构

```
Tissue
├── Cell Population (细胞群)
│   ├── Active Cells
│   ├── Stem Cells (干细胞，用于神经发生)
│   └── Population Control (数量调控)
│
├── Synapse Network (突触网络)
│   ├── Internal Connections (组织内连接)
│   ├── External Connections (组织间连接)
│   └── Topology Manager (拓扑管理)
│
├── Extracellular Matrix (细胞外基质)
│   ├── Shared Memory (共享内存)
│   └── Signal Molecules (信号分子池)
│
├── Neurogenesis System (神经发生系统)
│   ├── Trigger Detection (触发检测)
│   ├── Cell Generation (细胞生成)
│   └── Integration (新细胞整合)
│
└── Maintenance System (维护系统)
    ├── Dead Cell Cleanup (死细胞清理)
    ├── Population Balance (数量平衡)
    └── Connection Optimization (连接优化)
```

---

## 5. Organ 架构

### 5.1 器官组成

```
Brain (大脑)
├── Perception Tissue (感知组织)
├── Reasoning Tissue (推理组织)
├── Memory Tissue (记忆组织)
│   ├── Hippocampus (海马体 - 短期记忆)
│   └── Cortex (皮层 - 长期记忆)
└── Motor Tissue (运动组织)

Sensory Organ (感觉器官)
├── Visual Tissue (视觉组织)
├── Auditory Tissue (听觉组织)
└── Text Tissue (文本理解组织)

Executive Organ (执行器官)
├── Text Generation Tissue
├── Code Generation Tissue
└── Action Execution Tissue
```

### 5.2 器官间通讯

```
Sensory Organ ──信号──► Brain ──指令──► Executive Organ
      ▲                  │                    │
      │                  ▼                    │
      │            Memory System              │
      │                  │                    │
      └──────── 反馈 ────┴──── 结果 ──────────┘
```

---

## 6. Organism 架构

### 6.1 系统级组件

```
Organism
├── Organs
│   ├── Brain
│   ├── Sensory
│   ├── Executive
│   └── Metabolic
│
├── Nervous System (神经系统)
│   ├── Central: 全局协调
│   └── Peripheral: 局部反射
│
├── Endocrine System (内分泌系统)
│   ├── Growth Signals: 控制细胞增殖
│   ├── Stress Signals: 应激响应
│   └── Homeostasis Signals: 稳态维持
│
├── Immune System (免疫系统)
│   ├── Error Detection: 异常检测
│   ├── Error Recovery: 错误恢复
│   └── Adaptation: 免疫记忆
│
└── Circulatory System (循环系统)
    ├── Message Network: 消息传递
    └── Resource Distribution: 资源分配
```

---

## 7. 技术栈架构

```
┌─────────────────────────────────────────────┐
│         Visualization Layer                 │
│  React + D3.js + WebSocket                  │
├─────────────────────────────────────────────┤
│         Runtime Core (TypeScript)           │
│  Cell Lifecycle | Message Bus | Scheduler   │
├─────────────────────────────────────────────┤
│         AI Modules (Python)                 │
│  LLM Interface | Embeddings | Reasoning     │
├─────────────────────────────────────────────┤
│         MCP Tools (TypeScript)              │
│  File System | Web Search | Code Execution  │
├─────────────────────────────────────────────┤
│         Persistence Layer                   │
│  SQLite | LevelDB | JSON Files              │
└─────────────────────────────────────────────┘
```
