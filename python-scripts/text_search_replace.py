#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
批量文本查找替换工具

功能：在指定目录的文本文件中批量查找和替换指定文字
用法：python3 text_search_replace.py [目录] [查找文字] [替换文字] [扩展名] [是否正则]

参数：
  目录      - 要处理的文件目录（默认：当前目录）
  查找文字  - 要查找的文本内容（或正则表达式）
  替换文字  - 替换后的文本内容（默认：空字符串，即删除）
  扩展名    - 文件扩展名筛选，用逗号分隔多个（默认：.txt）
  是否正则   - 使用正则表达式：yes/no（默认：no）

说明：
  - 支持递归搜索子目录
  - 默认区分大小写
  - 支持预览模式（先用搜索结果查看匹配情况）
  - 修改前自动备份原文件（添加 .bak 后缀）

示例：
  python3 text_search_replace.py ./docs "旧文字" "新文字"
  python3 text_search_replace.py ./data "company" "COMPANY" .txt,yaml
  python3 text_search_replace.py ./configs "192.168.1." "10.0.0." .conf yes
  python3 text_search_replace.py ./src "print(" "logger.info(" .py  # 删除匹配行
"""

import os
import sys
import re
import shutil

# 默认排除的目录
EXCLUDE_DIRS = {'.git', '__pycache__', 'node_modules', '.svn', '.idea', 'venv', 'env'}


def get_text_files(directory, extensions):
    """递归获取所有符合条件的文本文件"""
    files = []
    extensions_lower = [ext.lower() if ext.startswith('.') else '.' + ext.lower() for ext in extensions]

    for root, dirs, filenames in os.walk(directory):
        # 排除不需要的目录
        dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS and not d.startswith('.')]

        for filename in filenames:
            ext = os.path.splitext(filename)[1].lower()
            if ext in extensions_lower:
                files.append(os.path.join(root, filename))

    return sorted(files)


def count_matches_in_file(filepath, search_pattern, use_regex):
    """统计文件中的匹配次数"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except UnicodeDecodeError:
        # 尝试其他常见编码
        for enc in ['gbk', 'gb2312', 'latin-1']:
            try:
                with open(filepath, 'r', encoding=enc) as f:
                    content = f.read()
                break
            except UnicodeDecodeError:
                continue
        else:
            return -1  # 无法读取

    try:
        if use_regex:
            matches = re.findall(search_pattern, content)
        else:
            matches = content.count(search_pattern)
        return len(matches)
    except re.error as e:
        print("  正则错误：{}".format(e))
        return -2


def replace_in_file(filepath, search_text, replace_text, use_regex, backup=True):
    """在文件中执行查找替换"""
    # 读取文件
    encoding_used = 'utf-8'
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except UnicodeDecodeError:
        for enc in ['gbk', 'gb2312', 'latin-1']:
            try:
                with open(filepath, 'r', encoding=enc) as f:
                    content = f.read()
                encoding_used = enc
                break
            except UnicodeDecodeError:
                continue
        else:
            return False, "无法识别文件编码"

    # 执行替换
    try:
        if use_regex:
            new_content, count = re.subn(search_text, replace_text, content)
        else:
            count = content.count(search_text)
            if count > 0:
                new_content = content.replace(search_text, replace_text)
            else:
                new_content = content
    except re.error as e:
        return False, "正则表达式错误：{}".format(e)

    if count == 0:
        return False, "无匹配内容"

    # 创建备份
    if backup:
        backup_path = filepath + ".bak"
        try:
            shutil.copy2(filepath, backup_path)
        except Exception:
            pass  # 备份失败不影响继续

    # 写入文件
    try:
        with open(filepath, 'w', encoding=encoding_used) as f:
            f.write(new_content)
        return True, "替换 {} 处".format(count)
    except Exception as e:
        return False, "写入失败：{}".format(e)


