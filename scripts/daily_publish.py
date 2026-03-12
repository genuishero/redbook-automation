#!/usr/bin/env python3
"""
每日自动发布脚本
- 获取热门话题
- AI 生成文章
- 发布到小红书

定时任务：每天 8:30
"""

import sys
import os
import random
import json
import requests
from datetime import datetime
from pathlib import Path

# 添加 scripts 目录到 path
SCRIPTS_DIR = Path(__file__).parent
sys.path.insert(0, str(SCRIPTS_DIR))

from mcp_publish import publish_note, check_mcp_status

# 导入智谱图片生成
try:
    from zhipu_image import generate_image
    ZHIPU_AVAILABLE = True
except ImportError:
    ZHIPU_AVAILABLE = False

# MCP 配置
MCP_URL = "http://localhost:18060"

# 热门话题库（可扩展）
TOPICS = [
    {
        "category": "生活方式",
        "topics": [
            "早起习惯养成",
            "极简生活技巧",
            "独居生活指南",
            "周末宅家攻略",
            "生活仪式感",
        ]
    },
    {
        "category": "职场成长",
        "topics": [
            "高效工作方法",
            "职场沟通技巧",
            "远程办公经验",
            "职业规划建议",
            "副业探索",
        ]
    },
    {
        "category": "科技数码",
        "topics": [
            "AI工具推荐",
            "效率工具分享",
            "数码好物测评",
            "App使用技巧",
            "智能办公 setup",
        ]
    },
    {
        "category": "学习成长",
        "topics": [
            "读书笔记分享",
            "学习方法总结",
            "技能提升指南",
            "知识管理工具",
            "自我提升经验",
        ]
    },
    {
        "category": "美食探店",
        "topics": [
            "家常菜谱分享",
            "网红店探店",
            "美食拍照技巧",
            "厨房好物推荐",
            "健康饮食指南",
        ]
    },
]

# 文章模板
ARTICLE_TEMPLATES = {
    "生活方式": """{intro}

{content}

{tips}

{ending}

{tags}""",

    "职场成长": """{intro}

{content}

{tips}

{ending}

{tags}""",

    "科技数码": """{intro}

{content}

{tips}

{ending}

{tags}""",

    "学习成长": """{intro}

{content}

{tips}

{ending}

{tags}""",

    "美食探店": """{intro}

{content}

{tips}

{ending}

{tags}""",
}


def get_trending_topics() -> list:
    """获取热门话题（可接入真实 API）"""
    # 目前使用内置话题库
    # 可以扩展为调用微博热搜、知乎热榜等 API
    all_topics = []
    for category in TOPICS:
        for topic in category["topics"]:
            all_topics.append({
                "category": category["category"],
                "topic": topic
            })
    return all_topics


def select_random_topic() -> dict:
    """随机选择一个话题"""
    topics = get_trending_topics()
    return random.choice(topics)


def generate_article(topic_info: dict) -> dict:
    """生成文章内容
    
    目前使用模板生成，可以扩展为调用 AI API
    """
    category = topic_info["category"]
    topic = topic_info["topic"]
    
    # 根据分类生成内容
    if category == "生活方式":
        article = generate_lifestyle_article(topic)
    elif category == "职场成长":
        article = generate_career_article(topic)
    elif category == "科技数码":
        article = generate_tech_article(topic)
    elif category == "学习成长":
        article = generate_learning_article(topic)
    elif category == "美食探店":
        article = generate_food_article(topic)
    else:
        article = generate_generic_article(topic)
    
    return article


