# 快速设置指南

## 🚀 5 分钟快速开始

这个指南将帮助你在 5 分钟内设置好自动化优化流程。

### 前提条件

- ✅ 已有 GitHub 账号
- ✅ 已 Fork [oceanengine/ad_open_sdk_go](https://github.com/oceanengine/ad_open_sdk_go)
- ✅ 本地安装了 Git

---

## 步骤 1: 克隆你的 Fork（1 分钟）

```bash
# 克隆你的 fork 仓库
git clone https://github.com/YOUR_USERNAME/ad_open_sdk_go.git
cd ad_open_sdk_go

# 确保你在 master 分支
git checkout master
```

---

## 步骤 2: 添加自动化文件（2 分钟）

自动化文件已经创建在你的项目中，你只需要确保它们存在：

```bash
# 检查文件是否存在
ls -la .github/workflows/sync-and-optimize.yml
ls -la scripts/remove_dot_imports.py
ls -la scripts/test_optimization.sh

# 如果不存在，从项目根目录复制它们
# （这些文件应该已经在项目中）
```

设置执行权限：

```bash
chmod +x scripts/remove_dot_imports.py
chmod +x scripts/test_optimization.sh
```

---

## 步骤 3: 提交并推送（1 分钟）

```bash
# 添加所有文件
git add .

# 提交
git commit -m "Add automation for optimization

- Add GitHub Actions workflow for sync and optimize
- Add script to remove dot imports
- Add test script for verification
- Use master branch as default
- Create optimize branch for optimized code"

# 推送到你的 fork
git push origin master
```

---

## 步骤 4: 在 GitHub 上触发工作流（1 分钟）

1. 打开浏览器，访问你的 fork 仓库：`https://github.com/YOUR_USERNAME/ad_open_sdk_go`

2. 点击 "Actions" 标签

3. 在左侧选择 "Sync and Optimize" 工作流

4. 点击 "Run workflow" 按钮

5. 配置选项：
   - **Use workflow from**: `master` 分支
   - **Upstream branch**: `master`（默认）
   - **Create tag**: `true`（默认）

6. 点击 "Run workflow" 绿色按钮

---

## 步骤 5: 等待完成（5-10 分钟）

工作流会自动执行以下步骤：

1. ✅ 同步上游代码到 master 分支
2. ✅ 从 master 创建 optimize 分支
3. ✅ 在 optimize 分支上执行优化脚本
   - 移除点导入
   - 添加 `models.` 前缀
4. ✅ 验证编译
5. ✅ 运行测试
6. ✅ 提交优化后的代码到 optimize 分支
7. ✅ 在 optimize 分支上创建版本标签
8. ✅ 创建 GitHub Release

你可以在 Actions 页面实时查看进度。

---

## 🎉 完成！

工作流完成后，你的 fork 仓库将：

- ✅ **master 分支**：包含最新的上游原始代码（未修改）
- ✅ **optimize 分支**：包含优化后的代码（推荐使用）
- ✅ 有新的版本标签（在 optimize 分支上）
- ✅ 有对应的 GitHub Release

---

## 📝 后续使用

### 方法 1: 使用 GitHub 的 "Sync fork" 功能

1. 进入你的 fork 仓库页面
2. 点击 "Sync fork" 按钮
3. 等待同步完成
4. 进入 "Actions" → "Sync and Optimize" → "Run workflow"
5. 等待优化完成

### 方法 2: 手动触发工作流

1. 进入你的 fork 仓库的 "Actions" 页面
2. 点击 "Sync and Optimize" → "Run workflow"
3. 等待完成

### 方法 3: 自动同步（每周一次）

工作流默认每周日凌晨 2 点（UTC）自动运行，相当于北京时间周日上午 10 点。

如需修改时间，编辑 `.github/workflows/sync-and-optimize.yml` 中的 `schedule` 部分：

```yaml
schedule:
  - cron: '0 2 * * 0'  # 每周日凌晨2点运行
```

---

## 🔍 验证优化效果

### 方法 1: 查看版本标签

```bash
# 拉取最新标签
git fetch --tags

# 查看最新标签
git tag -l | sort -V | tail -1
```

### 方法 2: 本地测试编译

```bash
# 切换到 optimize 分支
git checkout optimize

# 拉取最新代码
git pull origin optimize

# 测试编译
go build -v ./...

# 查看内存使用（macOS/Linux）
/usr/bin/time -l go build -o /dev/null ./...
```

### 方法 3: 查看优化报告

工作流完成后，在 Actions 页面的 "Summary" 部分会显示：
- 上游同步状态
- 分支更新情况
- 优化应用情况
- 版本标签信息
- 性能改善数据

---

## 🌿 分支策略说明

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
上游更新
    ↓
同步到 master 分支（保持原始）
    ↓
创建/更新 optimize 分支
    ↓
在 optimize 分支上执行优化
    ↓
提交到 optimize 分支
    ↓
在 optimize 分支上创建 tag
    ↓
创建 Release
```

---

## 🐛 常见问题

### Q: 工作流失败怎么办？

A:
1. 查看 Actions 日志，找到错误信息
2. 检查上游仓库地址是否正确
3. 确认 Go 版本兼容性
4. 在本地运行测试脚本：`bash scripts/test_optimization.sh`

### Q: 如何手动运行优化脚本？

A:
```bash
# 基本用法
python3 scripts/remove_dot_imports.py

# 跳过编译验证
python3 scripts/remove_dot_imports.py --no-verify

# 指定项目根目录
python3 scripts/remove_dot_imports.py --project-root /path/to/project
```

### Q: 优化后如何使用 SDK？

A: 需要修改导入方式：

```go
// 之前
import (
    "github.com/yourusername/ad_open_sdk_go/api"
    . "github.com/yourusername/ad_open_sdk_go/models"
)

// 之后
import (
    "github.com/yourusername/ad_open_sdk_go/api"
    "github.com/yourusername/ad_open_sdk_go/models"
)

// 使用时添加 models. 前缀
accountType := models.ACCOUNT_TYPE_ADVERTISER
```

### Q: 可以回退到未优化的版本吗？

A: 可以，使用 Git 回退：

```bash
# 查看提交历史
git log --oneline

# 回退到优化前的提交
git reset --hard <commit-hash>

# 推送（强制推送，谨慎使用）
git push origin optimize --force
```

或者直接使用 master 分支：

```bash
git checkout master
```

### Q: 两个分支有什么区别？

A:
- **master**: 原始上游代码，未修改
- **optimize**: 优化后的代码，推荐使用

建议在开发时使用 optimize 分支，需要对比原始代码时切换到 master 分支。

---

## 📚 更多信息

- 详细文档：[OPTIMIZATION.md](./OPTIMIZATION.md)
- GitHub Actions 文档：https://docs.github.com/en/actions
- 原始仓库：https://github.com/oceanengine/ad_open_sdk_go

---

## 💡 提示

- 🔄 建议每周同步一次上游更新
- 🧪 每次优化后运行测试确保功能正常
- 📊 关注 Actions 的 Summary 了解优化效果
- 🏷️ 使用版本标签管理不同版本
- 🌿 使用 optimize 分支进行开发
- 🔍 需要对比时切换到 master 分支

---

**祝你使用愉快！** 🎊
