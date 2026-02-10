#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
将Markdown文档转换为EPUB和PDF格式
需要安装: pandoc, calibre (ebook-convert), xelatex (可选, 用于pandoc生成PDF)
"""

import os
import sys
import subprocess
import argparse
from pathlib import Path
from datetime import datetime

def check_dependencies(pdf_engine='calibre'):
    """检查必要的依赖工具"""
    dependencies = {
        'pandoc': 'Pandoc (用于生成EPUB/PDF)',
    }
    
    if pdf_engine == 'calibre':
        dependencies['ebook-convert'] = 'Calibre (用于生成PDF)'
    elif pdf_engine == 'pandoc':
        dependencies['xelatex'] = 'XeLaTeX (用于生成PDF)'
    
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

def build_pdf_calibre(epub_file: str, output_file: str, args) -> bool:
    """
    使用Calibre的ebook-convert将EPUB转换为PDF
    
    Args:
        epub_file: 输入EPUB文件路径
        output_file: 输出PDF文件路径
        args: 命令行参数
        
    Returns:
        bool: 是否成功
    """
    print(f"\n📄 生成PDF (Calibre): {output_file}")
    
    cmd = [
        'ebook-convert',
        epub_file,
        output_file,
        '--paper-size', args.paper_size,
        '--pdf-page-margin-bottom', str(args.margin_bottom),
        '--pdf-page-margin-top', str(args.margin_top),
        '--pdf-page-margin-left', str(args.margin_left),
        '--pdf-page-margin-right', str(args.margin_right),
        '--pdf-default-font-size', '12',
        '--pdf-mono-font-size', '10',
        '--pdf-serif-family', args.font_serif,
        '--pdf-sans-family', args.font_sans,
        '--pdf-mono-family', args.font_mono,
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

def build_pdf_pandoc(input_file: str, output_file: str, metadata: dict, args) -> bool:
    """
    使用Pandoc (XeLaTeX) 生成PDF
    
    Args:
        input_file: 输入Markdown文件路径
        output_file: 输出PDF文件路径
        metadata: 元数据字典
        args: 命令行参数
        
    Returns:
        bool: 是否成功
    """
    print(f"\n📄 生成PDF (Pandoc): {output_file}")
    
    cmd = [
        'pandoc',
        input_file,
        '-o', output_file,
        '--pdf-engine=xelatex',
        '--toc',
        '--toc-depth=3',
        '-V', f'geometry:margin={args.margin_top}pt', # 简单起见统一边距，���者需要更复杂转换
        '-V', f'mainfont={args.font_sans}', # 使用无衬线字体作为主字体，或者根据需要调整
        '-V', f'sansfont={args.font_sans}',
        '-V', f'monofont={args.font_mono}',
        '-V', 'CJKmainfont=' + args.font_sans, # 关键：设置CJK字体
        '-V', f'papersize={args.paper_size}',
        f'--metadata=title:{metadata.get("title", "囚徒健身修订版")}',
        f'--metadata=author:{metadata.get("author", "Paul Wade (修订版)")}',
        f'--metadata=date:{metadata.get("date", datetime.now().strftime("%Y-%m-%d"))}',
    ]
    
    # 添加自定义Pandoc参数
    if args.pandoc_args:
        import shlex
        extra_args = shlex.split(args.pandoc_args)
        print(f"  添加自定义参数: {extra_args}")
        cmd.extend(extra_args)
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        print(f"✅ PDF生成成功")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ PDF生成失败: {e.stderr}")
        return False

def main():
    """主函数"""
    parser = argparse.ArgumentParser(description='囚徒健身修订版 - 电子书构建工具')
    parser.add_argument('--pdf-engine', choices=['calibre', 'pandoc'], default='calibre',
                        help='PDF生成引擎 (默认: calibre)')
    parser.add_argument('--paper-size', default='a4', help='纸张大小 (默认: a4)')
    parser.add_argument('--margin-top', default='72', help='上边距 (pt)')
    parser.add_argument('--margin-bottom', default='72', help='下边距 (pt)')
    parser.add_argument('--margin-left', default='72', help='左边距 (pt)')
    parser.add_argument('--margin-right', default='72', help='右边距 (pt)')
    parser.add_argument('--font-serif', default='Noto Serif CJK SC', help='衬线字体')
    parser.add_argument('--font-sans', default='Noto Sans CJK SC', help='无衬线字体')
    parser.add_argument('--font-mono', default='Noto Sans Mono CJK SC', help='等宽字体')
    parser.add_argument('--pandoc-args', help='Pandoc自定义参数 (例如: "--toc-depth=2 -V fontsize=12pt")')
    
    args = parser.parse_args()

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
    print(f"PDF引擎: {args.pdf_engine}")
    print("=" * 60)
    print()
    
    # 检查输入文件
    if not input_file.exists():
        print(f"❌ 错误：输入文件不存在: {input_file}")
        print("请先运行 merge_chapters.py 合并章节文件")
        sys.exit(1)
    
    # 检查依赖
    print("检查依赖工具...")
    if not check_dependencies(args.pdf_engine):
        print("\n⚠️  警告：部分依赖工具未安装")
        # 不退出，尝试继续
    
    # 元数据
    metadata = {
        'title': '囚徒健身 - 科学修订版',
        'author': 'Paul Wade (科学修订版)',
        'lang': 'zh-CN',
        'date': datetime.now().strftime('%Y-%m-%d')
    }
    
    # 生成EPUB (总是生成)
    epub_success = build_epub(str(input_file), str(epub_file), metadata)
    
    # 生成PDF
    pdf_success = False
    if args.pdf_engine == 'calibre':
        if epub_success and epub_file.exists():
            pdf_success = build_pdf_calibre(str(epub_file), str(pdf_file), args)
    else: # pandoc
        # pandoc 直接从 markdown 生成 PDF 通常效果更好
        pdf_success = build_pdf_pandoc(str(input_file), str(pdf_file), metadata, args)
    
    # 总结
    print("\n" + "=" * 60)
    print("构建完成！")
    print("=" * 60)
    
    if epub_success and epub_file.exists():
        size = epub_file.stat().st_size / 1024
        print(f"✅ EPUB: {epub_file.name} ({size:.2f} KB)")
    
    if pdf_success and pdf_file.exists():
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
