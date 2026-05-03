# AI Virtual Cell 渐进式架构平台设计规格

**版本**: v1.0
**日期**: 2026-05-03
**状态**: 待实施

---

## 1. 项目概览

### 1.1 目标

构建 **AI Virtual Cell 渐进式架构平台** — 一个基于 Astro + GitHub 的交互式网站，包含：

1. **渐进式架构展示**：将 7 层架构以交互式可视化方式呈现，每层有从概念到代码的完整文档路径
2. **集成讨论社区**：基于 GitHub Discussions API，每个架构模块都有对应讨论区

### 1.2 背景

- 项目处于 Phase 0（设计评审），有完整的设计文档但缺乏交互性
- 需要吸引生物学家、AI 研究者、架构师等不同领域的社区参与
- 现有 `website/index.html` 是静态展示页，讨论依赖外部 GitHub Discussions 链接

### 1.3 成功标准

**MVP（Sprint 1-2，4 周）：**
- 网站上线，展示 Layer 1-2 的交互式架构图
- 用户可点击架构图进入详细文档页
- 集成 GitHub Discussions，用户可在每个模块下讨论
- 收到 10+ 条社区反馈（通过 GitHub Discussions 计数衡量）

**完整版（Sprint 3+）：**
- 7 层架构全部可视化并可交互
- 支持架构视图和路线图视图两种导航
- 每周 5+ 新讨论
- 文档体系完善

---

## 2. 技术架构

### 2.1 技术栈

| 类别 | 选型 | 理由 |
|------|------|------|
| 前端框架 | Astro 4.x | Islands Architecture，默认零 JS，优秀的 Markdown 支持 |
| 交互组件 | React 18 + TypeScript | React Islands 按需加载，生态丰富 |
| 可视化 | React Flow | 节点和连接的交互式架构图 |
| 样式 | Tailwind CSS | 快速开发，响应式设计 |
| 内容 | Astro Content Collections + MDX | 结构化内容管理 |
| 讨论后端 | GitHub Discussions API (GraphQL) | 基于 GitHub 基础设施 |
| 部署 | GitHub Pages + GitHub Actions | 免费，自动 CI/CD |

### 2.2 项目结构

```
ai-virtual-cell/
├── website/                    # Astro 项目
│   ├── src/
│   │   ├── pages/
│   │   │   ├── index.astro            # 首页（架构全景图）
│   │   │   ├── layers/                # 各层详情页
│   │   │   │   ├── molecular.astro
│   │   │   │   ├── cell.astro
│   │   │   │   └── ...
│   │   │   ├── phases/                # 实施阶段页
│   │   │   │   ├── phase-0.astro
│   │   │   │   └── ...
│   │   │   └── discussions.astro      # 讨论区汇总页（所有分类的讨论入口）
│   │   ├── components/
│   │   │   ├── ArchitectureDiagram.tsx # 交互式架构图 (React Island)
│   │   │   ├── LayerCard.astro        # 层级卡片
│   │   │   ├── DiscussionWidget.tsx   # 讨论组件 (React Island)
│   │   │   └── ...
│   │   ├── content/                   # Content Collections
│   │   │   ├── layers/                # 各层架构文档 (Markdown)
│   │   │   ├── phases/                # 实施阶段文档
│   │   │   └── config.ts
│   │   ├── lib/
│   │   │   ├── github-api.ts          # GitHub API 封装
│   │   │   └── ...
│   │   └── styles/
│   ├── public/
│   │   └── diagrams/                  # 架构图 SVG
│   └── astro.config.mjs
├── docs/                              # 现有文档（保留，作为内容源）
└── ...
```

### 2.3 数据流

**构建时（SSG）：**
1. Astro 读取 `src/content/` 下的 Markdown 文档
2. Content Collections 转换为结构化数据
3. 生成静态 HTML 页面
4. 预取 GitHub Discussions 数据写入静态 JSON

**运行时（客户端）：**
1. 用户访问页面，加载静态 HTML（快速首屏）
2. React Islands 按需加载（架构图、讨论组件）
3. 点击架构图节点 → 客户端路由跳转到详情页
4. 讨论组件加载预取的 JSON 数据，点击跳转到 GitHub

---

## 3. 架构可视化设计

### 3.1 首页：7 层架构全景图

垂直层级布局，从下到上：

```
┌─────────────────────────────────────────┐
│  Layer 7: Ecosystem (生态系统)          │ ⚪ Phase 4
├─────────────────────────────────────────┤
│  Layer 6: Organism (生命体)             │ ⚪ Phase 3
├─────────────────────────────────────────┤
│  Layer 5: Organ (器官)                  │ ⚪ Phase 3
├─────────────────────────────────────────┤
│  Layer 4: Tissue (组织)                 │ ⚪ Phase 2
├─────────────────────────────────────────┤
│  Layer 3: Cell Network (细胞网络)       │ ⚪ Phase 2
├─────────────────────────────────────────┤
│  Layer 2: Cell (细胞)                   │ 🟡 Phase 1
├─────────────────────────────────────────┤
│  Layer 1: Molecular (分子)              │ 🟡 Phase 1
└─────────────────────────────────────────┘
```