def generate_lifestyle_article(topic: str) -> dict:
    """生成生活方式类文章"""
    templates = {
        "早起习惯养成": {
            "title": "坚持早起100天，我的人生彻底改变了",
            "content": """你是不是也立过无数次"明天开始早起"的 flag？

我以前也是，每天睡到最后一刻，匆忙赶路，一天昏昏沉沉。直到有一天决定改变，从 7:30 到 6:00，坚持了 100 天。

说说真实变化：

⚡ 精力充沛了
早起后的一小时是最高效的时刻——读书、运动、做计划，没人打扰。以前下午 3 点就困，现在一整天精神抖擞。

💪 皮肤变好了
早睡早起比护肤品有效，朋友都说我气色好了，黑眼圈淡了很多。

📚 读了 20 本书
每天早上 30 分钟，一年就是 180+ 小时。这些时间足够读很多书、学很多技能了。

🧘 心态平和了
不用匆忙赶路，可以慢慢吃早餐、化个妆，整个人的状态从"焦虑"变成"从容"。

分享几个有效的方法：

✅ 前一天准备好衣服和包，早上不用思考，直接执行。

✅ 闹钟放远，强迫自己下床关掉。

✅ 起床后立刻拉窗帘，让阳光进来，身体自然清醒。

✅ 给自己安排"期待"，比如好喝的咖啡，让早起有动力。

✅ 不要追求完美，偶尔睡过头没关系，第二天继续。

早起不是为了自律，而是有更多时间做自己喜欢的事。

你愿意明天早起 15 分钟试试吗？评论区打卡～""",
            "tags": "#早起 #生活习惯 #自我提升"
        },
        "极简生活技巧": {
            "title": "极简生活一年，我扔掉了1000件东西",
            "content": """去年搬家时，我被自己的东西震惊了——两个衣柜塞满、三个书架爆满...还有无数"可能用得上"的东西。

于是开始极简之旅，一年扔掉 1000+ 件东西。

说说极简后的变化：

💰 省钱了
不再冲动消费，每个月能存下更多钱。买东西前会问自己：真的需要吗？

⏰ 省时间
找东西不再翻箱倒柜，打扫卫生从 2 小时变成 30 分钟。

🧘 心态变好了
周围环境干净整洁，内心也跟着平静。以前总觉得焦虑，现在好很多。

🎯 更专注了
物品少了，选择也少了，反而更容易专注于重要的事。

分享几个有效的方法：

🏷️ 一进一出
买一件新东西，先处理一件旧的。物品总量不增加，家就不会乱。

🏷️ 7天考验法
纠结要不要扔的，放箱子里 7 天。没打开过？说明不需要。

🏷️ 数字化替代
纸质书→电子书，票据→扫描存档。很多东西可以数字化，不占空间。

🏷️ 买东西前问自己
- 真的需要吗？还是只是想要？
- 家里有类似的吗？
- 会经常用吗？

极简的终点不是空无一物，而是每件物品都有价值。

你有什么舍不得扔的东西吗？评论区聊聊～""",
            "tags": "#极简生活 #断舍离 #生活方式"
        },
    }
    
    default = {
        "title": f"关于{topic}，我想分享一些心得",
        "content": f"""最近在实践「{topic}」，分享一些真实体会。

先说说我的经历：

刚开始接触这个话题时，我也很迷茫。网上信息那么多，不知道从哪开始，也踩过不少坑。但经过一段时间的摸索，我总结了一些实用的经验。

分享我的方法：

1️⃣ 明确目标
知道自己要什么，行动才有方向。把大目标写下来，贴在显眼的地方。

2️⃣ 制定计划
把大目标拆成小目标，每天做一点点。不要贪多，一天进步一点点就够了。

3️⃣ 持续行动
坚持比完美重要。偶尔偷懒没关系，第二天继续就好。重点是长期坚持。

4️⃣ 及时调整
计划赶不上变化，要灵活调整。遇到问题就换方法，不要一条路走到黑。

我的工具推荐：
- Notion：记录计划和进度，可视化很强
- 小红书：找灵感和经验分享，看看别人怎么做
- 好看的本子：手写记录更有感觉，而且可以随时翻看

一点感悟：

这件事带给我的，不只是结果，更是过程中的成长。不要想太多，先做起来。边做边调整，比完美的计划更有用。

有问题评论区聊聊，我看到了都会回复～""",
        "tags": f"#{topic.replace(' ', '')} #生活方式 #分享"
    }
    
    return templates.get(topic, default)


def generate_career_article(topic: str) -> dict:
    """生成职场类文章"""
    templates = {
        "高效工作方法": {
            "title": "工作5年总结：这些效率工具帮我省了2000+小时",
            "content": """刚工作时，我每天"忙碌但低效"。看起来很忙，但一天下来不知道自己做了什么。加班到很晚，成果却不多。

后来我开始系统研究效率方法，整理出一套自己的效率体系，分享给你：

【时间管理】

⏰ 番茄工作法
25分钟专注+5分钟休息，每天8-10个番茄钟。比以前一整天"忙"的效果还好。

📅 每日三件事
只设定3个最重要任务，完成就收工。少即是多，不要贪多。

📋 时间块规划
上午专注深度工作，下午开会、处理邮件。不同时间段做不同类型的事。

【效率工具】

💻 Notion
知识库神器，所有的笔记、计划、文档都在这里。我用它搭建了"第二大脑"。

⚡ Raycast
Mac 效率启动器，快速打开 App、剪贴板历史、窗口管理。比 Spotlight 强太多。

🤖 ChatGPT/Claude
AI 助手，写文案、整理思路、翻译、代码助手。效率提升至少 50%。

📸 CleanShot X
截图+录屏+标注，一个工具搞定。

【工作习惯】

✅ 邮件只处理一次
打开邮件，立刻决定：回复/存档/删除。不要反复看同一封邮件。

✅ 会议前准备议程
没有议程的会议，我基本都会拒绝。没有目的的会议 = 浪费时间。

✅ 下班前写好明天的计划
第二天一开工就知道要做什么，不用纠结。

✅ 学会说"不"
不是所有事都要亲力亲为，能拒绝的尽量拒绝，能授权的尽量授权。

效率提升后，我每天能准时下班，有时间学习新东西、发展副业。

记住：效率不是做更多事，而是用更少时间做好重要的事。

你有什么效率工具推荐？评论区分享～""",
            "tags": "#工作效率 #职场 #效率工具"
        },
        "副业探索": {
            "title": "从0到月入5000副业，我用了这3个方法",
            "content": """一年前我也是"想搞副业但不知道从哪开始"的人。看了很多文章，买了一些课，但还是没行动。

直到有一天决定不再等待，直接开始。现在副业月入 5000+，分享经验：

【第一步：盘点变现资产】

问自己三个问题：
- 你会什么？（写作、设计、编程、翻译...）
- 你喜欢什么？
- 什么能变现？

我选择了内容创作：门槛低、能利用写作能力、有复利效应（内容持续产生价值）。

【第二步：选择方向】

💰 时间换钱型
家教、翻译、兼职设计。上手快，但收入和时间成正比。

📈 复利积累型
写作、视频、课程。前期投入大，后期持续产生收益。

🛍️ 买卖型
电商、代购、二手。需要本金和选品能力。

我的建议：
- 时间多、想快速见效 → 时间换钱型
- 想长期发展、有耐心 → 复利积累型

【第三步：低成本试错】

🎯 设定最小目标
先发 10 篇笔记，看看有没有人看。

⏱️ 限定试错时间
给自己 3 个月，不行就换方向。

💰 控制投入
不要买昂贵设备、课程。先用手头的资源开始。

【踩坑经验】

❌ 等"准备好了"再开始 → 永远准备不好
❌ 追求完美 → 先完成再完美
❌ 被割韭菜 → 真正赚钱的方法别人不会教你

副业不是一夜暴富，是给自己多一种可能。

你想做什么副业？评论区聊聊～""",
            "tags": "#副业 #职场成长 #赚钱"
        },
    }
    
    default = {
        "title": f"关于{topic}，这是我工作几年的感悟",
        "content": f"""工作这些年，我对「{topic}」有了更深的理解。

刚入职场时，很多事情不懂，踩过不少坑。现在回头看，有些经验想分享：

【认知转变】

💡 选择比努力重要
选对赛道，努力才有意义。不是所有方向都值得投入。

💡 学会向上管理
不要只是埋头苦干，让领导知道你的价值。定期汇报工作，展示成果。

💡 保持学习
行业变化很快，不学习就会被淘汰。每周抽时间学习新东西。

【实操建议】

✅ 建立自己的方法论
不只是完成任务，而是思考如何做得更好、更快。形成自己的工作方法。

✅ 积累人脉资源
同事、客户、行业朋友...都是你的资源。维护好关系，关键时刻能用上。

✅ 保持好奇心
多了解行业动态、新技术。保持敏感度，抓住机会。

【一点感悟】

职场是长跑，不是百米冲刺。不要只看眼前，要有长期规划。

你有什么职场困惑？评论区聊聊～""",
        "tags": f"#{topic} #职场 #成长"
    }
    
    return templates.get(topic, default)


