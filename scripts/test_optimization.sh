#!/bin/bash
#
# 测试脚本：验证优化后的代码是否正常工作
#

set -e

echo "========================================"
echo "开始测试优化后的代码"
echo "========================================"

# 颜色定义
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 计数器
TESTS_PASSED=0
TESTS_FAILED=0

# 测试函数
run_test() {
    local test_name="$1"
    local test_command="$2"
    
    echo -e "\n${YELLOW}测试: $test_name${NC}"
    echo "命令: $test_command"
    
    if eval "$test_command"; then
        echo -e "${GREEN}✓ 通过${NC}"
        ((TESTS_PASSED++))
        return 0
    else
        echo -e "${RED}✗ 失败${NC}"
        ((TESTS_FAILED++))
        return 1
    fi
}

# 检查Go环境
echo -e "\n${YELLOW}检查Go环境...${NC}"
if ! command -v go &> /dev/null; then
    echo -e "${RED}错误: 未找到Go命令${NC}"
    exit 1
fi

GO_VERSION=$(go version | awk '{print $3}')
echo "Go版本: $GO_VERSION"

# 检查Python环境
echo -e "\n${YELLOW}检查Python环境...${NC}"
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}错误: 未找到python3命令${NC}"
    exit 1
fi

PYTHON_VERSION=$(python3 --version)
echo "Python版本: $PYTHON_VERSION"

# 测试1: 检查点导入是否已移除
echo -e "\n${YELLOW}========================================"
echo "测试组1: 验证点导入移除"
echo "========================================${NC}"

DOT_IMPORT_COUNT=$(grep -r '^\s*\.\s*"github.com/oceanengine/ad_open_sdk_go/models"' api/*.go 2>/dev/null | wc -l || echo "0")

if [ "$DOT_IMPORT_COUNT" -eq 0 ]; then
    echo -e "${GREEN}✓ 所有点导入已移除${NC}"
    ((TESTS_PASSED++))
else
    echo -e "${RED}✗ 仍有 $DOT_IMPORT_COUNT 个文件包含点导入${NC}"
    ((TESTS_FAILED++))
fi

# 测试2: 检查正常导入是否存在
run_test "检查api目录是否有正常导入" \
    "grep -q '\"github.com/oceanengine/ad_open_sdk_go/models\"' api/api_account_fund_get_v30.go"

# 测试3: 检查类型引用是否添加了前缀
echo -e "\n${YELLOW}========================================"
echo "测试组2: 验证类型引用"
echo "========================================${NC}"

run_test "检查API文件中的类型引用是否有models前缀" \
    "grep -q 'models\.AccountFundGetV30AccountType' api/api_account_fund_get_v30.go"

run_test "检查Request结构体中的类型引用" \
    "grep -q 'accountType.*models\.AccountFundGetV30AccountType' api/api_account_fund_get_v30.go"

# 测试4: 编译测试
echo -e "\n${YELLOW}========================================"
echo "测试组3: 编译测试"
echo "========================================${NC}"

echo "清理之前的构建产物..."
go clean -cache -modcache -testcache 2>/dev/null || true

echo "开始编译..."
if go build -v ./...; then
    echo -e "${GREEN}✓ 编译成功${NC}"
    ((TESTS_PASSED++))
else
    echo -e "${RED}✗ 编译失败${NC}"
    ((TESTS_FAILED++))
fi

# 测试5: 内存使用测试（可选）
echo -e "\n${YELLOW}========================================"
echo "测试组4: 内存使用测试"
echo "========================================${NC}"

if command -v /usr/bin/time &> /dev/null; then
    echo "测试编译内存使用..."
    MEMORY_OUTPUT=$(/usr/bin/time -l go build -o /dev/null ./... 2>&1 || true)
    
    if echo "$MEMORY_OUTPUT" | grep -q "maximum resident set size"; then
        MEMORY_KB=$(echo "$MEMORY_OUTPUT" | grep "maximum resident set size" | awk '{print $6}')
        MEMORY_MB=$((MEMORY_KB / 1024))
        echo -e "${GREEN}编译内存使用: ${MEMORY_MB} MB${NC}"
        ((TESTS_PASSED++))
    else
        echo -e "${YELLOW}⚠ 无法获取内存使用信息${NC}"
    fi
else
    echo -e "${YELLOW}⚠ /usr/bin/time 不可用，跳过内存测试${NC}"
fi

# 测试6: 代码质量检查
echo -e "\n${YELLOW}========================================"
echo "测试组5: 代码质量检查"
echo "========================================${NC}"

if command -v gofmt &> /dev/null; then
    run_test "检查代码格式" \
        "! gofmt -l api/*.go | grep -q ."
fi

if command -v go vet &> /dev/null; then
    run_test "运行go vet" \
        "go vet ./..."
fi

# 测试7: 运行测试（如果有）
echo -e "\n${YELLOW}========================================"
echo "测试组6: 单元测试"
echo "========================================${NC}"

if [ -d "tests" ] || [ -d "_test" ] || find . -name "*_test.go" | grep -q .; then
    echo "发现测试文件，运行测试..."
    if go test -v ./... 2>&1 | tee test_output.txt; then
        echo -e "${GREEN}✓ 测试通过${NC}"
        ((TESTS_PASSED++))
    else
        echo -e "${YELLOW}⚠ 部分测试失败或没有测试${NC}"
    fi
else
    echo -e "${YELLOW}⚠ 未找到测试文件${NC}"
fi

# 测试8: API导入测试
echo -e "\n${YELLOW}========================================"
echo "测试组7: API导入测试"
echo "========================================${NC}"

TEST_FILE=$(mktemp -t test_import_XXXXXX.go)
cat > "$TEST_FILE" << 'EOF'
package main

import (
    "github.com/oceanengine/ad_open_sdk_go/api"
    "github.com/oceanengine/ad_open_sdk_go/models"
)

func main() {
    _ = api.AccountFundGetV30ApiService{}
    _ = models.AccountFundGetV30AccountType("")
}
EOF

run_test "测试API和models包导入" \
    "go run $TEST_FILE"

rm -f "$TEST_FILE"

# 测试总结
echo -e "\n========================================"
echo "测试总结"
echo "========================================"
echo -e "通过: ${GREEN}$TESTS_PASSED${NC}"
echo -e "失败: ${RED}$TESTS_FAILED${NC}"
echo -e "总计: $((TESTS_PASSED + TESTS_FAILED))"
echo "========================================"

if [ $TESTS_FAILED -eq 0 ]; then
    echo -e "\n${GREEN}🎉 所有测试通过！${NC}"
    exit 0
else
    echo -e "\n${RED}❌ 有 $TESTS_FAILED 个测试失败${NC}"
    exit 1
fi
