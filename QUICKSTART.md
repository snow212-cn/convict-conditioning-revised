# 快速开始指南

## 🚀 发布到 GitHub 的步骤

### 1. 初始化 Git 仓库（如果还没有）

```bash
cd d:/Downloads/Programs/qiutu
git init
```

### 2. 添加所有文件

```bash
git add .
```

### 3. 创建初始提交

```bash
git commit -m "初始提交：囚徒健身科学修订版项目"
```

### 4. 在 GitHub 上创建新仓库

1. 访问 https://github.com/new
2. 仓库名称：`convict-conditioning-revised` (或您喜欢的名称)
3. 描述：`囚徒健身 - 科学修订版 | Convict Conditioning - Scientific Revision`
4. 选择 Public 或 Private
5. **不要**勾选 "Initialize this repository with a README"
6. 点击 "Create repository"

### 5. 关联远程仓库并推送

```bash
# 替换 YOUR_USERNAME 为您的 GitHub 用户名
git remote add origin https://github.com/YOUR_USERNAME/convict-conditioning-revised.git

# 推送到 GitHub
git branch -M main
git push -u origin main
```

### 6. 启用 GitHub Actions

1. 进入仓库的 Settings → Actions → General
2. 在 "Workflow permissions" 部分选择 "Read and write permissions"
3. 勾选 "Allow GitHub Actions to create and approve pull requests"
4. 点击 "Save"

### 7. 测试自动化工作流

#### 方法 1：手动触发

1. 进入仓库的 Actions 标签页
2. 选择 "构建电子书并发布" 工作流
3. 点击 "Run workflow"
4. 选择 main 分支
5. 点击 "Run workflow" 按钮

#### 方法 2：修改文件触发

```bash
# 修改任意章节文件
echo "\n\n测试更新" >> revised_book_v2/00_Title.md

# 提交并推送
git add revised_book_v2/00_Title.md
git commit -m "测试自动构建工作流"
git push origin main
```

### 8. 查看构建结果

1. 进入 Actions 标签页查看工作流运行状态
2. 等待工作流完成（通常需要 2-5 分钟）
3. 进入 Releases 标签页查看自动创建的发布版本
4. 下载生成的电子书文件

## 📝 日常使用流程

### 修改章节内容

```bash
# 1. 编辑章节文件
code revised_book_v2/05_Chapter5_Pushups.md

# 2. 提交更改
git add revised_book_v2/05_Chapter5_Pushups.md
git commit -m "更新第5章：俯卧撑训练内容"

# 3. 推送到 GitHub
git push origin main

# 4. GitHub Actions 自动构建并发布新版本
```

### 本地测试构建

```bash
# 合并章节
python scripts/merge_chapters.py

# 生成电子书
python scripts/build_ebook.py

# 查看生成的文件
ls -lh Convict_Conditioning_Revised_Complete.*
```

## ⚠️ 注意事项

### 1. ��件编码

确保所有 Markdown 文件使用 UTF-8 编码，避免中文乱码。

### 2. 文件命名

章节文件必须按照数字顺序命名（00-12），以确保正确的合并顺序。

### 3. Git 配置

首次使用 Git 需要配置用户信息：

```bash
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

### 4. 大文件处理

如果遇到大文件推送问题，可以使用 Git LFS：

```bash
# 安装 Git LFS
git lfs install

# 追踪大文件
git lfs track "*.epub"
git lfs track "*.pdf"

# 提交 .gitattributes
git add .gitattributes
git commit -m "配置 Git LFS"
```

### 5. 私有仓库

如果使用私有仓库，确保：
- GitHub Actions 有足够的分钟数配额
- 协作者有适当的访问权限

## 🔧 故障排除

### 问题 1：推送被拒绝

```bash
# 先拉取远程更改
git pull origin main --rebase

# 再推送
git push origin main
```

### 问题 2：工作流权限错误

检查仓库设置中的 Actions 权限是否正确配置。

### 问题 3：Release 创建失败

确保没有同名的 tag 已存在。如需重新发布，先删除旧的 tag：

```bash
# 删除本地 tag
git tag -d v2026.02.10

# 删除远程 tag
git push origin :refs/tags/v2026.02.10
```

## 📚 更多资源

- [完整文档](DOCUMENTATION.md)
- [项目说明](README.md)
- [GitHub Actions 文档](https://docs.github.com/en/actions)
- [Pandoc 文档](https://pandoc.org/MANUAL.html)

## 🎉 完成！

现在您的项目已经成功发布到 GitHub，并配置了自动化构建流程。每次修改章节文件并推送后，都会自动生成新版本的电子书！
