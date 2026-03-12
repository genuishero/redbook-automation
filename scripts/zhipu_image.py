#!/usr/bin/env python3
"""
智谱 CogView-3-Flash 图片生成模块
免费图片生成 API

使用前请设置环境变量:
  export ZHIPU_API_KEY="your-api-key"
  
或在 .env 文件中配置:
  ZHIPU_API_KEY=your-api-key
"""

import os
import requests
import time
from pathlib import Path
from typing import Optional, List
import json

# 尝试加载 .env 文件
def load_env():
    """加载 .env 文件"""
    env_files = [
        Path(__file__).parent / ".env",  # scripts/.env
        Path(__file__).parent.parent / ".env",  # skill/.env
    ]
    for env_file in env_files:
        if env_file.exists():
            with open(env_file) as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith("#") and "=" in line:
                        key, value = line.split("=", 1)
                        if key.strip() not in os.environ:
                            os.environ[key.strip()] = value.strip()

load_env()

# 智谱 API 配置 - 从环境变量读取，不硬编码
ZHIPU_API_KEY = os.environ.get("ZHIPU_API_KEY", "")
ZHIPU_API_URL = "https://open.bigmodel.cn/api/paas/v4/images/generations"

if not ZHIPU_API_KEY:
    print("⚠️  警告: ZHIPU_API_KEY 未设置")
    print("   请设置环境变量: export ZHIPU_API_KEY='your-api-key'")

# 小红书封面风格
XHS_STYLES = {
    "lifestyle": "现代简约风格，温暖色调，生活美学，ins风，高级感",
    "career": "专业商务风格，蓝色调，科技感，简洁大气",
    "tech": "科技未来感，蓝紫渐变，赛博朋克风，数字元素",
    "learning": "清新学习风，绿色调，书香气，知识感",
    "food": "美食摄影风格，暖色调，诱人食欲，高级餐厅感"
}


def generate_image(
    prompt: str,
    size: str = "1024x1024",
    output_dir: str = "/tmp/xhs_zhipu"
) -> Optional[List[str]]:
    """
    使用智谱 CogView-3-Flash 生成图片
    
    Args:
        prompt: 图片描述
        size: 图片尺寸
        output_dir: 输出目录
    
    Returns:
        图片路径列表，失败返回 None
    """
    
    print(f"\n🎨 智谱图片生成")
    print(f"   模型: CogView-3-Flash")
    print(f"   尺寸: {size}")
    print(f"   提示词: {prompt[:50]}...")
    
    # 创建输出目录
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    headers = {
        "Authorization": f"Bearer {ZHIPU_API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": "cogview-3-flash",
        "prompt": prompt,
        "size": size,
        "watermark": False  # 关闭水印（需先签署免责声明）
    }
    
    try:
        print("   📤 发送请求...")
        response = requests.post(
            ZHIPU_API_URL,
            headers=headers,
            json=payload,
            timeout=60
        )
        
        if response.status_code != 200:
            print(f"   ❌ 请求失败: {response.status_code}")
            print(f"   响应: {response.text[:300]}")
            return None
        
        result = response.json()
        
        # 检查响应
        if "data" not in result:
            print(f"   ❌ 无生成结果: {result}")
            return None
        
        images = []
        for i, item in enumerate(result["data"]):
            url = item.get("url")
            if url:
                # 下载图片
                print(f"   📥 下载图片 {i+1}...")
                img_resp = requests.get(url, timeout=30)
                if img_resp.status_code == 200:
                    filename = f"zhipu_{int(time.time())}_{i}.png"
                    filepath = output_path / filename
                    
                    with open(filepath, "wb") as f:
                        f.write(img_resp.content)
                    
                    images.append(str(filepath))
                    print(f"   ✅ 已保存: {filepath}")
        
        return images if images else None
    
    except Exception as e:
        print(f"   ❌ 错误: {e}")
        return None


def generate_xhs_cover(
    title: str,
    category: str = "lifestyle"
) -> Optional[List[str]]:
    """
    生成小红书封面图
    
    Args:
        title: 笔记标题
        category: 分类
    
    Returns:
        图片路径列表
    """
    
    style_desc = XHS_STYLES.get(category, XHS_STYLES["lifestyle"])
    
    # 构建提示词
    prompt = f"""
    小红书封面图，{style_desc}，
    主题: {title}，
    高质量，精美设计，适合社交媒体，
    简洁大气，吸引眼球，
    不要在图片中添加文字
    """
    
    # 生成图片
    images = generate_image(
        prompt=prompt.strip(),
        size="768x1024",  # 小红书封面比例
        output_dir="/tmp/xhs_zhipu"
    )
    
    return images


# 测试
if __name__ == "__main__":
    print("=" * 50)
    print("🧪 测试智谱 CogView-3-Flash 图片生成")
    print("=" * 50)
    
    # 测试生成
    result = generate_image(
        "一只可爱的猫咪在阳光下打盹，温暖治愈风格，高质量摄影",
        "1024x1024",
        "/tmp/test_zhipu"
    )
    
    if result:
        print(f"\n✅ 测试成功！")
        for img in result:
            print(f"   图片: {img}")
    else:
        print("\n❌ 测试失败")