def show_results(filepath, search_text, use_regex, context_lines=2, max_preview=5):
    """预览匹配结果"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    except UnicodeDecodeError:
        for enc in ['gbk', 'gb2312', 'latin-1']:
            try:
                with open(filepath, 'r', encoding=enc) as f:
                    lines = f.readlines()
                break
            except UnicodeDecodeError:
                continue
        else:
            return

    file_name = os.path.basename(filepath)
    match_count = 0

    for i, line in enumerate(lines, 1):
        stripped = line.rstrip('\n\r')

        if use_regex:
            if re.search(search_text, stripped):
                match_count += 1
                if match_count <= max_preview:
                    # 显示上下文
                    start = max(0, i - 1 - context_lines)
                    end = min(len(lines), i + context_lines)
                    if match_count == 1:
                        print("  --- {} ---".format(file_name))
                    for j in range(start, end):
                        marker = ">>" if j == i - 1 else "  "
                        print("    {} {:{}}|{}".format(
                            marker, j + 1, 4, lines[j].rstrip('\n\r')
                        ))
                    print()
        else:
            if search_text in stripped:
                match_count += 1
                if match_count <= max_preview:
                    start = max(0, i - 1 - context_lines)
                    end = min(len(lines), i + context_lines)
                    if match_count == 1:
                        print("  --- {} ---".format(file_name))
                    for j in range(start, end):
                        marker = ">>" if j == i - 1 else "  "
                        print("    {} {:{}}|{}".format(
                            marker, j + 1, 4, lines[j].rstrip('\n\r')
                        ))
                    print()

    return match_count


def batch_search_replace(directory, search_text, replace_text, extensions, use_regex):
    """批量执行查找替换"""
    files = get_text_files(directory, extensions)

    if not files:
        print("目录 '{}' 中未找到匹配的文件".format(directory))
        sys.exit(1)

    print("搜索目录：{}".format(directory))
    print("查找内容：{}".format(search_text))
    print("替换内容：{}".format(replace_text))
    print("文件类型：{}".format(", ".join(extensions)))
    print("正则模式：{}".format("是" if use_regex else "否"))
    print("找到 {} 个文件".format(len(files)))
    print("-" * 50)

    # 第一阶段：预览匹配结果
    print("【预览匹配结果】")
    total_match_files = 0
    total_matches = 0
    matched_files = []

    for filepath in files:
        count = count_matches_in_file(filepath, search_text, use_regex)
        if count > 0:
            total_match_files += 1
            total_matches += count
            matched_files.append(filepath)

    if total_matches == 0:
        print("未找到任何匹配内容。")
        return

    print("找到 {} 个文件共 {} 处匹配。".format(total_match_files, total_matches))
    print()

    # 显示具体匹配行
    show_count = 0
    for filepath in matched_files[:10]:
        show_results(filepath, search_text, use_regex)
        show_count += 1
        if show_count >= 5:
            remaining = len(matched_files) - show_count
            if remaining > 0:
                print("  ... 还有 {} 个文件未预览".format(remaining))
            break

    # 第二阶段：确认后执行替换
    print("-" * 50)
    print("【执行替换】")

    success_count = 0
    fail_count = 0
    total_replaced = 0

    for filepath in matched_files:
        file_name = os.path.relpath(filepath, directory)
        print("[处理] {}".format(file_name), end=" ")

        success, msg = replace_in_file(filepath, search_text, replace_text, use_regex)

        if success:
            print("-> ✓ {}".format(msg))
            # 提取替换数量
            try:
                count = int(msg.replace("替换 ", "").replace(" 处", ""))
                total_replaced += count
            except ValueError:
                pass
            success_count += 1
        else:
            print("-> {}".format(msg))
            fail_count += 1

    print("-" * 50)
    print("✓ 替换完成！")
    print("  修改文件：{} 个".format(success_count))
    print("  替换次数：{} 处".format(total_replaced))
    print("  失败文件：{} 个".format(fail_count))
    if success_count > 0:
        print("  已自动备份原文件（.bak）")


def main():
    """主函数"""
    if len(sys.argv) < 2 or sys.argv[1] in ("-h", "--help", "help"):
        print("用法：python3 text_search_replace.py [目录] [查找文字] [替换文字] [扩展名] [正则]")
        print("示例：")
        print("  python3 text_search_replace.py ./docs 'old' 'new'")
        print("  python3 text_search_replace.py ./data 'hello' 'hi' .txt,yaml")
        print("  python3 text_search_replace.py ./src '\\d+' '[数字]' .py yes")
        sys.exit(0)

    directory = sys.argv[1]
    search_text = sys.argv[2] if len(sys.argv) > 2 else None
    replace_text = sys.argv[3] if len(sys.argv) > 3 else ""
    raw_extensions = sys.argv[4] if len(sys.argv) > 4 else ".txt"
    use_regex = sys.argv[5].lower() in ("yes", "y", "true", "1", "是") if len(sys.argv) > 5 else False

    if not os.path.isdir(directory):
        print("错误：目录 '{}' 不存在".format(directory))
        sys.exit(1)

    if not search_text:
        print("错误：请指定要查找的文字内容")
        sys.exit(1)

    # 解析扩展名
    extensions = [e.strip() for e in raw_extensions.split(",")]

    batch_search_replace(directory, search_text, replace_text, extensions, use_regex)


if __name__ == "__main__":
    main()
