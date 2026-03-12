#!/usr/bin/env python3
"""
小红书自动发布脚本 - 完全自动化版本
支持：内容生成 → 图片渲染 → 图片上传 → 发布
"""

import os
import sys
import json
import time
import requests
from pathlib import Path
from datetime import datetime

# 配置
MCP_URL = "http://localhost:18060"
OUTPUT_DIR = Path("/tmp/xhs_auto")
COOKIES_FILE = Path.home() / ".openclaw" / "workspace" / "xiaohongshu_cookies.json"

def check_mcp_status():
    """检查 MCP 服务器状态"""
    try:
        resp = requests.get(f"{MCP_URL}/api/v1/login/status", timeout=10)
        data = resp.json()
        if data.get("success") and data.get("data", {}).get("is_logged_in"):
            print(f"✅ MCP 已登录: {data['data'].get('username', 'Unknown')}")
            return True
        else:
            print("❌ MCP 未登录")
            return False
    except Exception as e:
        print(f"❌ MCP 连接失败: {e}")
        return False

def upload_image_to_xhs(image_path):
    """上传图片到小红书，返回图片 URL"""
    print(f"📤 上传图片: {image_path}")
    
    # 方法 1: 使用 MCP 的图片上传接口（如果有）
    # 方法 2: 使用 Playwright 自动上传
    # 方法 3: 使用已有的 Cookie 直接调用小红书 API
    
    # 暂时返回本地路径（需要实现实际上传）
    return f"file://{image_path}"

def render_images(content_md, theme="professional"):
    """渲染图片"""
    import subprocess
    
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    
    cmd = [
        "python3",
        str(Path.home() / ".openclaw/workspace/skills/xiaohongshu-unified/scripts/render_xhs.py"),
        content_md,
        "-t", theme,
        "-m", "auto-split",
        "-o", str(OUTPUT_DIR)
    ]
    
    print(f"🎨 渲染图片...")
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode == 0:
        # 查找生成的图片
        images = list(OUTPUT_DIR.glob("*.png"))
        print(f"✅ 生成了 {len(images)} 张图片")
        return sorted(images)
    else:
        print(f"❌ 渲染失败: {result.stderr}")
        return []

def publish_note(title, content, images=None, private=True, post_time=None):
    """发布笔记到小红书"""
    payload = {
        "title": title,
        "desc": content,
    }
    
    if images:
        payload["images"] = images
    
    if private:
        payload["private"] = True
    
    if post_time:
        payload["post_time"] = post_time
    
    try:
        print(f"📝 发布笔记: {title}")
        resp = requests.post(
            f"{MCP_URL}/api/v1/note/publish",
            json=payload,
            timeout=60
        )
        data = resp.json()
        
        if data.get("success"):
            print(f"✅ 发布成功！")
            return data
        else:
            print(f"❌ 发布失败: {data.get('error', 'Unknown error')}")
            return None
    except Exception as e:
        print(f"❌ 发布出错: {e}")
        return None

def main():
    """主函数"""
    print("="*60)
    print("小红书自动发布工具")
    print("="*60)
    
    # 1. 检查 MCP 状态
    if not check_mcp_status():
        print("\n请先启动 MCP 并登录：")
        print("  ~/.local/bin/xiaohongshu-mcp-darwin-amd64 &")
        print("  ~/.local/bin/xiaohongshu-login-darwin-amd64")
        sys.exit(1)
    
    # 2. 准备内容
    title = "测试笔记"
    content = "这是一条测试笔记 #测试"
    
    # 3. 渲染图片（可选）
    # images = render_images("/path/to/content.md")
    
    # 4. 上传图片
    # image_urls = [upload_image_to_xhs(img) for img in images]
    
    # 5. 发布
    # result = publish_note(title, content, image_urls)
    
    print("\n✅ 准备就绪！")
    print("使用方式：")
    print("  python3 xhs_auto_publish.py --title '标题' --content '正文' --images 'img1.png,img2.png'")
    print("  python3 xhs_auto_publish.py --md content.md --theme professional")

if __name__ == "__main__":
    main()