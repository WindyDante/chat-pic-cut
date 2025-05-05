#!/usr/bin/env python3
import os
import sys
import traceback
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image

def split_image_into_quadrants(input_path, output_dir):
    """Split a 2×2 image into 4 equal quadrants."""
    img = Image.open(input_path)
    w, h = img.size
    half_w, half_h = w // 2, h // 2

    boxes   = [
        (0, 0, half_w, half_h),     # 上左
        (half_w, 0, w, half_h),     # 上右
        (0, half_h, half_w, h),     # 下左
        (half_w, half_h, w, h)      # 下右
    ]
    suffixes = ['_ul', '_ur', '_ll', '_lr']

    base, ext = os.path.splitext(os.path.basename(input_path))
    for box, suf in zip(boxes, suffixes):
        out = img.crop(box)
        out_path = os.path.join(output_dir, f"{base}{suf}{ext}")
        out.save(out_path)

def main():
    # 隐藏主窗口、弹出目录选择框
    root = tk.Tk()
    root.withdraw()
    folder = filedialog.askdirectory(title="选择要分割的图片目录", mustexist=True)
    if not folder:
        messagebox.showinfo("已取消", "未选择任何目录，程序退出。")
        sys.exit(0)

    output_dir = os.path.join(folder, "split")
    try:
        os.makedirs(output_dir, exist_ok=True)
        # 批量处理
        files = [f for f in os.listdir(folder)
                 if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
        if not files:
            messagebox.showwarning("没有图片", f"目录中未发现 PNG/JPG 文件：\n{folder}")
            sys.exit(0)

        for fname in files:
            split_image_into_quadrants(os.path.join(folder, fname), output_dir)

        messagebox.showinfo("完成", f"所有图片已分割并保存在：\n{output_dir}")
    except Exception:
        err = traceback.format_exc()
        # 发生错误时弹窗显示，并写入日志文件
        log_path = os.path.join(folder, "split_error.log")
        with open(log_path, "w", encoding="utf-8") as f:
            f.write(err)
        messagebox.showerror("出错了", f"处理过程中发生异常，已记录到：\n{log_path}")

if __name__ == "__main__":
    main()