def generate_tech_article(topic: str) -> dict:
    """生成科技类文章"""
    templates = {
        "AI工具推荐": {
            "title": "2026年我每天都在用的AI工具，效率直接起飞",
            "content": """说实话，AI 真的改变了我的工作方式。

以前写一篇文章要 2 小时，现在 30 分钟搞定。以前整理会议纪要要半天，现在 10 分钟搞定。以前做 PPT 要一天，现在 2 小时搞定。

今天分享我每天离不开的 AI 工具，每一个都实实在在帮我提效：

【写作与思考】

🤖 ChatGPT / Claude
用途：写文案、整理思路、翻译、代码助手、问答...
我的使用场景：
- 写文章前让它帮我列大纲
- 卡壳的时候让它给我灵感
- 不确定的知识点问它确认
- 翻译、润色文案

💰 费用：ChatGPT Plus $20/月，Claude Pro $20/月
💡 建议：两个都试试，选顺手的

【图像生成】

🎨 Midjourney
用途：封面图、配图、海报设计
我的使用场景：
- 小红书笔记封面
- 文章配图
- 海报设计

💰 费用：$10-60/月
💡 建议：不需要很专业的，先用免费工具

【PPT 制作】

📊 Gamma
用途：AI 生成 PPT
我的使用场景：
- 输入主题，自动生成完整 PPT
- 调整内容、换模板

💰 费用：有免费额度
💡 建议：快速出 PPT 神器

【编程辅助】

💻 Cursor / Claude Code
用途：AI 编程助手
我的使用场景：
- 写代码、改 bug
- 代码解释、重构

💰 费用：Cursor 有免费版
💡 建议：写代码必备，效率翻倍

【笔记与知识管理】

📝 Notion AI
用途：笔记整理、会议纪要、文档润色
我的使用场景：
- 整理会议纪要
- 润色文档
- 生成总结

💰 费用：Notion AI $10/月（附加）
💡 建议：经常用 Notion 的可以考虑

【我的真实使用心得】

✅ 不要过度依赖
AI 是助手，不是替代品。保持思考能力很重要。

✅ 学会写提示词
好的提示词 = 好的输出。多练习，形成自己的模板。

✅ 多工具配合
没有万能工具，根据场景选择最合适的。

✅ 注意隐私
敏感信息不要输入 AI，重要数据本地处理。

【AI 工具使用原则】

1. 明确需求，再选工具
2. 输出要审核，不要盲信
3. 保持学习，工具在快速更新

未来是 AI 的时代，早点学会使用 AI 工具，你就比别人领先一步。

你平时用什么 AI 工具？评论区分享一波～""",
            "tags": "#AI工具 #效率提升 #科技 #ChatGPT #AI"
        },
        "效率工具分享": {
            "title": "这些效率工具让我的工作效率提升了 50%",
            "content": """去年我做了一个决定：系统性地整理和优化自己的工具库。

结果就是：同样的工作时间，产出增加了 50%，加班减少了 70%。

今天把这些工具分享给你，每一个都是我亲自验证过好用的：

【Mac 效率神器】

⚡ Raycast（免费）
替代 Spotlight，快速启动 App、搜索文件、剪贴板历史、各种小工具...

我常用的功能：
- 快速打开 App（Cmd+Space）
- 剪贴板历史（不再复制粘贴来粘贴去）
- 窗口管理（快捷键调整窗口大小）
- 计算器、汇率换算

📊 Rectangle（免费）
窗口管理神器，快捷键调整窗口大小和位置。

我的布局：左边浏览器，右边编辑器，分屏效率超高。

📸 CleanShot X（付费）
截图 + 录屏 + 标注，一个工具搞定。

比系统截图强的地方：
- 可以标注
- 可以滚动截图
- 可以录屏
- 截图后悬浮在屏幕上，方便对照

【笔记与知识管理】

📝 Notion（免费够用）
我的"第二大脑"，所有笔记、计划、文档都在这里。

我的 Notion 结构：
- 工作区：项目进度、会议纪要
- 学习区：读书笔记、学习计划
- 生活区：记账、习惯追踪

💡 Obsidian（免费）
本地 Markdown 笔记，双向链接，适合构建知识网络。

我用它来：
- 记录灵感
- 写作草稿
- 知识链接

【时间管理】

🍅 Tomato（免费）
番茄钟工具，25 分钟专注 + 5 分钟休息。

📊 Toggl（免费版够用）
时间追踪，看看时间都去哪了。

发现：我刷手机的时间比想象的多多了...

【自动化】

⚡ Shortcuts（苹果自带）
苹果快捷指令，很多重复操作可以自动化。

我的用法：
- 一键打开工作模式（打开所有工作 App）
- 一键生成日报模板

🔗 IFTTT（免费版够用）
自动化工作流，连接不同的 App。

我的用法：
- 新邮件自动保存到 Notion
- 发微博自动同步到 Twitter

【我的工具使用原则】

1. 少即是多
工具不在多，在于用精。选定了就深入使用。

2. 定期清理
不用的 App 及时删除，减少干扰。

3. 免费优先
先免费版，真的不够用再付费。

4. 保持更新
工具在进化，定期关注新功能。

工具是手段，不是目的。重要的是你要解决什么问题。

你有什么好用的工具推荐吗？评论区交流～""",
            "tags": "#效率工具 #生产力 #App推荐 #Mac #工具分享"
        },
    }
    
    default = {
        "title": f"{topic}｜科技改变生活，这些工具你必须知道",
        "content": f"""作为一个科技爱好者，我对「{topic}」有一些自己的看法。

科技的快速发展，让我们的生活变得更加便利。但同时，也带来了选择的困扰——工具太多，不知道选哪个。

今天分享一些我的经验：

【如何选择适合自己的工具？】

🎯 明确需求
你要解决什么问题？不要被功能迷惑，先想清楚需求。

⭐ 看口碑
去小红书、知乎搜一下，看看真实用户的评价。

💰 考虑成本
免费的优先，付费的要考虑性价比。

🔄 考虑迁移成本
从旧工具切换过来，需要多长时间？

【我的工具使用心得】

✅ 不要频繁更换工具
选定一个，深入使用，比频繁试新工具效率更高。

✅ 工具服务于目的
不要为了用工具而用工具。

✅ 保持学习
工具在更新，定期看看新功能。

科技发展很快，但我们的时间有限。选择对的工具，让科技真正为我们服务。

你平时用什么科技工具？评论区聊聊～""",
        "tags": f"#{topic} #科技 #数码 #工具推荐"
    }
    
    return templates.get(topic, default)


