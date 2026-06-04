#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
文件夹增量备份工具

功能：将源目录增量备份到目标目录（仅复制新增或修改过的文件）
用法：python3 folder_backup.py [源目录] [备份目录] [模式]

参数：
  源目录    - 要备份的文件夹路径
  备份目录  - 备份文件保存目录（默认：backup_YYYYMMDD_HHMMSS）
  模式      - backup(备份模式) / restore(恢复模式)（默认：backup）

说明：
  - 增量备份：仅复制源目录中新增或修改过的文件
  - 保留目录结构
  - 通过比较文件大小和修改时间判断文件是否变更
  - 支持排除隐藏文件/目录

示例：
  python3 folder_backup.py /home/user/projects ./my_backup
  python3 folder_backup.py /home/user/projects /backup/projects backup
  python3 folder_backup.py /backup/projects /home/user/projects restore
"""

import os
import sys
import shutil
import time
from datetime import datetime


def get_file_signature(filepath):
    """获取文件签名（大小+修改时间），用于判断文件是否变更"""
    try:
        stat = os.stat(filepath)
        return (stat.st_size, stat.st_mtime)
    except OSError:
        return None


def should_skip(name):
    """判断是否应跳过文件/目录"""
    return name.startswith(".")


def build_file_list(directory, base_path=""):
    """递归构建文件列表，返回相对路径列表"""
    file_list = []
    try:
        entries = sorted(os.listdir(directory))
    except PermissionError:
        print("  警告：无权限访问 '{}'".format(directory))
        return file_list

    for entry in entries:
        if should_skip(entry):
            continue

        rel_path = os.path.join(base_path, entry) if base_path else entry
        full_path = os.path.join(directory, entry)

        try:
            if os.path.isfile(full_path):
                file_list.append(rel_path)
            elif os.path.isdir(full_path):
                file_list.extend(build_file_list(full_path, rel_path))
        except PermissionError:
            print("  警告：无权限访问 '{}'".format(full_path))

    return file_list


def backup(source_dir, backup_dir):
    """执行增量备份"""
    if not os.path.isdir(source_dir):
        print("错误：源目录 '{}' 不存在".format(source_dir))
        sys.exit(1)

    if not os.path.exists(backup_dir):
        os.makedirs(backup_dir)
        print("创建备份目录：{}".format(backup_dir))

    print("源目录：{}".format(source_dir))
    print("备份目录：{}".format(backup_dir))
    print("模式：增量备份")
    print("-" * 50)

    # 构建源文件列表
    source_files = build_file_list(source_dir)
    print("源目录文件数：{}".format(len(source_files)))

    copied_count = 0
    skipped_count = 0
    error_count = 0
    total_size = 0

    for rel_path in source_files:
        src_path = os.path.join(source_dir, rel_path)
        dst_path = os.path.join(backup_dir, rel_path)

        # 确保目标子目录存在
        dst_subdir = os.path.dirname(dst_path)
        if dst_subdir and not os.path.exists(dst_subdir):
            os.makedirs(dst_subdir)

        # 判断是否需要复制
        need_copy = False
        if not os.path.exists(dst_path):
            need_copy = True
            reason = "新增"
        else:
            src_sig = get_file_signature(src_path)
            dst_sig = get_file_signature(dst_path)
            if src_sig and dst_sig and src_sig != dst_sig:
                need_copy = True
                reason = "已修改"
            else:
                skipped_count += 1
                continue

        # 执行复制
        try:
            shutil.copy2(src_path, dst_path)
            file_size = os.path.getsize(src_path)
            total_size += file_size
            copied_count += 1
            print("  [{}] {} ({})".format(reason, rel_path, _format_size(file_size)))
        except Exception as e:
            print("  [✗] {} 复制失败：{}".format(rel_path, e))
            error_count += 1

    print("-" * 50)
    print("✓ 备份完成！")
    print("  新增/更新：{} 个文件".format(copied_count))
    print("  跳过（未变更）：{} 个文件".format(skipped_count))
    print("  失败：{} 个文件".format(error_count))
    print("  总数据量：{}".format(_format_size(total_size)))


def restore(backup_dir, target_dir):
    """从备份恢复文件"""
    if not os.path.isdir(backup_dir):
        print("错误：备份目录 '{}' 不存在".format(backup_dir))
        sys.exit(1)

    if not os.path.exists(target_dir):
        os.makedirs(target_dir)
        print("创建目标目录：{}".format(target_dir))

    print("备份目录：{}".format(backup_dir))
    print("目标目录：{}".format(target_dir))
    print("模式：恢复")
    print("-" * 50)

    backup_files = build_file_list(backup_dir)
    print("备份文件数：{}".format(len(backup_files)))

    restored_count = 0
    error_count = 0

    for rel_path in backup_files:
        src_path = os.path.join(backup_dir, rel_path)
        dst_path = os.path.join(target_dir, rel_path)

        dst_subdir = os.path.dirname(dst_path)
        if dst_subdir and not os.path.exists(dst_subdir):
            os.makedirs(dst_subdir)

        try:
            shutil.copy2(src_path, dst_path)
            restored_count += 1
            print("  [恢复] {}".format(rel_path))
        except Exception as e:
            print("  [✗] {} 恢复失败：{}".format(rel_path, e))
            error_count += 1

    print("-" * 50)
    print("✓ 恢复完成！成功：{} | 失败：{}".format(restored_count, error_count))


def _format_size(size_bytes):
    """格式化文件大小"""
    if size_bytes < 1024:
        return "{} B".format(size_bytes)
    elif size_bytes < 1024 * 1024:
        return "{:.1f} KB".format(size_bytes / 1024)
    else:
        return "{:.1f} MB".format(size_bytes / (1024 * 1024))


def main():
    """主函数"""
    if len(sys.argv) < 2:
        print("用法：python3 folder_backup.py [源目录] [备份目录] [模式]")
        print("示例：")
        print("  python3 folder_backup.py ./myproject")  # 备份到时间戳目录
        print("  python3 folder_backup.py ./myproject ./backup")
        print("  python3 folder_backup.py ./backup ./restored restore")
        sys.exit(1)

    source_dir = os.path.abspath(sys.argv[1])

    # 生成默认备份目录名（含时间戳）
    if len(sys.argv) > 2:
        backup_dir = os.path.abspath(sys.argv[2])
    else:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_dir = os.path.abspath("backup_" + timestamp)

    mode = sys.argv[3].lower() if len(sys.argv) > 3 else "backup"

    if mode == "backup":
        backup(source_dir, backup_dir)
    elif mode == "restore":
        restore(source_dir, backup_dir)
    else:
        print("错误：不支持的模式 '{}'，请使用 backup 或 restore".format(mode))
        sys.exit(1)


if __name__ == "__main__":
    main()
