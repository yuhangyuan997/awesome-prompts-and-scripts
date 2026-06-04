#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
批量调整图片尺寸

功能：批量调整指定目录下图片的尺寸（宽度、高度或比例）
用法：python3 resize_images.py [源目录] [输出目录] [宽度] [高度] [模式]

参数：
  源目录    - 图片文件所在目录（默认：当前目录）
  输出目录  - 调整后图片保存目录（默认：resized_images）
  宽度      - 目标宽度（像素），设为0则按高度等比缩放（默认：800）
  高度      - 目标高度（像素），设为0则按宽度等比缩放（默认：0）
  模式      - 缩放模式：fit(适应)/fill(填充)/crop(裁剪)（默认：fit）

模式说明：
  fit  - 保持宽高比，图片完全显示在指定区域内
  fill - 保持宽高比，填充整个指定区域（可能裁剪边缘）
  crop - 直接拉伸到指定尺寸（不保持宽高比）

支持格式：JPG, JPEG, PNG, BMP, WebP

依赖：
  pip install Pillow

示例：
  python3 resize_images.py ./photos ./resized 1920 1080 fit
  python3 resize_images.py ./images ./small 800 0    # 宽度800，高度等比
  python3 resize_images.py ./pics ./thumbs 150 150 crop
"""

import os
import sys
import glob

try:
    from PIL import Image
except ImportError:
    print("错误：请先安装 Pillow：pip install Pillow")
    sys.exit(1)

SUPPORTED_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.bmp', '.webp'}


def get_image_files(directory):
    """获取目录下所有图片文件"""
    files = []
    for ext in SUPPORTED_EXTENSIONS:
        files.extend(glob.glob(os.path.join(directory, "*" + ext)))
        files.extend(glob.glob(os.path.join(directory, "*" + ext.upper())))
    return sorted(files)


def resize_image(img, target_w, target_h, mode):
    """按指定模式和尺寸调整图片"""
    orig_w, orig_h = img.size

    # 如果目标尺寸为0，等比计算
    if target_w == 0 and target_h == 0:
        return img.copy()
    if target_w == 0:
        ratio = target_h / orig_h
        target_w = int(orig_w * ratio)
    if target_h == 0:
        ratio = target_w / orig_w
        target_h = int(orig_h * ratio)

    if mode == "fit":
        # 适应模式：保持宽高比，图片完全显示
        img.thumbnail((target_w, target_h), Image.Resampling.LANCZOS)
        return img

    elif mode == "fill":
        # 填充模式：保持宽高比，填满区域（可能裁剪）
        ratio = max(target_w / orig_w, target_h / orig_h)
        new_w = int(orig_w * ratio)
        new_h = int(orig_h * ratio)
        img = img.resize((new_w, new_h), Image.Resampling.LANCZOS)

        # 居中裁剪
        left = (new_w - target_w) // 2
        top = (new_h - target_h) // 2
        img = img.crop((left, top, left + target_w, top + target_h))
        return img

    elif mode == "crop":
        # 裁剪模式：直接拉伸
        img = img.resize((target_w, target_h), Image.Resampling.LANCZOS)
        return img

    else:
        # 默认使用fit
        img.thumbnail((target_w, target_h), Image.Resampling.LANCZOS)
        return img


def batch_resize(source_dir, output_dir, target_w, target_h, mode):
    """批量调整图片尺寸"""
    files = get_image_files(source_dir)

    if not files:
        print("目录 '{}' 中未找到图片文件".format(source_dir))
        sys.exit(1)

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    print("找到 {} 个图片文件，目标尺寸：{}x{}，模式：{}".format(
        len(files), target_w, target_h, mode
    ))
    print("-" * 50)

    success_count = 0
    fail_count = 0

    for idx, file_path in enumerate(files, 1):
        file_name = os.path.basename(file_path)
        output_path = os.path.join(output_dir, file_name)

        print("[{}/{}] {}".format(idx, len(files), file_name), end=" ")

        try:
            img = Image.open(file_path)
            orig_w, orig_h = img.size

            resized = resize_image(img, target_w, target_h, mode)
            resized.save(output_path)

            new_w, new_h = resized.size
            print("-> {}x{} -> {}x{}".format(orig_w, orig_h, new_w, new_h))
            success_count += 1

            img.close()
            resized.close()
        except Exception as e:
            print("-> ✗ {}".format(e))
            fail_count += 1

    print("-" * 50)
    print("✓ 完成！成功 {} 张，失败 {} 张".format(success_count, fail_count))
    print("  输出目录：{}".format(os.path.abspath(output_dir)))


def main():
    """主函数"""
    source_dir = "."
    output_dir = "resized_images"
    target_w = 800
    target_h = 0
    mode = "fit"

    if len(sys.argv) > 1:
        source_dir = sys.argv[1]
    if len(sys.argv) > 2:
        output_dir = sys.argv[2]
    if len(sys.argv) > 3:
        try:
            target_w = max(0, int(sys.argv[3]))
        except ValueError:
            pass
    if len(sys.argv) > 4:
        try:
            target_h = max(0, int(sys.argv[4]))
        except ValueError:
            pass
    if len(sys.argv) > 5:
        mode = sys.argv[5].lower()
        if mode not in ("fit", "fill", "crop"):
            print("警告：不支持的模式 '{}'，使用默认 'fit'".format(mode))
            mode = "fit"

    if not os.path.isdir(source_dir):
        print("错误：目录 '{}' 不存在".format(source_dir))
        sys.exit(1)

    batch_resize(source_dir, output_dir, target_w, target_h, mode)


if __name__ == "__main__":
    main()