def generate_learning_article(topic: str) -> dict:
    """生成学习类文章"""
    templates = {
        "读书笔记分享": {
            "title": "2026年读完的10本好书，第3本彻底改变了我",
            "content": """以前我不是个爱读书的人，觉得读书没用，不如刷视频、看公众号。

直到有一天，我意识到：**那些厉害的人，都在读书**。巴菲特每天读 500 页书，比尔盖茨每年读 50 本书...

从那以后，我开始逼自己读书。从一年读不完 1 本，到现在一年能读 20+ 本。

今天分享 2026 年我读过的好书，每本都实实在在对我有帮助：

【📚 No.1 《原子习惯》】

一句话总结：小习惯，大改变。

为什么推荐：
以前我总觉得改变需要"大决心"、"大行动"，结果总是坚持不了几天。这本书告诉我：改变从微小习惯开始，比如每天 2 分钟。

我的改变：
- 每天读 2 页书（现在能读几十页了）
- 每天运动 5 分钟（现在能运动 30 分钟）
- 每天写 50 字（现在能写几百字）

金句：习惯是自我提升的复利。

【📚 No.2 《深度工作》】

一句话总结：在分心的世界里，专注是最稀缺的能力。

为什么推荐：
我们被手机、消息、通知包围，很难真正专注。这本书教我如何进入深度工作状态，效率提升了不只一点点。

我的改变：
- 手机放远一点，专注时不被打扰
- 每天安排 2-3 小时的"深度时间"
- 减少"浅工作"（刷邮件、刷群）

金句：深度工作能力正在成为新的核心竞争力。

【📚 No.3 《纳瓦尔宝典》】

一句话总结：硅谷投资人的智慧，关于财富、幸福、人生。

为什么推荐：
这本书彻底改变了我对财富和幸福的认知。纳瓦尔不是给你"成功学"，而是底层思维。

核心观点：
- 财富不是靠努力，而是靠杠杆（代码、资本、人力）
- 幸福是一种选择，不是结果
- 不要追钱，要追解决问题

我的改变：
- 开始思考如何建立"杠杆"
- 学会放下，减少内耗

金句：追求财富，而不是金钱或地位。

【📚 No.4 《系统之美》】

一句话总结：学会用系统思维看问题。

为什么推荐：
很多事情不是"头痛医头、脚痛医脚"，而是要看到整个系统。这本书帮我升维思考。

我的改变：
- 看问题不再只看表面
- 找到"杠杆点"，四两拨千斤

【📚 No.5 《被讨厌的勇气》】

一句话总结：阿德勒心理学入门，关于自我和人际关系。

为什么推荐：
如果你经常在意别人的看法、活在别人的期待里，这本书会给你勇气。

核心观点：
- 所有的烦恼都来自人际关系
- 课题分离：别人的看法是别人的课题
- 活在当下

我的改变：
- 不再那么在意别人的看法
- 敢于说"不"

【我的读书方法】

✅ 不追求读完
有些书只读几章，够用就行。

✅ 做笔记
读到有共鸣的地方，写下来。哪怕是几个字。

✅ 学以致用
读完一章，想想怎么应用到生活中。

✅ 重读经典
好书值得反复读，每次都有新收获。

读书是回报率最高的投资。一本书几十块钱，却可能改变你的人生。

你最近在读什么书？评论区推荐一波～""",
            "tags": "#读书 #书单推荐 #阅读 #成长 #读书笔记"
        },
        "学习方法总结": {
            "title": "从学渣到学霸，我只用了这 4 个方法",
            "content": """我不是个聪明人，以前学习很吃力。

同样的内容，别人看一遍就懂，我要看三遍。考试前拼命背，考完就忘。

后来我开始研究学习方法，试了很多，踩了很多坑。最后总结出几个真正有用的方法，分享给你：

【方法一：费曼学习法】

核心：用自己的话讲给别人听。

具体做法：
1. 学完一个知识点
2. 想象给一个不懂的人讲解
3. 讲不清楚的地方，就是你没真正懂的
4. 回去重新学，直到能讲清楚

我的经验：
这个方法看起来简单，但效果惊人。我考研的时候，把知识点讲给自己听，讲不清楚就回去看书。最后专业课考了 140+。

【方法二：间隔重复】

核心：不是一次性学完，而是分散在多个时间段。

原理：遗忘曲线告诉我们，学完后会快速遗忘。但如果在即将遗忘时复习，记忆会更牢固。

我的做法：
- 学完当天，复习一遍
- 一周后，再复习一遍
- 一个月后，再复习一遍

工具：Anki，自动安排复习时间。

【方法三：建立知识网络】

核心：知识点不是孤立的，要建立联系。

具体做法：
- 学新知识时，想想和旧知识有什么联系
- 画思维导图，把知识点连起来
- 用自己的话总结

我的经验：
以前学习是"碎片化"的，知识之间没有联系。后来开始画思维导图，知识形成网络，记忆更牢固，理解也更深入。

【方法四：输出倒逼输入】

核心：学完就要输出，输出会让你学得更认真。

输出方式：
- 写笔记
- 做分享
- 教别人
- 写文章

我的经验：
以前"只学不输出"，结果学完就忘。后来开始写笔记、做分享，发现：
1. 学的时候更认真了（因为知道要输出）
2. 理解更深入了（输出需要真正理解）
3. 记忆更牢固了（输出是最好的复习）

【我的学习原则】

✅ 理解 > 记忆
不要死记硬背，要真正理解。

✅ 少即是多
不要追求学得多，要学得精。

✅ 学以致用
学完立刻用，用是最好的学。

✅ 保持耐心
学习是个长期过程，不要急于求成。

【推荐的学习资源】

📚 书：《刻意练习》《如何高效学习》
📱 App：Anki、Notion
🎬 视频：B 站很多学习方法 UP 主

学习方法比努力更重要。找到适合自己的方法，事半功倍。

你有什么学习方法推荐吗？评论区聊聊～""",
            "tags": "#学习方法 #自我提升 #学霸 #效率 #学习技巧"
        },
    }
    
    default = {
        "title": f"关于{topic}，这是我的真实学习心得",
        "content": f"""最近在研究「{topic}」，分享一些我的真实体会。

以前我学习很随性，想到什么学什么，结果学了忘，忘了学，效率很低。

后来我开始系统性地学习，效果好了很多。分享几个我的经验：

【学习之前：明确目标】

🎯 为什么要学这个？
- 工作需要？
- 兴趣爱好？
- 想要改变？

目标明确，才有动力坚持下去。

【学习之中：讲究方法】

✅ 理解比记忆重要
不要死记硬背，要真正理解。

✅ 输出是最好的学习
学完写笔记、做分享、教别人。

✅ 间隔复习
学完不要一次扔掉，定期复习。

【学习之后：实践应用】

💡 学以致用
学完立刻用，用是最好的学。

💡 持续迭代
在实践中发现问题，回头再学。

【我的真实感受】

学习是一场马拉松，不是百米冲刺。不要急于求成，保持节奏，坚持下去。

有什么想学的吗？评论区聊聊，说不定能找到学习搭子～""",
        "tags": f"#{topic} #学习 #成长 #分享"
    }
    
    return templates.get(topic, default)


