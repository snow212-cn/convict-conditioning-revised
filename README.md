# 囚徒健身 - 科学修订版

## 修订说明

本修订版由 Gemini 3 AI 根据《囚徒健身》科学性修正与深度分析报告对原书进行系统性修订，主要改进包括：

- ✅ 修正了原书中不符合运动科学的训练建议
- ✅ 补充了现代运动生理学和生物力学的科学依据
- ✅ 优化了训练进阶方案，使其更加安全合理
- ✅ 增加了伤病预防和康复的相关内容
- ✅ 更新了营养和恢复方面的建议

## 项目结构

```
.
├── 囚徒健身-保罗•威德.epub              # 原版电子书
├── 《囚徒健身》科学性修正与深度分析报告.md  # 修订依据文档
├── revised_book_v2/                    # 分章节修订文件
│   ├── 00_Title.md                     # 标题页
│   ├── 01_Chapter1_The_Journey.md      # 第1章：旅程
│   ├── 02_Chapter2_Old_School.md       # 第2章：老派训练
│   ├── 03_Chapter3_Manifesto.md        # 第3章：宣言
│   ├── 04_Chapter4_About.md            # 第4章：关于本书
│   ├── 05_Chapter5_Pushups.md          # 第5章：俯卧撑
│   ├── 06_Chapter6_Squats.md           # 第6章：深蹲
│   ├── 07_Chapter7_Pullups.md          # 第7章：引体向上
│   ├── 08_Chapter8_LegRaises.md        # 第8章：举腿
│   ├── 09_Chapter9_TheBridge.md        # 第9章：桥
│   ├── 10_Chapter10_HandstandPushups.md # 第10章：倒立撑
│   ├── 11_Chapter11_BodyWisdom.md      # 第11章：身体智慧
│   └── 12_Chapter12_Routines.md        # 第12章：训练计划
├── Convict_Conditioning_Revised_Complete.md   # 完整合并版（Markdown）
└── Convict_Conditioning_Revised_Complete.epub # 完整合并版（EPUB）
```

## 自动化构建

本项目使用 GitHub Actions 实现自动化构建流程：

- 📝 当 `revised_book_v2/` 目录下的任何 Markdown 文件发生变更时自动触发
- 🔄 自动合并所有章节文件为完整版本
- 📚 自动生成 EPUB 和 PDF 格式的电子书
- 🚀 自动创建 GitHub Release 并上传生成的电子书文件
- 💾 自动提交合并后的 Markdown 文���到仓库

## 使用方法

### 在线阅读

访问本仓库的 [Releases](../../releases) 页面下载最新版本的电子书文件。

### 本地构建

如需本地构建电子书，请确保已安装以下依赖：

- Python 3.8+
- Pandoc 2.0+
- Calibre (用于 EPUB 转 PDF)

运行构建脚本：

```bash
# 合并所有章节
python scripts/merge_chapters.py

# 生成 EPUB
python scripts/build_epub.py

# 生成 PDF（可选）
python scripts/build_pdf.py
```

## 贡献指南

欢迎对本修订版提出改进建议！如果您发现任何问题或有更好的修订建议，请：

1. Fork 本仓库
2. 创建您的特性分支 (`git checkout -b feature/improvement`)
3. 提交您的修改 (`git commit -am 'Add some improvement'`)
4. 推送到分支 (`git push origin feature/improvement`)
5. 创建一个 Pull Request

## 版权声明

- 原书《囚徒健身》版权归保罗·威德（Paul Wade）所有
- 本修订版本仅供学习交流使用，不得用于商业用途
- 修订内容基于公开的科学研究和运动医学知识

## 免责声明

本修订版本旨在提供更科学的训练指导，但任何训练计划都应根据个人情况调整。开始任何新的训练计划前，请咨询专业医疗人员或认证教练。训练过程中如有不适，请立即停止并寻求专业帮助。

## 致谢

- 感谢保罗·威德创作了《囚徒健身》这部经典著作
- 感谢所有为运动科学研究做出贡献的学者和专家
- 感谢 Gemini 3 AI 提供的智能

## 许可证

本项目采用 [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/) 许可证。

---

**最后更新**: 2026-02-10
