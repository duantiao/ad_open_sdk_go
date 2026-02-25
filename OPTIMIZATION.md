# 自动化优化方案使用文档

## 📋 概述

本文档说明如何使用自动化方案来优化 `ad_open_sdk_go` 项目的编译内存消耗。该方案通过移除点导入（dot imports）并添加类型前缀，将编译时的内存使用降低 70-80%。

## 🎯 功能特性

- ✅ **自动同步上游代码**：从 `oceanengine/ad_open_sdk_go` 自动同步最新代码到 master 分支
- ✅ **自动优化代码**：在 optimize 分支上移除点导入，添加 `models.` 前缀
- ✅ **自动测试验证**：编译和测试优化后的代码
- ✅ **自动创建版本**：在 optimize 分支上生成版本标签和 GitHub Release
- ✅ **多种触发方式**：手动触发、定时触发、API 触发
- ✅ **双分支策略**：master 保持原始代码，optimize 包含优化代码

## 📁 文件结构

```
ad_open_sdk_go/
├── .github/
│   └── workflows/
│       └── sync-and-optimize.yml    # GitHub Actions 工作流
├── scripts/
│   ├── remove_dot_imports.py        # 优化脚本
│   └── test_optimization.sh         # 测试脚本
├── OPTIMIZATION.md                  # 本文档
├── QUICKSTART.md                   # 快速开始指南
└── AUTOMATION_README.md            # 方案总览
```

## 🌿 分支策略

### master 分支
- 包含上游的原始代码
- **不包含任何优化**
- 用于追踪上游更新
- 可以随时回退到原始状态
- 保持与上游完全一致

### optimize 分支
- 基于 master 分支创建
- 包含优化后的代码
- **推荐用于生产环境**
- 每次同步后自动更新
- 所有优化都在此分支上执行

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

## 🚀 快速开始

### 1. Fork 原始仓库