def generate_food_article(topic: str) -> dict:
    """生成美食类文章"""
    templates = {
        "家常菜谱分享": {
            "title": "一周不重样的快手晚餐，打工人必备！",
            "content": """作为一个打工人，每天下班最大的问题就是：吃什么？

外卖不健康，做饭太麻烦...我以前也这么想，直到我发现了一些快手菜。

不需要太多时间，不需要太多技巧，半小时内搞定一顿饭。今天分享我的一周晚餐：

【周一：番茄炒蛋 + 米饭】

耗时：15 分钟
难度：★☆☆☆☆

做法：
1. 鸡蛋打散，番茄切块
2. 先炒鸡蛋，盛出备用
3. 炒番茄，出汁后倒入鸡蛋
4. 加盐调味，出锅！

小技巧：
- 番茄要选软一点的，容易出汁
- 可以加一点糖提鲜

【周二：蒜蓉西兰花 + 鸡胸肉】

耗时：20 分钟
难度：★★☆☆☆

做法：
1. 西兰花焯水备用
2. 鸡胸肉切片，腌制（盐、料酒、淀粉）
3. 热锅炒鸡胸肉至变色
4. 加入西兰花、蒜末翻炒
5. 调味出锅！

小技巧：
- 鸡胸肉用淀粉腌制会更嫩
- 西兰花焯水时间不要太长，保持脆嫩

【周三：可乐鸡翅】

耗时：30 分钟
难度：★★☆☆☆

做法：
1. 鸡翅两面划刀，便于入味
2. 热锅少油，煎至两面金黄
3. 倒入可乐没过鸡翅
4. 加生抽、老抽、料酒
5. 大火收汁，出锅！

小技巧：
- 可乐要没过鸡翅
- 收汁的时候注意翻面，不要糊了
- 不需要加盐，酱油和可乐够了

【周四：葱油拌面】

耗时：10 分钟
难度：★☆☆☆☆

做法：
1. 小葱切段，热油炸至金黄
2. 捞出葱段，葱油备用
3. 面条煮熟，过凉水
4. 淋上葱油、生抽、拌匀！

小技巧：
- 葱段炸到金黄就可以，不要炸糊了
- 可以加一点醋提味

【周五：凉拌黄瓜 + 馒头】

耗时：5 分钟
难度：★☆☆☆☆

做法：
1. 黄瓜拍碎，切块
2. 加蒜末、香油、醋、生抽
3. 拌匀即可！

小技巧：
- 黄瓜要拍碎，比切的更入味
- 蒜末多一点更香

【周末：番茄牛腩】

耗时：2 小时
难度：★★★☆☆

周末可以炖一锅牛腩，留着吃两天。

做法：
1. 牛腩切块，冷水下锅焯水
2. 番茄切块，炒出汁
3. 加入牛腩、水、调料
4. 小火炖 1.5 小时

【我的做饭心得】

✅ 备好基础调料
生抽、老抽、料酒、醋、蚝油、盐、糖、香油，这些够了。

✅ 周末批量处理
周末可以洗好一周的菜，切好放冰箱。

✅ 简单的才是最好的
不要追求复杂的菜，简单的往往最好吃。

做饭是治愈，也是爱自己的一种方式。每天花 20 分钟，给自己做一顿饭，比外卖香多了。

你有什么快手菜推荐吗？评论区分享一下～""",
            "tags": "#家常菜 #快手菜 #打工人 #美食 #菜谱分享"
        },
    }
    
    default = {
        "title": f"{topic}｜美食分享，生活的小确幸",
        "content": f"""作为一个美食爱好者，我对「{topic}」有自己的理解。

美食不只是填饱肚子，更是生活的仪式感。

【我的美食理念】

🍳 自己做饭更有温度
哪怕是最简单的菜，自己做的总比外卖香。

👨‍🍳 不需要很厉害的厨艺
家常菜不需要太多技巧，用心就好。

🍜 美食是生活的小确幸
忙碌了一整天，一顿好吃的能治愈一切。

【我的做饭习惯】

✅ 周末备菜
洗好一周的蔬菜，切好放冰箱，工作日做饭更快。

✅ 常备调料
生抽、老抽、料酒、醋...这些调料有了，大部分菜都能做。

✅ 不要怕失败
刚开始做饭难免失败，多试几次就好了。

【推荐几个简单又好吃的菜】

- 番茄炒蛋：永远不会失败
- 蒜蓉西兰花：健康又好吃
- 可乐鸡翅：比红烧鸡简单多了
- 葱油拌面：10 分钟搞定

做饭这件事，开始就好。不用追求完美，用心就好。

你最喜欢吃什么？评论区聊聊～""",
        "tags": f"#{topic} #美食 #分享 #美食日常"
    }
    
    return templates.get(topic, default)


