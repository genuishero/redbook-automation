#!/usr/bin/env python3
"""
小红书 MCP 发布工具
支持本地图片路径，完全自动化发布

Usage:
    python mcp_publish.py --title "标题" --content "正文" --images img1.png,img2.png
    python mcp_publish.py --private  # 私密发布
    python mcp_publish.py --demo     # 演示模式
"""

import argparse
import json
import sys
import requests
from pathlib import Path
from typing import List, Optional

MCP_URL = "http://localhost:18060"
TIMEOUT = 180


def check_mcp_status() -> bool:
    """检查 MCP 服务器状态"""
    try:
        resp = requests.get(f"{MCP_URL}/api/v1/login/status", timeout=10)
        data = resp.json()
        if data.get("success"):
            login_info = data.get("data", {})
            if login_info.get("is_logged_in"):
                print(f"✅ MCP 登录状态: {login_info.get('username', 'Unknown')}")
                return True
            else:
                print("❌ MCP 未登录，请先运行登录工具")
                return False
        return False
    except requests.exceptions.ConnectionError:
        print("❌ MCP 服务器未运行，请先启动：")
        print("   ~/.local/bin/xiaohongshu-mcp-darwin-amd64 &")
        return False


def publish_note(
    title: str,
    content: str,
    images: List[str],
    private: bool = True,
    post_time: Optional[str] = None,
    max_retries: int = 3
) -> Optional[dict]:
    """
    发布笔记到小红书
    
    Args:
        title: 笔记标题
        content: 笔记正文
        images: 图片路径列表（支持本地路径）
        private: 是否私密发布
        post_time: 定时发布时间（格式：2026-03-10 08:00）
        max_retries: 最大重试次数（默认3次）
    
    Returns:
        发布结果字典，失败返回 None
    """
    
    payload = {
        "title": title,
        "content": content,
        "images": images,
        "private": private
    }
    
    if post_time:
        payload["post_time"] = post_time
    
    print(f"\n📤 发布笔记")
    print(f"   标题: {title}")
    print(f"   图片: {len(images)} 张")
    print(f"   模式: {'私密' if private else '公开'}")
    if post_time:
        print(f"   定时: {post_time}")
    
    import time
    
    for attempt in range(1, max_retries + 1):
        try:
            if attempt > 1:
                print(f"   🔄 第 {attempt}/{max_retries} 次重试...")
                time.sleep(2)  # 重试前等待2秒
            
            resp = requests.post(
                f"{MCP_URL}/api/v1/publish",
                json=payload,
                timeout=TIMEOUT
            )
            
            result = resp.json()
            
            if result.get("success"):
                print(f"\n✅ 发布成功！")
                return result
            else:
                error_msg = result.get('error', 'Unknown error')
                print(f"\n❌ 发布失败: {error_msg}")
                
                # 如果是参数错误，不重试
                if '参数' in error_msg or 'invalid' in error_msg.lower():
                    return None
                
                # 其他错误继续重试
                if attempt < max_retries:
                    print(f"   将在2秒后重试...")
                    continue
                return None
        
        except Exception as e:
            print(f"\n❌ 请求失败: {e}")
            if attempt < max_retries:
                print(f"   将在2秒后重试...")
                continue
            return None
    
    return None


def demo_publish():
    """演示发布流程"""
    
    print("🎬 演示模式：发布 AI 工具推荐笔记\n")
    
    # 演示内容
    title = "AI工具推荐"
    content = """Happy Coder 是 Claude Code 的移动端控制工具！

核心功能：
📱 手机远程控制 Claude Code
💻 支持 Codex、Gemini 模式
🔄 后台运行，随时连接

启动：happy --resume
连接：扫描二维码

#HappyCoder #ClaudeCode #AI工具"""
    
    images = [
        "/tmp/ai-tools-output/cover.png",
        "/tmp/ai-tools-output/card_1.png",
        "/tmp/ai-tools-output/card_2.png"
    ]
    
    # 检查图片是否存在
    missing = [img for img in images if not Path(img).exists()]
    if missing:
        print(f"⚠️  图片不存在，将创建测试发布（无图片）")
        print(f"   缺失: {missing}")
        images = []
    
    return publish_note(title, content, images, private=True)


def main():
    parser = argparse.ArgumentParser(
        description="小红书 MCP 发布工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 基础发布
  python mcp_publish.py --title "标题" --content "正文" --images img1.png,img2.png

  # 私密发布
  python mcp_publish.py --title "标题" --content "正文" --images img1.png --private

  # 定时发布
  python mcp_publish.py --title "标题" --content "正文" --images img1.png --time "2026-03-10 08:00"

  # 演示模式
  python mcp_publish.py --demo

MCP 服务器:
  启动: ~/.local/bin/xiaohongshu-mcp-darwin-amd64 &
  登录: ~/.local/bin/xiaohongshu-login-darwin-amd64
        """
    )
    
    parser.add_argument("--title", help="笔记标题")
    parser.add_argument("--content", help="笔记正文")
    parser.add_argument("--images", help="图片路径，逗号分隔")
    parser.add_argument("--private", action="store_true", default=True, help="私密发布（默认）")
    parser.add_argument("--public", action="store_true", help="公开发布")
    parser.add_argument("--time", help="定时发布时间（格式：2026-03-10 08:00）")
    parser.add_argument("--demo", action="store_true", help="演示模式")
    parser.add_argument("--check", action="store_true", help="仅检查 MCP 状态")
    
    args = parser.parse_args()
    
    # 仅检查状态
    if args.check:
        success = check_mcp_status()
        sys.exit(0 if success else 1)
    
    # 演示模式
    if args.demo:
        if not check_mcp_status():
            sys.exit(1)
        result = demo_publish()
        sys.exit(0 if result else 1)
    
    # 必须提供参数
    if not args.title or not args.content:
        parser.print_help()
        print("\n❌ 必须提供 --title 和 --content")
        sys.exit(1)
    
    # 检查 MCP 状态
    if not check_mcp_status():
        sys.exit(1)
    
    # 解析图片
    images = []
    if args.images:
        images = [img.strip() for img in args.images.split(",")]
        # 验证图片路径
        for img in images:
            if not Path(img).exists():
                print(f"⚠️  图片不存在: {img}")
    
    # 发布模式
    private = not args.public
    
    # 发布
    result = publish_note(
        title=args.title,
        content=args.content,
        images=images,
        private=private,
        post_time=args.time
    )
    
    if result:
        print(f"\n📊 结果:")
        print(json.dumps(result, indent=2, ensure_ascii=False))
        sys.exit(0)
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()