import os, cv2, sys, json, pdb, torch, treelib, clip, warnings, umap
import torch.nn as nn
import numpy as np
from tqdm import tqdm
from pathlib import Path
from treelib import Node, Tree
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from sklearn.manifold import TSNE
from sklearn.decomposition import PCA
from fontTools.ttLib import TTFont
from torchvision.models import resnet50
from torchvision.transforms import Normalize
from PIL import Image, ImageDraw, ImageFont

warnings.filterwarnings("ignore")



def assert_chars(char, font_path):
    try:
        with TTFont(font_path) as font:
            cmap = font.getBestCmap()
            return ord(char) in cmap
    except Exception as e:
        print(f"Error loading font: {e}")
        return False



def render_text_to_pdf(text, ttf_path, save_path):
    if not os.path.isfile(ttf_path):
        raise FileNotFoundError(f"字体文件 {ttf_path} 不存在")

    try:
        font = ImageFont.truetype(ttf_path, size=64)
    except OSError as e:
        raise OSError(f"无法加载字体文件 {ttf_path}: {e}")

    image = Image.new('RGB', (1, 1), color='black')  # 临时图像
    draw = ImageDraw.Draw(image)

    ascent, descent = font.getmetrics()
    text_width, text_height = draw.textsize(text, font=font)
    
    image_width = 96
    image_height = 96
    
    image = Image.new('RGB', (image_width, image_height), color='black')
    draw = ImageDraw.Draw(image)
    y = (image_height - text_height) // 2 # - ascent/4
    draw.text((10, y), text, font=font, fill='white')
    
    pdf_filename = f"{text}.pdf"
    pdf_filepath = os.path.join(save_path, pdf_filename)
    os.makedirs(save_path, exist_ok=True)
    c = canvas.Canvas(pdf_filepath, pagesize=(image_width, image_height))
    img = ImageReader(image)
    
    c.drawImage(img, 0, 0, width=image_width, height=image_height)
    c.showPage()
    c.save()
    
    return pdf_filename



def render_text_to_img(text, ttf_path, save_path, image_format='png'):
    if not os.path.isfile(ttf_path):
        raise FileNotFoundError(f"字体文件 {ttf_path} 不存在")
    try:
        font = ImageFont.truetype(ttf_path, size=64)
    except OSError as e:
        raise OSError(f"无法加载字体文件 {ttf_path}: {e}")

    temp_image = Image.new('RGB', (1, 1), color='black')  # 临时图像
    draw = ImageDraw.Draw(temp_image)
    ascent, descent = font.getmetrics()
    text_width, text_height = draw.textsize(text, font=font)

    image_width = 96
    image_height = 96

    image = Image.new('RGB', (image_width, image_height), color='black')
    draw = ImageDraw.Draw(image)
    x = (image_width - text_width) // 3
    y = (image_height - text_height) // 3
    draw.text((x, y), text, font=font, fill='white')
    os.makedirs(save_path, exist_ok=True)
    if image_format.lower() not in ['png', 'jpg', 'jpeg']:
        raise ValueError("不支持的图像格式，支持的格式为 'png' 或 'jpg'")
    
    image_filename = f"{text}.{image_format}"
    image_filepath = os.path.join(save_path, image_filename)
    image.save(image_filepath, format=image_format.upper())

    return image_filename



def render_glyphs(ids_file_path, glyph_styles_root, glyph_img_root, IMGPATH_FILE='imgs_path.txt'):
    mth = open(ids_file_path, 'r', encoding='utf-8').readlines() 
    char_set = set()
    for line in mth:
        char = line.split(':')[0]
        char_set.add(char)

    char_set = list(char_set)   

    glyph_styles = [style for style in os.listdir(glyph_styles_root) if style != '.ipynb_checkpoints']
    for style in tqdm(glyph_styles):
        style_img_path = os.path.join(glyph_img_root, style)
        if not os.path.exists(style_img_path):
            os.makedirs(style_img_path)

        ttf_files = os.listdir(os.path.join(glyph_styles_root, style))
        for file in tqdm(ttf_files):
            filename = file.split('.')[0]
            ttf_img_path = os.path.join(style_img_path, filename)
            if not os.path.exists(ttf_img_path):
                os.makedirs(ttf_img_path)

            ttf_file_path = os.path.join(glyph_styles_root, style, file)
            for char in char_set:
                if assert_chars(char, ttf_file_path):
                    img_name = render_text_to_img(char, ttf_file_path, ttf_img_path)
                    img_path = os.path.join(ttf_img_path, img_name)
                    # record img path
                    with open(IMGPATH_FILE, "a", encoding="utf-8") as f:
                        f.write(f"{img_path}\n")
                    
                else:
                    # print(f"{ttf_file_path} has not include {char}!")
                    pass