def generate_generic_article(topic: str) -> dict:
    """生成通用文章"""
    return {
        "title": f"关于{topic}，我想聊聊",
        "content": f"""最近关注{topic}，有一些想法分享给大家。

核心观点：
1. 保持开放的心态
2. 持续学习
3. 知行合一

希望对你有帮助～""",
        "tags": f"#{topic} #分享"
    }


# 智谱图片风格映射
XHS_IMAGE_STYLES = {
    "生活方式": "warm and cozy lifestyle photography, soft natural lighting, minimalist aesthetic, Instagram style, high quality",
    "职场成长": "professional business style, modern office aesthetic, blue and white tones, clean and elegant, corporate photography",
    "科技数码": "futuristic tech style, blue-purple gradient, cyberpunk vibes, digital elements, high-tech aesthetic",
    "学习成长": "bright and inspiring study atmosphere, books and notes, natural light, knowledge and growth feeling",
    "美食探店": "food photography, warm appetizing colors, restaurant ambiance, delicious and artistic plating",
    "default": "modern minimalist style, high quality, aesthetic, Instagram worthy, professional photography"
}


def generate_ai_cover(title: str, category: str = "default") -> list:
    """使用智谱 AI 生成封面图"""
    if not ZHIPU_AVAILABLE:
        return None
    
    style = XHS_IMAGE_STYLES.get(category, XHS_IMAGE_STYLES["default"])
    
    # 构建丰富的提示词
    prompt = f"""
    Create a stunning image for social media cover,
    {style},
    Theme: {title},
    Requirements:
    - Eye-catching and visually appealing
    - Modern and elegant design
    - Perfect for social media sharing
    - High quality professional look
    - Rich details and vibrant colors
    - No text or watermarks
    """
    
    try:
        images = generate_image(
            prompt=prompt.strip(),
            size="768x1024",
            output_dir="/tmp/xhs_zhipu"
        )
        return images
    except Exception as e:
        print(f"   ⚠️ 智谱生成失败: {e}")
        return None


