---
name: redbook-automation
description: >
  整合的小红书运营技能，提供完整的内容创作、图片渲染、自动发布和数据分析功能。
  包括：账号定位、选题生成、内容创作、多主题图片渲染、MCP API发布、
  搜索分析、评论管理等。一站式小红书运营解决方案。
---

# 小红书统一运营技能

整合了多个小红书技能的功能，提供一站式的运营解决方案。

---

## 🚀 快速开始

### 第一步：安装 xiaohongshu-mcp

**下载 MCP 工具**（Intel Mac）：
```bash
# 创建目录
mkdir -p ~/.local/bin

# 下载（选择 darwin-amd64 版本）
cd ~/.local/bin
curl -LO https://github.com/xpzouying/xiaohongshu-mcp/releases/download/v2026.03.09.0605/xiaohongshu-mcp-darwin-amd64.tar.gz
tar -xzf xiaohongshu-mcp-darwin-amd64.tar.gz
chmod +x xiaohongshu-mcp-darwin-amd64 xiaohongshu-login-darwin-amd64
rm xiaohongshu-mcp-darwin-amd64.tar.gz
```

**登录小红书**：
```bash
# 启动登录工具，扫描二维码
~/.local/bin/xiaohongshu-login-darwin-amd64
```

### 第二步：启动 MCP 服务器

```bash
# 后台启动
~/.local/bin/xiaohongshu-mcp-darwin-amd64 &

# 检查状态
curl http://localhost:18060/api/v1/login/status
```

### 第三步：发布笔记

```bash
# 演示发布
python3 ~/.openclaw/workspace/skills/xiaohongshu-unified/scripts/mcp_publish.py --demo

# 自定义发布
python3 ~/.openclaw/workspace/skills/xiaohongshu-unified/scripts/mcp_publish.py \
  --title "我的第一篇笔记" \
  --content "这是正文内容 #测试" \
  --images /path/to/cover.png,/path/to/card1.png \
  --private
```

---

## 🎯 核心功能

### 1. 自动发布（MCP API - 推荐）
- **完全自动化**：无需人工干预
- **本地图片支持**：直接使用本地路径，无需上传到图床
- **私密/公开**：支持私密发布预览
- **定时发布**：指定发布时间
- **登录持久**：MCP 登录状态长期有效

### 2. 图片渲染
- **多主题支持**：8种专业主题
- **自动分页**：智能切分长内容为多张卡片
- **高清输出**：1080x1440px，适合小红书

### 3. 数据分析
- **笔记搜索**：按关键词搜索热门笔记
- **详情分析**：获取笔记内容、评论、互动数据
- **推荐流获取**：获取平台推荐内容

---

## 📋 发布方式

### MCP 发布（推荐）

```bash
# 检查 MCP 状态
python3 scripts/mcp_publish.py --check

# 私密发布
python3 scripts/mcp_publish.py \
  --title "标题" \
  --content "正文 #标签" \
  --images img1.png,img2.png \
  --private

# 公开发布
python3 scripts/mcp_publish.py \
  --title "标题" \
  --content "正文" \
  --images img1.png \
  --public

# 定时发布
python3 scripts/mcp_publish.py \
  --title "标题" \
  --content "正文" \
  --images img1.png \
  --time "2026-03-10 08:00"

# 演示模式
python3 scripts/mcp_publish.py --demo
```

### 数据分析

```bash
# 检查登录状态
python3 scripts/xhs_client.py status

# 搜索笔记
python3 scripts/xhs_client.py search "关键词"

# 获取笔记详情
python3 scripts/xhs_client.py detail "feed_id" "xsec_token"

# 获取推荐流
python3 scripts/xhs_client.py feeds
```

---

## 🤖 定时自动发布

### 配置定时任务

```bash
# 编辑 crontab
crontab -e

# 添加定时任务（每天 8:00 发布）
0 8 * * * python3 ~/.openclaw/workspace/skills/xiaohongshu-unified/scripts/mcp_publish.py --demo >> ~/.openclaw/logs/xhs_publish.log 2>&1
```

### 自定义内容脚本

