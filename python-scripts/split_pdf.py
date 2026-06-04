#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
拆分PDF为单页文件

功能：将一个PDF文件的每一页拆分为独立的PDF文件
用法：python3 split_pdf.py [源PDF] [输出目录] [前缀]

参数：
  源PDF     - 要拆分的PDF文件路径
  输出目录  - 保存单页PDF的目录（默认：split_pdf_output）
  前缀      - 输出文件名前缀（默认：page）

依赖：
  pip install PyPDF2

示例：
  python3 split_pdf.py document.pdf
  python3 split_pdf.py report.pdf ./pages 报告
"""

import os
import sys

try:
    from PyPDF2 import PdfReader, PdfWriter
except ImportError:
    print("错误：请先安装 PyPDF2：pip install PyPDF2")
    sys.exit(1)


def split_pdf(pdf_path, output_dir, prefix):
    """将PDF拆分为单页文件"""
    # 读取PDF
    try:
        reader = PdfReader(pdf_path)
    except Exception as e:
        print("错误：无法读取PDF文件 '{}'：{}".format(pdf_path, e))
        sys.exit(1)

    page_count = len(reader.pages)
    if page_count == 0:
        print("错误：PDF文件为空")
        sys.exit(1)

    print("文件：{}".format(os.path.basename(pdf_path)))
    print("总页数：{} 页".format(page_count))

    # 创建输出目录
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # 获取原文件名（不含扩展名），用于生成文件名
    base_name = os.path.splitext(os.path.basename(pdf_path))[0]

    success_count = 0

    for i in range(page_count):
        page_num = i + 1
        # 生成带前导零的文件名（如 page_001.pdf）
        filename = "{}_{}_{:03d}.pdf".format(prefix, base_name, page_num)
        filepath = os.path.join(output_dir, filename)

        try:
            writer = PdfWriter()
            writer.add_page(reader.pages[i])

            with open(filepath, "wb") as f:
                writer.write(f)

            print("[{}/{}] {}".format(page_num, page_count, filename))
            success_count += 1
        except Exception as e:
            print("[{}/{}] ✗ 保存第{}页失败：{}".format(page_num, page_count, page_num, e))

    print("\n✓ 拆分完成！成功提取 {} / {} 页".format(success_count, page_count))
    print("  输出目录：{}".format(os.path.abspath(output_dir)))


def main():
    """主函数"""
    if len(sys.argv) < 2:
        print("用法：python3 split_pdf.py [源PDF] [输出目录] [前缀]")
        print("示例：python3 split_pdf.py document.pdf")
        sys.exit(1)

    pdf_path = sys.argv[1]
    if not os.path.isfile(pdf_path):
        print("错误：文件 '{}' 不存在".format(pdf_path))
        sys.exit(1)

    output_dir = sys.argv[2] if len(sys.argv) > 2 else "split_pdf_output"
    prefix = sys.argv[3] if len(sys.argv) > 3 else "page"

    split_pdf(pdf_path, output_dir, prefix)


if __name__ == "__main__":
    main()
