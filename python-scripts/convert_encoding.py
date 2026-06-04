#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
批量转换文本文件编码

功能：批量转换指定目录下文本文件的编码格式
用法：python3 convert_encoding.py [源目录] [源编码] [目标编码] [输出目录] [扩展名]

参数：
  源目录    - 文本文件所在目录（默认：当前目录）
  源编码    - 当前文件编码（默认：gbk）
  目标编码  - 目标编码（默认：utf-8）
  输出目录  - 转换后文件保存目录（默认：converted_encoding）
  扩展名    - 文件扩展名筛选（默认：.txt）

常用编码：
  gbk, gb2312, utf-8, utf-8-sig, ascii, latin-1, big5, shift_jis

示例：
  python3 convert_encoding.py ./data gbk utf-8
  python3 convert_encoding.py ./docs gb2312 utf-8-sig ./output .csv
  python3 convert_encoding.py ./files latin-1 utf-8 ./utf8_files .py
"""

import os
import sys
import glob


def get_text_files(directory, extension):
    """获取指定扩展名的文本文件"""
    pattern = os.path.join(directory, "*" + extension)
    files = glob.glob(pattern)
    # 也匹配大写扩展名
    pattern_upper = os.path.join(directory, "*" + extension.upper())
    files.extend(glob.glob(pattern_upper))
    return sorted(set(files))


def detect_possible_encodings(content_bytes):
    """尝试检测文件编码"""
    import codecs
    encodings = ['utf-8', 'gbk', 'gb2312', 'latin-1', 'shift_jis', 'big5', 'euc-kr']
    for enc in encodings:
        try:
            content_bytes.decode(enc)
            return enc
        except (UnicodeDecodeError, LookupError):
            continue
    return None


def convert_file(file_path, source_enc, target_enc, output_dir):
    """转换单个文件的编码"""
    file_name = os.path.basename(file_path)
    output_path = os.path.join(output_dir, file_name)

    try:
        # 读取原始文件（二进制模式）
        with open(file_path, "rb") as f:
            raw_data = f.read()
    except Exception as e:
        return False, "读取失败：{}".format(e)

    # 如果源编码为 auto，尝试自动检测
    if source_enc == "auto":
        detected = detect_possible_encodings(raw_data)
        if detected is None:
            return False, "无法自动检测编码"
        source_enc_actual = detected
    else:
        source_enc_actual = source_enc

    # 解码
    try:
        text = raw_data.decode(source_enc_actual)
    except UnicodeDecodeError:
        # 尝试用带忽略的方式解码
        try:
            text = raw_data.decode(source_enc_actual, errors="replace")
            print("  注意：部分字符无法解码，已替换为 ?")
        except Exception as e:
            return False, "解码失败（{}）：{}".format(source_enc_actual, e)
    except LookupError:
        return False, "不支持的编码：{}".format(source_enc_actual)

    # 编码并写入
    try:
        with open(output_path, "w", encoding=target_enc) as f:
            f.write(text)
        return True, "{} -> {}".format(source_enc_actual, target_enc)
    except Exception as e:
        return False, "写入失败：{}".format(e)


def batch_convert(source_dir, source_enc, target_enc, output_dir, extension):
    """批量转换编码"""
    files = get_text_files(source_dir, extension)

    if not files:
        print("目录 '{}' 中未找到 *{} 文件".format(source_dir, extension))
        sys.exit(1)

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    print("源编码：{} | 目标编码：{} | 扩展名：*{}".format(source_enc, target_enc, extension))
    print("找到 {} 个文件".format(len(files)))
    print("-" * 50)

    success_count = 0
    fail_count = 0

    for idx, file_path in enumerate(files, 1):
        file_name = os.path.basename(file_path)
        print("[{}/{}] {}".format(idx, len(files), file_name), end=" ")

        result, msg = convert_file(file_path, source_enc, target_enc, output_dir)

        if result:
            print("-> ✓ {}".format(msg))
            success_count += 1
        else:
            print("-> ✗ {}".format(msg))
            fail_count += 1

    print("-" * 50)
    print("✓ 完成！成功：{} | 失败：{}".format(success_count, fail_count))
    print("  输出目录：{}".format(os.path.abspath(output_dir)))


def main():
    """主函数"""
    source_dir = "."
    source_enc = "gbk"
    target_enc = "utf-8"
    output_dir = "converted_encoding"
    extension = ".txt"

    if len(sys.argv) > 1:
        source_dir = sys.argv[1]
    if len(sys.argv) > 2:
        source_enc = sys.argv[2]
    if len(sys.argv) > 3:
        target_enc = sys.argv[3]
    if len(sys.argv) > 4:
        output_dir = sys.argv[4]
    if len(sys.argv) > 5:
        extension = sys.argv[5]
        if not extension.startswith("."):
            extension = "." + extension

    if not os.path.isdir(source_dir):
        print("错误：目录 '{}' 不存在".format(source_dir))
        sys.exit(1)

    batch_convert(source_dir, source_enc, target_enc, output_dir, extension)


if __name__ == "__main__":
    main()
