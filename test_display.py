#!/usr/bin/env python3
import requests
import base64
import json
import time
import os

# 测试服务器地址
SERVER_URL = "http://localhost:5000"

def test_text_display():
    """测试文本显示功能"""
    print("测试文本显示...")
    data = {
        "content": "这是一段测试文本\n第二行文本",
        "type": "text"
    }
    response = requests.post(f"{SERVER_URL}/display", json=data)
    print(f"响应状态码: {response.status_code}")
    print(f"响应内容: {response.json()}")
    time.sleep(2)

def test_markdown_display():
    """测试Markdown显示功能"""
    print("\n测试Markdown显示...")
    markdown_content = """
# 标题1
## 标题2

- 列表项1
- 列表项2

1. 有序列表1
2. 有序列表2

**粗体文本** *斜体文本*

数学公式：
$E = mc^2$

块级公式：
$$\\int_{a}^{b} f(x) dx$$
    """
    data = {
        "content": markdown_content,
        "type": "markdown"
    }
    response = requests.post(f"{SERVER_URL}/display", json=data)
    print(f"响应状态码: {response.status_code}")
    print(f"响应内容: {response.json()}")
    time.sleep(2)

def test_image_display():
    """测试图片显示功能"""
    print("\n测试图片显示...")
    # 创建一个简单的测试图片
    from PIL import Image, ImageDraw
    img = Image.new('RGB', (200, 200), color='red')
    draw = ImageDraw.Draw(img)
    draw.text((100, 100), "测试图片", fill='white')
    
    # 将图片转换为base64
    buffered = img.tobytes()
    img_base64 = base64.b64encode(buffered).decode()
    
    data = {
        "content": img_base64,
        "type": "image"
    }
    response = requests.post(f"{SERVER_URL}/display", json=data)
    print(f"响应状态码: {response.status_code}")
    print(f"响应内容: {response.json()}")
    time.sleep(2)

def main():
    print("开始测试显示服务...")
    
    try:
        # 测试文本显示
        test_text_display()
        
        # 测试Markdown显示
        test_markdown_display()
        
        # 测试图片显示
        test_image_display()
        
        print("\n所有测试完成！")
        
    except requests.exceptions.ConnectionError:
        print("错误：无法连接到显示服务，请确保服务正在运行")
    except Exception as e:
        print(f"测试过程中发生错误: {str(e)}")

if __name__ == "__main__":
    main() 