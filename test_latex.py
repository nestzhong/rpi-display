#!/usr/bin/env python3
import requests
import time

# 测试服务器地址
SERVER_URL = "http://localhost:5000"

def test_simple_formulas():
    """测试简单公式"""
    formulas = [
        "E = mc^2",
        "x^2 + y^2 = r^2",
        "\\frac{1}{2}",
        "\\sqrt{2}",
        "\\sum_{i=1}^{n} i"
    ]
    
    for formula in formulas:
        print(f"\n测试公式: {formula}")
        markdown_content = f"行内公式: ${formula}$\n\n块级公式:\n$${formula}$$"
        
        data = {
            "content": markdown_content,
            "type": "markdown"
        }
        
        try:
            response = requests.post(f"{SERVER_URL}/display", json=data)
            print(f"响应状态码: {response.status_code}")
            print(f"响应内容: {response.json()}")
            time.sleep(2)
        except Exception as e:
            print(f"请求失败: {str(e)}")

def test_complex_formulas():
    """测试复杂公式"""
    complex_formulas = [
        "\\int_{a}^{b} f(x) dx",
        "\\frac{\\partial f}{\\partial x}",
        "\\begin{pmatrix} a & b \\\\ c & d \\end{pmatrix}",
        "\\lim_{x \\to \\infty} \\frac{1}{x} = 0",
        "\\sum_{n=1}^{\\infty} \\frac{1}{n^2} = \\frac{\\pi^2}{6}"
    ]
    
    for formula in complex_formulas:
        print(f"\n测试复杂公式: {formula}")
        markdown_content = f"行内公式: ${formula}$\n\n块级公式:\n$${formula}$$"
        
        data = {
            "content": markdown_content,
            "type": "markdown"
        }
        
        try:
            response = requests.post(f"{SERVER_URL}/display", json=data)
            print(f"响应状态码: {response.status_code}")
            print(f"响应内容: {response.json()}")
            time.sleep(2)
        except Exception as e:
            print(f"请求失败: {str(e)}")

def test_special_characters():
    """测试特殊字符"""
    special_formulas = [
        "\\alpha \\beta \\gamma",
        "\\mathbb{R} \\mathbb{C}",
        "\\mathcal{L} \\mathcal{H}",
        "\\vec{v} \\cdot \\vec{w}",
        "\\hat{x} \\bar{y}"
    ]
    
    for formula in special_formulas:
        print(f"\n测试特殊字符: {formula}")
        markdown_content = f"行内公式: ${formula}$\n\n块级公式:\n$${formula}$$"
        
        data = {
            "content": markdown_content,
            "type": "markdown"
        }
        
        try:
            response = requests.post(f"{SERVER_URL}/display", json=data)
            print(f"响应状态码: {response.status_code}")
            print(f"响应内容: {response.json()}")
            time.sleep(2)
        except Exception as e:
            print(f"请求失败: {str(e)}")

def main():
    print("开始测试 LaTeX 公式显示...")
    
    try:
        # 测试简单公式
        print("\n=== 测试简单公式 ===")
        test_simple_formulas()
        
        # 测试复杂公式
        print("\n=== 测试复杂公式 ===")
        test_complex_formulas()
        
        # 测试特殊字符
        print("\n=== 测试特殊字符 ===")
        test_special_characters()
        
        print("\n所有测试完成！")
        
    except requests.exceptions.ConnectionError:
        print("错误：无法连接到显示服务，请确保服务正在运行")
    except Exception as e:
        print(f"测试过程中发生错误: {str(e)}")

if __name__ == "__main__":
    main() 