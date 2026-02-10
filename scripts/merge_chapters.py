#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
合并所有章节文件为完整的Markdown文档
"""

import os
import sys
from pathlib import Path

def merge_chapters(input_dir: str, output_file: str) -> None:
    """
    合并所有章节文件
    
    Args:
        input_dir: 输入目录路径
        output_file: 输出文件路径
    """
    input_path = Path(input_dir)
    output_path = Path(output_file)
    
    if not input_path.exists():
        print(f"错误：输入目录不存在: {input_dir}")
        sys.exit(1)
    
    # 获取所有markdown文件并排序
    md_files = sorted(input_path.glob("*.md"))
    
    if not md_files:
        print(f"错误：在 {input_dir} 中未找到Markdown文件")
        sys.exit(1)
    
    print(f"找到 {len(md_files)} 个章节文件")
    
    # 合并内容
    merged_content = []
    
    for md_file in md_files:
        print(f"处理: {md_file.name}")
        
        with open(md_file, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # 添加内容
        merged_content.append(content)
        
        # 在���节之间添加分隔符（除了最后一个文件）
        if md_file != md_files[-1]:
            merged_content.append("\n\n---\n\n")
    
    # 写入输出文件
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(''.join(merged_content))
    
    print(f"\n✅ 成功合并 {len(md_files)} 个文件")
    print(f"📄 输出文件: {output_file}")
    print(f"📊 文件大小: {output_path.stat().st_size / 1024:.2f} KB")

def main():
    """主函数"""
    # 获取项目根目录
    script_dir = Path(__file__).parent
    project_root = script_dir.parent
    
    # 设置路径
    input_dir = project_root / "revised_book_v2"
    output_file = project_root / "Convict_Conditioning_Revised_Complete.md"
    
    print("=" * 60)
    print("囚徒健身修订版 - 章节合并工具")
    print("=" * 60)
    print(f"输入目录: {input_dir}")
    print(f"输出文件: {output_file}")
    print("=" * 60)
    print()
    
    merge_chapters(str(input_dir), str(output_file))
    
    print("\n" + "=" * 60)
    print("合并完成！")
    print("=" * 60)

if __name__ == "__main__":
    main()
