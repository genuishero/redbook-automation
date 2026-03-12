#!/usr/bin/env python3
"""
Xiaohongshu MCP Client - A Python client for xiaohongshu-mcp HTTP API.

Usage:
    python xhs_client.py <command> [options]

Commands:
    status              Check login status
    search <keyword>    Search notes by keyword
    detail <feed_id> <xsec_token>   Get note details
    feeds               Get recommended feed list
    publish <title> <content> <images>  Publish a note

Examples:
    python xhs_client.py status
    python xhs_client.py search "咖啡推荐"
    python xhs_client.py detail "abc123" "token456"
    python xhs_client.py feeds
"""

import argparse
import json
import sys
import requests

BASE_URL = "http://localhost:18060"
TIMEOUT = 60


def check_status():
    """Check login status."""
    try:
        resp = requests.get(f"{BASE_URL}/api/v1/login/status", timeout=TIMEOUT)
        data = resp.json()
        if data.get("success"):
            login_info = data.get("data", {})
            if login_info.get("is_logged_in"):
                print(f"✅ Logged in as: {login_info.get('username', 'Unknown')}")
            else:
                print("❌ Not logged in. Please run the login tool first.")
        else:
            print(f"❌ Error: {data.get('error', 'Unknown error')}")
        return data
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to MCP server. Make sure xiaohongshu-mcp is running on localhost:18060")
        sys.exit(1)


def search_notes(keyword, sort_by="综合", note_type="不限", publish_time="不限"):
    """Search notes by keyword with optional filters."""
    try:
        payload = {
            "keyword": keyword,
            "filters": {
                "sort_by": sort_by,
                "note_type": note_type,
                "publish_time": publish_time
            }
        }
        resp = requests.post(
            f"{BASE_URL}/api/v1/feeds/search",
            json=payload,
            timeout=TIMEOUT
        )
        data = resp.json()
        
        if data.get("success"):
            feeds = data.get("data", {}).get("feeds", [])
            print(f"🔍 Found {len(feeds)} notes for '{keyword}':\n")
            
            for i, feed in enumerate(feeds, 1):
                note_card = feed.get("noteCard", {})
                user = note_card.get("user", {})
                interact = note_card.get("interactInfo", {})
                
                print(f"[{i}] {note_card.get('displayTitle', 'No title')}")
                print(f"    Author: {user.get('nickname', 'Unknown')}")
                print(f"    Likes: {interact.get('likedCount', '0')} | Collects: {interact.get('collectedCount', '0')} | Comments: {interact.get('commentCount', '0')}")
                print(f"    feed_id: {feed.get('id')}")
                print(f"    xsec_token: {feed.get('xsecToken')}")
                print()
        else:
            print(f"❌ Search failed: {data.get('error', 'Unknown error')}")
        
        return data
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to MCP server.")
        sys.exit(1)


def get_note_detail(feed_id, xsec_token, load_comments=False):
    """Get detailed information about a specific note."""
    try:
        payload = {
            "feed_id": feed_id,
            "xsec_token": xsec_token,
            "load_all_comments": load_comments
        }
        resp = requests.post(
            f"{BASE_URL}/api/v1/note/detail",
            json=payload,
            timeout=TIMEOUT
        )
        data = resp.json()
        
        if data.get("success"):
            note = data.get("data", {})
            print(f"📝 Note Details:\n")
            print(f"Title: {note.get('title', 'No title')}")
            print(f"Description: {note.get('desc', 'No description')}")
            print(f"Type: {note.get('type', 'Unknown')}")
            print(f"Time: {note.get('time', 'Unknown')}")
            print(f"Location: {note.get('ipLocation', 'Unknown')}")
            
            # Images
            images = note.get("images", [])
            if images:
                print(f"\n📷 Images ({len(images)}):")
                for i, img in enumerate(images, 1):
                    print(f"  [{i}] {img}")
            
            # Tags
            tags = note.get("tags", [])
            if tags:
                print(f"\n🏷️ Tags: {', '.join(tags)}")
            
            # Interactions
            interact = note.get("interactInfo", {})
            print(f"\n💬 Engagement:")
            print(f"  Likes: {interact.get('likedCount', '0')}")
            print(f"  Collects: {interact.get('collectedCount', '0')}")
            print(f"  Comments: {interact.get('commentCount', '0')}")
            print(f"  Shares: {interact.get('shareCount', '0')}")
            
            # Comments
            if load_comments:
                comments = note.get("comments", [])
                if comments:
                    print(f"\n💭 Comments ({len(comments)}):")
                    for i, comment in enumerate(comments, 1):
                        user = comment.get("user", {})
                        print(f"  [{i}] {user.get('nickname', 'Anonymous')}: {comment.get('content', '')}")
        else:
            print(f"❌ Failed to get note details: {data.get('error', 'Unknown error')}")
        
        return data
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to MCP server.")
        sys.exit(1)


