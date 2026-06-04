#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
批量重命名文件（支持多种规则）

功能：批量重命名指定目录下的文件，支持多种命名规则
用法：python3 rename_files.py [目录] [规则] [选项]

规则说明：
  prefix     - 添加前缀：python3 rename_files.py ./files prefix "项目_"
  suffix     - 添加后缀：python3 rename_files.py ./files suffix "_v2"
  replace    - 替换文字：python3 rename_files.py ./files replace "旧文字" "新文字"
  number     - 数字编号：python3 rename_files.py ./files number "文件_" 1
  sequence   - 序号重命名：python3 rename_files.py ./files sequence "图片" 1
  lower      - 转为小写：python3 rename_files.py ./files lower
  upper      - 转为大写：python3 rename_files.py ./files upper
  strip      - 去除空格：python3 rename_files.py ./files strip

参数：
  目录      - 要处理的文件目录（默认：当前目录）
  规则      - 重命名规则（prefix/suffix/replace/number/sequence/lower/upper/strip）
  规则参数  - 根据规则不同，传入对应的参数

示例：
  python3 rename_files.py ./docs prefix "2024_"
  python3 rename_files.py ./photos number "照片_" 1
  python3 rename_files.py ./data replace "old" "new"
  python3 rename_files.py ./docs lower
"""

import os
import sys
import re


def get_files(directory):
    """获取目录中所有文件（排除目录本身）"""
    all_items = os.listdir(directory)
    files = []
    for item in sorted(all_items):
        full_path = os.path.join(directory, item)
        if os.path.isfile(full_path) and not item.startswith("."):
            files.append(item)
    return files


def safe_rename(src_dir, old_name, new_name):
    """安全重命名文件，处理文件名冲突"""
    src_path = os.path.join(src_dir, old_name)
    dst_path = os.path.join(src_dir, new_name)

    if old_name == new_name:
        return True, "不变"

    if os.path.exists(dst_path):
        # 文件名冲突，添加编号
        base, ext = os.path.splitext(new_name)
        counter = 1
        while os.path.exists(os.path.join(src_dir, "{}_{}{}".format(base, counter, ext))):
            counter += 1
        new_name = "{}_{}{}".format(base, counter, ext)
        dst_path = os.path.join(src_dir, new_name)

    try:
        os.rename(src_path, dst_path)
        return True, new_name
    except Exception as e:
        return False, str(e)


def apply_rule(rule, params, filename):
    """根据规则生成新文件名"""
    base, ext = os.path.splitext(filename)

    if rule == "prefix":
        prefix = params[0] if params else ""
        return prefix + filename

    elif rule == "suffix":
        suffix = params[0] if params else ""
        return base + suffix + ext

    elif rule == "replace":
        if len(params) >= 2:
            return filename.replace(params[0], params[1])
        return filename

    elif rule == "lower":
        return filename.lower()

    elif rule == "upper":
        return filename.upper()

    elif rule == "strip":
        # 去除首尾空格，并将中间多个空格替换为单个
        new_base = re.sub(r'\s+', ' ', base.strip())
        return new_base + ext

    elif rule == "number":
        prefix = params[0] if params else "file_"
        try:
            start = int(params[1]) if len(params) > 1 else 1
        except ValueError:
            start = 1
        return filename  # 占位，实际由batch_rename处理

    elif rule == "sequence":
        prefix = params[0] if params else "file_"
        try:
            start = int(params[1]) if len(params) > 1 else 1
        except ValueError:
            start = 1
        return filename  # 占位，实际由batch_rename处理

    return filename


def batch_rename(directory, rule, params):
    """执行批量重命名"""
    files = get_files(directory)
    if not files:
        print("目录 '{}' 中没有找到文件".format(directory))
        return

    print("目录：{}".format(directory))
    print("规则：{} {}".format(rule, " ".join(params)))
    print("找到 {} 个文件".format(len(files)))
    print("-" * 50)

    success_count = 0
    skip_count = 0
    fail_count = 0

    # 对于编号和序列规则，需要跟踪索引
    if rule == "number":
        try:
            start = int(params[1]) if len(params) > 1 else 1
        except (ValueError, IndexError):
            start = 1
        prefix = params[0] if params else "file_"

        for idx, filename in enumerate(files):
            base, ext = os.path.splitext(filename)
            new_name = "{}{:03d}{}".format(prefix, start + idx, ext)
            ok, msg = safe_rename(directory, filename, new_name)
            _print_result(filename, msg, ok)
            if ok:
                success_count += 1
            elif msg == "不变":
                skip_count += 1
            else:
                fail_count += 1

    elif rule == "sequence":
        try:
            start = int(params[1]) if len(params) > 1 else 1
        except (ValueError, IndexError):
            start = 1
        prefix = params[0] if params else "file_"

        for idx, filename in enumerate(files):
            base, ext = os.path.splitext(filename)
            new_name = "{}{:03d}{}".format(prefix, start + idx, ext)
            ok, msg = safe_rename(directory, filename, new_name)
            _print_result(filename, msg, ok)
            if ok:
                success_count += 1
            elif msg == "不变":
                skip_count += 1
            else:
                fail_count += 1

    else:
        for filename in files:
            new_name = apply_rule(rule, params, filename)
            ok, msg = safe_rename(directory, filename, new_name)
            _print_result(filename, msg, ok)
            if ok:
                success_count += 1
            elif msg == "不变":
                skip_count += 1
            else:
                fail_count += 1

    print("-" * 50)
    print("✓ 完成！成功：{} | 跳过：{} | 失败：{}".format(success_count, skip_count, fail_count))


def _print_result(old_name, msg, success):
    """统一打印重命名结果"""
    if success:
        print("  ✓ {} -> {}".format(old_name, msg))
    elif msg == "不变":
        print("  - {} (不变)".format(old_name))
    else:
        print("  ✗ {} -> 失败：{}".format(old_name, msg))


def show_help():
    """显示帮助信息"""
    help_text = """
批量重命名文件工具

用法：python3 rename_files.py [目录] [规则] [参数...]

规则：
  prefix  添加前缀    示例：python3 rename_files.py . prefix "项目_"
  suffix  添加后缀    示例：python3 rename_files.py . suffix "_v2"
  replace 替换文字    示例：python3 rename_files.py . replace "旧" "新"
  number  数字编号    示例：python3 rename_files.py . number "文件_" 1
  sequence 序号重命名 示例：python3 rename_files.py . sequence "图片" 1
  lower   转为小写    示例：python3 rename_files.py . lower
  upper   转为大写    示例：python3 rename_files.py . upper
  strip   去除空格    示例：python3 rename_files.py . strip
"""
    print(help_text)


def main():
    """主函数"""
    if len(sys.argv) < 2 or sys.argv[1] in ("-h", "--help", "help"):
        show_help()
        sys.exit(0)

    directory = sys.argv[1]
    rule = sys.argv[2] if len(sys.argv) > 2 else None

    if not os.path.isdir(directory):
        print("错误：目录 '{}' 不存在".format(directory))
        sys.exit(1)

    if not rule:
        print("错误：请指定重命名规则")
        show_help()
        sys.exit(1)

    valid_rules = ["prefix", "suffix", "replace", "number", "sequence", "lower", "upper", "strip"]
    if rule not in valid_rules:
        print("错误：不支持的重命名规则 '{}'".format(rule))
        print("可用规则：{}".format(", ".join(valid_rules)))
        sys.exit(1)

    params = sys.argv[3:]
    batch_rename(directory, rule, params)


if __name__ == "__main__":
    main()
