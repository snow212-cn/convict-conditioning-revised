#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
将Markdown文档转换为EPUB和PDF格式
需要安装: pandoc, calibre (ebook-convert)
"""

import os
import sys
import subprocess
from pathlib import Path
from datetime import datetime

def check_dependencies():
    """检查必要的依赖工具"""
    dependencies = {
        'pandoc': 'Pandoc (用于生成EPUB)',
        'ebook-convert': 'Calibre (用于生成PDF)'
    }
    
    missing = []
    for cmd, desc in dependencies.items():
        try:
            subprocess.run([cmd, '--version'], 
                         capture_output=True, 
                         check=True)
            print(f"✅ {desc} - 已安装")
        except (subprocess.CalledProcessError, FileNotFoundError):
            print(f"❌ {desc} - 未安装")
            missing.append(cmd)
    
    return len(missing) == 0

def build_epub(input_file: str, output_file: str, metadata: dict) -> bool:
    """
    使用Pandoc生成EPUB文件
    
    Args:
        input_file: 输入Markdown文件路径
        output_file: 输出EPUB文件路径
        metadata: 元数据字典
        
    Returns:
        bool: 是否成功
    """
    print(f"\n📚 生成EPUB: {output_file}")
    
    # 构建pandoc命令
    cmd = [
        'pandoc',
        input_file,
        '-o', output_file,
        '--toc',  # 生成目录
        '--toc-depth=3',  # 目录深度
        '--epub-cover-image=cover.jpg' if Path('cover.jpg').exists() else '',
        f'--metadata=title:{metadata.get("title", "囚徒健身修订版")}',
        f'--metadata=author:{metadata.get("author", "Paul Wade (修订版)")}',
        f'--metadata=lang:{metadata.get("lang", "zh-CN")}',
        f'--metadata=date:{metadata.get("date", datetime.now().strftime("%Y-%m-%d"))}',
        '--css=styles.css' if Path('styles.css').exists() else '',
    ]
    
    # 移除空字符串参数
    cmd = [arg for arg in cmd if arg]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        print(f"✅ EPUB生成成功")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ EPUB生成失败: {e.stderr}")
        return False

def build_pdf(epub_file: str, output_file: str) -> bool:
    """
    使用Calibre的ebook-convert将EPUB转换为PDF
    
    Args:
        epub_file: 输入EPUB文件路径
        output_file: 输出PDF文件路径
        
    Returns:
        bool: 是否成功
    """
    print(f"\n📄 生成PDF: {output_file}")
    
    cmd = [
        'ebook-convert',
        epub_file,
        output_file,
        '--paper-size', 'a4',
        '--pdf-page-margin-bottom', '72',
        '--pdf-page-margin-top', '72',
        '--pdf-page-margin-left', '72',
        '--pdf-page-margin-right', '72',
        '--pdf-default-font-size', '12',
        '--pdf-mono-font-size', '10',
        '--chapter', '//h:h1',
        '--level1-toc', '//h:h1',
        '--level2-toc', '//h:h2',
        '--level3-toc', '//h:h3',
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        print(f"✅ PDF生成成功")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ PDF生成失败: {e.stderr}")
        return False
    except FileNotFoundError:
        print(f"⚠️  未安装Calibre，跳过PDF生成")
        return False

def main():
    """主函数"""
    # 获取项目根目录
    script_dir = Path(__file__).parent
    project_root = script_dir.parent
    
    # 设置路径
    input_file = project_root / "Convict_Conditioning_Revised_Complete.md"
    epub_file = project_root / "Convict_Conditioning_Revised_Complete.epub"
    pdf_file = project_root / "Convict_Conditioning_Revised_Complete.pdf"
    
    print("=" * 60)
    print("囚徒健身修订版 - 电子书构建工具")
    print("=" * 60)
    print(f"输入文件: {input_file}")
    print(f"EPUB输出: {epub_file}")
    print(f"PDF输出: {pdf_file}")
    print("=" * 60)
    print()
    
    # 检查输入文件
    if not input_file.exists():
        print(f"❌ 错误：输入文件不存在: {input_file}")
        print("请先运行 merge_chapters.py 合并章节文件")
        sys.exit(1)
    
    # 检查依赖
    print("检查依赖工具...")
    if not check_dependencies():
        print("\n⚠️  警告：部分依赖工具未安装")
        print("请安装 Pandoc 和 Calibre:")
        print("  - Pandoc: https://pandoc.org/installing.html")
        print("  - Calibre: https://calibre-ebook.com/download")
        # 不退出，尝试继续
    
    # 元数据
    metadata = {
        'title': '囚徒健身 - 科学修订版',
        'author': 'Paul Wade (科学修订版)',
        'lang': 'zh-CN',
        'date': datetime.now().strftime('%Y-%m-%d')
    }
    
    # 生成EPUB
    epub_success = build_epub(str(input_file), str(epub_file), metadata)
    
    # 生成PDF
    pdf_success = False
    if epub_success and epub_file.exists():
        pdf_success = build_pdf(str(epub_file), str(pdf_file))
    
    # 总结
    print("\n" + "=" * 60)
    print("构建完成！")
    print("=" * 60)
    
    if epub_success:
        size = epub_file.stat().st_size / 1024
        print(f"✅ EPUB: {epub_file.name} ({size:.2f} KB)")
    
    if pdf_success:
        size = pdf_file.stat().st_size / 1024
        print(f"✅ PDF: {pdf_file.name} ({size:.2f} KB)")
    
    print("=" * 60)
    
    # 返回状态码
    if epub_success:
        sys.exit(0)
    else:
        sys.exit(1)

if __name__ == "__main__":
    main()
