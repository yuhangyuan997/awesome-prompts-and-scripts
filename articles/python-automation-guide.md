# Python办公自动化：12个脚本让你告别重复工作

> 发布于 2025年6月

## 为什么你需要这些脚本？

每天花1小时手动处理Excel、重命名文件、压缩图片？这些重复工作完全可以用Python自动化。

我整理了**12个可直接运行的Python脚本**，覆盖日常办公中最常见的工作场景。

## 脚本清单

### 1. Excel合并（merge_excel.py）
一键合并多个Excel文件为一个，支持不同工作表结构。

### 2. Excel拆分（split_excel.py）
按某列的值，将一个大Excel拆分为多个小文件。

### 3. Excel转CSV（excel_to_csv.py）
批量将Excel文件转为CSV格式，方便导入数据库。

### 4. PDF合并（merge_pdf.py）
将多个PDF文件合并为一个，支持自定义顺序。

### 5. PDF拆分（split_pdf.py）
将PDF按页拆分为单独文件。

### 6. 批量重命名（rename_files.py）
支持8种重命名规则：添加前缀、替换文字、编号排序等。

### 7. 图片压缩（compress_images.py）
批量压缩图片大小，保持清晰度，节省存储空间。

### 8. 图片缩放（resize_images.py）
批量调整图片尺寸，3种缩放模式可选。

### 9. 查找重复文件（find_duplicate_files.py）
基于SHA256哈希，快速查找硬盘中的重复文件。

### 10. 批量转编码（convert_encoding.py）
批量转换文本文件编码（如GBK转UTF-8）。

### 11. 文件夹备份（folder_backup.py）
增量备份文件夹，只复制新增和修改的文件。

### 12. 批量查找替换（text_search_replace.py）
在多个文件中批量查找替换文字，支持正则表达式。

## 如何使用

### 环境要求
- Python 3.6+
- 安装依赖：`pip install openpyxl pillow`

### 运行示例
```bash
# 合并Excel
python3 merge_excel.py -i ./文件夹/ -o 合并结果.xlsx

# 批量重命名
python3 rename_files.py -p "报告_" ./文件/
```

## 获取完整版

[>> 前往数字产品小铺 <<](https://yuhangyuan997.github.io/awesome-prompts-and-scripts/buy.html?product=py)

定价仅 **¥1.0**，凭诚信付款，输入交易单号即可下载。
