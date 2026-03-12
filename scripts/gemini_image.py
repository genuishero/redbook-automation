#!/usr/bin/env python3
"""
Gemini 图片生成模块
使用 Gemini 2.0 Flash Exp 模型生成图片
免费额度：每天 500 张
"""

import os
import requests
import base64
import time
from pathlib import Path
from typing import Optional, List
import json

# Gemini API 配置
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "AIzaSyAhluUdL8wkiY3C8VhXvbdCMYnUQ4SRD8U")
# 图片生成模型
GEMINI_MODEL = "gemini-2.0-flash-preview-image-generation"
GEMINI_API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/{GEMINI_MODEL}:generateContent"

# 小红书封面风格
XHS_STYLES = {
    "lifestyle": "modern minimalist style, warm colors, lifestyle aesthetics, Instagram style, premium feel",
    "career": "professional business style, blue tones, tech feel, clean and elegant",
    "tech": "futuristic tech style, blue-purple gradient, cyberpunk, digital elements",
    "learning": "fresh learning style, green tones, bookish atmosphere, knowledge feel",
    "food": "food photography style, warm tones, appetizing, high-end restaurant feel"
}


def generate_image(
    prompt: str,
    output_path: str = "/tmp/gemini_image.png"
) -> Optional[str]:
    """
    使用 Gemini 生成图片
    
    Args:
        prompt: 图片描述
        output_path: 输出路径
    
    Returns:
        图片路径，失败返回 None
    """
    
    print(f"\n🎨 Gemini 图片生成")
    print(f"   提示词: {prompt[:60]}...")
    
    headers = {
        "Content-Type": "application/json",
        "x-goog-api-key": GEMINI_API_KEY
    }
    
    payload = {
        "contents": [{
            "parts": [
                {"text": prompt}
            ]
        }],
        "generationConfig": {
            "responseModalities": ["TEXT", "IMAGE"]
        }
    }
    
    try:
        print("   📤 发送请求...")
        response = requests.post(
            GEMINI_API_URL,
            headers=headers,
            json=payload,
            timeout=60
        )
        
        if response.status_code != 200:
            print(f"   ❌ 请求失败: {response.status_code}")
            print(f"   响应: {response.text[:200]}")
            return None
        
        result = response.json()
        
        # 检查响应
        candidates = result.get("candidates", [])
        if not candidates:
            print(f"   ❌ 无生成结果")
            return None
        
        # 提取图片
        parts = candidates[0].get("content", {}).get("parts", [])
        
        for part in parts:
            if "inlineData" in part:
                inline_data = part["inlineData"]
                image_data = inline_data.get("data")
                mime_type = inline_data.get("mimeType", "image/png")
                
                if image_data:
                    # 解码并保存
                    image_bytes = base64.b64decode(image_data)
                    
                    output = Path(output_path)
                    output.parent.mkdir(parents=True, exist_ok=True)
                    
                    with open(output, "wb") as f:
                        f.write(image_bytes)
                    
                    print(f"   ✅ 图片已保存: {output}")
                    return str(output)
        
        print(f"   ❌ 响应中没有图片数据")
        return None
    
    except Exception as e:
        print(f"   ❌ 错误: {e}")
        return None


def generate_xhs_cover(
    title: str,
    category: str = "lifestyle",
    output_dir: str = "/tmp/xhs_gemini"
) -> Optional[List[str]]:
    """
    生成小红书封面图
    
    Args:
        title: 笔记标题
        category: 分类
        output_dir: 输出目录
    
    Returns:
        图片路径列表
    """
    
    style_desc = XHS_STYLES.get(category, XHS_STYLES["lifestyle"])
    
    # 构建提示词
    prompt = f"""
    Create a visually stunning image for social media cover.
    Style: {style_desc}
    Title theme: {title}
    Requirements:
    - Eye-catching and attractive
    - Modern and elegant design
    - Suitable for social media sharing
    - High quality, professional look
    - No text in the image (text will be added separately)
    """
    
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    images = []
    
    # 生成封面
    print("\n📌 生成封面...")
    cover_path = output_path / f"cover_{int(time.time())}.png"
    result = generate_image(prompt.strip(), str(cover_path))
    if result:
        images.append(result)
    
    # 生成2张内容卡片
    for i in range(2):
        print(f"\n📌 生成内容卡片 {i+1}...")
        card_prompt = f"""
        Create a visually appealing content card image.
        Style: {style_desc}
        Theme: {title} - Part {i+1}
        Requirements:
        - Clean and modern design
        - Easy to read
        - High quality
        - No text (text will be added separately)
        """
        card_path = output_path / f"card_{i+1}_{int(time.time())}.png"
        result = generate_image(card_prompt.strip(), str(card_path))
        if result:
            images.append(result)
    
    return images if images else None


# 测试
if __name__ == "__main__":
    print("=" * 50)
    print("🧪 测试 Gemini 图片生成")
    print("=" * 50)
    
    # 测试单张图片
    result = generate_image(
        "A beautiful sunset over mountains, artistic style, warm colors",
        "/tmp/test_gemini_image.png"
    )
    
    if result:
        print(f"\n✅ 测试成功！")
        print(f"   图片路径: {result}")
    else:
        print("\n❌ 测试失败")