def generate_cover_images(title: str, content: str, category: str = "default") -> list:
    """生成封面图和内容卡片（优先使用智谱 AI，失败时回退到 PIL）"""
    
    # 1. 优先使用智谱 AI 生成
    print("   尝试智谱 AI 生成...")
    ai_images = generate_ai_cover(title, category)
    
    if ai_images and len(ai_images) >= 1:
        print(f"   ✅ 智谱生成成功，共 {len(ai_images)} 张图片")
        return ai_images
    
    # 2. 回退到 PIL 生成
    print("   回退到 PIL 生成...")
    
    try:
        from PIL import Image, ImageDraw, ImageFont, ImageFilter
    except ImportError:
        print("⚠️  Pillow 未安装，跳过封面生成")
        return []
    
    images = []
    output_dir = Path("/tmp/xhs_covers")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # 加载字体
    try:
        font_paths = [
            '/System/Library/Fonts/Hiragino Sans GB.ttc',
            '/System/Library/Fonts/STHeiti Light.ttc',
        ]
        for font_path in font_paths:
            try:
                font_title = ImageFont.truetype(font_path, 90)
                font_large = ImageFont.truetype(font_path, 64)
                font_medium = ImageFont.truetype(font_path, 48)
                font_small = ImageFont.truetype(font_path, 38)
                print(f"   使用字体: {font_path}")
                break
            except:
                continue
    except:
        print("   ⚠️ 字体加载失败")
        font_title = font_large = font_medium = font_small = ImageFont.load_default()
    
    width, height = 1080, 1440
    
    # 提取关键内容
    lines = [l.strip() for l in content.split('\n') if l.strip() and not l.startswith('#')]
    # 过滤掉太短的行和符号行
    key_points = [l for l in lines if len(l) > 5 and not l.startswith('✅') and not l.startswith('❌')][:12]
    
    # === 配色方案（更丰富的渐变） ===
    color_schemes = [
        {
            'name': '紫蓝渐变',
            'colors': [(102, 126, 234), (118, 75, 162)],
            'accent': (255, 255, 255)
        },
        {
            'name': '粉橙渐变', 
            'colors': [(255, 119, 198), (255, 166, 158)],
            'accent': (255, 255, 255)
        },
        {
            'name': '青绿渐变',
            'colors': [(67, 206, 162), (24, 90, 157)],
            'accent': (255, 255, 255)
        }
    ]
    
    # === 第1张：封面 ===
    cover = Image.new('RGB', (width, height))
    draw = ImageDraw.Draw(cover)
    
    # 多层渐变背景
    scheme = color_schemes[0]
    for y in range(height):
        ratio = y / height
        # 使用三次插值实现更平滑的渐变
        if ratio < 0.5:
            r = scheme['colors'][0][0] + (scheme['colors'][1][0] - scheme['colors'][0][0]) * ratio * 2
            g = scheme['colors'][0][1] + (scheme['colors'][1][1] - scheme['colors'][0][1]) * ratio * 2
            b = scheme['colors'][0][2] + (scheme['colors'][1][2] - scheme['colors'][0][2]) * ratio * 2
        else:
            r = scheme['colors'][1][0]
            g = scheme['colors'][1][1]
            b = scheme['colors'][1][2]
        draw.line([(0, y), (width, y)], fill=(int(r), int(g), int(b)))
    
    # 装饰元素：角落圆形（半透明，不覆盖内容）
    # 左上角
    draw.ellipse([(-150, -150), (200, 200)], fill=(255, 255, 255, 20))
    # 右下角
    draw.ellipse([(width-180, height-180), (width+80, height+80)], fill=(255, 255, 255, 15))
    # 右上角小圆
    draw.ellipse([(width-250, -80), (width-80, 90)], fill=(255, 255, 255, 15))
    # 左下角小圆
    draw.ellipse([(-80, height-200), (100, height-50)], fill=(255, 255, 255, 15))
    
    # 装饰元素：几何线条
    for i in range(5):
        x1 = 100 + i * 180
        draw.line([(x1, 200), (x1 + 100, 250)], fill=(255, 255, 255, 40), width=3)
    
    # 主标题
    display_title = title[:12] + "..." if len(title) > 12 else title
    
    # 标题背景（半透明圆角矩形）
    bbox = draw.textbbox((0, 0), display_title, font=font_title)
    text_w, text_h = bbox[2] - bbox[0], bbox[3] - bbox[1]
    x, y = (width - text_w) // 2, height // 2 - 120
    
    # 绘制圆角矩形背景
    padding = 50
    draw.rounded_rectangle(
        [x - padding, y - padding//2, x + text_w + padding, y + text_h + padding//2],
        radius=20,
        fill=(0, 0, 0, 80)
    )
    
    draw.text((x, y), display_title, fill='white', font=font_title)
    
    # 副标题
    subtitle = "每日精选内容"
    bbox2 = draw.textbbox((0, 0), subtitle, font=font_medium)
    draw.text(((width - (bbox2[2] - bbox2[0])) // 2, y + text_h + 80), subtitle, fill=(255, 255, 255, 220), font=font_medium)
    
    # 底部装饰文字
    footer = " swipe → "
    draw.text((width - 180, height - 80), footer, fill=(255, 255, 255, 150), font=font_small)
    
    cover_path = output_dir / "cover_1.png"
    cover.save(cover_path)
    images.append(str(cover_path))
    print(f"   封面: {cover_path}")
    
    # === 第2-3张：内容卡片 ===
    for card_idx in range(2):
        scheme = color_schemes[card_idx + 1]
        card = Image.new('RGB', (width, height))
        draw = ImageDraw.Draw(card)
        
        # 渐变背景
        for y in range(height):
            ratio = y / height
            r = scheme['colors'][0][0] + (scheme['colors'][1][0] - scheme['colors'][0][0]) * ratio
            g = scheme['colors'][0][1] + (scheme['colors'][1][1] - scheme['colors'][0][1]) * ratio
            b = scheme['colors'][0][2] + (scheme['colors'][1][2] - scheme['colors'][0][2]) * ratio
            draw.line([(0, y), (width, y)], fill=(int(r), int(g), int(b)))
        
        # 装饰图案（只放在角落，不覆盖内容）
        draw.ellipse([(-100, -100), (150, 150)], fill=(255, 255, 255, 15))
        draw.ellipse([(width-150, height-150), (width+50, height+50)], fill=(255, 255, 255, 15))
        draw.ellipse([(width-200, -50), (width-50, 100)], fill=(255, 255, 255, 10))
        draw.ellipse([(-80, height-180), (50, height-50)], fill=(255, 255, 255, 10))
        
        # 卡片标题区域
        card_title = "核心要点" if card_idx == 0 else "重要内容"
        
        # 标题背景条
        draw.rectangle([0, 80, width, 200], fill=(0, 0, 0, 60))
        draw.text((60, 110), card_title, fill='white', font=font_large)
        
        # 分割线
        draw.line([(60, 220), (width-60, 220)], fill='white', width=2)
        
        # 内容要点
        start_idx = card_idx * 5
        card_points = key_points[start_idx:start_idx + 5]
        
        y_pos = 280
        for idx, point in enumerate(card_points):
            # 编号圆圈
            circle_x, circle_y = 100, y_pos + 20
            draw.ellipse([(circle_x - 30, circle_y - 30), (circle_x + 30, circle_y + 30)], 
                        fill=(255, 255, 255, 40))
            draw.text((circle_x - 10, circle_y - 20), str(idx + 1), fill='white', font=font_medium)
            
            # 内容文字（自动换行）
            text = point[:35] + "..." if len(point) > 35 else point
            draw.text((160, y_pos), text, fill='white', font=font_small)
            y_pos += 120
        
        # 底部装饰
        draw.text((60, height - 100), f"第 {card_idx + 2} 张 / 共 3 张", fill=(255, 255, 255, 150), font=font_small)
        
        card_path = output_dir / f"cover_{card_idx + 2}.png"
        card.save(card_path)
        images.append(str(card_path))
        print(f"   卡片{card_idx + 2}: {card_path}")
    
    print(f"   共生成 {len(images)} 张图片")
    return images


def main():
    """主函数"""
    import traceback
    
    print(f"\n{'='*50}")
    print(f"📅 每日自动发布 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*50}\n")
    
    # 日志文件
    log_file = Path.home() / ".openclaw" / "logs" / "xhs_daily_publish.log"
    log_file.parent.mkdir(parents=True, exist_ok=True)
    
    def log_error(msg: str):
        """记录错误日志"""
        print(msg)
        with open(log_file, "a") as f:
            f.write(f"\n[{datetime.now().isoformat()}] ERROR: {msg}\n")
    
    def log_info(msg: str):
        """记录信息日志"""
        print(msg)
    
    try:
        # 1. 检查 MCP 状态
        log_info("🔍 检查 MCP 状态...")
        if not check_mcp_status():
            log_error("❌ MCP 未就绪，退出")
            return 1
        
        # 2. 选择话题
        log_info("\n🎯 选择话题...")
        topic_info = select_random_topic()
        log_info(f"   分类: {topic_info['category']}")
        log_info(f"   话题: {topic_info['topic']}")
        
        # 3. 生成文章
        log_info("\n✍️ 生成文章...")
        article = generate_article(topic_info)
        log_info(f"   标题: {article['title']}")
        
        # 4. 生成封面图
        log_info("\n🎨 生成封面图...")
        image_paths = generate_cover_images(article['title'], article['content'], topic_info['category'])
        
        # 验证图片
        valid_images = []
        for img_path in image_paths:
            if Path(img_path).exists():
                valid_images.append(img_path)
                log_info(f"   ✅ 图片有效: {img_path}")
            else:
                log_error(f"   ❌ 图片不存在: {img_path}")
        
        if not valid_images:
            log_error("❌ 没有有效图片，无法发布")
            with open(log_file, "a") as f:
                f.write(f"\n{datetime.now().isoformat()}\n")
                f.write(f"标题: {article['title']}\n")
                f.write(f"话题: {topic_info['topic']}\n")
                f.write(f"状态: 失败 (无有效图片)\n")
            return 1
        
        # 5. 发布（带重试）
        log_info(f"\n📤 发布到小红书...")
        log_info(f"   有效图片: {len(valid_images)} 张")
        
        result = publish_note(
            title=article['title'],
            content=article['content'],
            images=valid_images,
            private=False  # 公开发布
        )
        
        if result:
            log_info(f"\n✅ 发布成功！")
            
            # 保存发布记录
            with open(log_file, "a") as f:
                f.write(f"\n{datetime.now().isoformat()}\n")
                f.write(f"标题: {article['title']}\n")
                f.write(f"话题: {topic_info['topic']}\n")
                f.write(f"状态: 成功\n")
            
            return 0
        else:
            log_error(f"\n❌ 发布失败")
            
            # 保存失败记录
            with open(log_file, "a") as f:
                f.write(f"\n{datetime.now().isoformat()}\n")
                f.write(f"标题: {article['title']}\n")
                f.write(f"话题: {topic_info['topic']}\n")
                f.write(f"状态: 失败\n")
            
            return 1
    
    except Exception as e:
        error_detail = f"异常: {type(e).__name__}: {e}\n{traceback.format_exc()}"
        log_error(f"\n❌ 发布异常:\n{error_detail}")
        
        # 保存异常记录
        with open(log_file, "a") as f:
            f.write(f"\n{datetime.now().isoformat()}\n")
            f.write(f"状态: 异常\n")
            f.write(f"错误: {error_detail}\n")
        
        return 1


if __name__ == "__main__":
    sys.exit(main())