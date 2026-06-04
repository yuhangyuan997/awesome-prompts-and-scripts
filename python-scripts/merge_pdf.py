#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
合并多个PDF文件为一个

功能：将指定目录下的多个PDF文件合并为一个PDF文件
用法：python3 merge_pdf.py [源目录/文件列表] [输出文件]

参数：
  源目录/文件列表 - PDF文件目录，或以逗号分隔的文件路径列表（默认：当前目录）
  输出文件        - 合并后的PDF路径（默认：merged_output.pdf）

依赖：
  pip install PyPDF2

示例：
  python3 merge_pdf.py ./pdfs ./合并结果.pdf
  python3 merge_pdf.py "file1.pdf,file2.pdf,file3.pdf" output.pdf
"""

import os
import sys
import glob

try:
    from PyPDF2 import PdfReader, PdfWriter
except ImportError:
    print("错误：请先安装 PyPDF2：pip install PyPDF2")
    sys.exit(1)


def get_pdf_files(source):
    """获取所有PDF文件路径"""
    files = []

    # 如果输入包含逗号，视为文件列表
    if "," in source and not os.path.isdir(source):
        parts = [s.strip() for s in source.split(",")]
        for p in parts:
            if os.path.isfile(p):
                files.append(p)
            else:
                print("  警告：文件不存在 '{}'".format(p))
    elif os.path.isfile(source):
        files = [source]
    elif os.path.isdir(source):
        files = sorted(glob.glob(os.path.join(source, "*.pdf")))
    else:
        print("错误：路径 '{}' 无效".format(source))
        sys.exit(1)

    return files


def merge_pdfs(pdf_files, output_file):
    """合并多个PDF文件"""
    writer = PdfWriter()
    total_pages = 0

    for idx, file_path in enumerate(pdf_files, 1):
        file_name = os.path.basename(file_path)
        print("[{}/{}] 读取: {}".format(idx, len(pdf_files), file_name))

        try:
            reader = PdfReader(file_path)
            page_count = len(reader.pages)

            for page in reader.pages:
                writer.add_page(page)

            total_pages += page_count
            print("  -> {} 页".format(page_count))
        except Exception as e:
            print("  ✗ 读取失败：{}".format(e))

    if total_pages == 0:
        print("错误：没有读取到任何有效PDF页面")
        sys.exit(1)

    # 写入合并文件
    try:
        with open(output_file, "wb") as f:
            writer.write(f)
        print("\n✓ 合并完成！共 {} 页".format(total_pages))
        print("  输出文件：{}".format(os.path.abspath(output_file)))
    except Exception as e:
        print("错误：保存文件失败：{}".format(e))
        sys.exit(1)


def main():
    """主函数"""
    source = "."
    output_file = "merged_output.pdf"

    if len(sys.argv) > 1:
        source = sys.argv[1]
    if len(sys.argv) > 2:
        output_file = sys.argv[2]

    # 确保输出目录存在
    output_dir = os.path.dirname(os.path.abspath(output_file))
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)

    pdf_files = get_pdf_files(source)

    if not pdf_files:
        print("错误：未找到任何PDF文件")
        sys.exit(1)

    print("找到 {} 个PDF文件，开始合并...".format(len(pdf_files)))
    merge_pdfs(pdf_files, output_file)


if __name__ == "__main__":
    main()