创建 `~/xhs_daily.py`：
```python
#!/usr/bin/env python3
import sys
sys.path.insert(0, '/Users/genuis/.openclaw/workspace/skills/xiaohongshu-unified/scripts')
from mcp_publish import publish_note, check_mcp_status

# 自定义内容生成逻辑
title = "今日推荐"
content = "..."

if check_mcp_status():
    publish_note(title, content, [], private=True)
```

---

## 🛠️ MCP 常用命令

```bash
# 启动 MCP 服务器
~/.local/bin/xiaohongshu-mcp-darwin-amd64 &

# 检查登录状态
curl http://localhost:18060/api/v1/login/status

# 或使用客户端
python3 scripts/mcp_publish.py --check

# 搜索笔记
python3 scripts/xhs_client.py search "关键词"

# 获取推荐流
python3 scripts/xhs_client.py feeds

# 获取笔记详情
python3 scripts/xhs_client.py detail <feed_id> <xsec_token>
```

---

## ⚠️ 重要提示

### MCP 登录有效期
- 登录状态会持续有效，无需重复登录
- **不要在其他浏览器登录同一账号**，否则会踢掉 MCP 的登录
- 如果登录失效，重新运行登录工具即可

### 图片要求
- 支持 PNG、JPG 格式
- 推荐尺寸：1080×1440px（3:4 比例）
- 最大 18 张图片

### 发布限制
- 私密发布建议先预览排版
- 发布后可在小红书 APP 中改为公开

---

## 🎨 图片主题

| 主题 | 说明 | 适用场景 |
|------|------|---------|
| `default` | 简约灰色 | 通用 |
| `professional` | 专业商务 | 商业、科技 |
| `playful-geometric` | 活力几何 | 生活方式 |
| `neo-brutalism` | 新粗野主义 | 设计、艺术 |
| `botanical` | 自然植物 | 美食、旅行 |
| `retro` | 复古风格 | 怀旧、文化 |
| `terminal` | 终端风格 | 技术、编程 |
| `sketch` | 手绘风格 | 创意、教育 |

---

## 📁 目录结构

```
xiaohongshu-unified/
├── SKILL.md                 # 本文件
├── scripts/                 # 工具脚本
│   ├── mcp_publish.py      # MCP发布（推荐）
│   ├── xhs_client.py       # MCP客户端（搜索/详情）
│   ├── render_xhs.py       # 图片渲染
│   ├── render_xhs_v2.py    # 图片渲染v2
│   ├── publish_xhs.py      # 浏览器发布（备用）
│   └── xhs_auto_publish.py # 自动发布流程
├── references/              # 参考文档
│   ├── xhs-runtime-rules.md
│   ├── xhs-publish-flows.md
│   └── xhs-viral-copy-flow.md
└── templates/               # 模板
    ├── article.md
    └── persona.md
```

---

## 🔧 故障排查

### 问题 1：MCP 连接失败

**症状**：`Cannot connect to MCP server`

**解决**：
```bash
# 启动 MCP 服务器
~/.local/bin/xiaohongshu-mcp-darwin-amd64 &

# 等待几秒后再试
sleep 3 && python3 scripts/mcp_publish.py --check
```

### 问题 2：MCP 未登录

**症状**：`Not logged in`

**解决**：
```bash
# 运行登录工具
~/.local/bin/xiaohongshu-login-darwin-amd64
# 扫描二维码登录
```

### 问题 3：登录被踢

**原因**：在其他浏览器登录了同一账号

**解决**：重新运行登录工具

### 问题 4：图片上传失败

**检查**：
- 图片路径是否正确（绝对路径）
- 图片格式是否支持（PNG/JPG）
- 图片数量是否超过 18 张

---

## 🎯 最佳实践

### 发布流程
1. **先渲染图片** - 使用 render_xhs.py 生成封面和卡片
2. **检查 MCP 状态** - `python3 scripts/mcp_publish.py --check`
3. **私密发布预览** - 使用 `--private` 先看效果
4. **APP 确认无误后改公开**

### MCP 维护
1. 启动后保持后台运行
2. 不要在同一账号的其他浏览器登录
3. 登录失效时重新扫码即可

---

## 🔗 相关链接

- [xiaohongshu-mcp](https://github.com/xpzouying/xiaohongshu-mcp) - MCP 服务器
- [小红书创作者平台](https://creator.xiaohongshu.com)

---

*最后更新: 2026-03-10*