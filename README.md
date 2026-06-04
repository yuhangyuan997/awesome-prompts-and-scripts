# 🐍 Python办公自动化脚本合集

> **12个实用脚本 · 一键搞定重复工作 · 告别手动操作**
>
> *适用于 Windows / macOS / Linux 全平台*

**定价：¥4.9**

---

## 📦 包含脚本

| # | 脚本名称 | 核心功能 | 依赖 |
|---|---------|---------|------|
| 1 | **merge_excel.py** | 合并多个Excel文件为一个，支持多Sheet合并 | openpyxl |
| 2 | **split_excel.py** | 按指定列的值拆分Excel为多个独立文件 | openpyxl |
| 3 | **excel_to_csv.py** | 批量将Excel(.xlsx)转换为CSV格式 | openpyxl |
| 4 | **merge_pdf.py** | 合并多个PDF文件为一个完整文档 | PyPDF2 |
| 5 | **split_pdf.py** | 将PDF按页拆分为独立单页文件 | PyPDF2 |
| 6 | **rename_files.py** | 批量重命名文件（前缀/后缀/替换/编号/大小写转换） | 标准库 |
| 7 | **compress_images.py** | 批量压缩图片，减小文件体积（支持JPG/PNG/BMP/WebP） | Pillow |
| 8 | **resize_images.py** | 批量调整图片尺寸（适应/填充/裁剪三种模式） | Pillow |
| 9 | **find_duplicate_files.py** | 查找重复文件（SHA256哈希比对，找出冗余文件） | 标准库 |
| 10 | **convert_encoding.py** | 批量转换文本文件编码（GBK→UTF-8等） | 标准库 |
| 11 | **folder_backup.py** | 文件夹增量备份（仅复制新增/修改的文件） | 标准库 |
| 12 | **text_search_replace.py** | 批量文本查找替换（支持正则，自动备份原文件） | 标准库 |

---

## 🔧 环境要求

### 系统要求
- Python 3.6 或更高版本
- 操作系统：Windows / macOS / Linux

### 安装依赖

大多数脚本使用 **Python标准库**，可直接运行。仅4个脚本需要安装额外依赖：

```bash
# 安装所有依赖（推荐）
pip install openpyxl pillow PyPDF2
```

| 依赖 | 版本 | 使用脚本 |
|------|------|---------|
| openpyxl | ≥3.0 | merge_excel.py, split_excel.py, excel_to_csv.py |
| Pillow | ≥8.0 | compress_images.py, resize_images.py |
| PyPDF2 | ≥3.0 | merge_pdf.py, split_pdf.py |

### 验证安装

```bash
python3 -c "import openpyxl; print('openpyxl OK')"
python3 -c "from PIL import Image; print('Pillow OK')"
python3 -c "import PyPDF2; print('PyPDF2 OK')"
```

---

## 📖 使用示例

### 1️⃣ 合并Excel文件 — merge_excel.py
```bash
# 合并当前目录下所有Excel文件
python3 merge_excel.py

# 指定源目录和输出文件
python3 merge_excel.py ./月度报表 ./年度汇总.xlsx
```

### 2️⃣ 拆分Excel文件 — split_excel.py
```bash
# 按"部门"列拆分
python3 split_excel.py 员工数据.xlsx 部门

# 按"城市"列拆分，指定输出目录
python3 split_excel.py 销售数据.xlsx 城市 ./按城市拆分
```

### 3️⃣ Excel转CSV — excel_to_csv.py
```bash
# 转换当前目录下所有Excel
python3 excel_to_csv.py

# 指定目录和输出位置
python3 excel_to_csv.py ./excel文件 ./csv文件
```

### 4️⃣ 合并PDF文件 — merge_pdf.py
```bash
# 合并当前目录下所有PDF
python3 merge_pdf.py

# 指定文件列表合并
python3 merge_pdf.py "报告1.pdf,报告2.pdf,报告3.pdf" 总报告.pdf
```

### 5️⃣ 拆分PDF文件 — split_pdf.py
```bash
# 将PDF拆分为单页
python3 split_pdf.py 合同文件.pdf

# 指定输出目录和文件前缀
python3 split_pdf.py 说明书.pdf ./单页 说明
```

### 6️⃣ 批量重命名文件 — rename_files.py
```bash
# 添加前缀
python3 rename_files.py ./照片 prefix "2024旅行_"

# 添加后缀
python3 rename_files.py ./文档 suffix "_v2"

# 替换文字
python3 rename_files.py ./代码 replace "draft" "final"

# 数字编号
python3 rename_files.py ./图片 number "IMG_" 1

# 转为小写
python3 rename_files.py ./文件 lower
```

### 7️⃣ 批量压缩图片 — compress_images.py
```bash
# 默认质量75压缩
python3 compress_images.py ./照片

# 指定输出目录和质量（70%）
python3 compress_images.py ./产品图 ./压缩后 70
```

### 8️⃣ 批量调整图片尺寸 — resize_images.py
```bash
# 调整为宽度800像素，高度等比缩放
python3 resize_images.py ./照片 ./缩放后 800 0

# 调整为1920x1080，适应模式
python3 resize_images.py ./壁纸 ./调整 1920 1080 fit

# 裁剪为150x150缩略图
python3 resize_images.py ./头像 ./缩略 150 150 crop
```

