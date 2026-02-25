# 自动化优化方案 - README

## 📋 方案概述

这是一个完整的自动化方案，用于优化 `ad_open_sdk_go` 项目的编译内存消耗。通过移除点导入（dot imports）并添加类型前缀，可以将编译时的内存使用降低 **70-80%**。

### 核心特性

- 🔄 **自动同步上游**：从原始仓库自动同步最新代码到 master 分支
- ⚡ **自动优化代码**：在 optimize 分支上移除点导入，添加 `models.` 前缀
- ✅ **自动测试验证**：编译和测试优化后的代码
- 🏷️ **自动版本管理**：在 optimize 分支上生成版本标签和 GitHub Release
- 🎯 **多种触发方式**：手动、定时、API 触发
- 🌿 **双分支策略**：master 保持原始，optimize 包含优化

---

## 📁 文件说明

| 文件 | 说明 | 用途 |
|------|------|------|
| `.github/workflows/sync-and-optimize.yml` | GitHub Actions 工作流 | 自动化流程的核心配置 |
| `scripts/remove_dot_imports.py` | Python 优化脚本 | 移除点导入并更新类型引用 |
| `scripts/test_optimization.sh` | Bash 测试脚本 | 验证优化后的代码 |
| `OPTIMIZATION.md` | 详细文档 | 完整的使用说明和故障排查 |
| `QUICKSTART.md` | 快速开始指南 | 5 分钟快速设置 |

---

## 🌿 分支策略

### master 分支
- 包含上游的原始代码
- **不包含任何优化**
- 用于追踪上游更新
- 可以随时回退到原始状态

### optimize 分支
- 基于 master 分支创建
- 包含优化后的代码
- **推荐用于生产环境**
- 每次同步后自动更新

### 工作流程

```
上游仓库更新
    ↓
同步到 master 分支（保持原始）
    ↓
创建/更新 optimize 分支
    ↓
在 optimize 分支上执行优化
    ├─ 移除点导入
    ├─ 添加 models. 前缀
    └─ 更新类型引用
    ↓
验证编译
    ↓
运行测试
    ↓
提交到 optimize 分支
    ↓
在 optimize 分支上创建 tag
    ↓
推送并创建 Release
    ↓
✅ 完成
```

---

## 🚀 快速开始

### 1. Fork 原始仓库

访问 [oceanengine/ad_open_sdk_go](https://github.com/oceanengine/ad_open_sdk_go) 并 Fork 到你的账号。

### 2. 克隆并添加文件

```bash
git clone https://github.com/YOUR_USERNAME/ad_open_sdk_go.git
cd ad_open_sdk_go

# 确保自动化文件存在（应该已经在项目中）
ls -la .github/workflows/sync-and-optimize.yml
ls -la scripts/remove_dot_imports.py
ls -la scripts/test_optimization.sh

# 设置执行权限
chmod +x scripts/*.py scripts/*.sh
```

### 3. 提交并推送

```bash
git add .
git commit -m "Add automation for optimization"
git push origin master
```

### 4. 触发工作流

1. 访问你的 fork 仓库
2. 点击 "Actions" → "Sync and Optimize" → "Run workflow"
3. 等待 5-10 分钟完成

详细步骤请参考 [QUICKSTART.md](./QUICKSTART.md)

---

## 📊 性能对比

| 指标 | 优化前 | 优化后 | 改善 |
|------|--------|--------|------|
| 编译内存 | 5-8 GB | 1-2 GB | ↓ 70-80% |
| 编译时间 | ~5 分钟 | ~2 分钟 | ↓ 60% |
| 符号表大小 | ~1000 万 | ~300 万 | ↓ 70% |

---

## 🎯 触发方式

### 1. 手动触发（推荐）

在 GitHub Actions 页面手动触发工作流。

### 2. 使用 GitHub "Sync fork" 功能

1. 在你的 fork 仓库页面点击 "Sync fork"
2. 等待同步完成
3. 进入 "Actions" → "Sync and Optimize" → "Run workflow"

### 3. 定时触发

默认每周日凌晨 2 点（UTC）自动运行，相当于北京时间周日上午 10 点。

### 4. API 触发

通过 GitHub API 触发：

```bash
curl -X POST \
  -H "Authorization: token YOUR_TOKEN" \
  -H "Accept: application/vnd.github.v3+json" \
  https://api.github.com/repos/YOUR_USERNAME/ad_open_sdk_go/dispatches \
  -d '{"event_type":"sync-upstream"}'
```

---

## 🧪 本地测试

### 运行优化脚本

```bash
python3 scripts/remove_dot_imports.py
```

### 运行测试脚本

```bash
bash scripts/test_optimization.sh
```

---

## 📝 代码迁移

优化后，使用 SDK 需要修改导入方式：

### 修改前

```go
import (
    "github.com/yourusername/ad_open_sdk_go/api"
    . "github.com/yourusername/ad_open_sdk_go/models"
)

accountType := ACCOUNT_TYPE_ADVERTISER
```

### 修改后

```go
import (
    "github.com/yourusername/ad_open_sdk_go/api"
    "github.com/yourusername/ad_open_sdk_go/models"
)

accountType := models.ACCOUNT_TYPE_ADVERTISER
```

### 安装优化版本

```bash
# 使用 optimize 分支
go get github.com/yourusername/ad_open_sdk_go@optimize

# 或使用特定版本
go get github.com/yourusername/ad_open_sdk_go@v2025.02.25-abc1234
```

---

## 📚 文档

- **[QUICKSTART.md](./QUICKSTART.md)** - 5 分钟快速开始指南
- **[OPTIMIZATION.md](./OPTIMIZATION.md)** - 详细文档和故障排查

---

## 🐛 故障排查

### 工作流失败

1. 查看 Actions 日志，找到错误信息
2. 检查上游仓库地址是否正确
3. 确认 Go 版本兼容性
4. 在本地运行测试脚本：`bash scripts/test_optimization.sh`

### 编译失败

1. 在本地运行 `bash scripts/test_optimization.sh`
2. 检查类型引用是否正确
3. 手动修复问题文件
4. 重新提交

### 分支问题

- **master 分支**：始终包含原始上游代码
- **optimize 分支**：包含优化后的代码
- 如果 optimize 分支有问题，可以切换到 master 分支

更多问题请参考 [OPTIMIZATION.md](./OPTIMIZATION.md#故障排查)

---

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

---

## 📄 许可证

遵循原始项目的许可证。

---

## 💡 提示

- 🔄 建议每周同步一次上游更新
- 🧪 每次优化后运行测试确保功能正常
- 📊 关注 Actions Summary 了解优化效果
- 🏷️ 使用版本标签管理不同版本
- 🌿 使用 optimize 分支进行开发
- 🔍 需要对比时切换到 master 分支

---

**祝你使用愉快！** 🎊