**交互设计：**
- 每层显示：层级名称、核心概念、实施状态（Phase X）、讨论数量
- Hover：该层的关键组件预览
- 点击：进入该层的详细页面

**实施状态可视化：**
- 🟢 已完成 | 🟡 进行中 | ⚪ 未开始
- 辅助文字标签确保色盲用户可识别

### 3.2 架构图数据模型

Sprint 1（静态 SVG）和 Sprint 2（React Flow）共享同一数据模型：

```typescript
// lib/architecture-data.ts
interface LayerNode {
  id: string;                    // "layer-1"
  label: string;                 // "Molecular"
  labelCn: string;               // "分子"
  phase: number;                 // 1
  status: "completed" | "in_progress" | "not_started";
  components: string[];          // ["Skill", "Agent", "Function", "MCP Tool"]
  discussionCount: number;       // 从构建时预取
  route: string;                 // "/layers/molecular"
}

interface LayerEdge {
  source: string;                // "layer-1"
  target: string;                // "layer-2"
  label?: string;                // "组成"
}

interface ArchitectureGraph {
  nodes: LayerNode[];
  edges: LayerEdge[];
}
```

Sprint 1 用此数据渲染静态 SVG，Sprint 2 直接传入 React Flow，无需重写。

### 3.4 详情页结构

每个层级详情页包含 4 个标签页：

| Tab | 内容 | 数据来源 |
|-----|------|---------|
| 概念设计 | 生物学映射、设计理念、第一性原理 | docs/DESIGN.md, docs/BIOLOGY_MAPPING.md |
| 技术规格 | 接口定义（TypeScript interfaces）、数据结构（CellState, Synapse 等）、状态机图（生命周期）、组件关系图 | 从 docs/ARCHITECTURE.md 提取并补充 |
| 实施路径 | Phase/Milestone、依赖关系、代码示例 | docs/ROADMAP.md |
| 讨论区 | Sprint 1：显示"前往 GitHub 讨论"链接；Sprint 2：嵌入 DiscussionWidget | GitHub API |

### 3.5 导航设计

**双视图导航：**

1. **架构视图（主导航）**：按 7 层架构组织，点击层级进入详情
2. **路线图视图（辅助导航）**：按 Phase 0-4 组织，点击阶段查看该阶段涉及的所有层级

顶部导航栏提供视图切换。

### 3.6 文档渐进细化策略

- **MVP**：Layer 1-2 从现有 docs/ 迁移，补充技术规格
- **后续**：每个 Sprint 完成 1-2 层，根据社区反馈逐步细化
- **同步**：文档和代码保持同步（如果开始实现）

---

## 4. GitHub Discussions 集成

### 4.1 讨论分类

在 GitHub 仓库创建以下分类（GitHub Discussions 分类为扁平结构，不支持嵌套）：

1. **Arch: Layer 1 - Molecular**
2. **Arch: Layer 2 - Cell**
3. **Arch: Layer 3 - Cell Network**
4. **Arch: Layer 4 - Tissue**
5. **Arch: Layer 5 - Organ**
6. **Arch: Layer 6 - Organism**
7. **Arch: Layer 7 - Ecosystem**
8. **Phase 0 - Design Review**
9. **Phase 1 - Prototype**
10. **Phase 2 - Tissue Building**
11. **Ideas**（创新想法）
12. **Q&A**（问答）
13. **Show and Tell**（展示与分享）

MVP 阶段先创建 Layer 1-2、Ideas 和 Q&A 分类，后续按需添加。

### 4.2 API 集成

```typescript
// lib/github-api.ts
interface Discussion {
  id: string;
  title: string;
  body: string;
  author: { login: string; avatarUrl: string };
  createdAt: string;
  comments: { totalCount: number };
  category: { name: string };
  url: string;
}

async function getDiscussionsByCategory(category: string): Promise<Discussion[]>
async function getDiscussion(id: string): Promise<Discussion>
```

### 4.3 认证策略

**MVP：** 只读访问，使用项目 GitHub Token（环境变量），用户点击"参与讨论"跳转到 GitHub
**完整版（可选）：** GitHub OAuth，用户可在网站上直接评论

### 4.4 缓存策略

1. **构建时预取**：`astro build` 时调用 GitHub API，写入静态 JSON
2. **客户端缓存**：localStorage，5 分钟过期
3. **增量更新**：git push 触发 GitHub Actions 重新构建

### 4.5 讨论与架构关联

Content Collections frontmatter 记录关联：