def get_feeds():
    """Get recommended feed list."""
    try:
        resp = requests.get(f"{BASE_URL}/api/v1/feeds", timeout=TIMEOUT)
        data = resp.json()
        
        if data.get("success"):
            feeds = data.get("data", {}).get("feeds", [])
            print(f"📱 Recommended Feeds ({len(feeds)}):\n")
            
            for i, feed in enumerate(feeds, 1):
                note_card = feed.get("noteCard", {})
                user = note_card.get("user", {})
                interact = note_card.get("interactInfo", {})
                
                print(f"[{i}] {note_card.get('displayTitle', 'No title')}")
                print(f"    Author: {user.get('nickname', 'Unknown')}")
                print(f"    Likes: {interact.get('likedCount', '0')} | feed_id: {feed.get('id')}")
                print()
        else:
            print(f"❌ Failed to get feeds: {data.get('error', 'Unknown error')}")
        
        return data
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to MCP server.")
        sys.exit(1)


def publish_note(title, content, images=None, video=None, post_time=None):
    """Publish a note to Xiaohongshu."""
    try:
        payload = {
            "title": title,
            "desc": content,
        }
        
        if images:
            if isinstance(images, str):
                payload["images"] = [img.strip() for img in images.split(",")]
            else:
                payload["images"] = images
        
        if video:
            payload["video"] = video
        
        if post_time:
            payload["post_time"] = post_time
        
        resp = requests.post(
            f"{BASE_URL}/api/v1/note/publish",
            json=payload,
            timeout=TIMEOUT
        )
        data = resp.json()
        
        if data.get("success"):
            note_id = data.get("data", {}).get("note_id", "Unknown")
            print(f"✅ Note published successfully!")
            print(f"   Note ID: {note_id}")
        else:
            print(f"❌ Failed to publish note: {data.get('error', 'Unknown error')}")
        
        return data
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to MCP server.")
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(
        description="Xiaohongshu MCP Client",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python xhs_client.py status
  python xhs_client.py search "咖啡推荐"
  python xhs_client.py detail "feed_id" "xsec_token"
  python xhs_client.py feeds
  python xhs_client.py publish "标题" "内容" "图片URL1,图片URL2"
        """
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # Status command
    subparsers.add_parser("status", help="Check login status")
    
    # Search command
    search_parser = subparsers.add_parser("search", help="Search notes by keyword")
    search_parser.add_argument("keyword", help="Search keyword")
    search_parser.add_argument("--sort", default="综合", help="Sort by (综合, 最新, 最热)")
    search_parser.add_argument("--type", default="不限", help="Note type filter")
    search_parser.add_argument("--time", default="不限", help="Publish time filter")
    
    # Detail command
    detail_parser = subparsers.add_parser("detail", help="Get note details")
    detail_parser.add_argument("feed_id", help="Feed ID")
    detail_parser.add_argument("xsec_token", help="Security token")
    detail_parser.add_argument("--comments", action="store_true", help="Load all comments")
    
    # Feeds command
    subparsers.add_parser("feeds", help="Get recommended feed list")
    
    # Publish command
    publish_parser = subparsers.add_parser("publish", help="Publish a note")
    publish_parser.add_argument("title", help="Note title")
    publish_parser.add_argument("content", help="Note content/description")
    publish_parser.add_argument("images", nargs="?", help="Comma-separated image URLs")
    publish_parser.add_argument("--video", help="Video URL")
    publish_parser.add_argument("--time", help="Scheduled post time")
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    if args.command == "status":
        check_status()
    elif args.command == "search":
        search_notes(args.keyword, args.sort, args.type, args.time)
    elif args.command == "detail":
        get_note_detail(args.feed_id, args.xsec_token, args.comments)
    elif args.command == "feeds":
        get_feeds()
    elif args.command == "publish":
        publish_note(args.title, args.content, args.images, args.video, args.time)


if __name__ == "__main__":
    main()