### 9️⃣ 查找重复文件 — find_duplicate_files.py
```bash
# 扫描当前目录
python3 find_duplicate_files.py

# 扫描指定目录，仅检查大于1KB的文件
python3 find_duplicate_files.py ./下载文件 1024
```

### 🔟 批量转换编码 — convert_encoding.py
```bash
# GBK转UTF-8
python3 convert_encoding.py ./文档 gbk utf-8

# 自动检测编码并转换
python3 convert_encoding.py ./数据 auto utf-8 ./utf8输出 .csv
```

### 1️⃣1️⃣ 文件夹增量备份 — folder_backup.py
```bash
# 备份到时间戳目录
python3 folder_backup.py ./项目文件

# 指定备份目录
python3 folder_backup.py ./项目文件 ./备份/项目

# 从备份恢复
python3 folder_backup.py ./备份/项目 ./恢复后的项目 restore
```

### 1️⃣2️⃣ 批量文本查找替换 — text_search_replace.py
```bash
# 简单文字替换
python3 text_search_replace.py ./文档 "旧文字" "新文字"

# 正则表达式替换
python3 text_search_replace.py ./配置 "192\.168\.\d+\.\d+" "10.0.0.1" .conf yes

# 替换多种文件类型
python3 text_search_replace.py ./源码 "copyright 2023" "copyright 2024" .py,.html,.js
```

---

## ⚠️ 注意事项

1. **备份重要数据** — 虽然脚本经过测试，但建议首次使用前先备份重要文件
2. **路径包含空格** — 如果路径包含空格，请用引号包裹：`python3 script.py "./我的文件夹"`
3. **编码问题** — 中文Windows系统默认编码为GBK，macOS/Linux为UTF-8，使用文本相关脚本时注意指定编码
4. **大文件处理** — 处理超大Excel/PDF文件时可能需要较长时间，请耐心等待
5. **PDF依赖** — PDF相关脚本需安装PyPDF2：`pip install PyPDF2`
6. **图片格式** — 图片处理脚本支持 JPG/JPEG/PNG/BMP/WebP 格式
7. **文件权限** — 在Linux/macOS下，确保对目标目录有读写权限
8. **文件占用** — 运行脚本前，请关闭正在使用的Excel/PDF/图片文件
9. **运行参数** — 每个脚本都支持 `-h` 或 `help` 参数查看详细帮助

---

## 🎯 典型应用场景

### 📊 行政/财务
- 合并各部门月度报表 → `merge_excel.py`
- 按部门拆分员工数据 → `split_excel.py`
- Excel数据导出为CSV给系统导入 → `excel_to_csv.py`

### 📄 文档处理
- 合并多个PDF合同 → `merge_pdf.py`
- 拆分PDF为单页分发 → `split_pdf.py`
- 批量替换合同中的模板文字 → `text_search_replace.py`

### 🖼️ 图片处理
- 压缩产品图上传网站 → `compress_images.py`
- 批量调整照片尺寸做统一封面 → `resize_images.py`

### 🗂️ 文件管理
- 给照片添加日期前缀 → `rename_files.py`
- 清理重复的下载文件 → `find_duplicate_files.py`
- 处理乱码文本文件 → `convert_encoding.py`
- 每天备份项目文件 → `folder_backup.py`

---

## 📂 文件结构

```
python-scripts/
├── README.md              # 本说明文件
├── merge_excel.py         # 1. 合并Excel
├── split_excel.py         # 2. 拆分Excel
├── excel_to_csv.py        # 3. Excel转CSV
├── merge_pdf.py           # 4. 合并PDF
├── split_pdf.py           # 5. 拆分PDF
├── rename_files.py        # 6. 批量重命名
├── compress_images.py     # 7. 批量压缩图片
├── resize_images.py       # 8. 批量调整尺寸
├── find_duplicate_files.py # 9. 查找重复文件
├── convert_encoding.py    # 10. 批量转换编码
├── folder_backup.py       # 11. 文件夹备份
└── text_search_replace.py # 12. 批量查找替换
```

---

## 🆘 常见问题

**Q: 运行报错"ModuleNotFoundError: No module named 'openpyxl'"**
A: 运行 `pip install openpyxl` 安装缺失的依赖。

**Q: Mac/Linux提示"Permission denied"**
A: 给脚本添加执行权限：`chmod +x *.py`

**Q: 中文文件名乱码**
A: 确保终端支持UTF-8。Windows下建议在 PowerShell 或 VS Code 终端中运行。

**Q: 脚本可以修改后二次分发吗？**
A: 本产品允许个人学习和内部使用。如需二次分发或作为产品的一部分销售，请联系作者。

---

## 📜 更新日志

**v1.0 (2024-12)**
- 首发12个办公自动化脚本
- 所有脚本支持命令行参数
- 完善的错误处理和中文注释

---

## 📞 联系方式

- CSDN博客：https://blog.csdn.net/（搜索作者）
- 爱发电：https://afdian.com/（搜索作者）

---

📢 **感谢购买！如果觉得好用，欢迎在CSDN点赞、收藏、关注！**