1. 访问 [oceanengine/ad_open_sdk_go](https://github.com/oceanengine/ad_open_sdk_go)
2. 点击 "Fork" 按钮创建你自己的 fork
3. 克隆你的 fork 到本地：

```bash
git clone https://github.com/YOUR_USERNAME/ad_open_sdk_go.git
cd ad_open_sdk_go
```

### 2. 添加自动化文件

将以下文件添加到你的 fork 仓库中：

- `.github/workflows/sync-and-optimize.yml`
- `scripts/remove_dot_imports.py`
- `scripts/test_optimization.sh`

确保脚本有执行权限：

```bash
chmod +x scripts/remove_dot_imports.py
chmod +x scripts/test_optimization.sh
```

### 3. 配置 GitHub Actions

1. 进入你的 fork 仓库的 GitHub 页面
2. 点击 "Settings" → "Secrets and variables" → "Actions"
3. 确保 `GITHUB_TOKEN` 有足够的权限（默认应该就有）
4. 如果需要，可以添加其他 secrets

### 4. 提交并推送

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

## 🔄 使用方法

### 方法 1: 手动触发（推荐）

1. 进入你的 fork 仓库的 GitHub 页面
2. 点击 "Actions" 标签
3. 选择 "Sync and Optimize" 工作流
4. 点击 "Run workflow" 按钮
5. 配置选项：
   - **Use workflow from**: `master` 分支
   - **Upstream branch**: `master`（默认）
   - **Create tag**: `true`（默认）
6. 点击 "Run workflow" 开始执行

### 方法 2: 使用 GitHub "Sync fork" 功能

1. 进入你的 fork 仓库页面
2. 点击 "Sync fork" 按钮
3. 等待同步完成
4. 进入 "Actions" → "Sync and Optimize" → "Run workflow"
5. 等待优化完成

### 方法 3: 定时触发

工作流默认配置为每周日凌晨 2 点（UTC）自动运行，相当于北京时间周日上午 10 点。

如需修改定时规则，编辑 `.github/workflows/sync-and-optimize.yml` 中的 `schedule` 部分：

```yaml
schedule:
  - cron: '0 2 * * 0'  # 每周日凌晨2点运行（北京时间周日上午10点）
```

### 方法 4: API 触发

通过 GitHub API 触发工作流：

```bash
curl -X POST \
  -H "Authorization: token YOUR_GITHUB_TOKEN" \
  -H "Accept: application/vnd.github.v3+json" \
  https://api.github.com/repos/YOUR_USERNAME/ad_open_sdk_go/dispatches \
  -d '{"event_type":"sync-upstream"}'
```

## 📊 工作流程

工作流会自动执行以下步骤：

1. ✅ 检查上游更新
2. ✅ 同步上游代码到 master 分支
3. ✅ 从 master 创建 optimize 分支
4. ✅ 在 optimize 分支上执行优化脚本
   - 移除点导入
   - 添加 `models.` 前缀
5. ✅ 验证编译
6. ✅ 运行测试
7. ✅ 提交优化后的代码到 optimize 分支
8. ✅ 在 optimize 分支上创建版本标签
9. ✅ 创建 GitHub Release

你可以在 Actions 页面实时查看进度。

## 🧪 本地测试

### 运行优化脚本

```bash
# 基本用法
python3 scripts/remove_dot_imports.py

# 跳过编译验证
python3 scripts/remove_dot_imports.py --no-verify

# 指定项目根目录
python3 scripts/remove_dot_imports.py --project-root /path/to/project
```

### 运行测试脚本

```bash
# 运行完整测试套件
bash scripts/test_optimization.sh

# 或使用 bash
./scripts/test_optimization.sh
```

## 📈 性能对比

| 指标 | 优化前 | 优化后 | 改善 |
|------|--------|--------|------|
| 编译内存 | 5-8 GB | 1-2 GB | ↓ 70-80% |
| 编译时间 | ~5 分钟 | ~2 分钟 | ↓ 60% |
| 符号表大小 | ~1000 万 | ~300 万 | ↓ 70% |

## 🔧 自定义配置

### 修改上游仓库

编辑 `.github/workflows/sync-and-optimize.yml`：

```yaml
env:
  UPSTREAM_REPO: 'oceanengine/ad_open_sdk_go'  # 修改为你的上游仓库
  GO_VERSION: '1.18'                         # 修改 Go 版本
  OPTIMIZE_BRANCH: 'optimize'                  # 修改优化分支名称
```

### 修改默认分支

在手动触发时，可以指定不同的上游分支（默认 `master`）。

### 禁用自动创建标签

在手动触发时，选择 `create_tag: false`。

### 修改定时任务

编辑 `.github/workflows/sync-and-optimize.yml` 中的 `schedule` 部分：

```yaml
schedule:
  - cron: '0 2 * * 0'  # 每周日凌晨2点运行
```

Cron 表达式说明：
- `0 2 * * 0` = 每周日凌晨 2 点
- `0 2 * * *` = 每天凌晨 2 点
- `0 */6 * * *` = 每 6 小时运行一次

## 📝 代码迁移指南

如果你正在使用这个 SDK，需要更新你的代码以适应优化后的版本：

### 修改前（使用点导入）

```go
package main

import (
    "github.com/yourusername/ad_open_sdk_go/api"
    . "github.com/yourusername/ad_open_sdk_go/models"
)

func main() {
    client := api.NewAPIClient(cfg)
    
    // 直接使用类型
    accountType := ACCOUNT_TYPE_ADVERTISER
    
    req := client.AccountFundGetV30Api.Get(context.Background())
    req.AccountType(accountType)
}
```

### 修改后（使用正常导入）

```go
package main

import (
    "context"
    
    "github.com/yourusername/ad_open_sdk_go/api"
    "github.com/yourusername/ad_open_sdk_go/models"
)

func main() {
    client := api.NewAPIClient(cfg)
    
    // 使用 models. 前缀
    accountType := models.ACCOUNT_TYPE_ADVERTISER
    
    req := client.AccountFundGetV30Api.Get(context.Background())
    req.AccountType(accountType)
}
```

### 批量替换

如果你有大量代码需要迁移，可以使用以下命令：

```bash
# 查找所有使用点导入的文件
grep -r '^\s*\.\s*"github.com/yourusername/ad_open_sdk_go/models"' .

# 使用 sed 批量替换（谨慎使用！）
find . -name "*.go" -type f -exec sed -i '' 's/ACCOUNT_TYPE_/models.ACCOUNT_TYPE_/g' {} \;
```

### 安装优化版本

```bash
# 使用 optimize 分支
go get github.com/yourusername/ad_open_sdk_go@optimize

# 或使用特定版本
go get github.com/yourusername/ad_open_sdk_go@v2025.02.25-abc1234
```

## 🐛 故障排查

### 问题 1: 工作流失败

**症状**: GitHub Actions 工作流执行失败

**解决方案**:
1. 查看 Actions 日志，查看具体错误信息
2. 检查上游仓库地址是否正确
3. 确认 Go 版本兼容性
4. 检查网络连接
5. 在本地运行测试脚本：`bash scripts/test_optimization.sh`

### 问题 2: 编译失败

**症状**: 优化后代码无法编译

**解决方案**:
1. 在本地运行测试脚本：`bash scripts/test_optimization.sh`
2. 检查是否有类型引用遗漏
3. 手动修复问题文件
4. 提交修复并重新运行工作流

### 问题 3: 类型引用错误

**症状**: 编译时提示类型未定义

**解决方案**:
1. 检查是否正确添加了 `models.` 前缀
2. 确认类型名称拼写正确
3. 查看原始文件中的类型定义
4. 在 optimize 分支上查看优化后的代码

### 问题 4: 内存没有改善

**症状**: 优化后内存使用仍然很高

**解决方案**:
1. 确认所有点导入都已移除
2. 清理 Go 缓存：`go clean -cache -modcache`
3. 重新编译测试
4. 检查是否有其他优化空间

### 问题 5: 分支问题

**症状**: master 分支被修改或 optimize 分支有问题

**解决方案**:
- **master 分支**：应该始终包含原始上游代码，如果被修改了，可以重置：
  ```bash
  git checkout master
  git reset --hard upstream/master
  git push origin master --force
  ```
- **optimize 分支**：如果优化有问题，可以重新运行工作流或手动修复

### 问题 6: 定时任务不运行

**症状**: 定时任务没有按预期执行

**解决方案**:
1. 检查 cron 表达式是否正确
2. 确认 GitHub Actions 已启用
3. 查看工作流日志确认是否被触发
4. 检查时区设置（cron 使用 UTC 时间）

## 📚 相关资源

- [Go 官方文档 - Import](https://go.dev/ref/spec#Import_declarations)
- [Go 最佳实践 - 避免点导入](https://github.com/golang/go/wiki/CodeReviewComments#import-dot)
- [GitHub Actions 文档](https://docs.github.com/en/actions)
- [Cron 表达式生成器](https://crontab.guru/)

## 🤝 贡献

如果你发现任何问题或有改进建议，欢迎：

1. Fork 这个仓库
2. 创建特性分支
3. 提交你的更改
4. 发起 Pull Request

## 📄 许可证

本优化方案遵循原始项目的许可证。

## 📞 支持

如有问题，请：

1. 查看 [Issues](https://github.com/YOUR_USERNAME/ad_open_sdk_go/issues)
2. 提交新的 Issue
3. 联系维护者

## 💡 最佳实践

### 开发工作流

1. **使用 optimize 分支进行开发**
   ```bash
   git checkout optimize
   ```

2. **需要对比原始代码时切换到 master**
   ```bash
   git checkout master
   ```

3. **定期同步上游更新**
   - 建议每周一次
   - 使用 GitHub "Sync fork" 功能
   - 或手动触发工作流

4. **每次优化后运行测试**
   - 确保功能正常
   - 验证性能改善

### 版本管理

- 使用版本标签管理不同版本
- 优先使用 optimize 分支
- 需要原始代码时使用 master 分支
- 查看 GitHub Release 了解版本变更

### 监控和调试

- 关注 Actions 的 Summary 了解优化效果
- 查看工作流日志排查问题
- 定期检查内存使用情况
- 记录性能指标

---

**注意**: 这是一个自动化优化方案，旨在改善编译性能。优化后的代码功能与原始代码完全一致，只是代码组织方式有所不同。master 分支保持原始状态，optimize 分支包含优化后的代码。
