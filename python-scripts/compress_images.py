#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
批量压缩图片大小

功能：批量压缩指定目录下的图片文件，减小文件体积
用法：python3 compress_images.py [源目录] [输出目录] [质量]

参数：
  源目录    - 图片文件所在目录（默认：当前目录）
  输出目录  - 压缩后图片保存目录（默认：compressed_images）
  质量      - JPEG压缩质量 1-100（默认：75，越高越清晰）

支持格式：JPG, JPEG, PNG, BMP, WebP

依赖：
  pip install Pillow

示例：
  python3 compress_images.py ./photos ./compressed 70
  python3 compress_images.py ./images          # 使用默认质量75
"""

import os
import sys
import glob

try:
    from PIL import Image
except ImportError:
    print("错误：请先安装 Pillow：pip install Pillow")
    sys.exit(1)

# 支持的图片格式
SUPPORTED_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.bmp', '.webp'}


def get_image_files(directory):
    """获取目录下所有支持的图片文件"""
    files = []
    for ext in SUPPORTED_EXTENSIONS:
        pattern = os.path.join(directory, "*" + ext)
        files.extend(glob.glob(pattern))
        pattern = os.path.join(directory, "*" + ext.upper())
        files.extend(glob.glob(pattern))
    return sorted(files)


def compress_image(input_path, output_path, quality):
    """压缩单张图片"""
    try:
        img = Image.open(input_path)
    except Exception as e:
        return False, "无法打开图片：{}".format(e)

    original_size = os.path.getsize(input_path)
    original_format = img.format

    try:
        # 如果是PNG，先转换为RGB再保存为JPEG以减小体积
        if original_format == 'PNG':
            # 对于带透明通道的PNG，保留PNG格式但优化
            if img.mode in ('RGBA', 'LA', 'P'):
                img.save(output_path, format='PNG', optimize=True)
            else:
                img = img.convert('RGB')
                img.save(output_path, format='JPEG', quality=quality, optimize=True)
        elif original_format == 'BMP':
            # BMP转为JPEG以大幅减小体积
            img = img.convert('RGB')
            img.save(output_path, format='JPEG', quality=quality, optimize=True)
        else:
            # JPEG/WebP等直接压缩
            img.save(output_path, quality=quality, optimize=True)

        compressed_size = os.path.getsize(output_path)
        reduction = (1 - compressed_size / original_size) * 100

        return True, "{:.1f}% 压缩".format(reduction)
    except Exception as e:
        return False, "压缩失败：{}".format(e)
    finally:
        img.close()


def batch_compress(source_dir, output_dir, quality):
    """批量压缩图片"""
    files = get_image_files(source_dir)

    if not files:
        print("目录 '{}' 中未找到支持的图片文件".format(source_dir))
        print("支持格式：{}".format(", ".join(SUPPORTED_EXTENSIONS)))
        sys.exit(1)

    # 创建输出目录
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    print("找到 {} 个图片文件，质量：{}".format(len(files), quality))
    print("-" * 50)

    total_original = 0
    total_compressed = 0
    success_count = 0
    fail_count = 0

    for idx, file_path in enumerate(files, 1):
        file_name = os.path.basename(file_path)
        original_size = os.path.getsize(file_path)
        total_original += original_size

        # 保持原文件名，但可能需要更改扩展名
        base_name = os.path.splitext(file_name)[0]
        img_format = Image.open(file_path).format

        # 确定输出格式
        if img_format in ('BMP',):
            output_name = base_name + ".jpg"
        else:
            output_name = file_name
            # PNG with alpha stays PNG
            img = Image.open(file_path)
            if img.format == 'PNG' and img.mode in ('RGBA', 'LA', 'P'):
                output_name = base_name + ".png"
            img.close()

        output_path = os.path.join(output_dir, output_name)

        print("[{}/{}] {}".format(idx, len(files), file_name), end=" ")

        success, msg = compress_image(file_path, output_path, quality)

        if success:
            compressed_size = os.path.getsize(output_path)
            total_compressed += compressed_size
            print("-> {:.1f} KB -> {:.1f} KB ({})".format(
                original_size / 1024, compressed_size / 1024, msg
            ))
            success_count += 1
        else:
            print("-> ✗ {}".format(msg))
            fail_count += 1

    print("-" * 50)
    if total_original > 0:
        total_reduction = (1 - total_compressed / total_original) * 100
        print("✓ 完成！成功 {} 张，失败 {} 张".format(success_count, fail_count))
        print("  原始大小：{:.1f} MB".format(total_original / (1024 * 1024)))
        print("  压缩后：{:.1f} MB".format(total_compressed / (1024 * 1024)))
        print("  总体压缩率：{:.1f}%".format(total_reduction))
    print("  输出目录：{}".format(os.path.abspath(output_dir)))


def main():
    """主函数"""
    source_dir = "."
    output_dir = "compressed_images"
    quality = 75

    if len(sys.argv) > 1:
        source_dir = sys.argv[1]
    if len(sys.argv) > 2:
        output_dir = sys.argv[2]
    if len(sys.argv) > 3:
        try:
            quality = int(sys.argv[3])
            quality = max(1, min(100, quality))
        except ValueError:
            print("警告：质量参数无效，使用默认值 75")
            quality = 75

    if not os.path.isdir(source_dir):
        print("错误：目录 '{}' 不存在".format(source_dir))
        sys.exit(1)

    batch_compress(source_dir, output_dir, quality)


if __name__ == "__main__":
    main()