```typescript
// content/config.ts
import { defineCollection, z } from "astro:content";

const layers = defineCollection({
  type: "content",
  schema: z.object({
    title: z.string(),
    titleCn: z.string(),
    layer: z.number().min(1).max(7),
    phase: z.number().min(0).max(4),
    status: z.enum(["completed", "in_progress", "not_started"]),
    components: z.array(z.string()),
    summary: z.string().optional(),       // 用于架构图 Hover 预览
    discussionCategory: z.string().optional(),
    discussionUrl: z.string().url().optional(),
    order: z.number(),
  }),
});

const phases = defineCollection({
  type: "content",
  schema: z.object({
    title: z.string(),
    phase: z.number(),
    status: z.enum(["completed", "in_progress", "not_started"]),
    milestones: z.array(z.object({
      id: z.string(),
      title: z.string(),
      status: z.enum(["completed", "in_progress", "not_started"]),
    })),
  }),
});

export const collections = { layers, phases };
```

---

## 5. 实施计划

### 5.1 Sprint 1：MVP 基础（Week 1-2）

**目标：** 项目框架 + Layer 1-2 基础展示 + 上线

**Week 1：**
- 初始化 Astro 项目（`website/` 目录）
- 配置 Tailwind CSS + TypeScript
- 设置 Content Collections（定义 schema）
- 创建基础页面结构（首页、层级详情页模板）
- 设计 7 层架构全景图（静态版本，CSS + SVG）

**Week 2：**
- 迁移 Layer 1（Molecular）文档到 Content Collections
- 迁移 Layer 2（Cell）文档到 Content Collections
- 实现基础架构图交互（点击跳转）
- 创建层级详情页（概念设计、技术规格、实施路径 3 个 Tab 完整；讨论区 Tab 显示"前往 GitHub 讨论"链接占位）
- 配置 GitHub Pages 部署（GitHub Actions）

**交付：** 可访问的网站，Layer 1-2 文档展示，可点击架构图

### 5.2 Sprint 2：完整功能（Week 3-4）

**目标：** GitHub Discussions 集成 + 交互增强

**Week 3：**
- 实现 GitHub API 封装
- 创建 DiscussionWidget 组件（React Island）
- 在 GitHub 仓库创建 Discussions 分类
- 构建时预取讨论数据
- 在详情页集成讨论组件

**Week 4：**
- 实现 React Flow 架构图（替换静态版本）
- 添加 Hover 效果和动画
- 实现实施状态可视化
- 添加搜索功能（Astro Pagefind — 构建时生成全文索引，客户端搜索，零后端依赖）
- 性能优化（Lighthouse 90+）

**交付：** 完整讨论功能，交互式架构图，搜索功能

### 5.3 Sprint 3+：迭代完善（Week 5+）

**迭代策略：** 每个 Sprint（2 周）完成 1-2 层

- Sprint 3: Layer 3（Cell Network）+ Layer 4（Tissue）
- Sprint 4: Layer 5（Organ）+ Layer 6（Organism）
- Sprint 5: Layer 7（Ecosystem）+ 整体优化

**每层工作流程：**
1. 完善架构文档（概念 → 技术规格 → 实施路径）
2. 更新架构图（添加节点和连接）
3. 创建详情页
4. 创建 GitHub Discussions 分类
5. 收集反馈并迭代

### 5.4 里程碑

| 时间 | 里程碑 | 关键决策点 |
|------|--------|-----------|
| Week 2 末 | MVP 上线 | 收集初步反馈 |
| Week 4 末 | 完整功能上线 | 评估社区参与度 |
| Week 6 末 | Layer 1-4 完成 | 评估是否继续扩展 |

---

## 6. 风险与缓解

| 风险 | 影响 | 缓解措施 |
|------|------|---------|
| GitHub API 速率限制 | 中 | 构建时预取 + 客户端缓存 |
| React Flow 学习曲线 | 低 | Sprint 1 先用静态 SVG，Sprint 2 再替换 |
| 社区参与度不足 | 中 | 多渠道推广，降低参与门槛 |
| 内容迁移工作量大 | 低 | 渐进迁移，MVP 只做 Layer 1-2 |
| GitHub Pages 限制 | 低 | 纯静态方案，不依赖 SSR |

---

## 7. 模块独立性

GitHub Discussions 集成（第 4 节）是一个可分离的模块。如果 Sprint 2 时间不足，可以延后讨论集成而不影响架构可视化功能。详情页的讨论 Tab 在集成完成前显示 GitHub 链接占位。

---

## 8. 无障碍访问

- 架构图节点支持键盘导航（Tab/Enter）
- 实施状态除颜色外附带文字标签（"已完成"/"进行中"/"未开始"）
- 图片和 SVG 提供 alt 文本
- 对比度符合 WCAG 2.1 AA 标准

完整的无障碍验证需要手动测试和专业评审。

---

**文档结束**
