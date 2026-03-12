# Redbook Automation

小红书自动化运营工具：内容创作、图片渲染、自动发布、数据分析。

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)

## ✨ 核心功能

### 📝 内容创作

**账号定位分析**
- 分析账号人设、内容风格
- 生成个性化内容建议

**选题生成**
- 基于热点话题生成选题
- 分析竞品爆款选题

**爆款复刻（Viral Copy）**
- 输入爆款笔记 URL，自动分析爆款因素
- 提取标题模板、封面模板、正文模板、互动模板
- 生成高贴合主题的新笔记（封面/配图、标题、正文、话题）
- 支持三种模式：`style-only`（仅风格）、`medium`（中等贴合）、`tight`（高一致性）

```
# 爆款复刻流程
1. 输入爆款笔记 URL
2. 分析：标题/封面/正文/互动机制
3. 参考封面风格生成新封面
4. 输出：3个标题 + 正文 + 封面文案 + 配图prompt + 话题
5. 发布（需确认）
```

### 🎨 图片渲染

**多主题支持**：8种专业主题

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

**智能分页**：自动切分长内容为多张卡片

**高清输出**：1080×1440px（3:4 比例）

### 🚀 自动发布

**MCP API 发布（推荐）**
- 完全自动化，无需人工干预
- 支持本地图片路径（无需图床）
- 私密/公开发布切换
- 定时发布

**浏览器自动化发布（备用）**
- 可视化确认
- 适用于 MCP 不可用时

### 💬 评论管理

**评论检查**
- 打开通知页「评论和@」
- 抓取最新评论：用户名、内容、时间
- 高风险信号识别（辱骂、钓鱼、诱导外链）

**评论回复**
- 通知页优先回复
- 对位校验（placeholder 确认）
- 风控节奏：默认每轮 1 条，间隔 8-15 秒
- 异常检测：频繁操作、发送失败自动停止

```
# 评论回复流程
1. 检查通知页新评论
2. 输出摘要 + 风险提示
3. 用户确认后回复
4. 校验 placeholder 为 "回复 <用户名>"
5. 逐字输入文案
6. 点击发送，确认成功
```

### 📊 数据分析

**笔记搜索**
- 按关键词搜索热门笔记
- 获取笔记详情（内容、评论、互动数据）

**推荐流获取**
- 获取平台推荐内容
- 分析热门趋势

**详情分析**
- 笔记内容提取
- 评论数据分析
- 互动指标统计

---

## 🚀 快速开始

### 安装 MCP 工具

```bash
# 下载（Intel Mac）
mkdir -p ~/.local/bin && cd ~/.local/bin
curl -LO https://github.com/xpzouying/xiaohongshu-mcp/releases/download/v2026.03.09.0605/xiaohongshu-mcp-darwin-amd64.tar.gz
tar -xzf xiaohongshu-mcp-darwin-amd64.tar.gz
chmod +x xiaohongshu-mcp-darwin-amd64 xiaohongshu-login-darwin-amd64

# 登录小红书（扫描二维码）
~/.local/bin/xiaohongshu-login-darwin-amd64

# 启动 MCP 服务器
~/.local/bin/xiaohongshu-mcp-darwin-amd64 &
```

### 安装依赖

```bash
git clone https://github.com/genuishero/redbook-automation.git
cd redbook-automation
pip install -r requirements.txt
```

---

## 📖 使用方法

### MCP 发布

```bash
# 检查 MCP 状态
python scripts/mcp_publish.py --check

# 私密发布
python scripts/mcp_publish.py \
  --title "标题" \
  --content "正文 #标签" \
  --images img1.png,img2.png \
  --private

# 公开发布
python scripts/mcp_publish.py \
  --title "标题" \
  --content "正文" \
  --images img1.png \
  --public

# 定时发布
python scripts/mcp_publish.py \
  --title "标题" \
  --content "正文" \
  --images img1.png \
  --time "2026-03-10 08:00"

# 演示模式
python scripts/mcp_publish.py --demo
```

### 图片渲染

```bash
# 基础渲染
python scripts/render_xhs.py input.md

# 指定主题
python scripts/render_xhs.py input.md -t professional

# 指定输出目录
python scripts/render_xhs.py input.md -o ./output/
```

### 数据分析

```bash
# 检查登录状态
python scripts/xhs_client.py status

# 搜索笔记
python scripts/xhs_client.py search "咖啡推荐"

# 获取笔记详情
python scripts/xhs_client.py detail "feed_id" "xsec_token"

# 获取推荐流
python scripts/xhs_client.py feeds
```

---

## 🤖 定时自动发布

```bash
# 编辑 crontab
crontab -e

# 每天 8:00 发布
0 8 * * * cd /path/to/redbook-automation && python scripts/mcp_publish.py --demo >> ~/.logs/xhs_publish.log 2>&1
```

---

## ⚠️ 重要提示

### MCP 登录
- 登录状态持续有效，无需重复登录
- **不要在其他浏览器登录同一账号**，否则会踢掉 MCP 登录
- 登录失效时重新扫码即可

### 图片要求
- 支持 PNG/JPG 格式
- 推荐尺寸：1080×1440px（3:4 比例）
- 最大 18 张图片

### 评论回复风控
- 默认每轮只发 1 条
- 间隔 8-15 秒
- 遇到"操作频繁"立即停止

---

## 🔧 故障排查

### MCP 连接失败

```bash
# 启动 MCP 服务器
~/.local/bin/xiaohongshu-mcp-darwin-amd64 &
sleep 3 && python scripts/mcp_publish.py --check
```

### MCP 未登录

```bash
~/.local/bin/xiaohongshu-login-darwin-amd64
# 扫描二维码登录
```

### 图片上传失败
- 检查图片路径（使用绝对路径）
- 检查图片格式（PNG/JPG）
- 检查图片数量（≤18张）

---

## 📁 目录结构

```
redbook-automation/
├── README.md
├── LICENSE
├── requirements.txt
├── scripts/
│   ├── mcp_publish.py      # MCP 发布
│   ├── xhs_client.py       # 数据分析
│   ├── render_xhs.py       # 图片渲染
│   ├── render_xhs_v2.py    # 图片渲染 v2
│   ├── publish_xhs.py      # 浏览器发布
│   └── xhs_auto_publish.py # 自动发布流程
├── references/
│   ├── xhs-comment-ops.md     # 评论操作指南
│   ├── xhs-viral-copy-flow.md # 爆款复刻流程
│   ├── xhs-publish-flows.md   # 发布流程
│   └── xhs-runtime-rules.md   # 运行规则
└── templates/
    └── persona.md          # 人设模板
```

---

## 🙏 致谢

- [xiaohongshu-mcp](https://github.com/xpzouying/xiaohongshu-mcp) - MCP 服务器
- [xhs](https://github.com/ReaJason/xhs) - Python 小红书库

---

## ⚠️ 免责声明

本工具仅供学习和研究使用。请遵守小红书平台规则，不要发布违规内容。

---

<p align="center">
  如果这个项目对你有帮助，请给一个 ⭐️ Star！
</p>