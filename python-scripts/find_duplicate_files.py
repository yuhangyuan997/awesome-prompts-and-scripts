#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
查找重复文件

功能：扫描指定目录，查找内容重复的文件（基于文件大小和哈希值）
用法：python3 find_duplicate_files.py [目录] [最小大小]

参数：
  目录      - 要扫描的目录路径（默认：当前目录）
  最小大小  - 仅检查大于此大小的文件（字节，默认：1，设为0检查所有）

说明：
  - 先按文件大小分组，再计算SHA256哈希值确认重复
  - 会跳过隐藏文件和目录
  - 符号链接不会被追踪

示例：
  python3 find_duplicate_files.py ./downloads
  python3 find_duplicate_files.py ./data 1024  # 仅检查大于1KB的文件
"""

import os
import sys
import hashlib


def get_all_files(directory, min_size=1):
    """递归获取目录下所有文件"""
    files = []
    for root, dirs, filenames in os.walk(directory):
        # 跳过隐藏目录
        dirs[:] = [d for d in dirs if not d.startswith(".")]
        for filename in filenames:
            # 跳过隐藏文件
            if filename.startswith("."):
                continue
            filepath = os.path.join(root, filename)
            try:
                file_size = os.path.getsize(filepath)
                if file_size >= min_size:
                    files.append((filepath, file_size))
            except (OSError, PermissionError):
                continue
    return files


def calculate_hash(filepath, chunk_size=8192):
    """计算文件的SHA256哈希值"""
    sha256 = hashlib.sha256()
    try:
        with open(filepath, "rb") as f:
            while True:
                chunk = f.read(chunk_size)
                if not chunk:
                    break
                sha256.update(chunk)
        return sha256.hexdigest()
    except (OSError, PermissionError):
        return None


def find_duplicates(directory, min_size):
    """查找重复文件"""
    print("正在扫描目录：{}".format(directory))
    print("最小文件大小：{} 字节".format(min_size))
    print("-" * 50)

    # 第一步：获取所有文件
    all_files = get_all_files(directory, min_size)
    print("找到 {} 个文件（大于 {} 字节）".format(len(all_files), min_size))

    if not all_files:
        print("没有找到任何文件")
        return

    # 第二步：按大小分组
    size_groups = {}
    for filepath, file_size in all_files:
        if file_size not in size_groups:
            size_groups[file_size] = []
        size_groups[file_size].append(filepath)

    # 筛选出大小相同的文件组
    duplicates_by_size = {size: paths for size, paths in size_groups.items() if len(paths) > 1}

    print("按大小分组完成，{} 组大小相同的文件".format(len(duplicates_by_size)))

    if not duplicates_by_size:
        print("未发现重复文件（基于大小比对）")
        return

    # 第三步：计算哈希值确认重复
    hash_groups = {}
    total_checked = 0
    total_possible = sum(len(paths) for paths in duplicates_by_size.values())

    for size, paths in duplicates_by_size.items():
        for filepath in paths:
            total_checked += 1
            if total_checked % 50 == 0:
                print("  进度：{}/{}".format(total_checked, total_possible))

            file_hash = calculate_hash(filepath)
            if file_hash is None:
                continue

            key = (size, file_hash)
            if key not in hash_groups:
                hash_groups[key] = []
            hash_groups[key].append(filepath)

    # 第四步：输出重复结果
    duplicate_groups = {k: v for k, v in hash_groups.items() if len(v) > 1}

    if not duplicate_groups:
        print("\n未发现重复文件（基于内容比对）")
        return

    print("\n" + "=" * 50)
    print("发现 {} 组重复文件：".format(len(duplicate_groups)))
    print("=" * 50)

    total_wasted = 0
    group_num = 0

    for (size, file_hash), paths in sorted(duplicate_groups.items(), key=lambda x: -x[0][0]):
        group_num += 1
        wasted = size * (len(paths) - 1)
        total_wasted += wasted

        print("\n[组 {}] {} 个文件，每个 {} ({:.1f})".format(
            group_num, len(paths),
            _format_size(size), size
        ))

        for i, path in enumerate(paths):
            marker = " [保留]" if i == 0 else ""
            print("  {}. {}{}".format(i + 1, path, marker))

        print("  可释放空间：{}".format(_format_size(wasted)))

    print("\n" + "=" * 50)
    print("总计：{} 组重复文件，共可释放 {}".format(
        len(duplicate_groups), _format_size(total_wasted)
    ))


def _format_size(size_bytes):
    """格式化文件大小显示"""
    if size_bytes < 1024:
        return "{} B".format(size_bytes)
    elif size_bytes < 1024 * 1024:
        return "{:.1f} KB".format(size_bytes / 1024)
    elif size_bytes < 1024 * 1024 * 1024:
        return "{:.1f} MB".format(size_bytes / (1024 * 1024))
    else:
        return "{:.2f} GB".format(size_bytes / (1024 * 1024 * 1024))


def main():
    """主函数"""
    directory = "."
    min_size = 1

    if len(sys.argv) > 1:
        directory = sys.argv[1]
    if len(sys.argv) > 2:
        try:
            min_size = max(0, int(sys.argv[2]))
        except ValueError:
            print("警告：最小大小参数无效，使用默认值 1")
            min_size = 1

    if not os.path.isdir(directory):
        print("错误：目录 '{}' 不存在".format(directory))
        sys.exit(1)

    find_duplicates(directory, min_size)


if __name__ == "__main__":
    main()
