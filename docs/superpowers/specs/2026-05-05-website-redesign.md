---
title: AI Virtual Cell 网站重构设计
date: 2026-05-05
status: approved
---

# AI Virtual Cell 网站重构设计

## 概述

将现有单页网站重构为 5 页多文件静态网站，采用深空生物风视觉风格，中等交互级别。

## 页面结构

| 文件 | 内容 |
|------|------|
| index.html | 首页：Hero + 核心突破 + 项目统计 + 导航卡片 |
| innovations.html | 3 个 P0 创新详细展示 + 实验数据 + 代码示例 |
| mapping.html | 13×15 矩阵可视化 + 映射关系表 + 方法论 |
| roadmap.html | 时间线 + 里程碑 + 预期产出 + 资源需求 |
| docs.html | 文档索引 + 贡献指南 + 社区链接 |

## 视觉设计

- 风格：深空生物风（深色背景 + 发光细胞形态元素）
- 背景色：#0f172a（slate-900）
- 卡片色：#1e293b（slate-800）
- 主色：#22c55e（green-500，发光效果）
- 辅色：#3b82f6（blue-500）
- 强调色：#a855f7（purple-500）
- 特效：CSS 发光粒子背景、毛玻璃卡片、渐变边框、悬停脉冲光晕

## 导航

- 顶部固定浮动导航栏
- 毛玻璃效果（backdrop-filter: blur）
- 当前页高亮
- 移动端汉堡菜单

## 交互效果

- IntersectionObserver 滚动触发淡入/上移动画
- 卡片悬停浮起 + 边框发光
- 数字递增动画（统计数据）
- 导航滚动变色

## 技术实现

- Tailwind CSS（CDN）
- Vanilla JS（ES6+）
- CSS Animations + Keyframes
- 共享 components.js 注入导航/页脚/粒子背景
- 无构建步骤，直接部署 website/ 目录

## 文件结构

```
website/
├── index.html
├── innovations.html
├── mapping.html
├── roadmap.html
├── docs.html
├── css/
│   └── style.css
├── js/
│   ├── components.js
│   └── animations.js
└── assets/
```
