#!/usr/bin/env python3
"""
自动移除点导入并更新类型引用的脚本
用于优化Go项目的编译内存消耗
"""

import os
import re
import sys
from pathlib import Path
from typing import List, Tuple, Set

class DotImportRemover:
    def __init__(self, project_root: str):
        self.project_root = Path(project_root)
        self.api_dir = self.project_root / "api"
        self.models_dir = self.project_root / "models"
        self.modified_files = []
        self.type_cache = {}
        
    def collect_model_types(self) -> Set[str]:
        """收集所有模型类型名称"""
        types = set()
        
        if not self.models_dir.exists():
            print(f"警告: models目录不存在: {self.models_dir}")
            return types
            
        for model_file in self.models_dir.glob("*.go"):
            try:
                with open(model_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    
                # 匹配类型定义: type TypeName struct/interface/string
                type_pattern = r'^type\s+(\w+)\s+(?:struct|interface|string)\b'
                matches = re.findall(type_pattern, content, re.MULTILINE)
                types.update(matches)
                
                # 匹配常量定义: const ( ... )
                const_pattern = r'^const\s+\(\s*\n((?:\s+\w+\s+\w+\s*=\s*"[^"]*"\s*\n)+)\s*\)'
                for match in re.finditer(const_pattern, content, re.MULTILINE):
                    const_block = match.group(1)
                    const_names = re.findall(r'\s+(\w+)\s+\w+\s*=', const_block)
                    types.update(const_names)
                    
            except Exception as e:
                print(f"警告: 读取文件失败 {model_file}: {e}")
                
        print(f"收集到 {len(types)} 个模型类型")
        return types
    
    def remove_dot_import(self, file_path: Path, model_types: Set[str]) -> bool:
        """移除点导入并更新类型引用"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            original_content = content
            has_dot_import = False
            
            # 检查并移除点导入
            dot_import_pattern = r'\.\s*"github\.com/oceanengine/ad_open_sdk_go/models"'
            if re.search(dot_import_pattern, content):
                has_dot_import = True
                
                # 移除点导入行
                lines = content.split('\n')
                new_lines = []
                for line in lines:
                    if not re.search(r'^\s*\.\s*"github\.com/oceanengine/ad_open_sdk_go/models"', line):
                        new_lines.append(line)
                
                content = '\n'.join(new_lines)
                
                # 添加正常导入（如果还没有）
                normal_import_pattern = r'"github\.com/oceanengine/ad_open_sdk_go/models"'
                if not re.search(normal_import_pattern, content):
                    # 找到import块并添加
                    import_block_pattern = r'(import\s*\([^)]*\))'
                    match = re.search(import_block_pattern, content, re.DOTALL)
                    if match:
                        import_block = match.group(1)
                        if not import_block.strip().endswith(')'):
                            # 在import块末尾添加
                            new_import = import_block.rstrip() + '\n\t"github.com/oceanengine/ad_open_sdk_go/models"\n)'
                            content = content.replace(import_block, new_import)
                    else:
                        # 创建新的import块
                        content = re.sub(
                            r'^(package\s+\w+)',
                            r'\1\n\nimport (\n\t"github.com/oceanengine/ad_open_sdk_go/models"\n)',
                            content,
                            count=1
                        )
            
            # 更新类型引用（添加models前缀）
            if has_dot_import:
                # 需要添加前缀的类型
                for type_name in sorted(model_types, key=len, reverse=True):
                    # 匹配类型引用（避免匹配字符串、注释等）
                    patterns = [
                        # 函数参数类型
                        r'(\s+)(%s)(\s+\*?\w+)' % type_name,
                        # 返回值类型
                        r'(\*?\w+\s+)(%s)(\s*[,\)])' % type_name,
                        # 结构体字段类型
                        r'(\s+\w+\s+)(%s)(\s*`)' % type_name,
                        # 变量声明
                        r'(\s+)(%s)(\s+)' % type_name,
                        # 类型转换
                        r'(\()(%s)(\))' % type_name,
                        # 指针类型
                        r'(\*+)(%s)(\s*[,\)])' % type_name,
                    ]
                    
                    for pattern in patterns:
                        content = re.sub(pattern, r'\1models.\2\3', content)
                
                # 移除重复的models.前缀
                content = re.sub(r'models\.models\.', 'models.', content)
            
            # 只在有修改时写入文件
            if content != original_content:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                self.modified_files.append(str(file_path.relative_to(self.project_root)))
                return True
                
            return False
            
        except Exception as e:
            print(f"错误: 处理文件失败 {file_path}: {e}")
            return False
    
    def process_api_files(self) -> int:
        """处理所有API文件"""
        if not self.api_dir.exists():
            print(f"错误: api目录不存在: {self.api_dir}")
            return 0
            
        print("正在收集模型类型...")
        model_types = self.collect_model_types()
        
        if not model_types:
            print("警告: 未找到任何模型类型")
            return 0
            
        print(f"\n开始处理API文件...")
        
        api_files = list(self.api_dir.glob("*.go"))
        processed_count = 0
        
        for api_file in api_files:
            if api_file.name == "client.go":
                continue  # 跳过client.go，单独处理
                
            if self.remove_dot_import(api_file, model_types):
                processed_count += 1
                print(f"✓ {api_file.name}")
        
        return processed_count
    
    def process_client_file(self) -> bool:
        """处理client.go文件"""
        client_file = self.api_dir / "client.go"
        if not client_file.exists():
            return False
            
        try:
            with open(client_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            original_content = content
            
            # client.go中已经有正常的models导入，只需要移除点导入
            lines = content.split('\n')
            new_lines = []
            for line in lines:
                if not re.search(r'^\s*\.\s*"github\.com/oceanengine/ad_open_sdk_go/models"', line):
                    new_lines.append(line)
            
            content = '\n'.join(new_lines)
            
            if content != original_content:
                with open(client_file, 'w', encoding='utf-8') as f:
                    f.write(content)
                self.modified_files.append("api/client.go")
                return True
                
            return False
            
        except Exception as e:
            print(f"错误: 处理client.go失败: {e}")
            return False
    
    def verify_compilation(self) -> bool:
        """验证代码是否可以编译"""
        print("\n正在验证编译...")
        import subprocess
        
        try:
            result = subprocess.run(
                ['go', 'build', './...'],
                cwd=self.project_root,
                capture_output=True,
                text=True,
                timeout=300
            )
            
            if result.returncode == 0:
                print("✓ 编译成功")
                return True
            else:
                print("✗ 编译失败:")
                print(result.stderr)
                return False
                
        except subprocess.TimeoutExpired:
            print("✗ 编译超时")
            return False
        except Exception as e:
            print(f"✗ 编译验证失败: {e}")
            return False
    
    def run(self, verify: bool = True) -> bool:
        """执行完整的优化流程"""
        print("=" * 60)
        print("开始移除点导入优化")
        print("=" * 60)
        
        # 处理API文件
        api_count = self.process_api_files()
        
        # 处理client.go
        client_modified = self.process_client_file()
        
        print(f"\n处理完成:")
        print(f"  - 修改的API文件: {api_count}")
        print(f"  - 修改client.go: {'是' if client_modified else '否'}")
        print(f"  - 总计修改文件: {len(self.modified_files)}")
        
        if self.modified_files:
            print(f"\n修改的文件列表:")
            for f in self.modified_files:
                print(f"  - {f}")
        
        # 验证编译
        if verify and self.modified_files:
            if not self.verify_compilation():
                print("\n⚠️  警告: 编译验证失败，请检查修改")
                return False
        
        print("\n" + "=" * 60)
        print("优化完成!")
        print("=" * 60)
        
        return len(self.modified_files) > 0


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='移除Go项目中的点导入以优化编译内存')
    parser.add_argument('--project-root', '-p', 
                       default='.',
                       help='项目根目录路径（默认: 当前目录）')
    parser.add_argument('--no-verify', '-n',
                       action='store_true',
                       help='跳过编译验证')
    
    args = parser.parse_args()
    
    project_root = Path(args.project_root).resolve()
    
    if not (project_root / "go.mod").exists():
        print(f"错误: {project_root} 不是有效的Go项目（未找到go.mod）")
        sys.exit(1)
    
    remover = DotImportRemover(str(project_root))
    success = remover.run(verify=not args.no_verify)
    
    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
