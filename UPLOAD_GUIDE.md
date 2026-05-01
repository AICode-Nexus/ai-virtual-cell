# GitHub 上传指南

本指南将帮助你将 AI Virtual Cell 项目上传到 GitHub。

## 📋 前提条件

1. 已安装 Git
2. 拥有 GitHub 账号
3. 已登录 GitHub CLI 或配置了 SSH 密钥

## 🚀 上传步骤

### 方法 1：使用 GitHub CLI（推荐）

```bash
# 1. 进入项目目录
cd ai-virtual-cell

# 2. 初始化 Git 仓库
git init

# 3. 添加所有文件
git add .

# 4. 创建初始提交
git commit -m "Initial commit: AI Virtual Cell design proposal"

# 5. 使用 GitHub CLI 创建仓库并推送
gh repo create AICode-Nexus/ai-virtual-cell --public --source=. --remote=origin --push

# 6. 启用 GitHub Pages（用于网站）
gh api repos/AICode-Nexus/ai-virtual-cell/pages -X POST -f source[branch]=main -f source[path]=/website
```

### 方法 2：手动创建仓库

```bash
# 1. 在 GitHub 网站上创建新仓库
# 访问：https://github.com/organizations/AICode-Nexus/repositories/new
# 仓库名：ai-virtual-cell
# 描述：A revolutionary AI architecture based on cellular biology mechanisms
# 公开仓库
# 不要初始化 README、.gitignore 或 license

# 2. 在本地初始化并推送
cd ai-virtual-cell
git init
git add .
git commit -m "Initial commit: AI Virtual Cell design proposal"
git branch -M main
git remote add origin https://github.com/AICode-Nexus/ai-virtual-cell.git
git push -u origin main
```

## 🌐 配置 GitHub Pages

### 启用 GitHub Pages

1. 进入仓库设置：`https://github.com/AICode-Nexus/ai-virtual-cell/settings/pages`
2. Source 选择：`Deploy from a branch`
3. Branch 选择：`main`
4. Folder 选择：`/website`
5. 点击 Save

网站将在几分钟后可访问：`https://aicode-nexus.github.io/ai-virtual-cell`

## 💬 启用 GitHub Discussions

1. 进入仓库设置：`https://github.com/AICode-Nexus/ai-virtual-cell/settings`
2. 向下滚动到 "Features" 部分
3. 勾选 "Discussions"
4. 点击 "Set up discussions"

### 创建讨论分类

建议创建以下分类：

1. **Biology（生物学验证）**
   - 描述：验证生物学机制的准确性和合理性
   - 格式：Open-ended discussion

2. **Technical（技术实现）**
   - 描述：探讨技术可行性、架构设计和实现细节
   - 格式：Open-ended discussion

3. **Applications（应用场景）**
   - 描述：探索实际应用场景和商业价值
   - 格式：Open-ended discussion

4. **Ideas（创新想法）**
   - 描述：分享创新想法和改进建议
   - 格式：Ideas

5. **Q&A（问答）**
   - 描述：提问和回答问题
   - 格式：Q&A

## 📝 添加仓库描述和标签

### 仓库描述
```
A revolutionary AI architecture based on cellular biology mechanisms - featuring memory as structure, capability as organization, and learning as evolution
```

### 推荐标签（Topics）
```
artificial-intelligence
ai-architecture
cellular-biology
neural-networks
machine-learning
distributed-systems
self-organizing-systems
neuroplasticity
multi-agent-systems
biomimicry
```

## 🔧 配置仓库设置

### 推荐设置

1. **General**
   - ✅ Issues
   - ✅ Discussions
   - ✅ Projects
   - ✅ Wiki（可选）

2. **Branches**
   - 设置 `main` 为默认分支
   - 添加分支保护规则（可选）

3. **Actions**
   - 启用 GitHub Actions（未来用于 CI/CD）

## ✅ 验证清单

上传完成后，请验证：

- [ ] 仓库已创建：`https://github.com/AICode-Nexus/ai-virtual-cell`
- [ ] README.md 正确显示
- [ ] 文档可访问：`docs/DESIGN.md`
- [ ] GitHub Pages 已启用
- [ ] 网站可访问：`https://aicode-nexus.github.io/ai-virtual-cell`
- [ ] Discussions 已启用
- [ ] 仓库描述和标签已添加

## 🎉 完成！

现在你可以：
1. 分享仓库链接
2. 邀请贡献者
3. 开始讨论
4. 迭代设计方案

## 📧 需要帮助？

如果遇到问题，可以：
- 查看 GitHub 文档：https://docs.github.com
- 在项目 Discussions 中提问
